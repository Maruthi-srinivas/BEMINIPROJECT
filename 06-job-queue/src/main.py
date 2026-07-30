"""Job queue with Redis workers and interval/cron-style schedules."""

from __future__ import annotations

import json
import logging
import os
import time
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta
from typing import Any, Callable

import httpx
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from redis import Redis
from redis.exceptions import RedisError
from sqlalchemy import Boolean, DateTime, Integer, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./job_queue.db")
REDIS_URL = os.getenv("REDIS_URL", "")
QUEUE_KEY = "job-queue:jobs"
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
redis_client = Redis.from_url(REDIS_URL, decode_responses=True) if REDIS_URL else None
_memory_queue: list[int] = []
logger = logging.getLogger("job_queue")


class Base(DeclarativeBase):
    pass


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str] = mapped_column(String(64))
    payload: Mapped[str] = mapped_column(Text, default="{}")
    status: Mapped[str] = mapped_column(String(32), default="queued")
    result: Mapped[str | None] = mapped_column(Text, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    run_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    task: Mapped[str] = mapped_column(String(64))
    payload: Mapped[str] = mapped_column(Text, default="{}")
    interval_seconds: Mapped[int] = mapped_column(Integer)
    next_run_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class CreateJob(BaseModel):
    task: str = Field(pattern="^(echo|http_ping)$")
    payload: dict[str, Any] = Field(default_factory=dict)
    run_at: datetime | None = None


class JobResponse(BaseModel):
    id: int
    task: str
    payload: dict[str, Any]
    status: str
    result: dict[str, Any] | None
    error: str | None
    run_at: datetime
    created_at: datetime
    updated_at: datetime


class CreateSchedule(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    task: str = Field(pattern="^(echo|http_ping)$")
    payload: dict[str, Any] = Field(default_factory=dict)
    interval_seconds: int = Field(gt=0, le=86400)


class ScheduleResponse(BaseModel):
    id: int
    name: str
    task: str
    payload: dict[str, Any]
    interval_seconds: int
    next_run_at: datetime
    enabled: bool


def get_db():
    with SessionLocal() as db:
        yield db


def utcnow() -> datetime:
    return datetime.now(UTC)


def job_response(row: Job) -> JobResponse:
    return JobResponse(
        id=row.id,
        task=row.task,
        payload=json.loads(row.payload),
        status=row.status,
        result=json.loads(row.result) if row.result else None,
        error=row.error,
        run_at=row.run_at,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def schedule_response(row: Schedule) -> ScheduleResponse:
    return ScheduleResponse(
        id=row.id,
        name=row.name,
        task=row.task,
        payload=json.loads(row.payload),
        interval_seconds=row.interval_seconds,
        next_run_at=row.next_run_at,
        enabled=row.enabled,
    )


def task_echo(payload: dict[str, Any]) -> dict[str, Any]:
    return {"echo": payload}


def task_http_ping(payload: dict[str, Any]) -> dict[str, Any]:
    url = payload.get("url", "https://example.com")
    response = httpx.get(url, timeout=10)
    return {"url": url, "status_code": response.status_code}


TASKS: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
    "echo": task_echo,
    "http_ping": task_http_ping,
}


def enqueue_job_id(job_id: int) -> None:
    if redis_client:
        try:
            redis_client.rpush(QUEUE_KEY, str(job_id))
            return
        except RedisError:
            logger.warning("redis enqueue failed; using memory queue")
    _memory_queue.append(job_id)


def pop_job_id(timeout: int = 1) -> int | None:
    if redis_client:
        try:
            item = redis_client.blpop(QUEUE_KEY, timeout=timeout)
            if item:
                return int(item[1])
            return None
        except RedisError:
            logger.warning("redis pop failed")
    if _memory_queue:
        return _memory_queue.pop(0)
    if timeout:
        time.sleep(min(timeout, 1))
    return None


def execute_job(job_id: int) -> None:
    with SessionLocal() as db:
        row = db.get(Job, job_id)
        if not row or row.status not in {"queued", "scheduled"}:
            return
        if row.run_at.replace(tzinfo=UTC) > utcnow():
            enqueue_job_id(job_id)
            return
        row.status = "running"
        row.updated_at = utcnow()
        db.commit()
        handler = TASKS.get(row.task)
        try:
            if not handler:
                raise ValueError(f"unknown task {row.task}")
            result = handler(json.loads(row.payload))
            row.result = json.dumps(result)
            row.status = "succeeded"
            row.error = None
        except Exception as exc:
            row.status = "failed"
            row.error = str(exc)
        row.updated_at = utcnow()
        db.commit()


def materialize_due_schedules() -> None:
    with SessionLocal() as db:
        now = utcnow()
        due = db.scalars(
            select(Schedule).where(Schedule.enabled.is_(True), Schedule.next_run_at <= now)
        ).all()
        for schedule in due:
            job = Job(
                task=schedule.task,
                payload=schedule.payload,
                status="queued",
                run_at=now,
            )
            db.add(job)
            db.flush()
            enqueue_job_id(job.id)
            schedule.next_run_at = now + timedelta(seconds=schedule.interval_seconds)
        db.commit()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Job Queue", version="1.0.0", lifespan=lifespan)

_cors_origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    with engine.connect() as connection:
        connection.exec_driver_sql("SELECT 1")
    return {"status": "ok"}


@app.post("/v1/jobs", response_model=JobResponse, status_code=status.HTTP_202_ACCEPTED)
def create_job(payload: CreateJob, db: Session = Depends(get_db)) -> JobResponse:
    run_at = payload.run_at or utcnow()
    if run_at.tzinfo is None:
        run_at = run_at.replace(tzinfo=UTC)
    row = Job(
        task=payload.task,
        payload=json.dumps(payload.payload),
        status="queued",
        run_at=run_at,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    enqueue_job_id(row.id)
    if not REDIS_URL:
        execute_job(row.id)
        db.refresh(row)
    return job_response(row)


@app.get("/v1/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)) -> JobResponse:
    row = db.get(Job, job_id)
    if not row:
        raise HTTPException(status_code=404, detail="job not found")
    return job_response(row)


@app.post("/v1/schedules", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_schedule(payload: CreateSchedule, db: Session = Depends(get_db)) -> ScheduleResponse:
    if db.scalar(select(Schedule).where(Schedule.name == payload.name)):
        raise HTTPException(status_code=409, detail="schedule name already exists")
    row = Schedule(
        name=payload.name,
        task=payload.task,
        payload=json.dumps(payload.payload),
        interval_seconds=payload.interval_seconds,
        next_run_at=utcnow() + timedelta(seconds=payload.interval_seconds),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return schedule_response(row)


@app.get("/v1/schedules", response_model=list[ScheduleResponse])
def list_schedules(db: Session = Depends(get_db)) -> list[ScheduleResponse]:
    rows = db.scalars(select(Schedule).order_by(Schedule.id)).all()
    return [schedule_response(row) for row in rows]


@app.delete("/v1/schedules/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)) -> None:
    row = db.get(Schedule, schedule_id)
    if not row:
        raise HTTPException(status_code=404, detail="schedule not found")
    db.delete(row)
    db.commit()

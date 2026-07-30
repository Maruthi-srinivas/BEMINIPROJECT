"""Feature flag service with percentage rollouts and attribute targeting."""

from __future__ import annotations

import hashlib
import json
import os
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Any, Literal

from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from redis import Redis
from redis.exceptions import RedisError
from sqlalchemy import Boolean, DateTime, Integer, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./feature_flags.db")
REDIS_URL = os.getenv("REDIS_URL", "")
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "60"))

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
redis_client = Redis.from_url(REDIS_URL, decode_responses=True) if REDIS_URL else None
_memory_cache: dict[str, str] = {}


class Base(DeclarativeBase):
    pass


class Flag(Base):
    __tablename__ = "flags"

    key: Mapped[str] = mapped_column(String(128), primary_key=True)
    description: Mapped[str] = mapped_column(String(512), default="")
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    percentage: Mapped[int] = mapped_column(Integer, default=100)
    rules_json: Mapped[str] = mapped_column(Text, default="[]")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class Rule(BaseModel):
    attribute: str
    op: Literal["eq", "neq", "in", "contains"]
    value: Any


class FlagInput(BaseModel):
    description: str = ""
    enabled: bool = True
    percentage: int = Field(default=100, ge=0, le=100)
    rules: list[Rule] = Field(default_factory=list)


class FlagResponse(FlagInput):
    key: str
    created_at: datetime
    updated_at: datetime


class EvaluateRequest(BaseModel):
    flag_key: str
    user_id: str
    attributes: dict[str, Any] = Field(default_factory=dict)


class BatchEvaluateRequest(BaseModel):
    flag_keys: list[str] = Field(min_length=1)
    user_id: str
    attributes: dict[str, Any] = Field(default_factory=dict)


class EvaluateResponse(BaseModel):
    flag_key: str
    enabled: bool
    reason: str


def get_db():
    with SessionLocal() as db:
        yield db


def cache_key(flag_key: str) -> str:
    return f"feature-flags:flag:{flag_key}"


def flag_to_dict(row: Flag) -> dict[str, Any]:
    return {
        "key": row.key,
        "description": row.description,
        "enabled": row.enabled,
        "percentage": row.percentage,
        "rules": json.loads(row.rules_json),
        "created_at": row.created_at.isoformat(),
        "updated_at": row.updated_at.isoformat(),
    }


def flag_response(row: Flag) -> FlagResponse:
    return FlagResponse(
        key=row.key,
        description=row.description,
        enabled=row.enabled,
        percentage=row.percentage,
        rules=[Rule.model_validate(rule) for rule in json.loads(row.rules_json)],
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def set_cache(flag_key: str, payload: dict[str, Any]) -> None:
    encoded = json.dumps(payload)
    if redis_client:
        try:
            redis_client.setex(cache_key(flag_key), CACHE_TTL_SECONDS, encoded)
            return
        except RedisError:
            pass
    _memory_cache[flag_key] = encoded


def delete_cache(flag_key: str) -> None:
    _memory_cache.pop(flag_key, None)
    if redis_client:
        try:
            redis_client.delete(cache_key(flag_key))
        except RedisError:
            pass


def get_cached(flag_key: str) -> dict[str, Any] | None:
    if redis_client:
        try:
            raw = redis_client.get(cache_key(flag_key))
            if raw:
                return json.loads(raw)
        except RedisError:
            pass
    raw = _memory_cache.get(flag_key)
    return json.loads(raw) if raw else None


def load_flag(db: Session, flag_key: str) -> dict[str, Any] | None:
    cached = get_cached(flag_key)
    if cached:
        return cached
    row = db.get(Flag, flag_key)
    if not row:
        return None
    payload = flag_to_dict(row)
    set_cache(flag_key, payload)
    return payload


def match_rule(rule: Rule, attributes: dict[str, Any]) -> bool:
    actual = attributes.get(rule.attribute)
    if rule.op == "eq":
        return actual == rule.value
    if rule.op == "neq":
        return actual != rule.value
    if rule.op == "in":
        return actual in (rule.value or [])
    if rule.op == "contains":
        return isinstance(actual, str) and str(rule.value) in actual
    return False


def sticky_bucket(flag_key: str, user_id: str) -> int:
    digest = hashlib.sha256(f"{flag_key}:{user_id}".encode()).hexdigest()
    return int(digest[:8], 16) % 100


def evaluate_flag(flag: dict[str, Any], user_id: str, attributes: dict[str, Any]) -> EvaluateResponse:
    key = flag["key"]
    if not flag.get("enabled", True):
        return EvaluateResponse(flag_key=key, enabled=False, reason="flag_disabled")
    rules = [Rule.model_validate(rule) for rule in flag.get("rules") or []]
    if rules and not all(match_rule(rule, attributes) for rule in rules):
        return EvaluateResponse(flag_key=key, enabled=False, reason="rules_mismatch")
    percentage = int(flag.get("percentage", 100))
    if percentage >= 100:
        return EvaluateResponse(flag_key=key, enabled=True, reason="percentage_full")
    if percentage <= 0:
        return EvaluateResponse(flag_key=key, enabled=False, reason="percentage_zero")
    bucket = sticky_bucket(key, user_id)
    if bucket < percentage:
        return EvaluateResponse(flag_key=key, enabled=True, reason=f"percentage_bucket_{bucket}")
    return EvaluateResponse(flag_key=key, enabled=False, reason=f"percentage_bucket_{bucket}")


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Feature Flag Service", version="1.0.0", lifespan=lifespan)

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


@app.put("/v1/flags/{key}", response_model=FlagResponse)
def upsert_flag(key: str, payload: FlagInput, db: Session = Depends(get_db)) -> FlagResponse:
    row = db.get(Flag, key)
    now = datetime.now(UTC)
    if not row:
        row = Flag(
            key=key,
            description=payload.description,
            enabled=payload.enabled,
            percentage=payload.percentage,
            rules_json=json.dumps([rule.model_dump() for rule in payload.rules]),
            created_at=now,
            updated_at=now,
        )
        db.add(row)
    else:
        row.description = payload.description
        row.enabled = payload.enabled
        row.percentage = payload.percentage
        row.rules_json = json.dumps([rule.model_dump() for rule in payload.rules])
        row.updated_at = now
    db.commit()
    db.refresh(row)
    set_cache(key, flag_to_dict(row))
    return flag_response(row)


@app.get("/v1/flags", response_model=list[FlagResponse])
def list_flags(db: Session = Depends(get_db)) -> list[FlagResponse]:
    rows = db.scalars(select(Flag).order_by(Flag.key)).all()
    return [flag_response(row) for row in rows]


@app.get("/v1/flags/{key}", response_model=FlagResponse)
def get_flag(key: str, db: Session = Depends(get_db)) -> FlagResponse:
    row = db.get(Flag, key)
    if not row:
        raise HTTPException(status_code=404, detail="flag not found")
    return flag_response(row)


@app.delete("/v1/flags/{key}", status_code=status.HTTP_204_NO_CONTENT)
def delete_flag(key: str, db: Session = Depends(get_db)) -> None:
    row = db.get(Flag, key)
    if not row:
        raise HTTPException(status_code=404, detail="flag not found")
    db.delete(row)
    db.commit()
    delete_cache(key)


@app.post("/v1/evaluate", response_model=EvaluateResponse)
def evaluate(payload: EvaluateRequest, db: Session = Depends(get_db)) -> EvaluateResponse:
    flag = load_flag(db, payload.flag_key)
    if not flag:
        raise HTTPException(status_code=404, detail="flag not found")
    return evaluate_flag(flag, payload.user_id, payload.attributes)


@app.post("/v1/evaluate/batch", response_model=list[EvaluateResponse])
def evaluate_batch(payload: BatchEvaluateRequest, db: Session = Depends(get_db)) -> list[EvaluateResponse]:
    results: list[EvaluateResponse] = []
    for key in payload.flag_keys:
        flag = load_flag(db, key)
        if not flag:
            results.append(EvaluateResponse(flag_key=key, enabled=False, reason="flag_missing"))
            continue
        results.append(evaluate_flag(flag, payload.user_id, payload.attributes))
    return results

"""Notification service with RabbitMQ workers, SMTP email, and webhooks."""

from __future__ import annotations

import json
import logging
import os
import smtplib
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from email.message import EmailMessage
from typing import Any

import httpx
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy import DateTime, Integer, String, Text, create_engine, desc, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./notifications.db")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "")
SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", "1025"))
SMTP_FROM = os.getenv("SMTP_FROM", "noreply@example.com")
MAX_ATTEMPTS = int(os.getenv("MAX_ATTEMPTS", "5"))
QUEUE_NAME = "notifications"
DLQ_NAME = "notifications.dlq"

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
logger = logging.getLogger("notification_service")
_memory_queue: list[int] = []


class Base(DeclarativeBase):
    pass


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    channel: Mapped[str] = mapped_column(String(32))
    recipient: Mapped[str] = mapped_column(String(512))
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    webhook_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="queued")
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class CreateNotification(BaseModel):
    channel: str = Field(pattern="^(email|webhook)$")
    to: str | None = None
    subject: str | None = None
    body: str | None = None
    webhook_url: HttpUrl | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class NotificationResponse(BaseModel):
    id: int
    channel: str
    recipient: str
    subject: str | None
    body: str | None
    webhook_url: str | None
    status: str
    attempts: int
    last_error: str | None
    created_at: datetime
    updated_at: datetime


def get_db():
    with SessionLocal() as db:
        yield db


def to_response(row: Notification) -> NotificationResponse:
    return NotificationResponse(
        id=row.id,
        channel=row.channel,
        recipient=row.recipient,
        subject=row.subject,
        body=row.body,
        webhook_url=row.webhook_url,
        status=row.status,
        attempts=row.attempts,
        last_error=row.last_error,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def deliver_email(row: Notification) -> None:
    message = EmailMessage()
    message["From"] = SMTP_FROM
    message["To"] = row.recipient
    message["Subject"] = row.subject or "(no subject)"
    message.set_content(row.body or "")
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as smtp:
        smtp.send_message(message)


def deliver_webhook(row: Notification) -> None:
    if not row.webhook_url:
        raise ValueError("webhook_url is required")
    response = httpx.post(
        row.webhook_url,
        json={"id": row.id, "channel": row.channel, "to": row.recipient, "body": row.body},
        timeout=10,
    )
    response.raise_for_status()


def process_notification(notification_id: int) -> None:
    with SessionLocal() as db:
        row = db.get(Notification, notification_id)
        if not row or row.status in {"delivered", "dead"}:
            return
        row.attempts += 1
        row.status = "processing"
        row.updated_at = datetime.now(UTC)
        db.commit()
        try:
            if row.channel == "email":
                deliver_email(row)
            else:
                deliver_webhook(row)
            row.status = "delivered"
            row.last_error = None
        except Exception as exc:  # delivery failures become retries / DLQ
            row.last_error = str(exc)
            row.status = "dead" if row.attempts >= MAX_ATTEMPTS else "queued"
            logger.warning("notification %s failed attempt %s: %s", row.id, row.attempts, exc)
        row.updated_at = datetime.now(UTC)
        db.commit()
        # Without RabbitMQ, retry inline; the worker handles requeue when Rabbit is enabled.
        if row.status == "queued" and not RABBITMQ_URL:
            process_notification(row.id)


def enqueue(notification_id: int) -> None:
    if not RABBITMQ_URL:
        _memory_queue.append(notification_id)
        process_notification(notification_id)
        return
    import asyncio

    async def _publish() -> None:
        import aio_pika

        connection = await aio_pika.connect_robust(RABBITMQ_URL)
        async with connection:
            channel = await connection.channel()
            await channel.declare_queue(QUEUE_NAME, durable=True)
            await channel.declare_queue(DLQ_NAME, durable=True)
            await channel.default_exchange.publish(
                aio_pika.Message(body=json.dumps({"id": notification_id}).encode(), delivery_mode=aio_pika.DeliveryMode.PERSISTENT),
                routing_key=QUEUE_NAME,
            )

    asyncio.run(_publish())


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Notification Service", version="1.0.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    with engine.connect() as connection:
        connection.exec_driver_sql("SELECT 1")
    return {"status": "ok"}


@app.post("/v1/notifications", response_model=NotificationResponse, status_code=status.HTTP_202_ACCEPTED)
def create_notification(payload: CreateNotification, db: Session = Depends(get_db)) -> NotificationResponse:
    if payload.channel == "email":
        if not payload.to:
            raise HTTPException(status_code=422, detail="to is required for email")
        recipient = payload.to
    else:
        if not payload.webhook_url:
            raise HTTPException(status_code=422, detail="webhook_url is required for webhook")
        recipient = payload.to or str(payload.webhook_url)
    row = Notification(
        channel=payload.channel,
        recipient=recipient,
        subject=payload.subject,
        body=payload.body,
        webhook_url=str(payload.webhook_url) if payload.webhook_url else None,
        status="queued",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    enqueue(row.id)
    db.refresh(row)
    return to_response(row)


@app.get("/v1/notifications/{notification_id}", response_model=NotificationResponse)
def get_notification(notification_id: int, db: Session = Depends(get_db)) -> NotificationResponse:
    row = db.get(Notification, notification_id)
    if not row:
        raise HTTPException(status_code=404, detail="notification not found")
    return to_response(row)


@app.get("/v1/notifications", response_model=list[NotificationResponse])
def list_notifications(limit: int = 50, db: Session = Depends(get_db)) -> list[NotificationResponse]:
    rows = db.scalars(select(Notification).order_by(desc(Notification.id)).limit(min(limit, 200))).all()
    return [to_response(row) for row in rows]

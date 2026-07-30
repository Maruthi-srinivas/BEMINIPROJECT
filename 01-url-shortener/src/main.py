"""URL shortening API with PostgreSQL persistence and Redis read-through cache."""

from __future__ import annotations

import base64
import hashlib
import logging
import os
import re
import uuid
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from urllib.parse import urlparse

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field, HttpUrl
from redis import Redis
from redis.exceptions import RedisError
from sqlalchemy import DateTime, Integer, String, create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./url_shortener.db")
REDIS_URL = os.getenv("REDIS_URL", "")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000").rstrip("/")
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "86400"))
ALIAS_PATTERN = re.compile(r"^[A-Za-z0-9_-]{4,64}$")

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
cache = Redis.from_url(REDIS_URL, decode_responses=True) if REDIS_URL else None
logger = logging.getLogger("url_shortener")


class Base(DeclarativeBase):
    pass


class ShortUrl(Base):
    __tablename__ = "short_urls"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    destination: Mapped[str] = mapped_column(String(2048))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    last_accessed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    click_count: Mapped[int] = mapped_column(Integer, default=0)


class CreateUrl(BaseModel):
    destination: HttpUrl
    alias: str | None = Field(default=None, description="4-64 URL-safe characters")


class UrlCreated(BaseModel):
    code: str
    short_url: str
    destination: str
    created_at: datetime


class UrlStats(UrlCreated):
    click_count: int
    last_accessed_at: datetime | None


def get_db():
    with SessionLocal() as db:
        yield db


def cache_key(code: str) -> str:
    return f"url-shortener:url:{code}"


def generated_code() -> str:
    digest = hashlib.blake2b(uuid.uuid4().bytes, digest_size=7).digest()
    return base64.urlsafe_b64encode(digest).decode().rstrip("=")


def set_cache(code: str, destination: str) -> None:
    if not cache:
        return
    try:
        cache.setex(cache_key(code), CACHE_TTL_SECONDS, destination)
    except RedisError:
        logger.warning("redis cache write failed")


def make_response(row: ShortUrl) -> UrlCreated:
    return UrlCreated(
        code=row.code,
        short_url=f"{BASE_URL}/{row.code}",
        destination=row.destination,
        created_at=row.created_at,
    )


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="URL Shortener", version="1.0.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    with engine.connect() as connection:
        connection.exec_driver_sql("SELECT 1")
    return {"status": "ok"}


@app.post("/api/v1/urls", response_model=UrlCreated, status_code=status.HTTP_201_CREATED)
def create_url(payload: CreateUrl, db: Session = Depends(get_db)) -> UrlCreated:
    alias = payload.alias
    if alias and not ALIAS_PATTERN.fullmatch(alias):
        raise HTTPException(status_code=422, detail="alias must be 4-64 URL-safe characters")

    # The generated code retry protects against the extremely unlikely hash collision.
    for _ in range(5):
        code = alias or generated_code()
        row = ShortUrl(code=code, destination=str(payload.destination))
        db.add(row)
        try:
            db.commit()
            db.refresh(row)
            set_cache(row.code, row.destination)
            return make_response(row)
        except IntegrityError:
            db.rollback()
            if alias:
                raise HTTPException(status_code=409, detail="alias is already in use") from None
    raise HTTPException(status_code=503, detail="could not allocate a unique short code")


@app.get("/{code}", include_in_schema=False)
def redirect(code: str, request: Request, db: Session = Depends(get_db)) -> RedirectResponse:
    destination: str | None = None
    if cache:
        try:
            destination = cache.get(cache_key(code))
        except RedisError:
            logger.warning("redis cache read failed")

    row = db.scalar(select(ShortUrl).where(ShortUrl.code == code))
    if not row:
        raise HTTPException(status_code=404, detail="short URL not found")
    if not destination:
        destination = row.destination
        set_cache(code, destination)

    row.click_count += 1
    row.last_accessed_at = datetime.now(UTC)
    db.commit()
    logger.info("short URL redirected", extra={"method": request.method, "path": request.url.path})
    return RedirectResponse(destination, status_code=status.HTTP_302_FOUND)


@app.get("/api/v1/urls/{code}/stats", response_model=UrlStats)
def get_stats(code: str, db: Session = Depends(get_db)) -> UrlStats:
    row = db.scalar(select(ShortUrl).where(ShortUrl.code == code))
    if not row:
        raise HTTPException(status_code=404, detail="short URL not found")
    return UrlStats(**make_response(row).model_dump(), click_count=row.click_count, last_accessed_at=row.last_accessed_at)

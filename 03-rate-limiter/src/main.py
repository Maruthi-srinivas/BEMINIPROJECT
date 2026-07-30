"""Policy-backed Redis token-bucket and sliding-window rate limiting API."""

from __future__ import annotations

import os
import time
from collections import defaultdict, deque
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field
from redis import Redis
from redis.exceptions import RedisError
from sqlalchemy import Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rate_limiter.db")
REDIS_URL = os.getenv("REDIS_URL", "")
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
redis_client = Redis.from_url(REDIS_URL, decode_responses=True) if REDIS_URL else None
memory_windows: dict[str, deque[float]] = defaultdict(deque)

TOKEN_BUCKET_SCRIPT = """
local capacity, refill_rate, cost = tonumber(ARGV[1]), tonumber(ARGV[2]), tonumber(ARGV[3])
local current = redis.call('HMGET', KEYS[1], 'tokens', 'updated_at')
local tokens, updated = tonumber(current[1]), tonumber(current[2])
local now = tonumber(redis.call('TIME')[1])
if not tokens then tokens = capacity end
if not updated then updated = now end
tokens = math.min(capacity, tokens + (now - updated) * refill_rate)
local allowed = tokens >= cost
if allowed then tokens = tokens - cost end
redis.call('HMSET', KEYS[1], 'tokens', tokens, 'updated_at', now)
redis.call('EXPIRE', KEYS[1], math.max(1, math.ceil(capacity / refill_rate) * 2))
return {allowed and 1 or 0, math.floor(tokens), now}
"""
SLIDING_WINDOW_SCRIPT = """
local now, window, limit, cost = tonumber(ARGV[1]), tonumber(ARGV[2]), tonumber(ARGV[3]), tonumber(ARGV[4])
local minimum = now - window
redis.call('ZREMRANGEBYSCORE', KEYS[1], 0, minimum)
local count = redis.call('ZCARD', KEYS[1])
local allowed = count + cost <= limit
if allowed then
  for i = 1, cost do redis.call('ZADD', KEYS[1], now, now .. '-' .. i .. '-' .. math.random()) end
end
redis.call('EXPIRE', KEYS[1], math.ceil(window))
return {allowed and 1 or 0, limit - count - (allowed and cost or 0), minimum + window}
"""


class Base(DeclarativeBase):
    pass


class Policy(Base):
    __tablename__ = "policies"

    client_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    algorithm: Mapped[str] = mapped_column(String(32), default="token_bucket")
    limit: Mapped[int] = mapped_column(Integer)
    window_seconds: Mapped[int] = mapped_column(Integer)


class PolicyInput(BaseModel):
    algorithm: str = Field(pattern="^(token_bucket|sliding_window)$")
    limit: int = Field(gt=0, le=1_000_000)
    window_seconds: int = Field(gt=0, le=86_400)


class PolicyResponse(PolicyInput):
    client_id: str


class CheckRequest(BaseModel):
    client_id: str = Field(min_length=1, max_length=128)
    cost: int = Field(default=1, gt=0, le=10_000)


class CheckResponse(BaseModel):
    allowed: bool
    limit: int
    remaining: int
    reset_at: int


def get_db():
    with SessionLocal() as db:
        yield db


def policy_response(policy: Policy) -> PolicyResponse:
    return PolicyResponse(
        client_id=policy.client_id,
        algorithm=policy.algorithm,
        limit=policy.limit,
        window_seconds=policy.window_seconds,
    )


def in_memory_check(request: CheckRequest, policy: Policy) -> tuple[bool, int, int]:
    now = time.time()
    values = memory_windows[request.client_id]
    while values and values[0] <= now - policy.window_seconds:
        values.popleft()
    allowed = len(values) + request.cost <= policy.limit
    if allowed:
        values.extend([now] * request.cost)
    return allowed, max(0, policy.limit - len(values)), int(now + policy.window_seconds)


def redis_check(request: CheckRequest, policy: Policy) -> tuple[bool, int, int]:
    if not redis_client:
        return in_memory_check(request, policy)
    try:
        key = f"rate-limiter:{policy.algorithm}:{request.client_id}"
        if policy.algorithm == "token_bucket":
            refill_rate = policy.limit / policy.window_seconds
            result = redis_client.eval(TOKEN_BUCKET_SCRIPT, 1, key, policy.limit, refill_rate, request.cost)
            return bool(result[0]), max(0, int(result[1])), int(result[2] + policy.window_seconds)
        result = redis_client.eval(
            SLIDING_WINDOW_SCRIPT, 1, key, time.time(), policy.window_seconds, policy.limit, request.cost
        )
        return bool(result[0]), max(0, int(result[1])), int(result[2])
    except RedisError:
        # Retaining availability in development is useful, but production should alert on this path.
        return in_memory_check(request, policy)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="API Rate Limiter", version="1.0.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    with engine.connect() as connection:
        connection.exec_driver_sql("SELECT 1")
    return {"status": "ok"}


@app.put("/v1/policies/{client_id}", response_model=PolicyResponse)
def upsert_policy(client_id: str, payload: PolicyInput, db: Session = Depends(get_db)) -> PolicyResponse:
    policy = db.get(Policy, client_id)
    if not policy:
        policy = Policy(client_id=client_id, **payload.model_dump())
        db.add(policy)
    else:
        policy.algorithm = payload.algorithm
        policy.limit = payload.limit
        policy.window_seconds = payload.window_seconds
    db.commit()
    db.refresh(policy)
    return policy_response(policy)


@app.get("/v1/policies/{client_id}", response_model=PolicyResponse)
def get_policy(client_id: str, db: Session = Depends(get_db)) -> PolicyResponse:
    policy = db.get(Policy, client_id)
    if not policy:
        raise HTTPException(status_code=404, detail="policy not found")
    return policy_response(policy)


@app.post("/v1/check", response_model=CheckResponse)
def check_limit(request: CheckRequest, response: Response, db: Session = Depends(get_db)) -> CheckResponse:
    policy = db.get(Policy, request.client_id)
    if not policy:
        raise HTTPException(status_code=404, detail="policy not found")
    allowed, remaining, reset_at = redis_check(request, policy)
    response.headers["X-RateLimit-Limit"] = str(policy.limit)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    response.headers["X-RateLimit-Reset"] = str(reset_at)
    if not allowed:
        response.status_code = status.HTTP_429_TOO_MANY_REQUESTS
    return CheckResponse(allowed=allowed, limit=policy.limit, remaining=remaining, reset_at=reset_at)

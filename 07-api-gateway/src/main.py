"""Self-contained API gateway with JWT auth, local rate limits, and reverse proxy."""

from __future__ import annotations

import json
import os
import time
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from typing import Any

import httpx
import jwt
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from redis import Redis
from redis.exceptions import RedisError

JWT_SECRET = os.getenv("JWT_SECRET", "change-this-in-production")
JWT_ALGORITHM = "HS256"
REDIS_URL = os.getenv("REDIS_URL", "")
RATE_LIMIT = int(os.getenv("RATE_LIMIT", "60"))
RATE_WINDOW_SECONDS = int(os.getenv("RATE_WINDOW_SECONDS", "60"))
GATEWAY_ROUTES_RAW = os.getenv(
    "GATEWAY_ROUTES",
    '[{"prefix":"/upstream","target":"https://httpbin.org","public":false}]',
)

redis_client = Redis.from_url(REDIS_URL, decode_responses=True) if REDIS_URL else None
memory_windows: dict[str, deque[float]] = defaultdict(deque)
PUBLIC_PATHS = {"/health", "/docs", "/openapi.json", "/redoc", "/gateway/routes"}


class RouteConfig(BaseModel):
    prefix: str = Field(min_length=1)
    target: str = Field(min_length=1)
    public: bool = False


def load_routes() -> list[RouteConfig]:
    data = json.loads(GATEWAY_ROUTES_RAW)
    return [RouteConfig.model_validate(item) for item in data]


ROUTES = load_routes()


class RouteResponse(BaseModel):
    prefix: str
    target: str
    public: bool


def match_route(path: str) -> RouteConfig | None:
    candidates = sorted(ROUTES, key=lambda route: len(route.prefix), reverse=True)
    for route in candidates:
        if path == route.prefix or path.startswith(route.prefix.rstrip("/") + "/"):
            return route
    return None


def extract_bearer(request: Request) -> str | None:
    header = request.headers.get("authorization")
    if not header or not header.lower().startswith("bearer "):
        return None
    return header.split(" ", 1)[1].strip()


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=401, detail="invalid or expired access token") from exc


def rate_limit_allow(key: str) -> tuple[bool, int, int]:
    now = time.time()
    if redis_client:
        try:
            redis_key = f"gateway:rl:{key}"
            pipe = redis_client.pipeline()
            pipe.zremrangebyscore(redis_key, 0, now - RATE_WINDOW_SECONDS)
            pipe.zcard(redis_key)
            pipe.zadd(redis_key, {f"{now}": now})
            pipe.expire(redis_key, RATE_WINDOW_SECONDS)
            _, count, _, _ = pipe.execute()
            remaining = max(0, RATE_LIMIT - int(count))
            allowed = int(count) <= RATE_LIMIT
            return allowed, remaining, int(now + RATE_WINDOW_SECONDS)
        except RedisError:
            pass
    values = memory_windows[key]
    while values and values[0] <= now - RATE_WINDOW_SECONDS:
        values.popleft()
    allowed = len(values) < RATE_LIMIT
    if allowed:
        values.append(now)
    remaining = max(0, RATE_LIMIT - len(values))
    return allowed, remaining, int(now + RATE_WINDOW_SECONDS)


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(title="API Gateway", version="1.0.0", lifespan=lifespan)

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
    return {"status": "ok"}


@app.get("/gateway/routes", response_model=list[RouteResponse])
def list_routes() -> list[RouteResponse]:
    return [RouteResponse(prefix=route.prefix, target=route.target, public=route.public) for route in ROUTES]


@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
async def proxy(full_path: str, request: Request) -> Response:
    path = "/" + full_path
    if path in PUBLIC_PATHS or path.startswith("/docs") or path.startswith("/openapi"):
        raise HTTPException(status_code=404, detail="not found")

    route = match_route(path)
    if not route:
        raise HTTPException(status_code=404, detail="no upstream route matched")

    claims: dict[str, Any] | None = None
    if not route.public:
        token = extract_bearer(request)
        if not token:
            raise HTTPException(status_code=401, detail="missing bearer token")
        claims = decode_token(token)

    rate_key = str(claims.get("sub")) if claims and claims.get("sub") else (request.client.host if request.client else "anonymous")
    allowed, remaining, reset_at = rate_limit_allow(rate_key)
    headers = {
        "X-RateLimit-Limit": str(RATE_LIMIT),
        "X-RateLimit-Remaining": str(remaining),
        "X-RateLimit-Reset": str(reset_at),
    }
    if not allowed:
        return JSONResponse(status_code=429, content={"detail": "rate limit exceeded"}, headers=headers)

    suffix = path[len(route.prefix) :] if path.startswith(route.prefix) else path
    if not suffix.startswith("/"):
        suffix = "/" + suffix if suffix else ""
    target_url = route.target.rstrip("/") + (suffix or "/")
    if request.url.query:
        target_url = f"{target_url}?{request.url.query}"

    excluded = {"host", "content-length", "authorization"}
    outbound_headers = {key: value for key, value in request.headers.items() if key.lower() not in excluded}
    if claims:
        outbound_headers["X-User-Id"] = str(claims.get("sub", ""))
        outbound_headers["X-User-Role"] = str(claims.get("role", ""))

    body = await request.body()
    async with httpx.AsyncClient(follow_redirects=False, timeout=30) as client:
        upstream = await client.request(
            request.method,
            target_url,
            headers=outbound_headers,
            content=body,
        )
    response_headers = {
        key: value
        for key, value in upstream.headers.items()
        if key.lower() not in {"content-encoding", "transfer-encoding", "connection"}
    }
    response_headers.update(headers)
    return Response(content=upstream.content, status_code=upstream.status_code, headers=response_headers)

"""In-memory mini Redis with TTL and WebSocket pub/sub over HTTP."""

from __future__ import annotations

import asyncio
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any

from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect, status
from pydantic import BaseModel, Field

STORE: dict[str, "Entry"] = {}
SUBSCRIBERS: dict[str, set[WebSocket]] = {}
_cleanup_task: asyncio.Task | None = None


@dataclass
class Entry:
    value: Any
    expires_at: float | None = None

    def expired(self, now: float | None = None) -> bool:
        if self.expires_at is None:
            return False
        return (now or time.time()) >= self.expires_at


class SetRequest(BaseModel):
    value: Any
    ttl_seconds: int | None = Field(default=None, gt=0, le=86400)


class KeyResponse(BaseModel):
    key: str
    value: Any
    ttl_seconds: int | None


class PublishRequest(BaseModel):
    channel: str = Field(min_length=1, max_length=256)
    message: Any


class PublishResponse(BaseModel):
    channel: str
    subscribers: int


def purge_if_expired(key: str) -> None:
    entry = STORE.get(key)
    if entry and entry.expired():
        STORE.pop(key, None)


def remaining_ttl(entry: Entry) -> int | None:
    if entry.expires_at is None:
        return None
    return max(0, int(entry.expires_at - time.time()))


async def cleanup_loop() -> None:
    while True:
        now = time.time()
        expired = [key for key, entry in list(STORE.items()) if entry.expired(now)]
        for key in expired:
            STORE.pop(key, None)
        await asyncio.sleep(1)


@asynccontextmanager
async def lifespan(_: FastAPI):
    global _cleanup_task
    _cleanup_task = asyncio.create_task(cleanup_loop())
    yield
    if _cleanup_task:
        _cleanup_task.cancel()
        try:
            await _cleanup_task
        except asyncio.CancelledError:
            pass


app = FastAPI(title="Mini Redis", version="1.0.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "keys": str(len(STORE))}


@app.put("/v1/keys/{key}", response_model=KeyResponse)
def set_key(key: str, payload: SetRequest) -> KeyResponse:
    expires_at = time.time() + payload.ttl_seconds if payload.ttl_seconds else None
    STORE[key] = Entry(value=payload.value, expires_at=expires_at)
    return KeyResponse(key=key, value=payload.value, ttl_seconds=payload.ttl_seconds)


@app.get("/v1/keys/{key}", response_model=KeyResponse)
def get_key(key: str) -> KeyResponse:
    purge_if_expired(key)
    entry = STORE.get(key)
    if not entry:
        raise HTTPException(status_code=404, detail="key not found")
    return KeyResponse(key=key, value=entry.value, ttl_seconds=remaining_ttl(entry))


@app.delete("/v1/keys/{key}", status_code=status.HTTP_204_NO_CONTENT)
def delete_key(key: str) -> None:
    purge_if_expired(key)
    if key not in STORE:
        raise HTTPException(status_code=404, detail="key not found")
    STORE.pop(key, None)


@app.get("/v1/keys")
def list_keys(limit: int = Query(default=100, ge=1, le=1000)) -> dict[str, list[str]]:
    now = time.time()
    keys = [key for key, entry in STORE.items() if not entry.expired(now)]
    return {"keys": sorted(keys)[:limit]}


@app.post("/v1/publish", response_model=PublishResponse)
async def publish(payload: PublishRequest) -> PublishResponse:
    sockets = list(SUBSCRIBERS.get(payload.channel, set()))
    dead: list[WebSocket] = []
    for socket in sockets:
        try:
            await socket.send_json({"channel": payload.channel, "message": payload.message})
        except Exception:
            dead.append(socket)
    for socket in dead:
        SUBSCRIBERS.get(payload.channel, set()).discard(socket)
    return PublishResponse(channel=payload.channel, subscribers=len(sockets) - len(dead))


@app.websocket("/v1/subscribe")
async def subscribe(websocket: WebSocket, channel: str | None = None) -> None:
    await websocket.accept()
    channels: set[str] = set()
    if channel:
        channels.add(channel)
        SUBSCRIBERS.setdefault(channel, set()).add(websocket)
        await websocket.send_json({"subscribed": list(channels)})
    try:
        while True:
            raw = await websocket.receive_json()
            if isinstance(raw, dict) and raw.get("action") == "subscribe":
                names = raw.get("channels") or ([raw["channel"]] if raw.get("channel") else [])
                for name in names:
                    channels.add(name)
                    SUBSCRIBERS.setdefault(name, set()).add(websocket)
                await websocket.send_json({"subscribed": sorted(channels)})
            elif isinstance(raw, dict) and raw.get("action") == "unsubscribe":
                names = raw.get("channels") or ([raw["channel"]] if raw.get("channel") else [])
                for name in names:
                    channels.discard(name)
                    SUBSCRIBERS.get(name, set()).discard(websocket)
                await websocket.send_json({"subscribed": sorted(channels)})
    except WebSocketDisconnect:
        for name in channels:
            SUBSCRIBERS.get(name, set()).discard(websocket)

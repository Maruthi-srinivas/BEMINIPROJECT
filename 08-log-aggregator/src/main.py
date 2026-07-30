"""Centralized log ingest and search backed by OpenSearch."""

from __future__ import annotations

import hashlib
import os
import secrets
import uuid
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Any

import httpx
from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import DateTime, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./log_aggregator.db")
OPENSEARCH_URL = os.getenv("OPENSEARCH_URL", "http://localhost:9200").rstrip("/")
LOG_INDEX = os.getenv("LOG_INDEX", "app-logs")

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class CreateSource(BaseModel):
    name: str = Field(min_length=1, max_length=128)


class SourceResponse(BaseModel):
    id: int
    name: str
    token: str
    created_at: datetime


class LogEvent(BaseModel):
    service: str = Field(min_length=1, max_length=128)
    level: str = Field(default="info", pattern="^(debug|info|warning|error|critical)$")
    message: str = Field(min_length=1)
    timestamp: datetime | None = None
    fields: dict[str, Any] = Field(default_factory=dict)


class IngestRequest(BaseModel):
    events: list[LogEvent] = Field(default_factory=list)
    service: str | None = None
    level: str | None = None
    message: str | None = None
    timestamp: datetime | None = None
    fields: dict[str, Any] | None = None


class IngestResponse(BaseModel):
    accepted: int
    ids: list[str]


class LogDocument(BaseModel):
    id: str
    service: str
    level: str
    message: str
    timestamp: datetime
    fields: dict[str, Any]
    source: str


class SearchResponse(BaseModel):
    total: int
    hits: list[LogDocument]


class OpenSearchClient:
    def __init__(self, base_url: str, index: str):
        self.base_url = base_url
        self.index = index
        self._memory: dict[str, dict[str, Any]] = {}

    def ensure_index(self) -> None:
        if not self.base_url:
            return
        try:
            with httpx.Client(timeout=5) as client:
                response = client.put(f"{self.base_url}/{self.index}")
                if response.status_code not in {200, 201, 400}:
                    response.raise_for_status()
        except httpx.HTTPError:
            # Local/dev without OpenSearch falls back to in-memory documents.
            pass

    def index_document(self, doc_id: str, body: dict[str, Any]) -> None:
        if not self.base_url:
            self._memory[doc_id] = body
            return
        try:
            with httpx.Client(timeout=10) as client:
                response = client.put(f"{self.base_url}/{self.index}/_doc/{doc_id}", json=body)
                response.raise_for_status()
        except httpx.HTTPError:
            self._memory[doc_id] = body

    def get_document(self, doc_id: str) -> dict[str, Any] | None:
        if doc_id in self._memory:
            return self._memory[doc_id]
        if not self.base_url:
            return None
        try:
            with httpx.Client(timeout=10) as client:
                response = client.get(f"{self.base_url}/{self.index}/_doc/{doc_id}")
                if response.status_code == 404:
                    return None
                response.raise_for_status()
                return response.json().get("_source")
        except httpx.HTTPError:
            return self._memory.get(doc_id)

    def search(
        self,
        *,
        q: str | None,
        service: str | None,
        level: str | None,
        from_ts: datetime | None,
        to_ts: datetime | None,
        size: int,
    ) -> tuple[int, list[tuple[str, dict[str, Any]]]]:
        if not self.base_url:
            hits = []
            for doc_id, body in self._memory.items():
                if service and body.get("service") != service:
                    continue
                if level and body.get("level") != level:
                    continue
                if q and q.lower() not in str(body.get("message", "")).lower():
                    continue
                ts = datetime.fromisoformat(body["timestamp"].replace("Z", "+00:00"))
                if from_ts and ts < from_ts:
                    continue
                if to_ts and ts > to_ts:
                    continue
                hits.append((doc_id, body))
            hits = hits[:size]
            return len(hits), hits

        must: list[dict[str, Any]] = []
        if q:
            must.append({"match": {"message": q}})
        if service:
            must.append({"term": {"service.keyword": service}})
        if level:
            must.append({"term": {"level.keyword": level}})
        if from_ts or to_ts:
            rang: dict[str, str] = {}
            if from_ts:
                rang["gte"] = from_ts.isoformat()
            if to_ts:
                rang["lte"] = to_ts.isoformat()
            must.append({"range": {"timestamp": rang}})
        query: dict[str, Any] = {"bool": {"must": must}} if must else {"match_all": {}}
        payload = {"size": size, "query": query, "sort": [{"timestamp": {"order": "desc"}}]}
        with httpx.Client(timeout=10) as client:
            response = client.post(f"{self.base_url}/{self.index}/_search", json=payload)
            response.raise_for_status()
            data = response.json()
        hits = [(hit["_id"], hit["_source"]) for hit in data.get("hits", {}).get("hits", [])]
        total = data.get("hits", {}).get("total", {})
        count = total.get("value", len(hits)) if isinstance(total, dict) else int(total)
        return count, hits


opensearch = OpenSearchClient(OPENSEARCH_URL if OPENSEARCH_URL else "", LOG_INDEX)


def get_db():
    with SessionLocal() as db:
        yield db


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def require_source(
    x_source_token: str = Header(..., alias="X-Source-Token"),
    db: Session = Depends(get_db),
) -> Source:
    row = db.scalar(select(Source).where(Source.token_hash == hash_token(x_source_token)))
    if not row:
        raise HTTPException(status_code=401, detail="invalid source token")
    return row


def normalize_events(payload: IngestRequest) -> list[LogEvent]:
    if payload.events:
        return payload.events
    if payload.service and payload.message:
        return [
            LogEvent(
                service=payload.service,
                level=payload.level or "info",
                message=payload.message,
                timestamp=payload.timestamp,
                fields=payload.fields or {},
            )
        ]
    raise HTTPException(status_code=422, detail="provide events[] or a single service/message")


def to_document(doc_id: str, body: dict[str, Any]) -> LogDocument:
    return LogDocument(
        id=doc_id,
        service=body["service"],
        level=body["level"],
        message=body["message"],
        timestamp=datetime.fromisoformat(body["timestamp"].replace("Z", "+00:00")),
        fields=body.get("fields") or {},
        source=body.get("source", ""),
    )


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    opensearch.ensure_index()
    yield


app = FastAPI(title="Log Aggregator", version="1.0.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    with engine.connect() as connection:
        connection.exec_driver_sql("SELECT 1")
    return {"status": "ok"}


@app.post("/v1/sources", response_model=SourceResponse, status_code=status.HTTP_201_CREATED)
def create_source(payload: CreateSource, db: Session = Depends(get_db)) -> SourceResponse:
    if db.scalar(select(Source).where(Source.name == payload.name)):
        raise HTTPException(status_code=409, detail="source name already exists")
    token = secrets.token_urlsafe(24)
    row = Source(name=payload.name, token_hash=hash_token(token))
    db.add(row)
    db.commit()
    db.refresh(row)
    return SourceResponse(id=row.id, name=row.name, token=token, created_at=row.created_at)


@app.post("/v1/logs", response_model=IngestResponse, status_code=status.HTTP_202_ACCEPTED)
def ingest_logs(payload: IngestRequest, source: Source = Depends(require_source)) -> IngestResponse:
    events = normalize_events(payload)
    ids: list[str] = []
    for event in events:
        doc_id = str(uuid.uuid4())
        ts = event.timestamp or datetime.now(UTC)
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=UTC)
        body = {
            "service": event.service,
            "level": event.level,
            "message": event.message,
            "timestamp": ts.isoformat(),
            "fields": event.fields,
            "source": source.name,
        }
        opensearch.index_document(doc_id, body)
        ids.append(doc_id)
    return IngestResponse(accepted=len(ids), ids=ids)


@app.get("/v1/logs/search", response_model=SearchResponse)
def search_logs(
    q: str | None = None,
    service: str | None = None,
    level: str | None = None,
    from_ts: datetime | None = Query(default=None, alias="from"),
    to_ts: datetime | None = Query(default=None, alias="to"),
    size: int = Query(default=50, ge=1, le=200),
) -> SearchResponse:
    total, hits = opensearch.search(q=q, service=service, level=level, from_ts=from_ts, to_ts=to_ts, size=size)
    return SearchResponse(total=total, hits=[to_document(doc_id, body) for doc_id, body in hits])


@app.get("/v1/logs/{doc_id}", response_model=LogDocument)
def get_log(doc_id: str) -> LogDocument:
    body = opensearch.get_document(doc_id)
    if not body:
        raise HTTPException(status_code=404, detail="log not found")
    return to_document(doc_id, body)

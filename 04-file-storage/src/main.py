"""Mini S3-style object storage with HMAC signed URLs."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import time
from base64 import urlsafe_b64decode, urlsafe_b64encode
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from pathlib import Path

from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile, status
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from sqlalchemy import DateTime, Integer, String, UniqueConstraint, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./file_storage.db")
STORAGE_ROOT = Path(os.getenv("STORAGE_ROOT", "./data/objects"))
SIGNING_SECRET = os.getenv("SIGNING_SECRET", "change-this-signing-secret")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8004").rstrip("/")
BUCKET_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$")

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Bucket(Base):
    __tablename__ = "buckets"

    name: Mapped[str] = mapped_column(String(64), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class StoredObject(Base):
    __tablename__ = "objects"
    __table_args__ = (UniqueConstraint("bucket", "key", name="uq_bucket_key"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    bucket: Mapped[str] = mapped_column(String(64), index=True)
    key: Mapped[str] = mapped_column(String(1024))
    size: Mapped[int] = mapped_column(Integer)
    content_type: Mapped[str] = mapped_column(String(255), default="application/octet-stream")
    etag: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class BucketResponse(BaseModel):
    name: str
    created_at: datetime


class ObjectMeta(BaseModel):
    bucket: str
    key: str
    size: int
    content_type: str
    etag: str
    created_at: datetime


class SignedUrlRequest(BaseModel):
    method: str = Field(pattern="^(GET|PUT)$")
    expires_in: int = Field(default=300, gt=0, le=86400)


class SignedUrlResponse(BaseModel):
    url: str
    method: str
    expires_at: int


def get_db():
    with SessionLocal() as db:
        yield db


def object_path(bucket: str, key: str) -> Path:
    safe_key = key.replace("\\", "/").lstrip("/")
    path = (STORAGE_ROOT / bucket / safe_key).resolve()
    root = STORAGE_ROOT.resolve()
    if not str(path).startswith(str(root)):
        raise HTTPException(status_code=400, detail="invalid object key")
    return path


def validate_bucket(name: str) -> None:
    if not BUCKET_PATTERN.fullmatch(name):
        raise HTTPException(status_code=422, detail="invalid bucket name")


def sign_payload(payload: dict) -> str:
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    digest = hmac.new(SIGNING_SECRET.encode(), body, hashlib.sha256).digest()
    return urlsafe_b64encode(body + b"." + digest).decode().rstrip("=")


def unsign_token(token: str) -> dict:
    padding = "=" * (-len(token) % 4)
    raw = urlsafe_b64decode(token + padding)
    try:
        body, digest = raw.rsplit(b".", 1)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="invalid signed token") from exc
    expected = hmac.new(SIGNING_SECRET.encode(), body, hashlib.sha256).digest()
    if not hmac.compare_digest(digest, expected):
        raise HTTPException(status_code=403, detail="invalid signed token signature")
    payload = json.loads(body)
    if int(payload["exp"]) < int(time.time()):
        raise HTTPException(status_code=403, detail="signed URL expired")
    return payload


def store_bytes(db: Session, bucket: str, key: str, data: bytes, content_type: str) -> ObjectMeta:
    path = object_path(bucket, key)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    etag = hashlib.md5(data).hexdigest()
    row = db.scalar(select(StoredObject).where(StoredObject.bucket == bucket, StoredObject.key == key))
    if not row:
        row = StoredObject(bucket=bucket, key=key, size=len(data), content_type=content_type, etag=etag)
        db.add(row)
    else:
        row.size = len(data)
        row.content_type = content_type
        row.etag = etag
        row.created_at = datetime.now(UTC)
    db.commit()
    db.refresh(row)
    return ObjectMeta(
        bucket=row.bucket,
        key=row.key,
        size=row.size,
        content_type=row.content_type,
        etag=row.etag,
        created_at=row.created_at,
    )


@asynccontextmanager
async def lifespan(_: FastAPI):
    STORAGE_ROOT.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Mini S3 Storage", version="1.0.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    with engine.connect() as connection:
        connection.exec_driver_sql("SELECT 1")
    return {"status": "ok"}


@app.put("/v1/buckets/{bucket}", response_model=BucketResponse, status_code=status.HTTP_201_CREATED)
def create_bucket(bucket: str, db: Session = Depends(get_db)) -> BucketResponse:
    validate_bucket(bucket)
    if db.get(Bucket, bucket):
        raise HTTPException(status_code=409, detail="bucket already exists")
    row = Bucket(name=bucket)
    db.add(row)
    db.commit()
    (STORAGE_ROOT / bucket).mkdir(parents=True, exist_ok=True)
    return BucketResponse(name=row.name, created_at=row.created_at)


@app.get("/v1/buckets", response_model=list[BucketResponse])
def list_buckets(db: Session = Depends(get_db)) -> list[BucketResponse]:
    rows = db.scalars(select(Bucket).order_by(Bucket.name)).all()
    return [BucketResponse(name=row.name, created_at=row.created_at) for row in rows]


@app.put("/v1/buckets/{bucket}/objects/{key:path}", response_model=ObjectMeta)
async def put_object(
    bucket: str,
    key: str,
    request: Request,
    file: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
) -> ObjectMeta:
    validate_bucket(bucket)
    if not db.get(Bucket, bucket):
        raise HTTPException(status_code=404, detail="bucket not found")
    if file is not None:
        data = await file.read()
        content_type = file.content_type or "application/octet-stream"
    else:
        data = await request.body()
        content_type = request.headers.get("content-type", "application/octet-stream")
    return store_bytes(db, bucket, key, data, content_type)


@app.get("/v1/buckets/{bucket}/objects/{key:path}")
def get_object(bucket: str, key: str, db: Session = Depends(get_db)) -> FileResponse:
    row = db.scalar(select(StoredObject).where(StoredObject.bucket == bucket, StoredObject.key == key))
    if not row:
        raise HTTPException(status_code=404, detail="object not found")
    path = object_path(bucket, key)
    if not path.exists():
        raise HTTPException(status_code=404, detail="object file missing")
    return FileResponse(path, media_type=row.content_type, filename=Path(key).name)


@app.delete("/v1/buckets/{bucket}/objects/{key:path}", status_code=status.HTTP_204_NO_CONTENT)
def delete_object(bucket: str, key: str, db: Session = Depends(get_db)) -> None:
    row = db.scalar(select(StoredObject).where(StoredObject.bucket == bucket, StoredObject.key == key))
    if not row:
        raise HTTPException(status_code=404, detail="object not found")
    path = object_path(bucket, key)
    if path.exists():
        path.unlink()
    db.delete(row)
    db.commit()


@app.post("/v1/buckets/{bucket}/objects/{key:path}/signed-url", response_model=SignedUrlResponse)
def create_signed_url(
    bucket: str, key: str, payload: SignedUrlRequest, db: Session = Depends(get_db)
) -> SignedUrlResponse:
    if not db.get(Bucket, bucket):
        raise HTTPException(status_code=404, detail="bucket not found")
    if payload.method == "GET":
        row = db.scalar(select(StoredObject).where(StoredObject.bucket == bucket, StoredObject.key == key))
        if not row:
            raise HTTPException(status_code=404, detail="object not found")
    expires_at = int(time.time()) + payload.expires_in
    token = sign_payload({"bucket": bucket, "key": key, "method": payload.method, "exp": expires_at})
    return SignedUrlResponse(url=f"{BASE_URL}/v1/signed/{token}", method=payload.method, expires_at=expires_at)


@app.api_route("/v1/signed/{token}", methods=["GET", "PUT"])
async def redeem_signed_url(token: str, request: Request, db: Session = Depends(get_db)):
    claims = unsign_token(token)
    if request.method != claims["method"]:
        raise HTTPException(status_code=405, detail="method not allowed for signed URL")
    bucket, key = claims["bucket"], claims["key"]
    if request.method == "GET":
        return get_object(bucket, key, db)
    if not db.get(Bucket, bucket):
        raise HTTPException(status_code=404, detail="bucket not found")
    data = await request.body()
    content_type = request.headers.get("content-type", "application/octet-stream")
    return store_bytes(db, bucket, key, data, content_type)

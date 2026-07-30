"""JWT authentication service with refresh-token rotation and role checks."""

from __future__ import annotations

import hashlib
import os
import secrets
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta
from urllib.parse import urlencode

import httpx
import jwt
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, Field
from pwdlib import PasswordHash
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./auth.db")
JWT_SECRET = os.getenv("JWT_SECRET", "change-this-in-production")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = int(os.getenv("ACCESS_TOKEN_MINUTES", "15"))
REFRESH_TOKEN_DAYS = int(os.getenv("REFRESH_TOKEN_DAYS", "14"))
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8002/auth/oauth/google/callback")

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
password_hash = PasswordHash.recommended()
bearer = HTTPBearer()


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(32), default="user")
    oauth_provider: Mapped[str | None] = mapped_column(String(32), nullable=True)
    oauth_subject: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="user")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    user: Mapped[User] = relationship(back_populates="refresh_tokens")


class Credentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


def get_db():
    with SessionLocal() as db:
        yield db


def user_response(user: User) -> UserResponse:
    return UserResponse(id=user.id, email=user.email, role=user.role)


def utcnow() -> datetime:
    return datetime.now(UTC)


def create_access_token(user: User) -> str:
    now = utcnow()
    return jwt.encode(
        {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
            "jti": secrets.token_hex(16),
            "iat": now,
            "exp": now + timedelta(minutes=ACCESS_TOKEN_MINUTES),
        },
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


def issue_tokens(user: User, db: Session) -> TokenResponse:
    raw_refresh = secrets.token_urlsafe(48)
    db.add(
        RefreshToken(
            user_id=user.id,
            token_hash=hashlib.sha256(raw_refresh.encode()).hexdigest(),
            expires_at=utcnow() + timedelta(days=REFRESH_TOKEN_DAYS),
        )
    )
    db.commit()
    return TokenResponse(access_token=create_access_token(user), refresh_token=raw_refresh)


def current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)
) -> User:
    try:
        claims = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user = db.get(User, int(claims["sub"]))
    except (jwt.PyJWTError, KeyError, ValueError):
        user = None
    if not user:
        raise HTTPException(status_code=401, detail="invalid or expired access token")
    return user


def admin_user(user: User = Depends(current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="admin role required")
    return user


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Authentication Service", version="1.0.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    with engine.connect() as connection:
        connection.exec_driver_sql("SELECT 1")
    return {"status": "ok"}


@app.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: Credentials, db: Session = Depends(get_db)) -> UserResponse:
    if db.scalar(select(User).where(User.email == str(payload.email).lower())):
        raise HTTPException(status_code=409, detail="email is already registered")
    user = User(email=str(payload.email).lower(), password_hash=password_hash.hash(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user_response(user)


@app.post("/auth/login", response_model=TokenResponse)
def login(payload: Credentials, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == str(payload.email).lower()))
    if not user or not user.password_hash or not password_hash.verify(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="invalid email or password")
    return issue_tokens(user, db)


@app.post("/auth/refresh", response_model=TokenResponse)
def refresh(payload: TokenRequest, db: Session = Depends(get_db)) -> TokenResponse:
    row = db.scalar(
        select(RefreshToken).where(RefreshToken.token_hash == hashlib.sha256(payload.refresh_token.encode()).hexdigest())
    )
    if not row or row.revoked or row.expires_at.replace(tzinfo=UTC) <= utcnow():
        raise HTTPException(status_code=401, detail="invalid or expired refresh token")
    row.revoked = True
    db.flush()
    return issue_tokens(row.user, db)


@app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(payload: TokenRequest, db: Session = Depends(get_db)) -> None:
    row = db.scalar(
        select(RefreshToken).where(RefreshToken.token_hash == hashlib.sha256(payload.refresh_token.encode()).hexdigest())
    )
    if row:
        row.revoked = True
        db.commit()


@app.get("/auth/me", response_model=UserResponse)
def me(user: User = Depends(current_user)) -> UserResponse:
    return user_response(user)


@app.get("/admin/users", response_model=list[UserResponse])
def list_users(_: User = Depends(admin_user), db: Session = Depends(get_db)) -> list[UserResponse]:
    return [user_response(user) for user in db.scalars(select(User).order_by(User.id)).all()]


@app.get("/auth/oauth/google/login")
def google_login() -> dict[str, str]:
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=503, detail="Google OAuth is not configured")
    state = jwt.encode(
        {"purpose": "google_oauth", "exp": utcnow() + timedelta(minutes=10)},
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )
    query = urlencode(
        {
            "client_id": GOOGLE_CLIENT_ID,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "state": state,
        }
    )
    return {"authorization_url": f"https://accounts.google.com/o/oauth2/v2/auth?{query}"}


@app.get("/auth/oauth/google/callback", response_model=TokenResponse)
def google_callback(code: str, state: str, db: Session = Depends(get_db)) -> TokenResponse:
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=503, detail="Google OAuth is not configured")
    try:
        if jwt.decode(state, JWT_SECRET, algorithms=[JWT_ALGORITHM]).get("purpose") != "google_oauth":
            raise ValueError
    except (jwt.PyJWTError, ValueError):
        raise HTTPException(status_code=400, detail="invalid OAuth state") from None
    token_response = httpx.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        },
        timeout=10,
    )
    if token_response.is_error:
        raise HTTPException(status_code=401, detail="Google OAuth token exchange failed")
    access_token = token_response.json().get("access_token")
    profile_response = httpx.get(
        "https://openidconnect.googleapis.com/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10,
    )
    if profile_response.is_error:
        raise HTTPException(status_code=401, detail="Google profile lookup failed")
    claims = profile_response.json()
    email, subject = claims.get("email"), claims.get("sub")
    if not email or not subject:
        raise HTTPException(status_code=401, detail="Google identity did not include email")
    user = db.scalar(select(User).where(User.oauth_provider == "google", User.oauth_subject == subject))
    if not user:
        user = db.scalar(select(User).where(User.email == email.lower()))
        if not user:
            user = User(email=email.lower(), oauth_provider="google", oauth_subject=subject)
            db.add(user)
            db.commit()
            db.refresh(user)
    return issue_tokens(user, db)

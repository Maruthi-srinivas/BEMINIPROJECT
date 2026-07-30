import importlib
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient


def test_registration_login_refresh_and_me(monkeypatch):
    with tempfile.TemporaryDirectory() as directory:
        database = Path(directory) / "test.db"
        monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database}")
        monkeypatch.setenv("JWT_SECRET", "test-secret-that-is-at-least-thirty-two-bytes")
        import src.main

        importlib.reload(src.main)
        with TestClient(src.main.app) as client:
            register = client.post(
                "/auth/register",
                json={"email": "user@example.com", "password": "a-strong-password"},
            )
            assert register.status_code == 201

            login = client.post(
                "/auth/login",
                json={"email": "user@example.com", "password": "a-strong-password"},
            )
            assert login.status_code == 200
            tokens = login.json()

            me = client.get("/auth/me", headers={"Authorization": f"Bearer {tokens['access_token']}"})
            assert me.status_code == 200
            assert me.json()["email"] == "user@example.com"

            refreshed = client.post("/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
            assert refreshed.status_code == 200
            assert refreshed.json()["access_token"] != tokens["access_token"]
        src.main.engine.dispose()

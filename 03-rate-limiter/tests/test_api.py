import importlib
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient


def test_policy_enforces_token_bucket(monkeypatch):
    with tempfile.TemporaryDirectory() as directory:
        database = Path(directory) / "test.db"
        monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database}")
        monkeypatch.delenv("REDIS_URL", raising=False)
        import src.main

        importlib.reload(src.main)
        with TestClient(src.main.app) as client:
            policy = client.put(
                "/v1/policies/test-client",
                json={"algorithm": "token_bucket", "limit": 2, "window_seconds": 60},
            )
            assert policy.status_code == 200

            assert client.post("/v1/check", json={"client_id": "test-client"}).status_code == 200
            assert client.post("/v1/check", json={"client_id": "test-client"}).status_code == 200
            exhausted = client.post("/v1/check", json={"client_id": "test-client"})
            assert exhausted.status_code == 429
            assert exhausted.json()["allowed"] is False
            assert exhausted.headers["x-ratelimit-remaining"] == "0"
        src.main.engine.dispose()

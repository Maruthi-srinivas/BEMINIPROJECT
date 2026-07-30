import importlib
from datetime import UTC, datetime, timedelta

import jwt
from fastapi.testclient import TestClient


def test_jwt_rate_limit_and_proxy(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "test-secret-that-is-at-least-thirty-two-bytes")
    monkeypatch.setenv("REDIS_URL", "")
    monkeypatch.setenv("RATE_LIMIT", "2")
    monkeypatch.setenv("RATE_WINDOW_SECONDS", "60")
    monkeypatch.setenv(
        "GATEWAY_ROUTES",
        '[{"prefix":"/upstream","target":"https://example.com","public":false}]',
    )
    import src.main

    importlib.reload(src.main)

    class FakeResponse:
        def __init__(self):
            self.content = b'{"ok":true}'
            self.status_code = 200
            self.headers = {"content-type": "application/json"}

    class FakeAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

        async def request(self, method, url, headers=None, content=None):
            assert method == "GET"
            assert url.startswith("https://example.com/")
            return FakeResponse()

    monkeypatch.setattr(src.main.httpx, "AsyncClient", FakeAsyncClient)

    token = jwt.encode(
        {
            "sub": "42",
            "role": "user",
            "exp": datetime.now(UTC) + timedelta(minutes=5),
        },
        "test-secret-that-is-at-least-thirty-two-bytes",
        algorithm="HS256",
    )

    with TestClient(src.main.app) as client:
        denied = client.get("/upstream/get")
        assert denied.status_code == 401

        first = client.get("/upstream/get", headers={"Authorization": f"Bearer {token}"})
        assert first.status_code == 200
        assert first.json() == {"ok": True}

        second = client.get("/upstream/get", headers={"Authorization": f"Bearer {token}"})
        assert second.status_code == 200

        limited = client.get("/upstream/get", headers={"Authorization": f"Bearer {token}"})
        assert limited.status_code == 429
        assert limited.headers["x-ratelimit-limit"] == "2"

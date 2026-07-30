import importlib
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient


def test_webhook_notification_inline(monkeypatch):
    with tempfile.TemporaryDirectory() as directory:
        database = Path(directory) / "test.db"
        monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database}")
        monkeypatch.delenv("RABBITMQ_URL", raising=False)
        monkeypatch.setenv("RABBITMQ_URL", "")

        calls: list[dict] = []

        def fake_post(url, json=None, timeout=10):
            calls.append({"url": url, "json": json})

            class Response:
                def raise_for_status(self):
                    return None

            return Response()

        import src.main

        importlib.reload(src.main)
        monkeypatch.setattr(src.main.httpx, "post", fake_post)

        with TestClient(src.main.app) as client:
            created = client.post(
                "/v1/notifications",
                json={
                    "channel": "webhook",
                    "webhook_url": "https://example.com/hook",
                    "body": "hello",
                },
            )
            assert created.status_code == 202
            notification_id = created.json()["id"]

            status = client.get(f"/v1/notifications/{notification_id}")
            assert status.status_code == 200
            assert status.json()["status"] == "delivered"
            assert calls and calls[0]["url"] == "https://example.com/hook"
        src.main.engine.dispose()

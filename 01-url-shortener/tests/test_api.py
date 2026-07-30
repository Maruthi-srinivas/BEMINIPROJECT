import tempfile
from pathlib import Path

from fastapi.testclient import TestClient


def test_create_redirect_and_stats(monkeypatch):
    with tempfile.TemporaryDirectory() as directory:
        database = Path(directory) / "test.db"
        monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database}")
        # Import after environment setup because the application creates its engine at import time.
        import importlib
        import src.main

        importlib.reload(src.main)
        with TestClient(src.main.app) as client:
            created = client.post(
                "/api/v1/urls",
                json={"destination": "https://example.com/docs", "alias": "guide"},
            )
            assert created.status_code == 201
            assert created.json()["code"] == "guide"

            redirected = client.get("/guide", follow_redirects=False)
            assert redirected.status_code == 302
            assert redirected.headers["location"] == "https://example.com/docs"

            stats = client.get("/api/v1/urls/guide/stats")
            assert stats.status_code == 200
            assert stats.json()["click_count"] == 1
        src.main.engine.dispose()

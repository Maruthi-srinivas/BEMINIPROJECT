import importlib
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient


def test_echo_job_and_schedule(monkeypatch):
    with tempfile.TemporaryDirectory() as directory:
        database = Path(directory) / "test.db"
        monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database}")
        monkeypatch.setenv("REDIS_URL", "")
        import src.main

        importlib.reload(src.main)
        with TestClient(src.main.app) as client:
            created = client.post("/v1/jobs", json={"task": "echo", "payload": {"hello": "world"}})
            assert created.status_code == 202
            assert created.json()["status"] == "succeeded"
            assert created.json()["result"] == {"echo": {"hello": "world"}}

            schedule = client.post(
                "/v1/schedules",
                json={
                    "name": "echo-every-minute",
                    "task": "echo",
                    "payload": {"tick": True},
                    "interval_seconds": 60,
                },
            )
            assert schedule.status_code == 201
            schedule_id = schedule.json()["id"]

            listed = client.get("/v1/schedules")
            assert listed.status_code == 200
            assert any(item["id"] == schedule_id for item in listed.json())

            deleted = client.delete(f"/v1/schedules/{schedule_id}")
            assert deleted.status_code == 204
        src.main.engine.dispose()

import importlib
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient


def test_rules_percentage_and_disabled(monkeypatch):
    with tempfile.TemporaryDirectory() as directory:
        database = Path(directory) / "test.db"
        monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database}")
        monkeypatch.setenv("REDIS_URL", "")
        import src.main

        importlib.reload(src.main)
        with TestClient(src.main.app) as client:
            created = client.put(
                "/v1/flags/beta",
                json={
                    "enabled": True,
                    "percentage": 100,
                    "rules": [{"attribute": "plan", "op": "eq", "value": "pro"}],
                },
            )
            assert created.status_code == 200

            allowed = client.post(
                "/v1/evaluate",
                json={"flag_key": "beta", "user_id": "u1", "attributes": {"plan": "pro"}},
            )
            assert allowed.status_code == 200
            assert allowed.json()["enabled"] is True

            denied = client.post(
                "/v1/evaluate",
                json={"flag_key": "beta", "user_id": "u1", "attributes": {"plan": "free"}},
            )
            assert denied.status_code == 200
            assert denied.json()["enabled"] is False
            assert denied.json()["reason"] == "rules_mismatch"

            client.put("/v1/flags/beta", json={"enabled": False, "percentage": 100, "rules": []})
            disabled = client.post(
                "/v1/evaluate",
                json={"flag_key": "beta", "user_id": "u1", "attributes": {}},
            )
            assert disabled.json()["enabled"] is False
            assert disabled.json()["reason"] == "flag_disabled"

            client.put("/v1/flags/rollout", json={"enabled": True, "percentage": 0, "rules": []})
            zero = client.post(
                "/v1/evaluate",
                json={"flag_key": "rollout", "user_id": "anyone", "attributes": {}},
            )
            assert zero.json()["enabled"] is False

            first = client.post(
                "/v1/evaluate",
                json={"flag_key": "rollout", "user_id": "sticky-user", "attributes": {}},
            )
            client.put("/v1/flags/rollout", json={"enabled": True, "percentage": 100, "rules": []})
            second = client.post(
                "/v1/evaluate",
                json={"flag_key": "rollout", "user_id": "sticky-user", "attributes": {}},
            )
            assert first.json()["enabled"] is False
            assert second.json()["enabled"] is True
        src.main.engine.dispose()

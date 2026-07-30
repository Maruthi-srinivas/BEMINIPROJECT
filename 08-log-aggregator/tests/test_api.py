import importlib
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient


def test_source_ingest_and_search(monkeypatch):
    with tempfile.TemporaryDirectory() as directory:
        database = Path(directory) / "test.db"
        monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database}")
        monkeypatch.setenv("OPENSEARCH_URL", "")
        import src.main

        importlib.reload(src.main)
        with TestClient(src.main.app) as client:
            source = client.post("/v1/sources", json={"name": "api"})
            assert source.status_code == 201
            token = source.json()["token"]

            denied = client.post("/v1/logs", json={"service": "api", "message": "nope"})
            assert denied.status_code == 422

            unauthorized = client.post(
                "/v1/logs",
                json={"service": "api", "message": "nope"},
                headers={"X-Source-Token": "bad"},
            )
            assert unauthorized.status_code == 401

            ingested = client.post(
                "/v1/logs",
                json={"service": "api", "level": "info", "message": "hello world"},
                headers={"X-Source-Token": token},
            )
            assert ingested.status_code == 202
            doc_id = ingested.json()["ids"][0]

            searched = client.get("/v1/logs/search", params={"q": "hello"})
            assert searched.status_code == 200
            assert searched.json()["total"] >= 1

            fetched = client.get(f"/v1/logs/{doc_id}")
            assert fetched.status_code == 200
            assert fetched.json()["message"] == "hello world"
        src.main.engine.dispose()

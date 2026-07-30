import importlib
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient


def test_bucket_object_and_signed_get(monkeypatch):
    with tempfile.TemporaryDirectory() as directory:
        database = Path(directory) / "test.db"
        storage = Path(directory) / "objects"
        monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database}")
        monkeypatch.setenv("STORAGE_ROOT", str(storage))
        monkeypatch.setenv("SIGNING_SECRET", "test-signing-secret")
        monkeypatch.setenv("BASE_URL", "http://testserver")
        import src.main

        importlib.reload(src.main)
        with TestClient(src.main.app) as client:
            created = client.put("/v1/buckets/demo")
            assert created.status_code == 201

            uploaded = client.put(
                "/v1/buckets/demo/objects/hello.txt",
                content=b"hello world",
                headers={"content-type": "text/plain"},
            )
            assert uploaded.status_code == 200
            assert uploaded.json()["size"] == 11

            downloaded = client.get("/v1/buckets/demo/objects/hello.txt")
            assert downloaded.status_code == 200
            assert downloaded.content == b"hello world"

            signed = client.post(
                "/v1/buckets/demo/objects/hello.txt/signed-url",
                json={"method": "GET", "expires_in": 60},
            )
            assert signed.status_code == 200
            token = signed.json()["url"].rsplit("/", 1)[-1]
            via_signed = client.get(f"/v1/signed/{token}")
            assert via_signed.status_code == 200
            assert via_signed.content == b"hello world"
        src.main.engine.dispose()

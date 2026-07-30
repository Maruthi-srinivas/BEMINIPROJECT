import importlib
import time

from fastapi.testclient import TestClient


def test_kv_ttl_and_pubsub(monkeypatch):
    import src.main

    importlib.reload(src.main)
    src.main.STORE.clear()
    src.main.SUBSCRIBERS.clear()

    with TestClient(src.main.app) as client:
        created = client.put("/v1/keys/greeting", json={"value": "hello", "ttl_seconds": 1})
        assert created.status_code == 200
        assert client.get("/v1/keys/greeting").json()["value"] == "hello"

        time.sleep(1.1)
        assert client.get("/v1/keys/greeting").status_code == 404

        client.put("/v1/keys/keep", json={"value": 42})
        assert client.delete("/v1/keys/keep").status_code == 204
        assert client.get("/v1/keys/keep").status_code == 404

        with client.websocket_connect("/v1/subscribe?channel=news") as websocket:
            assert websocket.receive_json()["subscribed"] == ["news"]
            published = client.post("/v1/publish", json={"channel": "news", "message": "ping"})
            assert published.status_code == 200
            assert published.json()["subscribers"] == 1
            event = websocket.receive_json()
            assert event == {"channel": "news", "message": "ping"}

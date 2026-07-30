# Mini Redis

In-process key/value store with TTL and pub/sub over HTTP + WebSocket.
Data lives in memory and is lost when the process restarts.

## Run

```bash
docker compose up --build
```

API: `http://localhost:8010` — docs at `/docs`.

## API

```bash
curl -X PUT http://localhost:8010/v1/keys/greeting \
  -H "content-type: application/json" \
  -d '{"value":"hello","ttl_seconds":60}'
curl http://localhost:8010/v1/keys/greeting
curl -X POST http://localhost:8010/v1/publish \
  -H "content-type: application/json" \
  -d '{"channel":"news","message":"ping"}'
```

Subscribe with WebSocket at `/v1/subscribe?channel=news`, or send
`{"action":"subscribe","channel":"news"}` after connecting.

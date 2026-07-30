# Job Queue

Enqueue background tasks, run them with a Redis-backed worker, and create
interval schedules that materialize into jobs.

## Run

```bash
docker compose up --build
```

API: `http://localhost:8006` — docs at `/docs`.

## API

```bash
curl -X POST http://localhost:8006/v1/jobs \
  -H "content-type: application/json" \
  -d '{"task":"echo","payload":{"hello":"world"}}'
curl -X POST http://localhost:8006/v1/schedules \
  -H "content-type: application/json" \
  -d '{"name":"ping","task":"http_ping","payload":{"url":"https://example.com"},"interval_seconds":60}'
```

Environment: `DATABASE_URL`, `REDIS_URL`.

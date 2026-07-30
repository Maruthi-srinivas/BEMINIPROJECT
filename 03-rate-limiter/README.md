# API Rate Limiter

An independent quota service with durable client policies and Redis-backed
token-bucket or sliding-window enforcement.

## Run

```bash
docker compose up --build
```

The API runs at `http://localhost:8003`; OpenAPI docs are at `/docs`.

## API

Create a policy, then consume its quota:

```bash
curl -X PUT http://localhost:8003/v1/policies/demo \
  -H "content-type: application/json" \
  -d '{"algorithm":"token_bucket","limit":10,"window_seconds":60}'
curl -i -X POST http://localhost:8003/v1/check \
  -H "content-type: application/json" \
  -d '{"client_id":"demo","cost":1}'
```

`POST /v1/check` returns `429` when exhausted and includes
`X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset`.

Environment: `DATABASE_URL` and `REDIS_URL`.

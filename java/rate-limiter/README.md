# API Rate Limiter (Spring Boot)

Durable client policies with Redis-backed token-bucket or sliding-window
enforcement. API-compatible with the Python service in `03-rate-limiter`.

## Run

```bash
docker compose up --build
```

The API is available at `http://localhost:8003`; interactive OpenAPI docs are
at `/docs`. The frontend rate-limiter page already calls this port.

Only one of this stack or the Python `03-rate-limiter` compose can bind port
8003 at a time. Stop the Python stack before starting this one.

For a local H2-only run (no Redis, in-memory limits):

```bash
mvn spring-boot:run
```

That listens on port 8000. Set `SERVER_PORT=8003` if the frontend should reach it.

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

Environment: `DATABASE_URL`, `DATABASE_USER`, `DATABASE_PASSWORD`, `REDIS_URL`,
and `CORS_ORIGINS`.

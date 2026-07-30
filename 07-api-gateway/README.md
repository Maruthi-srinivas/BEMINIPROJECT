# API Gateway

Self-contained reverse proxy with embedded JWT validation and local Redis
(or in-memory) rate limiting. Does not call auth or rate-limiter services.

## Run

```bash
docker compose up --build
```

API: `http://localhost:8007` — docs at `/docs`.

## API

```bash
curl http://localhost:8007/gateway/routes
curl -i http://localhost:8007/upstream/get \
  -H "Authorization: Bearer <jwt>"
```

Mint a compatible JWT with claims `sub`, `role`, and `exp` using `JWT_SECRET`.

Environment: `JWT_SECRET`, `REDIS_URL`, `RATE_LIMIT`, `RATE_WINDOW_SECONDS`,
`GATEWAY_ROUTES` (JSON array of `{prefix,target,public}`).

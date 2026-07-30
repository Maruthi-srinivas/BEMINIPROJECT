# Backend Engineering Mini Projects

Ten independently deployable backend projects. Each can be run with its own
Docker Compose stack:

1. `01-url-shortener` — short links, Redis cache, click analytics
2. `02-auth-service` — JWTs, refresh tokens, Google OAuth, RBAC
3. `03-rate-limiter` — Redis token-bucket and sliding-window policies
4. `04-file-storage` — object storage with HMAC signed URLs
5. `05-notification-service` — RabbitMQ workers, SMTP/Mailhog email, webhooks
6. `06-job-queue` — Redis job workers and interval schedules
7. `07-api-gateway` — reverse proxy with embedded JWT and local rate limits
8. `08-log-aggregator` — OpenSearch ingest/search with source tokens
9. `09-feature-flags` — percentage rollouts and attribute targeting
10. `10-mini-redis` — in-memory KV, TTL, and WebSocket pub/sub

## Frontend console

A Vite + React UI lives in [`frontend/`](frontend/) and calls each service on
ports `8001`–`8010`:

```bash
cd frontend
npm install
npm run dev
```

See [`frontend/README.md`](frontend/README.md) for details.

## Backends

Run a service from its directory:

```bash
cd 08-log-aggregator
docker compose up --build
```

Each service publishes OpenAPI documentation at `/docs`. Shared conventions are
documented in [`shared/README.md`](shared/README.md).

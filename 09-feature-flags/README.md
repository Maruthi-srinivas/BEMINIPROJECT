# Feature Flag Service

Manage feature flags with percentage rollouts and attribute targeting. Flag
definitions are cached in Redis for fast evaluation.

## Run

```bash
docker compose up --build
```

API: `http://localhost:8009` — docs at `/docs`.

## API

```bash
curl -X PUT http://localhost:8009/v1/flags/new-checkout \
  -H "content-type: application/json" \
  -d '{"enabled":true,"percentage":50,"rules":[{"attribute":"plan","op":"eq","value":"pro"}]}'
curl -X POST http://localhost:8009/v1/evaluate \
  -H "content-type: application/json" \
  -d '{"flag_key":"new-checkout","user_id":"u1","attributes":{"plan":"pro"}}'
```

Rules are AND-combined. Percentage bucketing is sticky on `sha256(flag:user_id)`.

Environment: `DATABASE_URL`, `REDIS_URL`, `CACHE_TTL_SECONDS`.

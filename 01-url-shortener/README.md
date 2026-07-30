# URL Shortener

Creates short links, redirects visitors, caches destinations in Redis, and
tracks aggregate click analytics.

## Run

```bash
docker compose up --build
```

The API is available at `http://localhost:8001`; interactive OpenAPI docs are
at `/docs`.

For a local SQLite-only run:

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## API

```bash
curl -X POST http://localhost:8001/api/v1/urls \
  -H "content-type: application/json" \
  -d '{"destination":"https://example.com","alias":"example"}'
curl -i http://localhost:8001/example
curl http://localhost:8001/api/v1/urls/example/stats
```

Environment: `DATABASE_URL`, `REDIS_URL`, `BASE_URL`, and
`CACHE_TTL_SECONDS`.

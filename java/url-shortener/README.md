# URL Shortener (Spring Boot)

Creates short links, redirects visitors, caches destinations in Redis, and
tracks aggregate click analytics. API-compatible with the Python service in
`01-url-shortener`.

## Run

```bash
docker compose up --build
```

The API is available at `http://localhost:8001`; interactive OpenAPI docs are
at `/docs`.

Only one of this stack or the Python `01-url-shortener` compose can bind port
8001 at a time.

For a local H2-only run (no Redis):

```bash
mvn spring-boot:run
```

## API

```bash
curl -X POST http://localhost:8001/api/v1/urls \
  -H "content-type: application/json" \
  -d '{"destination":"https://example.com","alias":"example"}'
curl -i http://localhost:8001/example
curl http://localhost:8001/api/v1/urls/example/stats
```

Environment: `DATABASE_URL`, `DATABASE_USER`, `DATABASE_PASSWORD`, `REDIS_URL`,
`BASE_URL`, and `CACHE_TTL_SECONDS`.

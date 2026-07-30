# Log Aggregator

Ingest structured logs into OpenSearch and search by text, service, level, and
time range. Sources authenticate with `X-Source-Token`.

## Run

```bash
docker compose up --build
```

API: `http://localhost:8008` — OpenSearch: `http://localhost:9200`.

## API

```bash
TOKEN=$(curl -s -X POST http://localhost:8008/v1/sources \
  -H "content-type: application/json" \
  -d '{"name":"api"}' | python -c "import sys,json; print(json.load(sys.stdin)['token'])")
curl -X POST http://localhost:8008/v1/logs \
  -H "content-type: application/json" \
  -H "X-Source-Token: $TOKEN" \
  -d '{"service":"api","level":"info","message":"hello"}'
curl "http://localhost:8008/v1/logs/search?q=hello"
```

Environment: `DATABASE_URL`, `OPENSEARCH_URL`, `LOG_INDEX`.

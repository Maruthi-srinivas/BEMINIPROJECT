# Mini S3 Storage

Local filesystem object storage with bucket/object APIs and HMAC signed URLs.

## Run

```bash
docker compose up --build
```

API: `http://localhost:8004` — docs at `/docs`.

## API

```bash
curl -X PUT http://localhost:8004/v1/buckets/demo
curl -X PUT http://localhost:8004/v1/buckets/demo/objects/hello.txt \
  -H "content-type: text/plain" \
  --data-binary "hello world"
curl http://localhost:8004/v1/buckets/demo/objects/hello.txt
curl -X POST http://localhost:8004/v1/buckets/demo/objects/hello.txt/signed-url \
  -H "content-type: application/json" \
  -d '{"method":"GET","expires_in":300}'
```

Environment: `DATABASE_URL`, `STORAGE_ROOT`, `SIGNING_SECRET`, `BASE_URL`.

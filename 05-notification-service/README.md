# Notification Service

Queues email and webhook deliveries through RabbitMQ with retries and a DLQ.
Local Compose includes Mailhog for SMTP inspection.

## Run

```bash
docker compose up --build
```

API: `http://localhost:8005` — Mailhog UI: `http://localhost:8025`.

## API

```bash
curl -X POST http://localhost:8005/v1/notifications \
  -H "content-type: application/json" \
  -d '{"channel":"email","to":"user@example.com","subject":"Hi","body":"Hello"}'
curl -X POST http://localhost:8005/v1/notifications \
  -H "content-type: application/json" \
  -d '{"channel":"webhook","webhook_url":"https://httpbin.org/post","body":"ping"}'
```

Environment: `DATABASE_URL`, `RABBITMQ_URL`, `SMTP_HOST`, `SMTP_PORT`,
`SMTP_FROM`, `MAX_ATTEMPTS`.

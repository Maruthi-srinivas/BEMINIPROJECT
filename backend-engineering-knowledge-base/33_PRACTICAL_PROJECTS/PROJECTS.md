# Practical projects

Ten backend projects that reuse the checklist. Each one names the topic IDs it is meant to exercise.
Reading these pages does not require Docker. The Compose files are local demos and are unexecuted until you run them.

| Project | File | You practice |
| --- | --- | --- |
| Production-style REST API | [01-rest-api.md](./01-rest-api.md) | HTTP contracts, validation, PostgreSQL |
| Auth service | [02-auth-service.md](./02-auth-service.md) | Sessions or JWT, passwords, authorization |
| URL shortener | [03-url-shortener.md](./03-url-shortener.md) | Keys, cache, redirects |
| Distributed rate limiter | [04-rate-limiter.md](./04-rate-limiter.md) | Redis, quotas, correctness under concurrency |
| Notification service | [05-notifications.md](./05-notifications.md) | Queue, retries, idempotent delivery |
| Order processing | [06-orders.md](./06-orders.md) | Outbox, consumers, payments timeout |
| Multi-tenant SaaS | [07-multi-tenant.md](./07-multi-tenant.md) | Tenant isolation and noisy neighbors |
| Job scheduler | [08-job-scheduler.md](./08-job-scheduler.md) | Leases, at-least-once execution |
| Signed file storage | [09-file-storage.md](./09-file-storage.md) | Object storage and pre-signed URLs |
| RAG backend | [10-rag-backend.md](./10-rag-backend.md) | Ingestion, retrieval, grounded answers |

Build at least one of these far enough to show PostgreSQL, Redis, a queue, auth, tests, logs, and Docker together. The order-processing project and the multi-tenant project are the ones that force the most of the checklist into one system.

"""Write the ten practical project briefs."""

from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "33_PRACTICAL_PROJECTS"

PROJECTS = [
    (
        "01-rest-api.md",
        "Production-style REST API",
        "D05-T001, D05-T004, D06-T001, D06-T004, D06-T009, D07-T011, D07-T018, D20-T001",
        "A task service: create, read, update, and list tasks for an authenticated user.",
        "POST /v1/tasks, GET /v1/tasks/{id}, PATCH /v1/tasks/{id}, GET /v1/tasks?limit=&cursor=",
        "tasks(id uuid pk, owner_id uuid not null, title text not null, status text not null, version int not null, created_at timestamptz)",
        "Client creates a task. API validates the body, writes one row in a transaction, returns 201 with the resource. List uses a cursor on (created_at, id).",
        "Invalid body returns 400 with a field error. Lost update returns 409 when version mismatches. Database down returns 503.",
        "Unit tests for validation. API tests with a real database for the transaction and the cursor. One test that two patches of the same version produce a single winner.",
        "Request log with correlation id, latency histogram, and error rate by status code.",
    ),
    (
        "02-auth-service.md",
        "Authentication and authorization service",
        "D12-T001, D12-T002, D12-T003, D12-T010, D12-T008, D12-T023",
        "Register, log in, and call an API that only the owner of a resource may change.",
        "POST /v1/register, POST /v1/login, POST /v1/logout, GET /v1/me",
        "users(id uuid pk, email text unique, password_hash text, created_at timestamptz). sessions(id uuid pk, user_id uuid, expires_at timestamptz)",
        "Login verifies a password hash, creates a server-side session, sets an HttpOnly cookie. Each request loads the session and checks resource ownership.",
        "Wrong password is a generic 401. Expired session is 401. User A requesting user B's task is 403 or 404, chosen so you do not leak existence if the product requires that.",
        "Tests that a missing cookie is rejected, a tampered session id is rejected, and a user cannot patch another user's row.",
        "Count login failures by IP and account, without logging the password or the session token.",
    ),
    (
        "03-url-shortener.md",
        "URL shortener with caching",
        "D17-T001, D11-T001, D11-T003, D07-T018, D06-T004",
        "Create a short code for a long URL. Redirect with low latency. Expire codes.",
        "POST /v1/links, GET /{code} as a 302",
        "links(code text pk, target_url text not null, owner_id uuid, expires_at timestamptz, created_at timestamptz)",
        "Write the row, then cache code to target. Read path checks cache, then database, then fills cache. A miss on an unknown code is a 404, not a cached empty that never expires.",
        "Cache and database disagree after an update. A stampede on a hot code. A code that expires in SQL but lives on in cache.",
        "Test redirect, unknown code, and expiry. Test that an update deletes or replaces the cache key.",
        "Cache hit ratio, redirect latency, and 404 rate.",
    ),
    (
        "04-rate-limiter.md",
        "Distributed rate limiter",
        "D17-T002, D11-T020, D11-T021, D06-T012, D15-T019",
        "Limit each API key to N requests per window across more than one app instance.",
        "The limiter is middleware on any route. Response includes remaining quota when you choose to expose it.",
        "Redis keys only. No quota stored solely in process memory.",
        "A Redis-side counter or sliding window decides allow or deny atomically. Two app servers must share the same Redis key.",
        "Redis timeout: fail open or fail closed, and document which. A clock jump. A key that is so hot one Redis shard saturates.",
        "Concurrent test that 100 parallel allows never exceed the limit. Test the Redis-down policy.",
        "Allow rate, deny rate, Redis latency, and error rate of the limiter itself.",
    ),
    (
        "05-notifications.md",
        "Notification service with a queue",
        "D14-T001, D14-T009, D14-T013, D05-T015, D14-T011",
        "Accept an email request and deliver it through a worker. Retries must not send two emails for one request.",
        "POST /v1/notifications with an Idempotency-Key. GET /v1/notifications/{id} for status.",
        "notifications(id uuid pk, idempotency_key text unique, status text, payload jsonb). A queue holds the id, not a second copy of the business effect.",
        "The API writes the row and enqueues the id in one logical handoff. Prefer an outbox row in the same database transaction, then a publisher. The worker sends and marks sent.",
        "Worker crashes after the provider accepts and before the status update. Redelivery must see status sent and not send again.",
        "Test duplicate POST with the same idempotency key. Test a crash between send and status update using a fake provider.",
        "Queue depth, delivery success, duplicate-send count (must stay zero), provider latency.",
    ),
    (
        "06-orders.md",
        "Event-driven order processing",
        "D14-T021, D14-T023, D15-T019, D15-T030, D07-T011, D12-T001",
        "Place an order, reserve inventory, and take payment. A timeout from the payment provider must not create two charges or a stuck order with no record.",
        "POST /v1/orders with Idempotency-Key. GET /v1/orders/{id}.",
        "orders, order_items, outbox(id, aggregate_id, type, payload, published_at). Inventory holds a reservation row, not only a counter decrement without a record.",
        "The order insert and the outbox insert commit together. A consumer reserves stock. Another charges payment. Failure runs a compensation that releases the reservation.",
        "Payment timeout after the provider charged. Duplicate event delivery. Inventory reserved but the process dies.",
        "Test the outbox publishes after commit and not before. Test a redelivered event does not double-charge. Test compensation releases stock.",
        "Outbox age, consumer lag, orders stuck in pending, payment error rate.",
    ),
    (
        "07-multi-tenant.md",
        "Multi-tenant SaaS backend",
        "D28-T001, D28-T002, D28-T003, D12-T020, D07-T018",
        "Many customers share the deployment. One tenant must not read another's rows, and one tenant must not consume the whole database.",
        "Every route is under /v1 and takes the tenant from the authenticated token, not from a client-supplied tenant id alone.",
        "Shared schema with tenant_id on every tenant-owned table. Composite indexes start with tenant_id. Optional later split is a documented decision, not the first step.",
        "The repository adds tenant_id to every query. A per-tenant rate limit sits in front of expensive routes.",
        "A missing tenant predicate returns another tenant's data. A report query without tenant_id in the index scans the whole table. One tenant's import saturates the pool.",
        "A test that user from tenant A cannot read tenant B even if they guess the id. A test that the generated SQL contains tenant_id.",
        "Queries missing tenant_id (via a check or review), pool wait time, per-tenant request rate.",
    ),
    (
        "08-job-scheduler.md",
        "Distributed job scheduler",
        "D17-T023, D15-T011, D14-T009, D13-T001",
        "Run a job at a time, on one worker, even if several workers poll.",
        "POST /v1/jobs, GET /v1/jobs/{id}. Workers are internal processes, not a public API.",
        "jobs(id, run_at, status, locked_by, locked_until, attempts). The lock is a lease, not a forever flag.",
        "A worker updates a due job to locked where status is pending and locked_until is in the past, in one conditional update. Only the worker that changed a row runs it.",
        "Two workers take the same job. A worker dies and the lease never expires. A retry runs a job that already succeeded.",
        "Concurrent test with two workers and one due job. Test that a lease expiry allows another worker to take it. Test that success is not repeated if the effect already happened.",
        "Jobs due and not locked, lock expirations, job failure rate, run duration.",
    ),
    (
        "09-file-storage.md",
        "File storage with signed URLs",
        "D29-T011, D29-T012, D29-T014, D12-T013, D06-T001",
        "The API stores metadata. Bytes go directly to object storage using a time-limited URL.",
        "POST /v1/files returns an upload URL. GET /v1/files/{id}/download returns a download URL. The API never proxies the bytes on the hot path.",
        "files(id, owner_id, bucket, object_key, checksum, byte_size, status). The object key is server-generated.",
        "The API authorizes the user, writes a pending metadata row, and signs a PUT. A completion call records size and checksum after the client finishes.",
        "A signed URL leaked and still valid. A client marks complete without uploading. A key that includes a user-supplied path.",
        "Test that user B cannot get a download URL for user A's file. Test that the object key ignores client path input. Test expiry.",
        "Sign latency, upload completion rate, 403 rate on download.",
    ),
    (
        "10-rag-backend.md",
        "Production-style RAG backend",
        "D30-T001, D30-T012, D30-T013, D30-T014, D30-T017, D30-T022, D30-T025",
        "Ingest documents for one tenant, answer a question from retrieved passages, and refuse to invent citations.",
        "POST /v1/documents, POST /v1/answers with the question. The answer returns text plus the passage ids used.",
        "documents and chunks(id, document_id, tenant_id, text, embedding). Queries always filter tenant_id.",
        "Ingest splits text, embeds chunks, and stores them. Answer embeds the question, retrieves a bounded set, and calls the model with those passages only.",
        "Retrieval from the wrong tenant. The model cites a passage that was not retrieved. The provider times out. A prompt asks the model to ignore the documents.",
        "Test tenant isolation on retrieval. Test that a timeout returns a clear error and does not bill a second hidden call unless you meant to retry. Test an empty retrieval returns 'I do not have that' rather than a fluent guess.",
        "Retrieval latency, model latency, token use, empty-retrieval rate, and error rate. Do not log document text if it is sensitive.",
    ),
]


def body(filename: str, title: str, topics: str, summary: str, api: str, schema: str, flow: str, failures: str, tests: str, observe: str) -> str:
    slug = filename.replace(".md", "")
    return f"""# {title}

Topics: {topics}

## Requirements

{summary}

Functional: the API behaves as specified below, including the error cases.
Non-functional: one failed dependency must not corrupt data. A second identical request must not double-apply a side effect where the project says so.

## API

{api}

Use JSON. Return a stable error shape: code, message, and field errors when the input is bad.

## Data model

{schema}

## Architecture

```mermaid
flowchart TD
  client[Client]
  api[API]
  db[PostgreSQL]
  extra[Redis_or_queue_or_object_store]
  client --> api
  api --> db
  api --> extra
```

Read it as the request path. The extra box is Redis, a queue, or object storage depending on the project. If a step can fail, the API still leaves the database consistent.

## Component responsibilities

- The API validates input, authenticates the caller, and writes the database.
- The database holds the source of truth for the business record.
- The extra component is a cache, a queue, or a blob store. It is not the only copy of a fact you must not lose, unless the project is explicitly the rate limiter, whose quota state lives in Redis.

## Flow

{flow}

## Failure scenarios

{failures}

## Testing

{tests}

## Observability

{observe}

## Local demonstration

Docker is optional for reading this page. A demo Compose file would pin `postgres:16` and, when the project needs it, `redis:7`. Do not put real passwords in the file. Use a local-only password such as `localdev` and say so in the README.

This Compose sketch was not executed as part of writing the knowledge base.

```yaml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: localdev
      POSTGRES_DB: app
    ports:
      - "5432:5432"
```

## Interview prompts

- Walk the write path and name the transaction boundary.
- What happens if the process dies at the worst line?
- Which topic IDs did you actually exercise, and which did you skip?
- What metric would page you?

## Trade-off

The smallest version that passes the tests is the one to build first. Add a queue, a cache, or a second region only when this document's failure scenario requires it.
"""


def main() -> None:
    for item in PROJECTS:
        path = OUT / item[0]
        path.write_text(body(*item), encoding="utf-8")
        print(path.name)


if __name__ == "__main__":
    main()

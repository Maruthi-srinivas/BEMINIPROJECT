# Workflow Architecture

BE Mini Lab is **ten independently deployable FastAPI services** plus a Vite/React console. Services do **not** call each other. Each owns its config, datastore, and Docker Compose stack. Host ports are `8000 + service number` (`8001`–`8010`). Every API exposes `/health` and OpenAPI at `/docs`.

Shared conventions live in [`shared/`](../shared/README.md). A Spring Boot rewrite of the URL shortener lives in [`java/url-shortener/`](../java/url-shortener/) and is API-compatible with service 01 (same port `8001`; only one stack can bind it).

---

## System map

```mermaid
flowchart TB
  Browser["Browser"]
  Console["Frontend console<br/>Vite + React :5173"]

  subgraph Services["Independent FastAPI services"]
    S01["01 URL Shortener :8001"]
    S02["02 Auth Service :8002"]
    S03["03 Rate Limiter :8003"]
    S04["04 File Storage :8004"]
    S05["05 Notifications :8005"]
    S06["06 Job Queue :8006"]
    S07["07 API Gateway :8007"]
    S08["08 Log Aggregator :8008"]
    S09["09 Feature Flags :8009"]
    S10["10 Mini Redis :8010"]
  end

  subgraph Infra["Per-stack infrastructure — not shared across services"]
    PG["PostgreSQL"]
    RD["Redis"]
    MQ["RabbitMQ"]
    OS["OpenSearch"]
    FS["Filesystem volume"]
    SMTP["Mailhog SMTP"]
  end

  CI["GitHub Actions<br/>pytest matrix 01-10"]
  Upstream["Configured upstream<br/>e.g. httpbin.org"]
  Google["Google OIDC"]

  Browser --> Console
  Console -->|"HTTP CORS"| S01 & S02 & S03 & S04 & S05 & S06 & S07 & S08 & S09 & S10
  Console -->|"WebSocket"| S10

  S01 --> PG & RD
  S02 --> PG
  S02 --> Google
  S03 --> PG & RD
  S04 --> PG & FS
  S05 --> PG & MQ & SMTP
  S06 --> PG & RD
  S07 --> RD
  S07 --> Upstream
  S08 --> PG & OS
  S09 --> PG & RD

  CI -.-> Services
```

The frontend talks **directly** to each backend. The API gateway is a standalone reverse-proxy lab — it does **not** front the other nine services.

| # | Directory | Port | Persistence | Cache / queue | Extra |
|---|-----------|------|-------------|---------------|-------|
| 01 | `01-url-shortener` | 8001 | PostgreSQL `short_urls` | Redis read-through | optional Java twin |
| 02 | `02-auth-service` | 8002 | PostgreSQL `users`, `refresh_tokens` | — | Google OIDC |
| 03 | `03-rate-limiter` | 8003 | PostgreSQL `policies` | Redis Lua scripts | in-memory fallback |
| 04 | `04-file-storage` | 8004 | PostgreSQL `buckets`, `objects` | — | disk volume |
| 05 | `05-notification-service` | 8005 | PostgreSQL `notifications` | RabbitMQ + worker | Mailhog |
| 06 | `06-job-queue` | 8006 | PostgreSQL `jobs`, `schedules` | Redis list + worker | `echo` / `http_ping` |
| 07 | `07-api-gateway` | 8007 | — | Redis sliding window | JWT + proxy |
| 08 | `08-log-aggregator` | 8008 | PostgreSQL `sources` | OpenSearch index | source tokens |
| 09 | `09-feature-flags` | 8009 | PostgreSQL `flags` | Redis flag cache | sticky % buckets |
| 10 | `10-mini-redis` | 8010 | in-process dict | — | WebSocket pub/sub |

---

## Frontend console

Vite + React app in [`frontend/`](../frontend/). Routes under `/services/{slug}` each call one backend via `VITE_*_URL` (defaults `http://localhost:8001`–`8010`). Health badges poll `/health`. Mini Redis also opens a WebSocket at `/v1/subscribe`.

```mermaid
flowchart LR
  User["User"] --> Pages["Home + 10 service pages"]
  Pages --> Http["http.ts fetch"]
  Http --> APIs["Service APIs :8001-8010"]
  Pages --> WS["WebSocket — Mini Redis only"]
```

---

## 01 — URL Shortener

**Role:** Create short codes (or custom aliases), 302-redirect visitors, cache destinations in Redis, track click counts.

**Stack:** FastAPI, PostgreSQL, Redis (`CACHE_TTL_SECONDS`, default 24h). Compose: `app` + `postgres` + `redis`.

### Create short URL

```mermaid
flowchart TD
  A["POST /api/v1/urls<br/>destination + optional alias"] --> B{Alias valid<br/>4-64 URL-safe?}
  B -->|no| E422["422"]
  B -->|yes| C["Generate blake2b code<br/>or use alias"]
  C --> D["INSERT short_urls"]
  D --> F{IntegrityError?}
  F -->|alias taken| E409["409"]
  F -->|generated collision| R["Retry up to 5 times"]
  R --> C
  F -->|ok| G["Redis SETEX url-shortener:url:{code}"]
  G --> H["201 UrlCreated<br/>code, short_url, destination"]
```

### Redirect + stats

```mermaid
flowchart TD
  R["GET /{code}"] --> C{Redis GET}
  C -->|hit| D["Load row from Postgres"]
  C -->|miss or Redis down| D
  D --> M{Row exists?}
  M -->|no| N404["404"]
  M -->|yes| Fill["On miss: SETEX destination"]
  Fill --> Inc["click_count += 1<br/>last_accessed_at = now"]
  Inc --> Red["302 RedirectResponse"]

  S["GET /api/v1/urls/{code}/stats"] --> P["SELECT short_urls"]
  P --> Stats["UrlStats including click_count"]
```

Redirect always writes analytics to Postgres even on a cache hit. Redis is a destination cache, not a click store.

---

## 02 — Auth Service

**Role:** Email/password auth, short-lived JWT access tokens, rotating refresh tokens, RBAC, optional Google OIDC.

**Stack:** FastAPI, PostgreSQL, `pwdlib` (Argon2), PyJWT HS256. Compose: `app` + `postgres`.

### Register / login / refresh / logout

```mermaid
flowchart TD
  Reg["POST /auth/register"] --> RH["Hash password"]
  RH --> RU["INSERT users role=user"]
  RU --> R201["201 UserResponse"]
  RU --> R409["409 if email exists"]

  Login["POST /auth/login"] --> LV["Verify password"]
  LV --> Issue["issue_tokens"]

  Ref["POST /auth/refresh"] --> Hash["SHA-256 lookup refresh_tokens"]
  Hash --> Valid{Row valid<br/>not revoked, not expired?}
  Valid -->|no| U401["401"]
  Valid -->|yes| Revoke["revoked = true"]
  Revoke --> Issue

  Issue --> AT["JWT access: sub, email, role, jti, exp"]
  Issue --> RT["Raw refresh token returned once<br/>only hash stored"]

  LO["POST /auth/logout"] --> Rev2["Revoke refresh hash"]
```

### Protected routes + Google OIDC

```mermaid
flowchart TD
  Me["GET /auth/me"] --> Bearer["HTTPBearer JWT"]
  Bearer --> User["Load User by sub"]
  Admin["GET /admin/users"] --> Role{role == admin?}
  Role -->|no| F403["403"]
  Role -->|yes| List["List users"]

  G1["GET /auth/oauth/google/login"] --> State["JWT state purpose=google_oauth"]
  State --> URL["authorization_url → Google"]
  G2["GET /auth/oauth/google/callback"] --> StateOK{State valid?}
  StateOK -->|no| B400["400"]
  StateOK -->|yes| Tok["POST oauth2.googleapis.com/token"]
  Tok --> Prof["GET OpenID userinfo"]
  Prof --> Find["Find or create user by google sub / email"]
  Find --> Issue["issue_tokens"]
```

---

## 03 — Rate Limiter

**Role:** Durable per-client policies; atomic quota checks via Redis Lua (token bucket or sliding window). Falls back to an in-memory deque if Redis is down.

**Stack:** FastAPI, PostgreSQL, Redis. Compose: `app` + `postgres` + `redis`.

```mermaid
flowchart TD
  Put["PUT /v1/policies/{client_id}<br/>algorithm, limit, window_seconds"] --> Upsert["INSERT or UPDATE policies"]
  Get["GET /v1/policies/{client_id}"] --> Read["SELECT policy"]

  Check["POST /v1/check<br/>client_id, cost"] --> Pol["Load Policy from Postgres"]
  Pol -->|missing| N404["404"]
  Pol --> Redis{Redis available?}
  Redis -->|yes + token_bucket| TB["EVAL TOKEN_BUCKET_SCRIPT<br/>refill tokens, deduct cost"]
  Redis -->|yes + sliding_window| SW["EVAL SLIDING_WINDOW_SCRIPT<br/>ZSET timestamps in window"]
  Redis -->|error or unset| Mem["In-memory deque window"]
  TB --> Hdr["X-RateLimit-Limit / Remaining / Reset"]
  SW --> Hdr
  Mem --> Hdr
  Hdr --> Out{allowed?}
  Out -->|yes| OK["200 CheckResponse"]
  Out -->|no| R429["429 CheckResponse"]
```

Token bucket refills continuously (`limit / window_seconds`). Sliding window counts events in the last `window_seconds` via a Redis sorted set.

---

## 04 — File Storage

**Role:** Mini S3: buckets, object upload/download/delete, HMAC-SHA256 signed URLs. Bytes on disk; metadata in Postgres. Path traversal is rejected.

**Stack:** FastAPI, PostgreSQL, filesystem volume. Compose: `app` + `postgres` + volume `objects`.

```mermaid
flowchart TD
  B["PUT /v1/buckets/{name}"] --> BV{Bucket name pattern?}
  BV -->|no| E422["422"]
  BV -->|yes| BI["INSERT buckets + mkdir"]

  P["PUT /v1/buckets/{b}/objects/{key}"] --> W["Write file under STORAGE_ROOT<br/>MD5 etag, upsert objects row"]
  G["GET .../objects/{key}"] --> FR["FileResponse from disk"]
  D["DELETE .../objects/{key}"] --> Unlink["Unlink file + DELETE row"]

  S["POST .../signed-url<br/>method GET or PUT, expires_in"] --> Sign["HMAC-SHA256 token<br/>bucket, key, method, exp"]
  Sign --> URL["{BASE_URL}/v1/signed/{token}"]

  R["GET or PUT /v1/signed/{token}"] --> Unsign["Verify HMAC + expiry"]
  Unsign --> Method{HTTP method matches claim?}
  Method -->|no| E405["405"]
  Method -->|GET| G
  Method -->|PUT| W
```

---

## 05 — Notification Service

**Role:** Queue email and webhook deliveries. RabbitMQ worker with retries and a dead-letter queue. Local Compose includes Mailhog (`:8025` UI, SMTP `:1025`).

**Stack:** FastAPI, PostgreSQL, RabbitMQ, SMTP. Compose: `app` + `worker` + `postgres` + `rabbitmq` + `mailhog`.

Without `RABBITMQ_URL`, enqueue processes inline (in-process retry).

```mermaid
flowchart TD
  C["POST /v1/notifications<br/>channel email or webhook"] --> Row["INSERT notifications status=queued"]
  Row --> Enq{RABBITMQ_URL set?}
  Enq -->|no| Inline["process_notification immediately"]
  Enq -->|yes| Pub["Publish persistent message<br/>queue notifications"]

  W["Worker src.worker"] --> Cons["Consume notifications"]
  Cons --> Proc["process_notification"]
  Proc --> Attempt["attempts += 1, status=processing"]
  Attempt --> Ch{channel}
  Ch -->|email| SMTP["smtplib → Mailhog / SMTP"]
  Ch -->|webhook| HTTP["httpx POST webhook_url"]
  SMTP --> Res{success?}
  HTTP --> Res
  Res -->|yes| Del["status=delivered"]
  Res -->|no, attempts < MAX_ATTEMPTS| Re["status=queued<br/>sleep 2^attempts then republish"]
  Res -->|no, attempts >= MAX_ATTEMPTS| Dead["status=dead<br/>publish to notifications.dlq"]

  L["GET /v1/notifications and /{id}"] --> DB["Read status from Postgres"]
```

API returns **202** on create. Delivery is asynchronous when RabbitMQ is enabled.

---

## 06 — Job Queue

**Role:** Enqueue background tasks (`echo`, `http_ping`), Redis list worker, interval schedules that materialize into jobs.

**Stack:** FastAPI, PostgreSQL, Redis. Compose: `app` + `worker` + `postgres` + `redis`.

Without Redis, jobs execute inline in the API process.

```mermaid
flowchart TD
  J["POST /v1/jobs<br/>task, payload, optional run_at"] --> Ins["INSERT jobs status=queued"]
  Ins --> RP["RPUSH job-queue:jobs"]
  RP --> Inline{REDIS_URL?}
  Inline -->|no| ExecNow["execute_job in API"]
  Inline -->|yes| Acc["202 JobResponse"]

  Sch["POST /v1/schedules"] --> SRow["INSERT schedules<br/>next_run_at = now + interval"]
  LS["GET /v1/schedules"] --> List
  DS["DELETE /v1/schedules/{id}"] --> Del

  Worker["Worker loop"] --> Mat["materialize_due_schedules"]
  Mat --> Due["For each due schedule:<br/>create Job, RPUSH, bump next_run_at"]
  Worker --> Pop["BLPOP job-queue:jobs"]
  Pop --> Ex["execute_job"]
  Ex --> Wait{run_at in future?}
  Wait -->|yes| Requeue["RPUSH again"]
  Wait -->|no| Run["status=running"]
  Run --> Task{task}
  Task -->|echo| Echo["return payload"]
  Task -->|http_ping| Ping["httpx GET url"]
  Echo --> Done["status=succeeded + result JSON"]
  Ping --> Done
  Ping -->|error| Fail["status=failed + error"]
```

---

## 07 — API Gateway

**Role:** Self-contained reverse proxy. Embedded JWT validation and local rate limits. **Does not call** the auth or rate-limiter services.

**Stack:** FastAPI, Redis (optional; in-memory fallback), httpx. Compose: `app` + `redis`. Routes from `GATEWAY_ROUTES` JSON (default `/upstream` → `https://httpbin.org`, private).

```mermaid
flowchart TD
  Req["Any method /{full_path}"] --> Pub{Path is /health, /docs,<br/>/gateway/routes?}
  Pub -->|yes| Native["Handled by FastAPI"]
  Pub -->|no| Match["Longest-prefix match GATEWAY_ROUTES"]
  Match -->|none| N404["404"]
  Match --> Auth{route.public?}
  Auth -->|no, missing Bearer| E401["401"]
  Auth -->|no| JWT["jwt.decode HS256 JWT_SECRET"]
  JWT -->|invalid| E401
  JWT --> RL
  Auth -->|yes| RL["Rate limit by sub or client IP"]
  RL --> Redis["Redis ZSET gateway:rl:{key}<br/>or in-memory deque"]
  Redis -->|over RATE_LIMIT| R429["429"]
  Redis -->|ok| Fwd["Strip hop headers<br/>inject X-User-Id, X-User-Role"]
  Fwd --> Up["httpx request to target + suffix"]
  Up --> Resp["Proxy status, body, rate-limit headers"]
```

`GET /gateway/routes` lists configured prefixes without proxying.

---

## 08 — Log Aggregator

**Role:** Register ingest sources (token shown once, stored hashed). Index structured logs in OpenSearch; search by text, service, level, time. Falls back to in-memory docs if OpenSearch is down.

**Stack:** FastAPI, PostgreSQL, OpenSearch. Compose: `app` + `postgres` + `opensearch` (`:9200`).

```mermaid
flowchart TD
  Src["POST /v1/sources {name}"] --> Tok["Generate token_urlsafe"]
  Tok --> Hash["Store SHA-256 in sources"]
  Hash --> Once["201 returns raw token once"]

  In["POST /v1/logs"] --> Hdr["Header X-Source-Token"]
  Hdr --> Auth{Hash matches?}
  Auth -->|no| E401["401"]
  Auth -->|yes| Norm["Normalize events[] or single message"]
  Norm --> Idx["PUT OpenSearch {LOG_INDEX}/_doc/{uuid}"]
  Idx --> Acc["202 accepted + ids"]

  Q["GET /v1/logs/search<br/>q, service, level, from, to"] --> Search["OpenSearch bool query<br/>or in-memory filter"]
  One["GET /v1/logs/{doc_id}"] --> Get["_doc get"]
```

Search is open (no source token). Ingest is token-gated.

---

## 09 — Feature Flags

**Role:** Upsert flags with percentage rollouts and AND-combined attribute rules. Definitions cached in Redis for evaluate.

**Stack:** FastAPI, PostgreSQL, Redis (`CACHE_TTL_SECONDS`, default 60s). Compose: `app` + `postgres` + `redis`.

```mermaid
flowchart TD
  Put["PUT /v1/flags/{key}"] --> Save["Upsert flags + SETEX cache"]
  List["GET /v1/flags"] --> All["SELECT all flags"]
  Del["DELETE /v1/flags/{key}"] --> DC["Delete row + cache"]

  Ev["POST /v1/evaluate<br/>flag_key, user_id, attributes"] --> Load["Redis GET feature-flags:flag:{key}<br/>else Postgres then cache"]
  Load -->|missing| N404["404"]
  Load --> Off{enabled?}
  Off -->|no| R1["enabled=false reason=flag_disabled"]
  Off -->|yes| Rules{All rules match?}
  Rules -->|no| R2["enabled=false reason=rules_mismatch"]
  Rules -->|yes| Pct{percentage}
  Pct -->|100| On["enabled=true percentage_full"]
  Pct -->|0| Off2["enabled=false percentage_zero"]
  Pct -->|1-99| Bucket["sha256 flag:user_id % 100"]
  Bucket -->|bucket < percentage| StickyOn["enabled=true"]
  Bucket -->|else| StickyOff["enabled=false"]

  Batch["POST /v1/evaluate/batch"] --> Loop["Same evaluate per key<br/>missing → reason=flag_missing"]
```

Rule ops: `eq`, `neq`, `in`, `contains`. Percentage bucketing is sticky per `(flag_key, user_id)`.

---

## 10 — Mini Redis

**Role:** In-process key/value with optional TTL and WebSocket pub/sub. Data is lost on process restart. No Postgres/Redis sidecar.

**Stack:** FastAPI only. Compose: `app` on `:8010`. A background task purges expired keys every second.

```mermaid
flowchart TD
  Set["PUT /v1/keys/{key}<br/>value, ttl_seconds"] --> Store["STORE dict Entry"]
  Get["GET /v1/keys/{key}"] --> Purge["Drop if expired"]
  Purge --> Val["KeyResponse + remaining TTL"]
  Del["DELETE /v1/keys/{key}"] --> Pop["Remove key"]
  Keys["GET /v1/keys"] --> List["Non-expired keys"]

  Sub["WS /v1/subscribe?channel="] --> Acc["Accept socket"]
  Acc --> Reg["Register in SUBSCRIBERS"]
  Acc --> Msg["JSON action subscribe / unsubscribe"]

  Pub["POST /v1/publish channel, message"] --> Fan["send_json to live sockets"]
  Fan --> Count["subscribers count"]
```

---

## Java URL Shortener (optional twin)

[`java/url-shortener`](../java/url-shortener/) is a Spring Boot port of service 01: same REST contract, PostgreSQL + Redis, OpenAPI at `/docs`, port `8001`. Workflow matches [01 — URL Shortener](#01--url-shortener). Run either the Python or Java compose stack, not both.

---

## CI

```mermaid
flowchart LR
  Push["push / PR on service paths"] --> Matrix["GitHub Actions matrix<br/>01 … 10"]
  Matrix --> Py["Python 3.12"]
  Py --> Test["pytest -q per service"]
```

Workflow: [`.github/workflows/test-services.yml`](../.github/workflows/test-services.yml).

---

## Design notes

- **No service mesh.** The console and each Compose stack are the only “integration.” Gateway JWT/rate-limit logic is duplicated on purpose so the gateway stays self-contained.
- **Degraded modes.** Rate limiter, gateway, feature-flag cache, job queue, notifications, and log aggregator keep working without Redis / RabbitMQ / OpenSearch via in-memory or inline paths.
- **Workers.** Only notifications and the job queue run a second process (`python -m src.worker`).
- **Auth boundary.** Auth issues JWTs; the gateway verifies JWTs with its own `JWT_SECRET`. They are compatible only if those secrets match.

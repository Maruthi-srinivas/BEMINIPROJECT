# BE Mini Lab — Interview & Learning Guide

A 20-minute senior-engineer interview script plus a study document for every service.

Use this file in two ways:

1. **Speak from Part A** in the interview (timed, ~20 minutes).
2. **Study Parts B–D** so you can answer follow-up questions without freezing.

When a word is in **bold** the first time, a short definition follows in parentheses. There is also a full glossary at the end.

---

## How to talk to a senior engineer

A senior is not scoring “I used Redis.” They are scoring:

- Can you explain **why** this piece exists in a real product?
- Do you know what happens on the **unhappy path** (Redis down, duplicate click, stolen token, poison message)?
- Can you name **trade-offs** without being asked?
- Do you know where this lab is **not production-ready**, and what you would change?

Rules of delivery:

- Lead with the problem, then the design, then one limitation.
- Never list technologies without a sentence of purpose.
- If you do not know something, say so and reason out loud. That is critical thinking. Pretending is worse.
- These ten services are **independent labs**, not one wired-together product. Say that early. It is a feature of the design, not a bug.

Suggested 20-minute shape:

| Minutes | What you cover |
|--------:|----------------|
| 0–2 | What this is, why you built it, the one-sentence architecture |
| 2–5 | How real backends are split, and how *this* repo is split |
| 5–14 | All ten services, ~50 seconds each |
| 14–17 | One end-to-end company story (campaign platform) |
| 17–20 | Security, trade-offs, what you would ship next |

If they interrupt, let them. Follow-ups *are* the interview. Jump to the matching service section in Part B.

---

# Part A — 20-minute spoken script

Read this until you can say it in your own words. Do not memorize it word-for-word.

---

### 0:00–2:00 — Opening

I built a backend systems lab called **BE Mini Lab**: ten independently deployable **microservices** (small programs that each own one job, their own database, and their own deploy) written in **Python 3.12** with **FastAPI** (a web framework that turns Python functions into HTTP APIs and generates **OpenAPI** docs — a machine-readable description of every endpoint).

Each service has:

- its own **Docker Compose** stack (a file that starts the app plus the databases it needs, as containers)
- **PostgreSQL** where durable records matter, **Redis** where speed or coordination matters, **RabbitMQ** for notifications, **OpenSearch** for logs
- **pytest** tests and **GitHub Actions** CI (automated tests that run on every push)

There is also a **React + Vite** console on port 5173 that talks to services on ports 8001–8010, plus a **Spring Boot** reimplementation of the URL shortener to show the same API in Java.

The point of the project is not “ten CRUD apps.” It is to practice the pieces that show up in real companies: authentication, caching, rate limiting, object storage, async messaging, job workers, an API gateway, centralized logs, feature flags, and an in-memory key-value store.

A design choice I would mention first: **these services do not call each other**. The API gateway does not call the auth service. The rate limiter is not wired into the gateway. Each lab owns its config, store, and deploy. That is closer to “I can explain this system in isolation” than to a Kubernetes mesh. In a real company you *would* compose them; I kept them independent so each one is demoable and failurable on its own.

---

### 2:00–5:00 — How real applications work internally

A user-facing product is rarely one program. Typical layers:

1. **Client** — browser or mobile app. Ours is the Vite console.
2. **Edge / API gateway** — the public front door. Checks identity, rate-limits, then **reverse-proxies** (forwards the HTTP request to an internal service).
3. **Stateless API processes** — FastAPI apps. They should be replaceable. State lives in stores.
4. **Stateful stores** — PostgreSQL for truth, Redis for hot data, a queue for work that can wait, a search index for logs.
5. **Workers** — separate processes that consume queues. The HTTP request returns quickly; the slow work happens later.

That split exists because of **latency**, **failure isolation**, and **scale**. You do not want “send welcome email” to block “create account.” You do not want a log search spike to take down login.

Two consistency ideas you will get asked about:

- **Source of truth** — the database row is canonical. Redis is a copy that can be wrong or missing.
- **At-least-once delivery** — queues usually deliver a message one or more times. Consumers must be **idempotent** (running the same work twice must not double-charge, double-email forever, etc.). This lab is honest about that: notifications can retry; they are not perfectly idempotent.

Another idea: **fail open vs fail closed**.

- Fail open = if Redis is down, allow the request (availability over strict limits).
- Fail closed = if Redis is down, reject (safety over availability).

The rate limiter **fails open** to an in-memory fallback. I would say that is fine for a demo and dangerous in production, because each app replica would have its own memory and attackers could bypass the limit.

---

### 5:00–14:00 — All ten services (about 50 seconds each)

Speak this block as a tour. Pause after any service they lean into.

#### 01 — URL Shortener (`8001`)

**Problem:** marketing and chat need short, shareable links that redirect and report clicks.

**How it works:** `POST /api/v1/urls` stores a destination in PostgreSQL. If you do not pass a custom **alias** (the human-readable short code), it generates one with **BLAKE2b** (a fast cryptographic hash) over a UUID, then **base64url** encoding. Redirect `GET /{code}` is the hot path: it tries **Redis** first (**read-through cache** — on a miss, load from DB and fill Redis with a **TTL**, time-to-live, default 24 hours), then issues **HTTP 302** to the destination. Click count and last-accessed time still update in Postgres on every hit.

**Why Redis:** redirects are extremely read-heavy. Memory lookups are microseconds; disk/SQL is milliseconds. Cache is optional — if Redis is down, we log and still serve from Postgres.

**Trade-off I would name:** analytics writes still hit Postgres on every click, so the cache only speeds the *destination lookup*, not the whole request. Bitly-scale systems often batch click events into a queue. Also, 302 is temporary; some shorteners use 301 for SEO. 302 is safer if destinations can change.

**Security:** open create API (anyone can mint links — **open redirect** / phishing risk). No auth, no expiration of links, no malware scan of destinations.

#### 02 — Auth Service (`8002`)

**Problem:** who is this user, and what may they do?

**How it works:** register/login with email+password. Passwords are hashed with **Argon2** via `pwdlib` (**password hashing** — one-way, slow on purpose so stolen hashes are expensive to crack). Login returns:

- a short-lived **JWT access token** (JSON Web Token: a signed blob of **claims** like user id, email, role, expiry). Algorithm **HS256** (HMAC with a shared secret). Default 15 minutes.
- a **refresh token**: 48 bytes of random, stored in DB as **SHA-256** hash only. Default 14 days.

**Refresh rotation:** using a refresh token immediately **revokes** it and issues a new pair. If an attacker steals a refresh token and the real user also uses it, one of them will present a revoked token — that is a reuse signal. This lab revokes on use but does not currently revoke the *whole family* of tokens on reuse, which is the production upgrade.

**RBAC:** roles `user` and `admin`. `/admin/users` requires admin. **RBAC** means role-based access control: permissions come from a role string, not per-user ACLs.

**Google OIDC:** **OpenID Connect** is identity on top of **OAuth 2.0**. We send the browser to Google, Google returns an authorization **code**, we exchange it for tokens, fetch userinfo, and upsert a user. **State** is a short JWT so we can reject CSRF-ish callback tampering.

**Security talking points:** default `JWT_SECRET` is unsafe; HS256 means every replica must share the secret (**symmetric**). Production often uses **RS256** (asymmetric: auth service signs with a private key, gateways verify with a public key). No login rate limit → **credential stuffing**. No email verification. OAuth account linking by email can attach a Google login to an existing password user — that is a real account-takeover class of bug if email is not verified.

#### 03 — Rate Limiter (`8003`)

**Problem:** stop one client from exhausting the API.

**How it works:** policies live in Postgres per `client_id`: algorithm, limit, window. `POST /v1/check` consumes `cost` tokens and returns 429 when exhausted, plus `X-RateLimit-*` headers.

Two algorithms, both in **Lua** scripts so Redis runs them **atomically** (no two requests can interleave mid-update):

1. **Token bucket** — bucket holds up to `limit` tokens, refills at `limit/window` per second. Bursts are allowed if tokens have accumulated. Good for APIs that should allow a short spike.
2. **Sliding window** — Redis **sorted set** of timestamps; drop entries older than the window; reject if count + cost > limit. Smoother, stricter, more memory.

**Why Lua:** `GET` then `SET` from Python is a race. Two requests can both see “1 remaining” and both pass. Lua + Redis is one round trip, one script.

**Fallback:** Redis error → in-process deque. Availability over correctness. Multi-instance this is wrong.

**Security:** creating policies is unauthenticated. In production this service is internal-only.

#### 04 — File Storage (`8004`) — mini S3

**Problem:** store blobs (images, PDFs) without putting them in Postgres.

**How it works:** **buckets** (namespaces, like S3 buckets) and **objects** (files keyed by path). Bytes go on the local filesystem; metadata (size, content-type, **ETag**) goes in Postgres. ETag is **MD5** of bytes — a checksum so clients can detect change; MD5 is not a security hash.

**Signed URLs:** the API builds a payload `{bucket, key, method, exp}`, **HMAC-SHA256** with `SIGNING_SECRET`, and hands the client a time-limited URL. The client can GET or PUT without other credentials. This is how browsers upload to S3 without your secret keys.

**Path traversal:** keys are resolved under `STORAGE_ROOT`; if the resolved path escapes the root, 400. That is the classic `../../etc/passwd` defense.

**Security:** no auth on create/download except signed URLs. HMAC secret default is weak. No virus scan, no size cap in code (DoS by huge upload). Signed tokens are in the URL → they leak via logs and Referer. Production uses short TTL and, often, content-disposition / bucket policies.

#### 05 — Notification Service (`8005`)

**Problem:** send email and webhooks without blocking the caller.

**Pattern:** **async processing**. `POST /v1/notifications` writes a row (`queued`) and returns **202 Accepted**. A **worker** process does the slow I/O.

**RabbitMQ:** durable queue `notifications` plus **DLQ** `notifications.dlq` (**dead-letter queue** — messages that failed too many times, for humans to inspect). Messages are **persistent**. Worker **prefetch** is 10 (don’t take the whole queue into memory). On failure: exponential backoff `min(2^attempts, 60)` seconds, requeue; after `MAX_ATTEMPTS` (5) mark `dead` and publish to DLQ.

**Email:** **SMTP** to **Mailhog** in Compose (a fake mailbox UI on port 8025). **Webhooks:** HTTP POST of JSON.

**Critical idea:** this is **at-least-once**. A crash after send-but-before-ack can double-send. Email is often “best effort”; payments cannot be.

**Security / SSRF:** webhook URL is caller-controlled. A worker that POSTs to it can hit `http://169.254.169.254/` (cloud metadata) or internal hosts. Production needs URL allowlists. Also, no auth on enqueue.

#### 06 — Job Queue (`8006`)

**Problem:** run work later, or on a timer, in a generic way.

**How it works:** jobs in Postgres (`echo` or `http_ping`). Job ids are pushed to a Redis list (`RPUSH` / `BLPOP` — blocking pop, the classic queue). A worker loop: materialize due **schedules** (interval timers that insert new jobs and bump `next_run_at`), then pop and execute. If `run_at` is in the future, the job is pushed back.

This is a small **Celery** / **Sidekiq** / **SQS + worker**.

**Trade-off vs notifications:** Redis lists are simpler than RabbitMQ but weaker: no native DLQ, weaker persistence story, no routing. Good for internal jobs; Rabbit is better for cross-service messaging.

**Security:** `http_ping` is another **SSRF** vector. Task names are allowlisted (`echo|http_ping`) which is good — never `eval` user code.

#### 07 — API Gateway (`8007`)

**Problem:** one public hostname, many internal services, identity checked once.

**How it works:** config `GATEWAY_ROUTES` is a JSON list of `{prefix, target, public}`. Longest prefix wins. For private routes: require `Authorization: Bearer`, verify JWT with **the gateway’s own** `JWT_SECRET` (it does **not** call auth-service). Then local sliding-window rate limit (Redis pipeline, or memory). Then **httpx** forwards method, query, body; strips `Host` / `Authorization`; injects `X-User-Id` and `X-User-Role` for the upstream.

This is **Kong / nginx / AWS API Gateway** in miniature.

**Why not call auth-service on every request?** Latency and coupling. At the edge you verify signatures locally. Auth-service *issues* tokens; the gateway *verifies* them. That only works if they share the JWT secret (HS256) or the gateway has the public key (RS256).

**Trade-off:** Redis pipeline is **not** as atomic as the rate-limiter’s Lua. Under concurrency you can slightly overshoot the limit. Also, trusting `X-User-*` headers only works if upstreams are not reachable except through the gateway (**network isolation**).

#### 08 — Log Aggregator (`8008`)

**Problem:** `grep` on one machine does not work when you have many services and containers.

**How it works:** register a **source**, get a secret token shown once, store **SHA-256** of the token. Ingest requires header `X-Source-Token`. Events go to **OpenSearch** (Elasticsearch-compatible search engine). Search by text, service, level, time range using a **bool must** query.

If OpenSearch is down, documents fall back to an in-memory dict.

This is **ELK / Datadog / CloudWatch Logs** as a teaching slice.

**Security:** ingest is token-gated (good). **Search is open** (bad — logs contain secrets if you are sloppy). Tokens in logs are a classic leak. Production: RBAC on search, index-per-tenant, redact PII.

#### 09 — Feature Flags (`8009`)

**Problem:** ship code dark, turn it on for 5% of users, abort without redeploying.

**How it works:** flag key, `enabled`, `percentage` 0–100, **rules** (attribute `eq` / `neq` / `in` / `contains`, all AND-ed). Evaluation:

1. disabled → off  
2. rules fail → off  
3. percentage: **sticky bucket** = `sha256(flag:user_id)` first 8 hex chars mod 100. If bucket < percentage, on.

Sticky matters: without it, a user at 50% could flip every request. Hashing the id keeps them in the same bucket.

Flags are cached in Redis (TTL 60s) so evaluate is fast. **Cache invalidation** on upsert/delete.

This is **LaunchDarkly / Unleash / ConfigCat**.

**Trade-off:** 60s cache means a kill-switch can take a minute. Client-supplied attributes are a trust issue: if the caller lies about `plan=pro`, they get pro features. Evaluate must run in a trusted backend.

#### 10 — Mini Redis (`8010`)

**Problem:** understand what Redis *is* by building a tiny one.

**How it works:** a process-local `dict` of key → `{value, expires_at}`. GET/PUT/DELETE over HTTP. A background task deletes expired keys every second. **Pub/sub** over **WebSocket**: subscribe to a channel, `POST /v1/publish` fans out JSON to subscribers.

This is Redis’s mental model: **in-memory**, optional **TTL**, **pub/sub**. Data dies on restart. No **AOF/RDB** persistence, no replication, no auth.

Use it in the interview to prove you know *why* companies pay for Redis: speed, TTL, and shared state across processes — and why you still need Postgres for money and identity.

---

### 14:00–17:00 — One real-world story (speak this as a product)

Imagine a **SaaS marketing platform** like a baby HubSpot / Bitly / Mailchimp.

1. A company signs up through **Auth**. Access JWT in the browser, refresh token in an **httpOnly cookie** in a real app (this lab returns it in JSON, which is XSS-sensitive).
2. They hit the public internet through the **API Gateway**, which verifies the JWT and rate-limits them so a buggy script cannot melt us.
3. They upload a logo through **File Storage** using a signed PUT URL — the browser never sees our signing secret.
4. They create campaign links with the **URL Shortener**. Clicks 302 to the landing page; stats show which ad worked.
5. New-campaign emails go to **Notifications**. HTTP returns 202; RabbitMQ workers talk to SMTP. Failed webhooks land in the DLQ for ops.
6. Nightly “email digest” is a **Job Queue** schedule, not a request that waits.
7. We roll out a new checkout page with **Feature Flags** at 10% sticky on `user_id`, only if `plan` is `pro`.
8. Every service ships structured logs to the **Log Aggregator** so on-call can search `level=error` across boxes.
9. Hot session fragments or live “campaign updated” events could sit in **Mini Redis** / real Redis pub/sub.
10. Partner APIs are wrapped by the **Rate Limiter** so each `client_id` has a contract: 1000 req/min, token bucket for bursty batch jobs.

That is how the labs map onto a company. In this repo they are **not** actually wired that way — I would say that out loud so I do not oversell.

---

### 17:00–20:00 — How good is it, trade-offs, security, what I would do next

**What is genuinely good**

- Independently deployable services with Compose, health checks, OpenAPI, tests, CI.
- Real stores, not mocks: Postgres, Redis, RabbitMQ, OpenSearch.
- Algorithms with teeth: Lua atomic rate limits, refresh rotation, HMAC signed URLs, sticky flag buckets, DLQ + backoff.
- Honest fallbacks documented in code (Redis down, no Rabbit, no OpenSearch).
- A frontend that can demo each service live.

**What it is not**

- Not a production mesh. No service-to-service **mTLS**, no **service discovery**, no tracing (**OpenTelemetry**).
- Most write APIs are **unauthenticated**. Fine for a lab; catastrophic on a public IP.
- Secrets default to `"change-this-in-production"`.
- Schema via `create_all` — no **Alembic** migrations.
- Workers are single-process; no poison-message isolation beyond DLQ.
- Gateway rate limit is not Lua-atomic; URL shortener click counts are not batched.

**Cross-cutting vulnerabilities I would volunteer**

| Theme | Where | Risk |
|--------|--------|------|
| Unauthenticated mutating APIs | almost every service | anyone on the network can create users’ data |
| Default HMAC/JWT secrets | auth, gateway, file storage | token forgery |
| SSRF | notifications webhooks, job `http_ping` | hit cloud metadata / internal IPs |
| Fail-open rate limits | rate limiter, gateway | bypass under Redis outage or multi-replica memory |
| Open log search | log aggregator | log disclosure |
| Refresh reuse not family-revoked | auth | stolen refresh can race the victim |
| Open redirects | URL shortener | phishing with your domain |
| XSS + refresh in JSON | auth + SPA | stolen refresh if XSS exists |
| Header trust | gateway `X-User-*` | privilege if upstream is reachable directly |
| Path traversal (mitigated) | file storage | would be RCE-adjacent if the resolve check were wrong |

**If I had another sprint for “production”**

1. Put every service behind the gateway; mutual TLS internally; no public 8001–8010.
2. RS256 JWTs; auth issues, gateway verifies with JWKS.
3. Login rate limits + Argon2 already there; add lockout and email verify.
4. Lua at the gateway; fail closed for paid APIs.
5. SSRF allowlists; block link-local and private ranges.
6. Outbox pattern for notifications so DB commit and queue publish cannot diverge.
7. OpenTelemetry traces + the log aggregator as a sink.
8. Migrations, backups, and Redis persistence for queues.

That close shows critical thinking: I am proud of the lab, and I can attack it.

---

# Part B — Each service in depth (study this)

For every service: purpose, internals, data model, request flow, real-world analog, design decisions, trade-offs, security, likely interview questions.

---

## Shared conventions (all Python services)

- **FastAPI** app, **Pydantic** models (request/response validation).
- **SQLAlchemy 2.0** ORM, `create_all` on startup.
- **CORS** from `CORS_ORIGINS` (default `http://localhost:5173`) so the browser console can call APIs. **CORS** is a browser rule: a page on origin A may only read responses from origin B if B opts in.
- `GET /health` — **liveness** for Compose/k8s. Most ping the database with `SELECT 1`.
- Config only from **environment variables**.
- Ports: service number + 8000.
- Tests: **pytest** + **httpx**. CI matrix in `.github/workflows/test-services.yml`.

**Frontend:** Vite dev server, polls `/health`, one console per service. Not a unified product UI.

**Java twin:** `java/url-shortener` is API-compatible Spring Boot (JPA + Redis). Talking point: same contract, two runtimes.

---

## 01 — URL Shortener

### What it is

A service that maps a long URL to a short code and, when someone visits the short URL, redirects them and counts the click.

### Data model

Table `short_urls`:

- `code` — unique short id (index)
- `destination` — up to 2048 chars
- `created_at`, `last_accessed_at`, `click_count`

Redis key `url-shortener:url:{code}` → destination string, TTL default 86400 seconds.

### Internals

**Create**

1. Validate destination as `HttpUrl` (Pydantic — must look like a URL).
2. Optional alias must match `^[A-Za-z0-9_-]{4,64}$`.
3. Else generate: `blake2b(uuid4, digest_size=7)` → urlsafe base64, strip `=`.
4. Insert. On unique violation: if alias, **409 Conflict**; if generated, retry up to 5 times, then 503.
5. Write cache.

**Redirect**

1. Try Redis GET.
2. Always load the row from Postgres (needed for click_count). If missing, 404.
3. If cache miss, fill cache from row.
4. Increment `click_count`, set `last_accessed_at`, commit.
5. `RedirectResponse` 302.

**Stats:** `GET /api/v1/urls/{code}/stats`.

### Why 302, not 301

- **301 Moved Permanently** — browsers and Google cache it. Hard to change destination later.
- **302 Found** — “temporary.” We keep control. Bitly-style products often prefer 302 for that reason.

### Cache correctness

This is **read-through**, not write-behind. Destination in Redis can be stale only if we updated Postgres without invalidating — we do not have an update-destination API, so staleness is mostly TTL expiry. Click counts are **not** in Redis; they are always SQL. Under high QPS, `click_count += 1` row updates will serialize on that row — a real bottleneck. Upgrade: `INCR` in Redis and flush to SQL in batches, accepting approximate counts.

### Real-world analog

Bitly, TinyURL, Twitter’s `t.co`, AWS CloudFront + DynamoDB designs. Hot path is redirect; write path is create.

### Trade-offs

| Choice | Benefit | Cost |
|--------|---------|------|
| Postgres + Redis | durable + fast | two systems to run |
| Cache optional | works on a laptop | prod must monitor Redis misses/errors |
| Sync click writes | accurate counts | DB load on viral links |
| Open API | easy demo | spam/phishing |
| BLAKE2b short codes | compact, random | not sequential (good against enumeration somewhat, still brute-forceable) |

### Vulnerabilities

- **Open redirect / branded phishing:** attacker creates `yoursite/paypal-login` → malware.
- **Enumeration:** short codes can be scanned.
- **No HTTPS enforcement** on destination in a strong sense (HttpUrl allows http).
- **Cache poisoning** is not really an issue here because we set cache from our own DB, not from the client on redirect.

### Likely questions

- “What if two creates collide?” — IntegrityError retry.
- “What if Redis is down?” — log, serve DB.
- “Is click_count race-safe?” — two requests can read the same count and both add 1 with lost update depending on isolation; SQLAlchemy default is not `SELECT FOR UPDATE`. Honest answer: not strictly safe; use `UPDATE ... SET click_count = click_count + 1`.
- “How would you shard?” — hash code modulo N, or key-range; cache still in Redis cluster.

---

## 02 — Auth Service

### What it is

Identity: register, login, session refresh, logout, “who am I,” admin user list, Google login.

### Data model

`users`: email (unique, lowercased), `password_hash` nullable (OAuth users may have none), `role`, `oauth_provider`, `oauth_subject`.

`refresh_tokens`: `token_hash`, `expires_at`, `revoked`, FK to user.

### Token design (memorize this)

**Access JWT claims:** `sub` (user id), `email`, `role`, `jti` (random id of this token), `iat`, `exp`. Signed with `JWT_SECRET`, HS256. **Not stored in DB.** To revoke a specific access token before expiry you would need a denylist (`jti` in Redis until exp). This lab does not denylist access tokens — that is why they are short-lived (15 min).

**Refresh token:** high-entropy random string given to the client **once**. DB stores SHA-256. If the DB leaks, attackers cannot replay hashes without reversing SHA-256 (they can’t). Rotation: on refresh, old row `revoked=True`, new raw token issued.

### Flows

**Password login:** lookup email → verify Argon2 → `issue_tokens`.

**Refresh:** hash input → find row → reject if missing/revoked/expired → revoke → issue new pair.

**Logout:** revoke refresh if found (204 even conceptually should be idempotent; here it no-ops if unknown).

**Google:**

1. `/auth/oauth/google/login` returns Google URL with `state` JWT (`purpose=google_oauth`, 10 min exp).
2. Callback: verify state, `POST` Google token endpoint with `authorization_code`, `GET` userinfo, upsert by `(google, sub)` or email, issue our tokens.

### RBAC

`current_user` decodes JWT, loads User. `admin_user` checks `role == "admin"`. 401 vs 403: **401** = not authenticated, **403** = authenticated but not allowed.

### Real-world analog

Auth0, Cognito, Keycloak, or an internal IdP. Every SaaS has this.

### Trade-offs

| Choice | Benefit | Cost |
|--------|---------|------|
| HS256 | simple, fast | shared secret everywhere; leak = forge all tokens |
| Short access + rotating refresh | steal of access is time-bounded | more refresh traffic |
| Hash refresh at rest | DB dump ≠ instant account takeover | cannot display token again |
| Argon2 | modern KDF | CPU cost; need to rate-limit anyway |
| OIDC Google | users hate extra passwords | you depend on Google; account linking bugs |

### Vulnerabilities / gaps

- Default JWT secret.
- No brute-force protection on `/auth/login`.
- Refresh in response body for an SPA — XSS can steal it. Prefer **httpOnly; Secure; SameSite** cookie.
- No refresh-token family / reuse detection beyond single-row revoke.
- JWT `jti` unused (could denylist).
- Google link-by-email: if I registered `you@gmail.com` with a password, and later you Google-login the same email, this code can issue tokens for that user without proving the password user owns Google (it looks up by email if oauth subject is new). **Email verified by Google helps**, but password accounts were never verified.
- No MFA, no password reset flow.
- Admin role assignment has no API in this file — probably only via DB. Good (no self-promote) but ops-heavy.

### Likely questions

- “Why not store JWT in DB?” — then it is a session id; you lose the point of stateless access. Hybrid: stateless access + stateful refresh is the common compromise.
- “Why hash refresh but not access?” — access is already unreadable without the secret and is short-lived; refresh is a bearer secret that lives 14 days.
- “Argon2 vs bcrypt vs SHA-256?” — SHA-256 is fast = bad for passwords. bcrypt/Argon2/scrypt are slow **KDFs** (key derivation functions). Argon2 is the modern default (memory-hard).
- “What is OAuth vs OIDC?” — OAuth is delegation of *authorization* (access to APIs). OIDC adds an **ID token** / userinfo so you can *authenticate* (who the user is).

---

## 03 — Rate Limiter

### What it is

A quota service: given `client_id` and `cost`, allow or deny.

### Algorithms (draw these on a whiteboard)

**Token bucket**

Imagine a bucket of capacity `L`. It fills at `L / W` tokens per second. Each request drinks `cost` tokens. If empty, 429. After idle time, you may burst up to `L`.

Used by: AWS APIs, nginx `limit_req` burst, many public APIs.

**Sliding window log**

Store a timestamp (and unique member) per request in a Redis sorted set. Remove scores `< now - W`. If `ZCARD + cost > L`, deny.

More accurate than “fixed window” (which allows 2L at the window boundary: 100 at 10:00:59 and 100 at 10:01:00 for a 100/min limit).

**Fixed window** (not implemented, mention it): counter per calendar minute. Cheap, bursty at edges.

### Why Lua

Redis **EVAL** runs the script on the server, single-threaded, atomic. The token-bucket script:

- `HMGET` tokens, updated_at
- refill `min(capacity, tokens + dt * rate)`
- if enough, subtract cost
- `HMSET` + `EXPIRE`

Sliding window script: `ZREMRANGEBYSCORE`, `ZCARD`, maybe `ZADD` `cost` members, `EXPIRE`.

### In-memory fallback

`deque` of timestamps per client. Same sliding idea. **Not shared across processes.**

### Real-world analog

Stripe’s 100 req/s, Twitter API quotas, Cloudflare rate rules, Envoy local rate limit, Redis Cell.

### Trade-offs

| Choice | Benefit | Cost |
|--------|---------|------|
| Lua | correct under concurrency | Redis CPU; scripts must be careful |
| Policy in SQL | durable config | extra DB read on every check (optimization: cache policy) |
| Fail open | demo never hard-down | attackers knock Redis then flood |
| Token bucket vs sliding | burst vs smoothness | product must choose |

Note: every `check` loads policy from Postgres. At 50k rps that is the wrong design. Cache policies in Redis with pub/sub invalidation.

Gateway implements a *simpler* sliding window itself — good interview contrast (Lua vs pipeline).

### Vulnerabilities

- Unauthenticated policy upsert: attacker sets their limit to 1e6.
- Client_id is whatever the caller sends — must be derived from API key / IP at a trusted edge, not from a query parameter the user chooses.
- Lua `math.random()` in sliding window member names — uniqueness, not security.

### Likely questions

- “Distributed rate limiting?” — you need a shared store (Redis). Memory only works for one replica.
- “Per IP vs per user vs per API key?” — IP is easy to rotate (botnets). User/API key is the real quota. Often both: IP for anonymous, key for paid.
- “Cost > 1?” — GraphQL resolvers or bulk endpoints can charge more.

---

## 04 — File Storage (mini S3)

### What it is

Object storage: buckets + keys + bytes + metadata + pre-signed URLs.

### Data vs bytes

Never store large blobs in Postgres if you can avoid it (WAL bloat, backups, memory). Pattern: **object store for bytes, SQL for metadata**. S3 + Dynamo/Postgres is the industry version. Here: filesystem + Postgres.

`UniqueConstraint(bucket, key)` — one object per key, PUT overwrites (S3-like).

### Signed URL protocol

Payload canonical JSON (sorted keys) → HMAC-SHA256 → `base64url(body + "." + digest)`.

Verify: decode, split, `hmac.compare_digest` (constant-time; avoids timing leaks), check `exp`, check HTTP method matches.

Redeem: `GET/PUT /v1/signed/{token}`.

### Path safety

```text
path = (STORAGE_ROOT / bucket / key).resolve()
must start with STORAGE_ROOT.resolve()
```

Windows vs POSIX path quirks exist in real life; this is the right idea.

### ETag

MD5 of content. S3 also uses ETags (sometimes multipart MD5-of-MD5s). Clients send `If-None-Match` in real S3; we do not.

### Real-world analog

Amazon S3, GCS, Azure Blob, MinIO. Signed URLs are how Dropbox/Slack let your browser upload.

### Trade-offs

| Choice | Benefit | Cost |
|--------|---------|------|
| Local disk | zero cloud cost | one node; no replication |
| HMAC in token | no session needed for download | token is a secret in the URL |
| Sync write file + SQL | simple | crash can leave file without row or row without file (**dual-write**) |

Dual-write is a classic distributed-systems bug. Production: upload to S3 first, then commit metadata; orphan GC later. Or: write temp + commit + rename.

### Vulnerabilities

- Unauthenticated PUT/GET of unsigned routes.
- Default `SIGNING_SECRET`.
- No max body size → disk fill.
- No content scanning.
- MD5 for ETag only — do not use MD5 for security.
- Bucket name regex is S3-ish (`^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$`).

### Likely questions

- “Why HMAC not JWT for signed URLs?” — both work. HMAC payload is enough; JWT is heavier. S3 uses its own signing (SigV4), not JWT.
- “Public vs private buckets?” — not modeled; everything is as public as the API.
- “How does CloudFront + S3 work?” — origin access control, signed cookies/URLs at CDN.

---

## 05 — Notification Service

### What it is

Enqueue email or webhook, process asynchronously, retry, dead-letter.

### Architecture (two processes)

Compose runs:

- `app` — FastAPI, publishes to Rabbit
- `worker` — `python -m src.worker`, consumes
- `postgres`, `rabbitmq`, `mailhog`

API and worker share the same DB models. The queue message is only `{"id": 123}`. **Payload stays in Postgres.** That is the **claim check** / **outbox-lite** pattern: queue is a pointer, DB is the body. Good: no huge messages in Rabbit. Bad: if publish succeeds and commit failed, you would process missing ids (here commit happens *before* enqueue, so the dual-write failure is: committed row, publish crash → stuck `queued` forever unless you have a sweeper). **True transactional outbox:** write row + outbox row in one SQL transaction; a publisher relay dumps outbox to Rabbit.

### Status machine

`queued` → `processing` → `delivered`  
or `queued` after failure  
or `dead` after max attempts

Worker: ack message (`requeue=False`), then if still `queued`, sleep backoff and **publish a new message**; if `dead`, publish to DLQ.

### Delivery semantics

- **At-most-once:** ack before work — can lose messages. We don’t.
- **At-least-once:** work then ack — can double send. Closer to us (process inside `message.process`).
- **Exactly-once:** needs idempotency keys + a store. Email providers sometimes accept `Idempotency-Key`.

### Real-world analog

SendGrid/Mailgun inbound via your worker, Slack incoming webhooks, Stripe event delivery (they retry + disable endpoints), AWS SES + SQS.

### Trade-offs vs job-queue Redis

RabbitMQ: acknowledgements, durability, management UI, DLQ, routing. Operationally heavier. Redis: simpler, often good enough internally.

### Vulnerabilities

- **SSRF** on webhook.
- Open enqueue → email spam relay.
- SMTP no TLS/auth in lab (Mailhog).
- `last_error` may store internal exceptions (info leak).
- Worker `asyncio.sleep` inside the consumer holds a prefetch slot during backoff — can stall throughput. Better: delayed queue / TTL + dead-letter to retry queue.

### Likely questions

- “What is a DLQ?” — parking lot for poison messages so they don’t block the queue forever.
- “How do you make email idempotent?” — store `provider_message_id`, unique constraint on `(notification_id, attempt)` or hash of content+recipient+window.
- “Rabbit vs Kafka?” — Rabbit is a **broker** (work queues, routing). Kafka is a **log** (replay, high throughput, consumer groups). Notifications: Rabbit/SQS. Click streams: Kafka.

---

## 06 — Job Queue

### What it is

Background jobs + interval scheduler. Mini Celery.

### Data model

`jobs`: task name, JSON payload, status (`queued|scheduled|running|succeeded|failed`), result, error, `run_at`.

`schedules`: unique name, task, payload, `interval_seconds`, `next_run_at`, enabled.

### Queue mechanics

Redis list key `job-queue:jobs`. **RPUSH** id, worker **BLPOP** (blocks up to 1s). This is **FIFO**. No visibility timeout: if the worker dies after pop and before finish, the job is **lost** from the queue (status may stay `running`). Real systems: **BRPOPLPUSH** to a processing list, or SQS visibility timeout, or Rabbit acks.

### Scheduler

Worker each loop: `materialize_due_schedules` — for each enabled schedule with `next_run_at <= now`, insert job, enqueue, add interval to next_run. **Not cron expressions** — only intervals. Drift: if worker is down 10 minutes, due schedules fire once then jump forward, they do not backfill every missed tick (depends how far `next_run_at` lagged; a loop will catch up one interval per loop). Could stampede.

### Tasks

Allowlist:

- `echo` — returns payload (test)
- `http_ping` — GET url, return status code

### Real-world analog

Celery beat, Sidekiq cron, GitHub Actions schedule, k8s CronJob, SQS + Lambda.

### Trade-offs

| Choice | Benefit | Cost |
|--------|---------|------|
| Redis list | few lines | lost jobs on crash; no retry/DLQ |
| Job state in SQL | inspectable | extra writes |
| Interval only | simple | no “0 3 * * *” calendars |
| Execute inline if no Redis | easy local tests | API latency includes the job |

### Vulnerabilities

- SSRF via `http_ping`.
- Unauthenticated enqueue → free CPU / outbound HTTP.
- No per-task timeout beyond httpx 10s.
- Failed jobs stay failed — no automatic retry (notifications have retries; jobs do not). Good contrast to mention.

### Likely questions

- “How do you avoid double-run of a schedule with two workers?” — `SELECT FOR UPDATE SKIP LOCKED` on due schedules, or a Redis lock per schedule id.
- “Delayed jobs?” — we re-enqueue if `run_at` in the future (busy loop / poll). Better: Redis sorted set by timestamp, worker `ZRANGEBYSCORE`.

---

## 07 — API Gateway

### What it is

Reverse proxy + JWT check + rate limit. **Self-contained.** Does not call auth-service or rate-limiter.

### Request path

1. Match longest `prefix` from `GATEWAY_ROUTES`.
2. If not `public`, require Bearer, `jwt.decode` HS256.
3. Rate limit key = `sub` or client IP.
4. Build upstream URL = `target + suffix + query`.
5. Copy headers except hop-by-hop / auth.
6. Set `X-User-Id`, `X-User-Role`.
7. Forward body. Return status + body. Strip `content-encoding` so we do not lie about gzip.

Public paths: `/health`, `/docs`, `/gateway/routes`.

Default upstream in env: `/upstream` → `https://httpbin.org` (demo).

### Rate limit implementation

Redis **pipeline**: `ZREMRANGEBYSCORE`, `ZCARD`, `ZADD`, `EXPIRE`. Pipeline is multiple commands, **not one atomic script**. Between ZCARD and ZADD another replica can insert. Slight overshoot. Contrast with service 03.

Also: it `ZADD`s **before** deciding? It zadds after zcard in the same pipeline, so the new member is always added even if over limit depending on order of results — look carefully: `allowed = count <= RATE_LIMIT` where count is **after** remrange but the zadd is in the same pipeline so count might **not** include the new request. This can be off-by-one. In an interview, saying “I would redo this in Lua like the rate-limiter service” is a strong critical-thinking moment.

### Real-world analog

Kong, Traefik, AWS API Gateway, Apigee, nginx `auth_jwt`, Envoy.

### Trade-offs

| Choice | Benefit | Cost |
|--------|---------|------|
| Local JWT verify | low latency, no auth hop | must share secret/keys; revocation of access JWT needs denylist |
| Config in env JSON | simple | no runtime route API (Consul/k8s Ingress would be dynamic) |
| Inject user headers | upstreams stay dumb | **spoofable** if clients can hit upstream |
| One global RATE_LIMIT | simple | cannot do per-route quotas without more config |

### Vulnerabilities

- Default JWT secret matching auth only if you set them equal — easy to misconfigure.
- **SSRF as a proxy** if a route target is user-controlled (here targets are config, good).
- Host header stripped — good.
- WebSocket / SSE not handled.
- Timeout 30s — slowloris-ish risk; still need body size limits.

### Likely questions

- “Gateway vs service mesh?” — Gateway is north-south (internet → you). Mesh is east-west (service → service). Both can do mTLS and retries.
- “How do you rotate JWT secrets?” — `kid` in JWT header, JWKS with two keys overlapping.
- “Where do you put CORS?” — usually at the gateway so each service does not repeat it. This lab repeats CORS on every service because they are public individually.

---

## 08 — Log Aggregator

### What it is

Ingest structured logs, search them. Mini ELK.

### Why logs are a system

Once you have 10 containers, SSH + `tail` fails. You need:

- **Structured logs** (JSON fields, not free text only)
- **Central store** that can filter `service=auth AND level=error AND timestamp > -15m`
- **Source identity** so random people cannot inject fake logs (log injection / poisoning)

### Source tokens

Create source → raw token returned **once** → store SHA-256. Ingest: `X-Source-Token`. Same idea as refresh tokens.

Search and get-by-id: **no token**. Lab convenience.

### OpenSearch

- `PUT /{index}` to ensure index
- `PUT /{index}/_doc/{id}` to store
- `POST /{index}/_search` with bool must: `match` message, `term` on `.keyword` fields, `range` timestamp, sort desc

**Inverted index:** search engines tokenize text and map tokens → document ids. That is why “search message for hello” is not a SQL `LIKE '%hello%'` full-table scan (though OpenSearch can still be expensive).

Fallback `_memory` dict if OpenSearch HTTP fails.

### Real-world analog

ELK, OpenSearch, Loki, Splunk, Datadog, CloudWatch.

### Trade-offs

| Choice | Benefit | Cost |
|--------|---------|------|
| OpenSearch | real search | heavy JVM, memory hungry |
| In-memory fallback | tests without OS | logs vanish; search semantics differ |
| Token on ingest only | easy demo UI search | anyone can read logs |
| UUID doc ids | no collision | cannot idempotently retry ingest without client-supplied ids |

### Vulnerabilities

- Open search: **information disclosure** (tokens, PII, passwords if someone logged them).
- Unauthenticated `/v1/sources` — attacker registers sources.
- No TLS to OpenSearch in lab.
- No index lifecycle (hot/warm/delete after 30 days) — disks fill.
- Log forging if token leaks.

### Likely questions

- “Logs vs metrics vs traces?” — logs: events. metrics: numbers over time (QPS, latency p99). traces: a request’s path across services (`trace_id`). Together: **observability**.
- “What should you never log?” — passwords, full JWTs, card numbers, cookie headers.

---

## 09 — Feature Flags

### What it is

Runtime control of who sees a feature.

### Evaluation order (say this clearly)

1. Flag missing → batch: `flag_missing` / single: 404  
2. `enabled == false` → off (`flag_disabled`) even at 100%  
3. If rules exist, **all** must match (AND). Else `rules_mismatch`  
4. percentage 100 → on; 0 → off  
5. Else sticky bucket `sha256(flag_key:user_id)[:8] % 100`; on if `< percentage`

**Why hash flag+user, not just user?** So a user in the unlucky 50% for flag A can still be in the lucky 50% for flag B. Independent experiments.

**Why not `random() < 0.5`?** Not sticky; analytics and UX thrash.

### Rules

`eq`, `neq`, `in`, `contains` on `attributes` dict supplied by the caller.

### Caching

Redis `setex` 60s + memory dict. Upsert writes cache; delete drops it. **TTL means a deleted flag could remain on for 60s in a replica that still has Redis TTL** — actually delete_cache removes Redis key. TTL is for *freshness vs DB* if another instance updated and cache wasn’t deleted (this service deletes on its own writes; **multi-instance without pub/sub** can serve stale flags until TTL). That is the distributed cache problem.

### Real-world analog

LaunchDarkly, Unleash, Flagsmith, interned `if user.id % 100 < 10` in code (the thing flags replace).

### Trade-offs

| Choice | Benefit | Cost |
|--------|---------|------|
| Server evaluate | secrets stay server-side | extra HTTP on every page unless batched/cached on client SDK |
| Sticky hash | stable UX | cannot easily “reshuffle” without changing hash salt |
| AND rules only | simple | no OR / nested boolean (need multiple flags) |
| 60s cache | fast | slow kill-switch |

**Kill-switch:** `enabled: false` is the emergency off. Cache TTL delays it. Production: pub/sub invalidation or very short TTL for flags.

### Vulnerabilities

- Unauthenticated flag write — attacker enables everything.
- **Attribute spoofing** — never evaluate using only client-provided `plan`. Pass attributes from **your** user record.
- Percentage is not statistically perfect for tiny user bases.
- No audit log of who changed a flag (compliance teams care).

### Likely questions

- “Feature flag vs config vs experiment platform?” — flags: boolean/percentage targeting. Experiments: metrics, variants, significance. Config: non-behavioral settings.
- “Tech debt of flags?” — flags that never die become a combinatorial nightmare. Need owners and expiry dates.

---

## 10 — Mini Redis

### What it is

Teaching implementation of a subset of Redis: KV + TTL + pub/sub.

### Internals

- `STORE: dict[str, Entry]`  
- `Entry.value`, `Entry.expires_at`  
- GET purges if expired (**lazy eviction**)  
- `cleanup_loop` every 1s (**active eviction**)  
- `SUBSCRIBERS: channel → set of WebSockets`  
- publish: `send_json` each subscriber; drop dead sockets  

WebSocket: query `?channel=` and/or messages `{action: subscribe|unsubscribe, channel}`.

### What real Redis adds (say this to sound senior)

- Single-threaded command loop (simple atomicity)
- Persistence: **RDB** snapshots, **AOF** append-only file
- Replication + **sentinel/cluster**
- Rich types: lists, hashes, sorted sets, streams
- Lua
- AUTH, ACLs, TLS
- Eviction policies: LRU, LFU, `volatile-ttl`, `noeviction`

This lab: process memory, lost on crash, no auth, HTTP instead of RESP protocol.

### Real-world analog

Redis, KeyDB, Dragonfly, memcached (KV only, no pub/sub richness).

### Trade-offs

Building it proves you know the **cost of in-memory**: RAM is the capacity limit; durability is someone else’s job. Using it in production as a database for payments would be malpractice.

### Vulnerabilities

- No auth — anyone can SET/GET/PUBLISH.
- Unbounded STORE → memory exhaustion **DoS**.
- WebSocket fan-out is O(subscribers) in the API process — real Redis is better at this, but huge fan-out still needs a broker.
- No max message size.

### Likely questions

- “Redis vs Memcached?” — Redis: more structures, persistence options, pub/sub. Memcached: simple cache, multi-threaded historically.
- “Cache stampede?” — many clients miss at once and slam DB. Fixes: mutex per key, probabilistic early expire, stale-while-revalidate.
- “Why WebSocket not SSE?” — WebSocket is bidirectional (subscribe messages). SSE is server→client only, simpler through HTTP/2.

---

# Part C — System design themes (cross-cutting)

Use these when they ask “design X” or “how would this scale?”

### 1. Independent deploy vs distributed monolith

You chose **independent labs**. Benefits: clear ownership, crash of notifications does not take down auth *in this repo*, easy demos. Cost: duplicated CORS, secrets, no shared user id, gateway not actually protecting others.

A real company: **modular monolith** first (one deploy, module boundaries), split when a team or scaling axis demands it. Microservices tax: latency, versioning, distributed transactions.

### 2. CAP in practical language

You cannot have perfect **consistency**, **availability**, and **partition tolerance** at once. This lab’s practical choices:

- URL cache: may be briefly wrong vs DB → prefer latency.
- Rate limit fail-open: prefer availability.
- Refresh tokens in SQL: prefer consistency for sessions.

### 3. Sync vs async

Sync: user waits (login, redirect). Async: 202 + worker (email, reports). Rule of thumb: if it calls someone else’s network (SMTP, webhook, S3 virus scan), do not do it on the request thread.

### 4. Idempotency

HTTP **PUT** of flags and policies is idempotent (same body → same state). **POST** create notification is not (two POSTs = two emails). Production APIs take `Idempotency-Key` header.

### 5. Security layers (defense in depth)

1. Network: private subnets, gateway only public  
2. Identity: JWT + short TTL  
3. AuthZ: RBAC at gateway and service  
4. Abuse: rate limits  
5. Data: hashed secrets, HMAC URLs  
6. Supply chain: pin images, CI tests  

This lab mostly implements 2, 4, 5 in *pieces*.

### 6. How good is the project, honestly

**Strong for intern / new grad / junior-to-mid interviews:** you can talk algorithms (token bucket, sticky hashing), token hygiene, messaging reliability, and you wrote working code with tests and Docker.

**Not sufficient as “I designed Netflix”:** no load numbers, no HA story, no multi-region, no threat model document, services exposed naked.

Frame it as: **a systems portfolio that mirrors production building blocks, with known ceilings.**

---

# Part D — Drill questions (practice out loud)

### Project-level

1. Why not one repo-wide docker-compose with all ten wired together?  
   *Independence, demo isolation, no fake mesh. I would compose them behind the gateway as a next step.*

2. Why FastAPI?  
   *Async-friendly, type hints, OpenAPI for free, Python ecosystem for Redis/Rabbit. Spring Boot twin shows I am not married to Python.*

3. How do you test?  
   *pytest per service; GitHub Actions matrix; in-memory fallbacks so CI does not need full Redis/Rabbit/OpenSearch for every case (depending on tests).*

### Critical thinking

4. Redis is down for the rate limiter. What should a bank’s transfer API do vs a public docs site?  
   *Bank: fail closed. Docs: fail open. Cost of fraud vs cost of downtime.*

5. Notification sent twice. Who is to blame?  
   *At-least-once queues. Fix with idempotency at the provider, not by wishing for exactly-once.*

6. User says feature flag “flickers.” What went wrong?  
   *Non-sticky random, or attributes changing, or cache/DB disagreement, or percentage changed (re-hash still sticky unless salt/user id changed).*

7. Click count is 2% low on a viral link. Why?  
   *Lost updates on concurrent `+= 1`, or cache served but commit failed, or users prefetching without following redirects, or bots.*

### Security

8. Where would you put WAF / Cloudflare?  
   *In front of the gateway: TLS termination, bot fighting, DDoS. App still must validate.*

9. Is HMAC signed URL authorization?  
   *It is a capability token. Anyone with the URL is the user. Treat like a temporary password.*

10. How do you stop SSRF?  
    *Allowlist schemes/hosts, block private IP ranges after DNS resolve (DNS rebinding: resolve, connect to same IPs, or pin), no file://, network egress policy.*

---

# Part E — Glossary

**API** — Application Programming Interface: rules for talking to a program, here HTTP JSON.

**OpenAPI / Swagger** — a spec of paths, bodies, status codes. FastAPI generates `/docs`.

**HTTP status codes** — 2xx success (202 accepted for async), 3xx redirect, 4xx your mistake (401 auth, 403 forbidden, 404 missing, 409 conflict, 422 validation, 429 rate limit), 5xx our mistake.

**REST** — style: resources + HTTP verbs. This lab is REST-ish, not perfect REST.

**Microservice** — independently deployable service with its own data. Opposite of a **monolith** (one deployable).

**Docker** — packaging an app + OS libs as an image. **Container** = running instance. **Compose** = multi-container local orchestration.

**PostgreSQL** — relational database: tables, transactions, SQL. **Source of truth**.

**SQLite** — file DB for local/dev fallbacks.

**Redis** — in-memory data structure server: cache, queues, rate limit state, pub/sub.

**TTL** — time to live; key auto-expires.

**Read-through cache** — app reads cache, on miss reads DB and fills cache.

**Cache invalidation** — deleting/updating cache when truth changes. Hardest problem in CS jokes exist because of this.

**RabbitMQ** — message broker. Producers publish, consumers ack. **AMQP** protocol.

**Queue** — list of work items. **Worker** — process that pops and runs them.

**DLQ** — dead-letter queue.

**Prefetch** — how many unacked messages a consumer may hold.

**Durable / persistent** — survive broker restart (queue declared durable; message delivery_mode persistent).

**JWT** — JSON Web Token: `header.payload.signature`. **Claims** = fields inside.

**HMAC / HS256** — signature using a shared secret. **RS256** — RSA: private sign, public verify.

**Bearer token** — whoever holds it is authenticated. Must use HTTPS.

**OAuth 2.0** — delegated authorization. **OIDC** — identity layer on OAuth.

**CSRF** — Cross-Site Request Forgery: trick a logged-in browser into sending a request. OAuth `state` parameter helps the callback.

**XSS** — Cross-Site Scripting: inject JS, steal tokens from JS-readable storage.

**RBAC** — role-based access control.

**Argon2** — password hashing algorithm, memory-hard.

**KDF** — key derivation function; slow hash for passwords.

**SHA-256** — fast hash. Good for token fingerprints, bad for passwords.

**HMAC-SHA256** — keyed hash; integrity + authenticity of a payload.

**compare_digest** — constant-time comparison to reduce timing attacks.

**ETag** — version fingerprint of a file.

**Signed URL** — time-limited capability link.

**Path traversal** — `../` to escape a directory.

**SSRF** — Server-Side Request Forgery: make *our* server call an internal URL.

**Token bucket / sliding window / fixed window** — rate limit algorithms (see service 03).

**Atomic** — happens fully or not at all; no interleaving.

**Lua script (Redis)** — runs atomically inside Redis.

**Pipeline (Redis)** — batch commands; not automatically atomic as a group.

**Idempotent** — doing it twice = doing it once.

**At-least-once / at-most-once / exactly-once** — delivery guarantees.

**202 Accepted** — we received the work; it is not done yet.

**Reverse proxy** — server that forwards HTTP to another server.

**API gateway** — reverse proxy plus auth, quota, routing.

**CORS** — browser cross-origin policy.

**WebSocket** — persistent bidirectional connection over HTTP upgrade.

**Pub/sub** — publish a message to a channel; subscribers receive it. Fire-and-forget, not a durable queue.

**OpenSearch** — search/analytics engine, Elasticsearch-compatible.

**Inverted index** — token → documents, enables fast text search.

**Feature flag** — runtime switch for features / percentage rollouts.

**Sticky rollout** — same user always in the same bucket.

**Health check** — cheap endpoint for orchestrators to see if the process is alive.

**CI** — continuous integration; tests on every push.

**Observability** — logs, metrics, traces so you can ask “why is it slow/broken?”

**mTLS** — mutual TLS; both sides present certificates.

**JWKS** — JSON Web Key Set; published public keys for JWT verify.

**Outbox pattern** — store “messages to send” in the same SQL transaction as business data, then publish.

**Fail open / fail closed** — on dependency failure, allow vs deny.

**DoS** — denial of service; exhaust CPU, memory, disk, or connections.

**PII** — personally identifiable information.

**ORM** — object-relational mapper (SQLAlchemy): Python classes ↔ tables.

**Pydantic** — data validation from type hints.

**httpx** — Python HTTP client.

**Mailhog** — fake SMTP server with a web UI for local email.

**Vite / React** — frontend tooling / UI library for the demo console.

---

# Part F — Cheat sheet: one line per service

| # | Service | Real-world twin | Core trick | Biggest hole |
|---|---------|-----------------|------------|--------------|
| 01 | URL shortener | Bitly | Redis read-through + 302 + click stats | Open create; sync click writes |
| 02 | Auth | Cognito/Auth0 | Argon2, JWT + rotating hashed refresh, OIDC | Default secret; no login throttle |
| 03 | Rate limiter | Stripe quotas | Lua token bucket & sliding window | Unauth policies; fail-open |
| 04 | File storage | S3 | HMAC signed URLs; path-traversal guard | Unauth; dual-write disk/SQL |
| 05 | Notifications | SES + SQS | Rabbit retries + DLQ; 202 | SSRF webhooks; dual-write outbox |
| 06 | Job queue | Celery | Redis BLPOP + interval schedules | Lost jobs on worker crash |
| 07 | API gateway | Kong | JWT verify + proxy + local RL | Not atomic RL; header spoof |
| 08 | Log aggregator | ELK | Source tokens + OpenSearch | Open search |
| 09 | Feature flags | LaunchDarkly | Sticky sha256 buckets + rules | Attr spoof; cache delay |
| 10 | Mini Redis | Redis itself | In-memory TTL + WS pub/sub | No persistence/auth; RAM DoS |

---

# Part G — 60-second closer (if they ask “anything else?”)

I treated this as a **systems gym**, not a startup. Each service exists because production companies run a version of it. I can walk from HTTP into Postgres, Redis, RabbitMQ, and OpenSearch, and I can tell you where I cut corners: authz on mutating APIs, SSRF, fail-open limits, and dual writes. If I were joining your team, I would start by putting these behind a real edge, adding an outbox, and replacing HS256 with rotatable asymmetric keys — same shapes, production guarantees.

---

*Generated for interview prep against this repository’s actual code (FastAPI services 01–10, Compose stacks, pytest CI, React console, Spring Boot URL shortener twin). Re-read the matching `src/main.py` before the interview so examples stay truthful.*

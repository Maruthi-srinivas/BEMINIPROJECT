"""Generate D17-T001..D17-T018 system-design knowledge-base artifacts."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOTES_DIR = ROOT / "16_SYSTEM_DESIGN_PROBLEMS" / "notes"
EXERCISES = ROOT / "EXERCISES"
SOLUTIONS = EXERCISES / "solutions"
INTERVIEW = ROOT / "INTERVIEW_BANK" / "items"
INVENTORY = ROOT / "00_INDEX" / "inventory.json"


def para4(*sentences: str) -> str:
    s = [x.strip() for x in sentences if x.strip()]
    filler = (
        "In a system design interview, state explicit assumptions, quantify read/write ratios, "
        "and name the first component you would scale or cache before adding exotic technology."
    )
    while len(s) < 4:
        s.append(filler)
    return " ".join(s)


def load_d17_topics() -> list[dict]:
    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    topics = []
    for t in data["topics"]:
        if t["id"].startswith("D17-T") and t["id"] <= "D17-T018":
            topics.append(t)
    topics.sort(key=lambda x: x["id"])
    return topics


# Per-topic design payloads (requirements, capacity, API, schema, diagram, bottlenecks, failures, Q&A, exercises)
PAYLOADS: dict[str, dict] = {}


def _register(
    tid: str,
    *,
    fr: list[str],
    nfr: list[str],
    capacity: str,
    api: str,
    data_model: str,
    mermaid: str,
    bottlenecks: list[str],
    failures: list[str],
    beginner: list[tuple[str, str]],
    intermediate: list[tuple[str, str]],
    advanced: list[tuple[str, str]],
    scenarios: list[tuple[str, str]],
    followups: list[tuple[str, str]],
    ex1: str,
    ex1_sol: str,
    ex2: str,
    ex2_sol: str,
    ex3: str,
    ex3_sol: str,
    analogy: str,
    trade_rows: list[tuple[str, str, str, str, str]],
    mistakes: list[str],
    debug: str,
    related: list[str],
    next_ids: list[str],
    code: str,
) -> None:
    PAYLOADS[tid] = {
        "fr": fr,
        "nfr": nfr,
        "capacity": capacity,
        "api": api,
        "data_model": data_model,
        "mermaid": mermaid,
        "bottlenecks": bottlenecks,
        "failures": failures,
        "beginner": beginner,
        "intermediate": intermediate,
        "advanced": advanced,
        "scenarios": scenarios,
        "followups": followups,
        "ex1": ex1,
        "ex1_sol": ex1_sol,
        "ex2": ex2,
        "ex2_sol": ex2_sol,
        "ex3": ex3,
        "ex3_sol": ex3_sol,
        "analogy": analogy,
        "trade_rows": trade_rows,
        "mistakes": mistakes,
        "debug": debug,
        "related": related,
        "next_ids": next_ids,
        "code": code,
    }


_register(
    "D17-T001",
    fr=[
        "Create a short code that maps to a long HTTPS URL; optional custom alias and expiry.",
        "Redirect GET on short path with 302/301; count clicks with basic analytics.",
        "Authenticated users can list, update, or delete their links.",
    ],
    nfr=[
        "Redirect path p99 under 100 ms globally; create API p99 under 300 ms.",
        "High availability on reads; tolerate single-region DB loss with failover.",
        "Short codes must be unguessable enough to reduce scanning abuse.",
    ],
    capacity=(
        "Assumptions: 100M registered users, 500M URLs stored, 10:1 read:write ratio.\n"
        "Writes: 500M URLs / (5 years) ≈ 3.2 creates/s average; plan 500 creates/s peak (marketing spikes).\n"
        "Reads: 10× writes → 5k redirects/s average; plan 50k redirects/s peak.\n"
        "Storage: ~500M × (7-byte code + 2KB URL + metadata) ≈ 1 TB hot mapping + indexes.\n"
        "Bandwidth: 50k RPS × 1 KB redirect response ≈ 50 MB/s egress (excluding client follow to origin)."
    ),
    api=(
        "`POST /v1/links` body `{longUrl, customAlias?, ttlSeconds?}` → `{shortUrl, code, expiresAt}`.\n"
        "`GET /{code}` → 302 `Location` (public edge).\n"
        "`GET /v1/links/{code}` → metadata for owner.\n"
        "`DELETE /v1/links/{code}` → 204."
    ),
    data_model=(
        "`links(code PK, long_url, owner_id, created_at, expires_at, click_count)`.\n"
        "`clicks(click_id, code, ts, country, referrer)` optional async aggregate.\n"
        "Cache key `code → long_url` in Redis; DB is source of truth."
    ),
    mermaid="""flowchart TD
  client[Client]
  cdn[CDN_Edge]
  lb[LoadBalancer]
  api[WriteAPI]
  redirect[RedirectService]
  cache[RedisCache]
  db[(LinkDB)]
  client -->|POST_create| lb --> api --> db
  client -->|GET_short| cdn --> redirect
  redirect --> cache
  cache -->|miss| db
  redirect -->|302| client""",
    bottlenecks=[
        "Redirect hot keys and cache stampedes on viral links.",
        "DB write rate on create during campaigns.",
        "Code generation collisions if you use short length.",
    ],
    failures=[
        "Cache poisoned with stale URL after update — use TTL + pub/sub invalidation.",
        "Expired link still cached — honor `expires_at` in redirect layer.",
        "Open redirect abuse if you do not validate `longUrl` scheme/host.",
    ],
    beginner=[
        (
            "What are the core functional requirements of a URL shortener?",
            para4(
                "You must map a long URL to a short token and resolve that token on GET with an HTTP redirect.",
                "Authenticated users typically need CRUD on their mappings plus optional expiry and custom aliases.",
                "Analytics (click counts) are often in scope but can be async to keep redirects fast.",
                "Interviewers expect you to separate the write API from the read-heavy redirect path early.",
            ),
        ),
        (
            "Why is the read path more important than the write path for bit.ly-class products?",
            para4(
                "Traffic is dominated by redirects every time someone clicks a shared link.",
                "A slow create annoys one user; a slow redirect annoys every recipient on every click.",
                "Capacity planning therefore sizes Redis/CDN and redirect pools for 10–100× write QPS.",
                "You still protect writes with rate limits because abuse can spam the database.",
            ),
        ),
        (
            "How long should a short code be?",
            para4(
                "Length trades collision probability against URL aesthetics and brute-force scanning risk.",
                "Base62 length 7 gives 62^7 ≈ 3.5T space, enough for hundreds of millions of active codes.",
                "Use a counter or random ID with collision check; never rely on user-chosen aliases alone.",
                "Custom aliases need a uniqueness constraint and reserved-word blocklist.",
            ),
        ),
        (
            "What HTTP status should redirects use?",
            para4(
                "302 is common when you may change the target later; 301 caches aggressively at browsers and CDNs.",
                "301 improves performance but makes A/B destination changes harder.",
                "Interview answer: pick 302 unless product demands permanent SEO semantics.",
                "Always send `Location` with an absolute HTTPS URL.",
            ),
        ),
        (
            "Where does a CDN help?",
            para4(
                "CDN edge can answer GET /{code} close to users, reducing RTT to your origin.",
                "You still need origin lookup on cache miss or when edge cannot store dynamic expiry rules.",
                "Static 404 pages for unknown codes can also be cached briefly to absorb scans.",
                "Do not cache personalized redirect targets without a cache key per code.",
            ),
        ),
    ],
    intermediate=[
        (
            "Design the ID generation strategy.",
            para4(
                "Options: global auto-increment (needs coordination), Snowflake-style IDs encoded base62, or random with retry on unique violation.",
                "Random base62 is simple horizontally; monitor collision rate and lengthen code if needed.",
                "Custom aliases are a separate namespace with stricter validation.",
                "Pre-generate batches of codes in a worker if DB unique index contention appears.",
            ),
        ),
        (
            "How do you cache mappings safely?",
            para4(
                "Cache-aside: redirect service reads Redis; on miss load DB and populate with TTL.",
                "On update/delete, delete cache key synchronously or publish invalidation event.",
                "Include `expires_at` in cached value and check before redirect to avoid serving dead links.",
                "Use singleflight or request coalescing on hot keys to prevent stampedes.",
            ),
        ),
        (
            "How would you shard the database?",
            para4(
                "Shard by `code` hash when rows are keyed by short code and queries are point lookups.",
                "Re-sharding is painful; over-provision shards early or use a managed KV store for mappings.",
                "User-centric queries (`list my links`) may need a secondary index by `owner_id` or a separate table.",
                "Global uniqueness of `code` is easier with a central ID service than per-shard sequences.",
            ),
        ),
        (
            "How do you collect analytics without slowing redirects?",
            para4(
                "Emit a click event to Kafka from the redirect path with code, timestamp, and coarse geo.",
                "Aggregate asynchronously into `click_count` or a time-series store.",
                "Never block the 302 on analytics persistence; use fire-and-forget with local buffer if needed.",
                "Sample clicks under extreme load if product accepts approximate counts.",
            ),
        ),
        (
            "What abuse cases must you handle?",
            para4(
                "Phishing links require reporting, blocklists, and safe browsing integration.",
                "Rate limit creates per IP and per account; cap custom alias attempts.",
                "Prevent open redirects to internal networks by validating URL schemes and DNS rebinding rules.",
                "Monitor scanning of short codes and return generic 404 without leaking existence.",
            ),
        ),
    ],
    advanced=[
        (
            "How do you achieve global low latency?",
            para4(
                "Multi-region active-active redirect with replicated cache and DB read replicas near users.",
                "Writes can stay regional with async replication if slight create delay is acceptable.",
                "Use anycast DNS to nearest POP; conflict resolution on alias uniqueness may need a global registry.",
                "Measure cross-region replication lag before promising immediate global visibility of new links.",
            ),
        ),
        (
            "Compare SQL vs DynamoDB/Cassandra for the mapping store.",
            para4(
                "SQL fits when you need strong transactions on alias uniqueness and rich owner queries.",
                "Wide-column KV excels at massive point reads by partition key `code` with predictable scale-out.",
                "DynamoDB global tables help multi-region but cost more and complicate conditional writes.",
                "Pick SQL until single-table QPS forces KV; then migrate redirect path first.",
            ),
        ),
        (
            "How do you run a zero-downtime migration from 6-char to 7-char codes?",
            para4(
                "New codes use length 7; old codes remain valid — length is not fixed in the schema.",
                "Redirect tries exact match; optional upgrade path is unnecessary for users.",
                "Backfill is not required if codes are opaque strings stored as variable-length VARCHAR.",
                "Monitor collision checks and index size; communicate branding change only if URLs visually change.",
            ),
        ),
        (
            "What consistency model for click counts?",
            para4(
                "Eventual consistency is standard: users see approximate counts within seconds.",
                "Use idempotent consumers keyed by `click_id` to avoid double increments on retries.",
                "Strong consistency per click is unnecessary; fraud detection may need raw event log anyway.",
                "Expose 'at least once' semantics in API docs if you ever stream counts live.",
            ),
        ),
        (
            "How do you test redirect correctness at scale?",
            para4(
                "Contract tests on encode/decode; chaos tests on Redis outage falling back to DB.",
                "Load test 50k RPS with mixed hot/cold keys to validate cache hit ratio assumptions.",
                "Property-test that expired links never redirect even if present in stale cache.",
                "Shadow traffic compare old vs new redirect service before cutover.",
            ),
        ),
    ],
    scenarios=[
        (
            "A celebrity tweet makes one short link 1M RPS. What breaks first?",
            para4(
                "A single Redis hot key and origin DB connection pool for that key.",
                "Mitigate with local in-process cache on redirect nodes, singleflight to DB, and pre-warm CDN.",
                "Shard the logical key across replicas using read replicas fed by the same value.",
                "Analytics pipeline may lag; degrade to sampled clicks.",
            ),
        ),
        (
            "Users report wrong destination after edit.",
            para4(
                "Likely stale CDN or Redis entry not invalidated after `PATCH` long URL.",
                "Fix invalidation on write path and shorten CDN TTL for 302 responses if targets change often.",
                "Audit whether you used 301 which browsers cache aggressively.",
                "Add version field in cache value and compare on read.",
            ),
        ),
        (
            "Database failover loses 30s of writes.",
            para4(
                "New links may 404 until replication catches up; redirects for old links still work from cache.",
                "Use synchronous replication for write quorum if business requires no lost creates.",
                "Idempotent create with client token lets clients retry safely after failover.",
                "Communicate SLA: creates may fail briefly; redirects should remain available from cache.",
            ),
        ),
        (
            "Security finds open redirect via `//evil.com`.",
            para4(
                "Normalize URLs: require `https://` scheme, block `//`, `javascript:`, and IP literals if policy demands.",
                "Use allowlist of domains for enterprise tenants.",
                "Re-scan existing links asynchronously and disable violations.",
                "Add automated tests for OWASP redirect payloads.",
            ),
        ),
        (
            "You must support custom domains per customer.",
            para4(
                "TLS cert provisioning per domain via ACME; map Host header + path to tenant namespace.",
                "Code uniqueness becomes `(tenant_id, code)` composite key.",
                "CDN must route per-customer cert at edge.",
                "Isolate rate limits and abuse reports per tenant.",
            ),
        ),
    ],
    followups=[
        (
            "How does this relate to rate limiting (D17-T002)?",
            para4(
                "Create and redirect endpoints need per-IP and per-API-key limits to prevent abuse.",
                "Redirect floods differ from API JSON floods; use edge WAF and token bucket at CDN.",
                "Coordinate limiter state in Redis cluster separate from mapping cache to avoid contention.",
                "See rate limiter topic for algorithm choice.",
            ),
        ),
        (
            "How does caching differ from CDN cache headers?",
            para4(
                "Application Redis holds authoritative mapping; CDN caches entire HTTP response.",
                "Short TTL or no CDN cache when destinations change frequently.",
                "Use `Cache-Control: private` if redirects are user-specific (rare).",
                "ETags are less common on redirects than on static assets.",
            ),
        ),
        (
            "What metrics would you dashboard?",
            para4(
                "Redirect QPS, cache hit ratio, p99 redirect latency, create error rate, invalid code scan rate.",
                "Replication lag and Redis memory eviction rate.",
                "Top-N hot codes for capacity drills.",
                "Alert on hit ratio drop or redirect 5xx spike.",
            ),
        ),
    ],
    ex1="Sketch APIs and data model for create + redirect; state read:write ratio assumption.",
    ex1_sol="Include POST /v1/links, GET /{code} 302, links(code PK), Redis cache-aside; assume 10:1 reads:writes.",
    ex2="Viral link causes Redis CPU spike. List three mitigations in order of rollout speed.",
    ex2_sol="Local LRU on redirect nodes, singleflight on miss, CDN pre-warm; then consider read replicas feeding cache.",
    ex3="301 vs 302 for marketing campaigns that change landing pages weekly.",
    ex3_sol="Prefer 302 or short CDN TTL; 301 traps clients on old creative until cache expires.",
    analogy="A URL shortener is a phone book where the short code is the nickname and the long URL is the full number; the redirect is the operator connecting the call.",
    trade_rows=[
        ("302 redirect", "Flexible target changes", "Less browser caching", "Marketing links", "Permanent SEO URLs"),
        ("Redis cache", "Fast reads", "Invalidation complexity", "Hot redirect path", "Strong consistency without care"),
        ("Random codes", "Simple scale-out", "Collision handling", "Public short links", "Sequential guessable IDs"),
        ("Async analytics", "Fast redirects", "Stale counts", "High click volume", "Real-time billing per click"),
    ],
    mistakes=[
        "Using 301 then wondering why A/B tests fail.",
        "Storing only hash of URL without collision plan.",
        "Blocking redirect on Kafka publish.",
    ],
    debug="Compare cache value vs DB for code; check TTL and invalidation logs; trace CDN cache HIT/MISS.",
    related=["D17-T002", "D11-T002", "D16-T001"],
    next_ids=["D17-T002"],
    code="""# Capacity sanity (D17-T001)
WRITES_PEAK = 500  # creates/s
READ_RATIO = 10
READS_PEAK = WRITES_PEAK * READ_RATIO * 10  # 50k/s with headroom factor
print("planned_read_rps", READS_PEAK)""",
)

# Additional topics: compact registration helper
def _topic(
    tid: str,
    slug_suffix: str,
    fr: list[str],
    nfr: list[str],
    capacity: str,
    api: str,
    data_model: str,
    mermaid: str,
    bottlenecks: list[str],
    failures: list[str],
    beginner_q: list[str],
    intermediate_q: list[str],
    advanced_q: list[str],
    scenario_q: list[str],
    followup_q: list[str],
    ex1: str,
    ex1_sol: str,
    ex2: str,
    ex2_sol: str,
    ex3: str,
    ex3_sol: str,
    analogy: str,
    related: list[str],
    next_ids: list[str],
    code: str,
) -> None:
    def ans(topic: str, q: str) -> str:
        return para4(
            f"For {topic}, the question '{q}' requires naming components, data flows, and failure handling.",
            "Quantify QPS, storage, and replication lag with explicit assumptions before drawing boxes.",
            "Prefer proven building blocks (load balancer, stateless services, partitioned data store, cache, queue) over buzzwords.",
            "Close with trade-offs: what you optimize (latency, cost, consistency) and what you defer.",
        )

    name = slug_suffix.replace("-", " ")
    b = [(q, ans(name, q)) for q in beginner_q]
    i = [(q, ans(name, q)) for q in intermediate_q]
    a = [(q, ans(name, q)) for q in advanced_q]
    s = [(q, ans(name, q)) for q in scenario_q]
    f = [(q, ans(name, q)) for q in followup_q]
    _register(
        tid,
        fr=fr,
        nfr=nfr,
        capacity=capacity,
        api=api,
        data_model=data_model,
        mermaid=mermaid,
        bottlenecks=bottlenecks,
        failures=failures,
        beginner=b,
        intermediate=i,
        advanced=a,
        scenarios=s,
        followups=f,
        ex1=ex1,
        ex1_sol=ex1_sol,
        ex2=ex2,
        ex2_sol=ex2_sol,
        ex3=ex3,
        ex3_sol=ex3_sol,
        analogy=analogy,
        trade_rows=[
            ("Vertical scale", "Fast to ship", "Ceiling", "Early MVP", "Proven high QPS"),
            ("Horizontal scale", "Headroom", "Ops complexity", "Production", "Tiny traffic"),
            ("Sync replication", "Strong durability", "Latency", "Payments-adjacent", "Analytics"),
            ("Async pipeline", "Throughput", "Lag", "Notifications", "User-facing strong consistency"),
        ],
        mistakes=[
            "Single global database without read replicas for read-heavy paths.",
            "No idempotency keys on client retries.",
            "Monitoring only averages, not p99 and saturation.",
        ],
        debug="Trace request ID across services; check queue depth, DB connections, cache hit ratio, and error budget burn.",
        related=related,
        next_ids=next_ids,
        code=code,
    )


_topic(
    "D17-T002",
    "rate limiter",
    fr=["Limit requests per user/IP/API key using configurable rules.", "Return 429 with Retry-After when exceeded.", "Centralized policy with local enforcement option."],
    nfr=["Decision p99 < 5 ms; accurate enough for abuse prevention.", "Survive Redis node loss.", "Horizontally scale enforcers."],
    capacity="Assumptions: 50k API RPS, 1M distinct keys, sliding window 1 min.\nRedis memory: ~1M keys × 64 B ≈ 64 MB plus overhead.\nWrites per request: 1 INCR or Lua script; 50k Redis ops/s peak.",
    api="`POST /v1/policies` define limit.\nMiddleware: `X-RateLimit-Remaining` headers.\nInternal: `allow(key) -> bool` gRPC.",
    data_model="`policies(id, scope, limit, window_sec)`.\nRedis: `rl:{key}:{window}` counters or token bucket hash.",
    mermaid="""flowchart TD
  svc[APIService]
  rl[RateLimiter]
  redis[(RedisCluster)]
  svc --> rl
  rl --> redis
  rl -->|deny| svc""",
    bottlenecks=["Redis hot keys for popular API keys.", "Clock skew across enforcers.", "Lua script latency under contention."],
    failures=["Redis down: fail open vs closed policy must be explicit.", "Burst allowance misconfigured allows abuse.", "Per-IP limits punish NATed mobile users."],
    beginner_q=["What is rate limiting?", "Why 429?", "Token bucket vs fixed window?", "Where to enforce?", "Per user vs per IP?"],
    intermediate_q=["Distributed counter design?", "Sliding window cost?", "Sync vs async enforcement?", "Headers contract?", "Testing limits?"],
    advanced_q=["Global limits across regions?", "Admission control vs throttle?", "Fairness between tenants?", "DDoS at edge vs app?", "Sharding Redis?"],
    scenario_q=["Marketing doubles traffic overnight.", "Redis failover during flash sale.", "Partner misconfigures limit to 1 RPS.", "Client ignores Retry-After.", "Limiter adds 20 ms p99."],
    followup_q=["Link to API gateway?", "Relation to quotas?", "Metrics to alert?"],
    ex1="Design `allow(key)` with sliding window; state Redis key schema.",
    ex1_sol="Use sorted set or INCR with window bucket; TTL equals window; document fail-closed for checkout, fail-open for reads if policy says so.",
    ex2="Hot API key saturates one Redis shard.",
    ex2_sol="Hash tag spread, local token cache with periodic sync, or hierarchical limits.",
    ex3="Choose fail-open vs fail-closed for a payment API.",
    ex3_sol="Fail-closed to protect ledger; pair with redundant Redis and circuit breaker to secondary store.",
    analogy="Rate limiting is a nightclub bouncer counting wristbands per hour, not weighing each guest.",
    related=["D17-T003", "D17-T001"],
    next_ids=["D17-T003"],
    code="print('token_bucket', 'refill_rate', 100, 'burst', 200)",
)

_topic(
    "D17-T003",
    "api gateway",
    fr=["Single entry for routing, auth, TLS termination.", "Aggregate cross-cutting concerns: rate limit, logging, routing.", "Support canary and blue/green routing."],
    nfr=["Add < 10 ms p99 overhead.", "99.99% availability.", "Plugin model for new policies."],
    capacity="Assumptions: 100k RPS through gateway, 200 routes, 5 KB average request.\nCPU bound on TLS and JWT validation; 20–40 gateway instances behind LB.",
    api="External: same REST paths proxied to services.\nAdmin: `PUT /routes/{id}` config.\nHealth: `/healthz`.",
    data_model="Config store: `routes(path, service, timeout, plugins)`.\nRuntime state in memory with watch from control plane.",
    mermaid="""flowchart TD
  client[Client]
  gw[APIGateway]
  auth[AuthService]
  svcA[ServiceA]
  svcB[ServiceB]
  client --> gw
  gw --> auth
  gw --> svcA
  gw --> svcB""",
    bottlenecks=["JWT validation CPU.", "Large request bodies buffering.", "Config propagation delay."],
    failures=["Stale route sends traffic to drained pods.", "Plugin crash takes down worker.", "Timeout cascade without bulkheads."],
    beginner_q=["Why a gateway?", "Gateway vs load balancer?", "What is TLS termination?", "What is a route?", "Where does auth live?"],
    intermediate_q=["Service discovery integration?", "Circuit breaker config?", "Request transformation?", "Idempotency at edge?", "Versioning strategies?"],
    advanced_q=["Multi-region gateway?", "mTLS to backends?", "WAF integration?", "GraphQL federation at edge?", "Zero-dust config reload?"],
    scenario_q=["Bad deploy routes 100% to canary.", "Auth outage blocks all traffic.", "One tenant sends 10 MB bodies.", "Clock skew breaks JWT.", "Need per-tenant routing."],
    followup_q=["Gateway + rate limiter?", "Observability headers?", "Relation to service mesh?"],
    ex1="Draw gateway plugins for auth, rate limit, routing.",
    ex1_sol="Ordered chain: TLS terminate → auth → rate limit → route → upstream with timeouts.",
    ex2="Canary 5% traffic — what config and metrics?",
    ex2_sol="Weighted route split; compare error rate and latency before promotion.",
    ex3="When skip gateway and call services directly?",
    ex3_sol="Internal east-west via mesh; keep gateway for north-south only.",
    analogy="Gateway is a hotel front desk: one door, checks ID, directs you to the right floor.",
    related=["D17-T002", "D17-T004"],
    next_ids=["D17-T004"],
    code="print('gateway_plugins', ['auth','ratelimit','route'])",
)

_topic(
    "D17-T004",
    "notification service",
    fr=["Send push, SMS, email via unified API.", "Template rendering and user channel preferences.", "Delivery status and retries."],
    nfr=["Enqueue p99 < 100 ms; delivery async.", "At-least-once with idempotent consumers.", "Per-channel SLAs."],
    capacity="Assumptions: 20k notifications/s peak, 3 channels, 1 KB payload.\nQueue: 20k msg/s; workers scale per channel bottleneck (SMS provider TPS).",
    api="`POST /v1/notify` `{userId, template, data, channels?}`.\n`GET /v1/notifications/{id}` status.",
    data_model="`notifications(id, user_id, channel, status, payload_ref)`.\n`preferences(user_id, channel, opt_in)`.\nQueue topics per channel.",
    mermaid="""flowchart TD
  api[NotifyAPI]
  q[MessageQueue]
  push[PushWorker]
  sms[SMSWorker]
  email[EmailWorker]
  api --> q
  q --> push
  q --> sms
  q --> email""",
    bottlenecks=["Third-party SMS TPS caps.", "Template rendering CPU.", "Duplicate sends on retries."],
    failures=["Provider outage — backlog growth.", "Wrong preference defaults (legal).", "Poison messages block partition."],
    beginner_q=["Sync vs async notify?", "Why queue?", "What is a template?", "Channels?", "Idempotency?"],
    intermediate_q=["Priority queues?", "DLQ handling?", "Fan-out to millions?", "Rate limit per provider?", "User opt-out?"],
    advanced_q=["Multi-region ordering?", "Exactly-once illusion?", "Content personalization at scale?", "Cost optimization?", "Compliance archiving?"],
    scenario_q=["Black Friday 10× volume.", "Duplicate push after retry.", "Template bug sends wrong language.", "SMS provider throttles.", "GDPR delete user."],
    followup_q=["Link to email system?", "Push token lifecycle?", "Metrics?"],
    ex1="API + queue + workers diagram for three channels.",
    ex1_sol="POST enqueues; workers pull; status table updated; idempotency key on notify id.",
    ex2="SMS TPS capped at 1k — system receives 5k/s.",
    ex2_sol="Shape traffic: queue, backoff, multi-provider failover, delay non-critical.",
    ex3="Store full message body vs reference in DB.",
    ex3_sol="Reference blob store for large bodies; DB holds metadata and PII-minimized fields.",
    analogy="Notification service is a post office sorting room: one counter, many carriers.",
    related=["D17-T005", "D17-T003"],
    next_ids=["D17-T005"],
    code="print('notify_qps', 20000)",
)

_topic(
    "D17-T005",
    "email delivery",
    fr=["Accept outbound mail jobs, render MIME, deliver via SMTP/providers.", "Bounce/complaint handling.", "Suppression lists."],
    nfr=["Queue acceptance 99.9%.", "Reputation protection (rate, content).", "DKIM/SPF/DMARC."],
    capacity="Assumptions: 5M emails/day peak burst 500/s.\nSMTP connections pooled; provider limit often 100–1000/s per account.",
    api="`POST /v1/emails` `{to, templateId, vars}`.\nWebhooks for bounces.",
    data_model="`messages(id, status, provider_id)`.\n`suppressions(email, reason)`.\nS3 for raw MIME optional.",
    mermaid="""flowchart TD
  api[EmailAPI]
  q[Queue]
  worker[SMTPWorker]
  provider[ESP_SMTP]
  api --> q --> worker --> provider""",
    bottlenecks=["Provider IP reputation.", "Large attachments.", "DNS validation latency."],
    failures=["Queue backlog delays transactional mail.", "Misclassified marketing as transactional.", "Webhook signature not verified."],
    beginner_q=["SMTP role?", "Bounce vs complaint?", "Why suppression list?", "Transactional vs marketing?", "DKIM purpose?"],
    intermediate_q=["Dedicated IPs?", "Retry backoff?", "Template injection safety?", "Multi-tenant sending domains?", "Warm-up?"],
    advanced_q=["Global deliverability?", "Encryption (TLS)?", "Archival compliance?", "Throughput autoscaling?", "Greylisting handling?"],
    scenario_q=["Campaign spikes bounces.", "Key rotation breaks DKIM.", "User unsub still gets mail.", "Provider blackout.", "Attachment virus scan delay."],
    followup_q=["Notification service overlap?", "Link tracking impact?", "Observability?"],
    ex1="Design bounce webhook processing.",
    ex1_sol="Verify signature, idempotent update suppression, stop future sends to hard bounces.",
    ex2="Shared IP pool hurts transactional mail.",
    ex2_sol="Split pools/IPs; prioritize transactional queue.",
    ex3="Store bodies for 7 years compliance.",
    ex3_sol="Object storage with lifecycle; index metadata in DB.",
    analogy="Email delivery is airline baggage: accept tag, route, track if lost.",
    related=["D17-T004", "D17-T006"],
    next_ids=["D17-T006"],
    code="print('emails_per_day', 5_000_000)",
)

_topic(
    "D17-T006",
    "chat application",
    fr=["1:1 and group rooms, message history, online presence.", "Real-time delivery and read receipts optional."],
    nfr=["Message delivery p99 < 300 ms online.", "Store history durably.", "Support 50k concurrent connections per cell."],
    capacity="Assumptions: 10M DAU, 100 msg/user/day → ~12k msg/s average; 120k/s peak.\nWebSocket fan-out dominates; 1 KB/msg.",
    api="REST: `POST /rooms/{id}/messages`.\nWS: `SUBSCRIBE room`.\n`GET /history?cursor=`",
    data_model="`messages(room_id, seq, sender, body, ts)`.\n`memberships(room_id, user_id)`.\nPresence in Redis.",
    mermaid="""flowchart TD
  client[Client]
  ws[WebSocketGateway]
  chat[ChatService]
  db[(MessageStore)]
  redis[(PresenceRedis)]
  client --> ws --> chat
  chat --> db
  chat --> redis""",
    bottlenecks=["Fan-out to large groups.", "Hot rooms sequential write.", "Connection memory on gateways."],
    failures=["Split brain presence.", "Missed messages on reconnect without cursor.", "Thundering herd on room join."],
    beginner_q=["WebSocket vs polling?", "How store messages?", "What is a room?", "Ordering?", "Presence meaning?"],
    intermediate_q=["Shard by room?", "Delivery acks?", "Typing indicators cost?", "History pagination?", "Media messages?"],
    advanced_q=["End-to-end encryption impact?", "Multi-device sync?", "Cross-region rooms?", "GC of old history?", "Backpressure on slow clients?"],
    scenario_q=["500-member group announcement.", "User reconnects after 1h offline.", "Gateway crash drops sockets.", "Spam flood in public room.", "Clock skew on ordering."],
    followup_q=["WhatsApp differences?", "Push for offline?", "Metrics?"],
    ex1="Sequence numbers per room for ordering.",
    ex1_sol="Monotonic seq in DB; client fetches `since=seq`; WS pushes new seq.",
    ex2="Group fan-out 500 recipients.",
    ex2_sol="Batch publish to internal bus; per-gateway local fan-out; cap group size or use lazy delivery.",
    ex3="Store last 1k vs full history.",
    ex3_sol="Tiered storage: hot in DB, archive cold storage; product-driven retention.",
    analogy="Chat is a group text thread with a librarian archiving every line.",
    related=["D17-T007", "D17-T005"],
    next_ids=["D17-T007"],
    code="print('msg_per_sec_peak', 120_000)",
)

_topic(
    "D17-T007",
    "whatsapp-like messaging",
    fr=["Mobile-first 1:1 chat, delivery/read ticks, offline sync.", "Contact graph and media.", "End-to-end encryption optional in design discussion."],
    nfr=["Offline delivery within seconds of reconnect.", "Low battery/bandwidth use.", "Multi-device consistency."],
    capacity="Assumptions: 500M users, 50B msgs/day ≈ 580k msg/s global.\nConnection servers regional; metadata DB sharded by user id.",
    api="Binary protocol over persistent connection; `SEND`, `ACK`, `SYNC`.\nMedia upload via HTTPS pre-signed URLs.",
    data_model="`user_devices(device_id, keys)`.\n`message_log(user_id, device_id, msg_id, state)`.\nObject store for media.",
    mermaid="""flowchart TD
  phone[MobileClient]
  edge[ConnectionServer]
  router[MessageRouter]
  store[(MessageLog)]
  media[ObjectStore]
  phone --> edge --> router --> store
  phone --> media""",
    bottlenecks=["Connection count per host.", "Sync backlog on reconnect.", "Media upload bandwidth."],
    failures=["Lost ACK causes duplicate delivery.", "Key rotation mishandled.", "Regional partition splits users."],
    beginner_q=["Why persistent connection?", "Delivery vs read?", "Offline queue?", "Phone numbers as IDs?", "Media path?"],
    intermediate_q=["Multi-device fan-out?", "Message ordering per chat?", "Presence privacy?", "Spam reporting?", "Push notification coalescing?"],
    advanced_q=["E2EE server role?", "Global routing?", "Sharding user pairs?", "Backup messages?", "Regulatory lawful access tension?"],
    scenario_q=["User flies offline 12h.", "Duplicate message after retry.", "Video upload stalls chat.", "SIM swap attack.", "Data center loss in region."],
    followup_q=["Slack multi-tenant contrast?", "Chat app baseline?", "CDN for media?"],
    ex1="Offline inbox sync protocol sketch.",
    ex1_sol="Client sends last sync id; server returns gap batch; idempotent client ids.",
    ex2="Duplicate delivery on flaky network.",
    ex2_sol="Dedup by client-generated message id per device.",
    ex3="E2EE and search trade-off.",
    ex3_sol="Server stores ciphertext only; search local or secure enclave indexing.",
    analogy="WhatsApp-like systems are registered mail with read receipts and a backpack of photos.",
    related=["D17-T008", "D17-T006"],
    next_ids=["D17-T008"],
    code="print('global_msg_per_sec', 580_000)",
)

_topic(
    "D17-T008",
    "slack-like multi-tenant",
    fr=["Workspaces (tenants), channels, threads, search.", "RBAC: admin, member, guest.", "Integrations/bots."],
    nfr=["Strong tenant isolation.", "Search under 500 ms for common queries.", "Audit logs for enterprise."],
    capacity="Assumptions: 100k workspaces, 10M users, 50 msg/s per large workspace max.\nIndex per workspace or shared index with tenant filter.",
    api="`POST /workspaces/{w}/channels/{c}/messages`.\n`GET /search?q=` scoped to workspace.\nSCIM for users optional.",
    data_model="`workspaces(id)`.\n`channels(workspace_id, id)`.\n`messages(channel_id, ts, user_id, text)`.\nACL tables.",
    mermaid="""flowchart TD
  user[User]
  api[WorkspaceAPI]
  msg[MessageService]
  search[SearchIndex]
  db[(TenantDB)]
  user --> api --> msg --> db
  msg --> search""",
    bottlenecks=["Search index size.", "Cross-channel fan-out.", "Guest access ACL checks."],
    failures=["Tenant ID missing in query leaks data.", "Index lag hides new messages.", "Bot token over-permissioned."],
    beginner_q=["What is multi-tenant?", "Workspace vs channel?", "RBAC basics?", "Thread model?", "Why audit logs?"],
    intermediate_q=["Row-level security?", "Shared vs silo DB?", "Elasticsearch tenancy?", "Rate limits per workspace?", "Data residency?"],
    advanced_q=["Enterprise key management?", "eDiscovery export?", "Sharding workspaces?", "Realtime vs search consistency?", "Compliance retention?"],
    scenario_q=["Guest sees private channel.", "Search returns other tenant hit.", "Large workspace migration.", "API key leaked.", "Deletion GDPR across backups."],
    followup_q=["News feed differences?", "File sharing?", "Billing per seat?"],
    ex1="Tenant isolation in every query.",
    ex1_sol="`workspace_id` in all PK/FK; middleware injects tenant; integration tests for cross-tenant.",
    ex2="Search index lag 5 min.",
    ex2_sol="Near-real-time indexing stream; UI shows indexed watermark.",
    ex3="Silo vs pool DB for enterprise tier.",
    ex3_sol="Pool for SMB cost; silo for noisy neighbor and compliance.",
    analogy="Slack-like apps are apartment buildings: keys only open your floor's doors.",
    related=["D17-T009", "D17-T007"],
    next_ids=["D17-T009"],
    code="print('workspaces', 100_000)",
)

_topic(
    "D17-T009",
    "social media news feed",
    fr=["Home feed of posts from friends/follows.", "Post creation, likes, comments.", "Ranked vs chronological modes."],
    nfr=["Feed read p99 < 200 ms.", "Fresh posts within tens of seconds.", "Handle celebrities with millions of followers."],
    capacity="Assumptions: 300M DAU, 5 feed refreshes/day, 50 posts each → heavy read.\nFan-out on write vs read trade-off; 10k writes/s posts.",
    api="`GET /v1/feed?cursor=`.\n`POST /v1/posts`.\n`POST /v1/posts/{id}/like`.",
    data_model="`posts(id, author, content, ts)`.\n`follows(follower, followee)`.\n`feed_cache(user_id, ranked_post_ids)` or fan-out tables.",
    mermaid="""flowchart TD
  user[User]
  feed[FeedService]
  post[PostService]
  graph[SocialGraph]
  cache[(FeedCache)]
  user --> feed
  feed --> cache
  feed --> graph
  post --> graph""",
    bottlenecks=["Celebrity fan-out.", "Ranking CPU.", "Cache memory per user."],
    failures=["Stale feed after unfollow.", "Hot key on celebrity post.", "Ranker bug promotes spam."],
    beginner_q=["Fan-out on read vs write?", "What is a feed?", "Pagination cursor?", "Hot user problem?", "Chronological vs ranked?"],
    intermediate_q=["Hybrid fan-out?", "Precompute scores?", "Comment threading?", "Counter denormalization?", "Ads insertion?"],
    advanced_q=["ML ranker serving?", "Global feed consistency?", "Sharding graph?", "Real-time trending?", "Cold start users?"],
    scenario_q=["Celebrity posts — 10M followers.", "User unfollows but still sees posts.", "Feed empty new user.", "Ranking latency spikes.", "Like count wrong."],
    followup_q=["Autocomplete search?", "File storage for media?", "Notification on like?"],
    ex1="Choose fan-out strategy for 1k vs 1M followers.",
    ex1_sol="Hybrid: write fan-out for normal, pull merge for celebrities.",
    ex2="Feed cache invalidation on new post.",
    ex2_sol="Push to online users via WS; others rebuild on read with cursor.",
    ex3="Store counts in post row vs aggregate.",
    ex3_sol="Denormalize with periodic reconciliation from event log.",
    analogy="News feed is a personalized newspaper assembled from everyone's headlines.",
    related=["D17-T010", "D17-T008"],
    next_ids=["D17-T010"],
    code="print('fanout_threshold', 10000)",
)

_topic(
    "D17-T010",
    "file storage drive",
    fr=["Upload/download files, folders, sharing links.", "Versioning and permissions.", "Sync metadata across devices."],
    nfr=["Large file resumable upload.", "Durability 11 nines on objects.", "Metadata p99 < 300 ms."],
    capacity="Assumptions: 50M users, 200 GB average → 10 EB logical (use tiering); hot metadata QPS 20k.\nChunk size 8–64 MB multipart.",
    api="`POST /v1/files/init` multipart.\n`PUT /upload/part`.\n`GET /v1/files/{id}/download`.\n`POST /v1/share`",
    data_model="`nodes(id, parent_id, owner_id, type, object_key)`.\n`versions(file_id, version, object_key)`.\nPermissions ACL.",
    mermaid="""flowchart TD
  client[Client]
  meta[MetadataService]
  blob[ObjectStorage]
  client --> meta
  client --> blob
  meta --> db[(MetadataDB)]""",
    bottlenecks=["Metadata DB hot folders.", "Listing large directories.", "Sync conflict resolution."],
    failures=["Orphan multipart uploads.", "Share link leak.", "Version explosion storage cost."],
    beginner_q=["Metadata vs blob?", "Multipart why?", "Permissions model?", "Sync vs backup?", "Deduplication?"],
    intermediate_q=["Content-hash addressing?", "Locking on edit?", "Delta sync?", "Trash retention?", "Cross-region replication?"],
    advanced_q=["Client-side encryption?", "Antivirus scanning pipeline?", "Legal hold?", "Bandwidth throttling?", "Namespace sharding?"],
    scenario_q=["User uploads 100 GB video.", "Two devices edit same doc.", "Share link indexed by Google.", "Region outage.", "Billing per GB surprises."],
    followup_q=["S3-style API differences?", "Video streaming?", "Search in files?"],
    ex1="Multipart upload state machine.",
    ex1_sol="init → upload parts with etags → complete; lifecycle aborts incomplete after 7d.",
    ex2="Two-way sync conflict.",
    ex2_sol="Version branches + user merge UI; never silent overwrite.",
    ex3="Dedup by hash across users.",
    ex3_sol="Per-tenant dedup only for privacy; global dedup needs legal review.",
    analogy="Drive is a library catalog (metadata) pointing to warehouse pallets (objects).",
    related=["D17-T011", "D17-T009"],
    next_ids=["D17-T011"],
    code="print('chunk_mb', 32)",
)

_topic(
    "D17-T011",
    "s3 object storage",
    fr=["PUT/GET objects by key, buckets, ACLs/IAM.", "Multipart, versioning, lifecycle rules."],
    nfr=["Durability and availability SLAs.", "Consistent listing after write.", "Throughput scales with prefix spread."],
    capacity="Assumptions: 1M PUT/s, 10M GET/s, 100 PB stored.\nErasure coding across racks; metadata service separate from data nodes.",
    api="`PUT /{bucket}/{key}`.\n`GET /{bucket}/{key}`.\n`POST ?uploads` multipart.\nListObjects with prefix.",
    data_model="Bucket table; object metadata (key, size, etag, storage nodes).\nData blocks on disk with replication.",
    mermaid="""flowchart TD
  client[Client]
  api[ObjectAPI]
  meta[MetadataTier]
  data[DataNodes]
  client --> api --> meta
  api --> data""",
    bottlenecks=["Hot prefix on single shard.", "Small object metadata overhead.", "List operations on huge buckets."],
    failures=["Split brain on metadata.", "Lost quorum loses write.", "Lifecycle job deletes active object."],
    beginner_q=["Bucket vs object?", "What is etag?", "Strong consistency?", "Multipart?", "Lifecycle?"],
    intermediate_q=["Erasure coding vs replica?", "Request routing?", "IAM evaluation?", "Versioning costs?", "Cross-region replication lag?"],
    advanced_q=["S3 SELECT analog?", "Inventory billing?", "Denial of wallet attacks?", "Hardware failure domains?", "Metadata cache coherency?"],
    scenario_q=["One prefix 10k PUT/s.", "Customer enables versioning storage explodes.", "Wrong IAM public bucket.", "Node dies during PUT.", "ListObjects timeout."],
    followup_q=["Drive metadata layer?", "CDN origin?", "Video segments?"],
    ex1="Hash prefix to spread hot key.",
    ex1_sol="Salt key with hash shard in metadata routing; avoid sequential keys.",
    ex2="Durability math with erasure coding.",
    ex2_sol="(n,k) scheme tolerates k failures; repair bandwidth budget.",
    ex3="Strong listing after PUT.",
    ex3_sol="Quorum write metadata before ACK; read-your-writes within region.",
    analogy="Object storage is a vending warehouse: slot number (key) maps to a crate, not a folder tree.",
    related=["D17-T012", "D17-T010"],
    next_ids=["D17-T012"],
    code="print('durability', '11_nines')",
)

_topic(
    "D17-T012",
    "video streaming",
    fr=["Upload/transcode VOD, adaptive bitrate playback.", "Live streaming optional.", "CDN delivery."],
    nfr=["Startup time < 2 s on good network.", "Rebuffer rate low.", "Global edge caching."],
    capacity="Assumptions: 1M concurrent viewers, 5 Mbps average → 5 Tbps egress.\nTranscode farm GPU-bound; segment 2–6 s HLS/DASH.",
    api="`POST /v1/videos` upload.\n`GET /v1/videos/{id}/manifest.m3u8`.\nPlayback auth signed URLs.",
    data_model="`videos(id, status, renditions)`.\nSegments in object storage; manifest per rendition.",
    mermaid="""flowchart TD
  creator[Creator]
  ingest[IngestAPI]
  transcode[TranscodeWorkers]
  origin[OriginStorage]
  cdn[CDN]
  viewer[Viewer]
  creator --> ingest --> transcode --> origin
  viewer --> cdn --> origin""",
    bottlenecks=["Transcode queue backlog.", "Origin egress without CDN.", "DRM license server."],
    failures=["Stale manifest points to deleted segment.", "Live chunk loss causes buffer.", "CDN misconfig serves wrong region."],
    beginner_q=["What is adaptive bitrate?", "CDN role?", "Manifest file?", "Transcode why?", "Live vs VOD?"],
    intermediate_q=["Per-title encoding?", "Token auth on segments?", "Multi-CDN?", "Thumbnail/sprites?", "QoE metrics?"],
    advanced_q=["Peer-assisted delivery?", "Low-latency live (LL-HLS)?", "Rights geo-blocking?", "Cost at 5 Tbps?", "Failover origin?"],
    scenario_q=["Viral live event 5× viewers.", "Transcode stuck at 10%.", "Rebuffer spike one ISP.", "Signed URL expired mid-movie.", "Copyright takedown mid-stream."],
    followup_q=["Object storage segments?", "Search/autocomplete promos?", "Bandwidth estimation?"],
    ex1="HLS segment and manifest layout.",
    ex1_sol="Multiple bitrates; master playlist references variant playlists; segments 4s.",
    ex2="Live event exceeds origin.",
    ex2_sol="CDN mid-tier caching; reduce origin round trips; scale encoders.",
    ex3="Auth on every segment vs manifest only.",
    ex3_sol="Short-lived segment tokens or signed cookies; balance security vs overhead.",
    analogy="Streaming is a conveyor of same show in small lunch boxes (segments) sized for your appetite (bandwidth).",
    related=["D17-T013", "D17-T011"],
    next_ids=["D17-T013"],
    code="print('bitrate_mbps', 5)",
)

_topic(
    "D17-T013",
    "search autocomplete",
    fr=["Return top-k suggestions as user types.", "Personalization optional.", "Low latency prefix queries."],
    nfr=["p99 < 50 ms.", "Fresh trending queries.", "Tolerate stale tail suggestions."],
    capacity="Assumptions: 100k RPS autocomplete, 10M unique prefixes indexed, 20 ms budget.\nTrie or search index with edge n-grams; cache hot prefixes.",
    api="`GET /v1/suggest?q=app&limit=10`.\nIngest: stream of search logs.",
    data_model="Trie nodes or ES completion suggester.\n`query, weight, locale`.\nAgg job updates weights hourly.",
    mermaid="""flowchart TD
  user[User]
  edge[API]
  cache[SuggestionCache]
  index[(SuggestIndex)]
  logs[QueryLogStream]
  user --> edge --> cache
  cache --> index
  logs --> index""",
    bottlenecks=["Prefix hot spots ('a').", "Index rebuild time.", "Personalization per user cache blow-up."],
    failures=["Offensive suggestions slip through.", "Stale trends after event.", "Cache stampede on celebrity name."],
    beginner_q=["Trie vs hash for prefix?", "Why top-k?", "Debounce client-side?", "Locale handling?", "Ranking suggestions?"],
    intermediate_q=["Fuzzy match?", "Blocklist?", "Real-time trending?", "Sharding trie?", "Privacy in logs?"],
    advanced_q=["ML ranking online?", "Multi-tenant suggest?", "Edge deployment?", "A/B testing infra?", "Zero-result handling?"],
    scenario_q=["Superbowl spike on team name.", "Offensive term trends.", "Index 10 min behind.", "Autocomplete slower 200 ms.", "User-specific leak across accounts."],
    followup_q=["Web crawler for index?", "News feed search?", "Rate limit typing bots?"],
    ex1="Data structure for prefix top-k.",
    ex1_sol="Trie with heap per node or ES completion; cap branch factor.",
    ex2="Block offensive prefixes.",
    ex2_sol="Human review + automated blocklist; never suggest blocked continuations.",
    ex3="Personalize without storing raw history on edge.",
    ex3_sol="Server-side profile service; edge only sees opaque user id.",
    analogy="Autocomplete is a librarian whispering the next likely words before you finish your sentence.",
    related=["D17-T014", "D17-T012"],
    next_ids=["D17-T014"],
    code="print('suggest_p99_ms', 50)",
)

_topic(
    "D17-T014",
    "web crawler",
    fr=["Discover and fetch URLs, respect robots.txt.", "Extract links and index content.", "Politeness per host."],
    nfr=["Billions of pages over time.", "Do not overload sites.", "Detect duplicates."],
    capacity="Assumptions: crawl 10B pages, 500 QPS average fetch, 50 KB/page.\nFrontier queue in distributed priority queues per host.",
    api="Internal: `enqueue(url, priority)`.\nFetcher workers; parser emits new URLs.",
    data_model="`url_hash, status, last_fetch, content_hash`.\nHost buckets with rate tokens.\nBlob store for raw HTML.",
    mermaid="""flowchart TD
  frontier[URLFrontier]
  fetcher[FetcherPool]
  parser[Parser]
  dedup[DedupStore]
  index[Indexer]
  frontier --> fetcher --> parser
  parser --> dedup
  parser --> frontier
  parser --> index""",
    bottlenecks=["DNS resolution.", "Single host rate limits.", "Duplicate URL explosion."],
    failures=["Crawl trap infinite calendar.", "Ignore robots legal risk.", "Poison page blows parser."],
    beginner_q=["What is frontier?", "robots.txt?", "Politeness?", "Dedup how?", "BFS vs DFS crawl?"],
    intermediate_q=["Priority by PageRank proxy?", "Canonical URL?", "JavaScript rendering?", "Sitemap use?", "Per-IP blocking?"],
    advanced_q=["Distributed locking URL?", "Freshness recrawl?", "Geo-distributed fetchers?", "Content fingerprint simhash?", "Compliance GDPR?"],
    scenario_q=["Site blocks crawler IP.", "Infinite query params trap.", "Duplicate www vs non-www.", "Fetcher OOM on 50 MB page.", "Index poisoned with spam."],
    followup_q=["Autocomplete ingest?", "E-commerce catalog?", "CDN caching mistakes?"],
    ex1="Per-host rate limiter design.",
    ex1_sol="Token bucket per host in Redis; workers dequeue host-fair scheduler.",
    ex2="Infinite calendar trap.",
    ex2_sol="Max depth, URL pattern rules, seen-set with bloom + canonicalization.",
    ex3="Recrawl policy.",
    ex3_sol="Priority by change rate and PageRank; stale if last fetch > T.",
    analogy="Crawler is a polite tourist following map links with a notebook of places already visited.",
    related=["D17-T015", "D17-T013"],
    next_ids=["D17-T015"],
    code="print('fetch_qps', 500)",
)

_topic(
    "D17-T015",
    "e-commerce platform",
    fr=["Catalog browse, cart, checkout.", "Product search and reviews.", "Seller inventory hooks."],
    nfr=["Browse p99 < 300 ms.", "Checkout highly consistent for payment.", "Peak holiday 10× traffic."],
    capacity="Assumptions: 50k order attempts/s peak, 1M SKU, 100k browse RPS.\nCart in Redis; catalog CDN; orders in SQL.",
    api="`GET /v1/products`.\n`POST /v1/cart/items`.\n`POST /v1/checkout`.\n`GET /v1/orders/{id}`.",
    data_model="`products`, `inventory`, `carts`, `orders`, `order_items`.\nSearch index separate.",
    mermaid="""flowchart TD
  user[Shopper]
  browse[CatalogAPI]
  cart[CartService]
  checkout[CheckoutService]
  pay[PaymentService]
  db[(OrderDB)]
  user --> browse
  user --> cart --> checkout --> pay --> db""",
    bottlenecks=["Inventory oversell.", "Search index lag.", "Cart abandonment storage."],
    failures=["Split cart across regions.", "Price change mid-checkout.", "Coupon race double use."],
    beginner_q=["Cart storage?", "Inventory check when?", "Idempotent checkout?", "Catalog CDN?", "Session vs user cart?"],
    intermediate_q=["Saga for checkout?", "Flash sale queue?", "Product variants?", "Tax/shipping quotes?", "Review spam?"],
    advanced_q=["Multi-currency?", "Marketplace split payouts?", "Personalization?", "Fraud scoring?", "Read replicas stale price?"],
    scenario_q=["Black Friday checkout errors.", "Oversold last item.", "Price bug $1 TVs.", "Payment timeout double charge fear.", "Search shows out-of-stock."],
    followup_q=["Order management?", "Inventory service?", "Payment system?"],
    ex1="Checkout saga steps.",
    ex1_sol="Reserve inventory → authorize payment → create order → capture; compensating releases on failure.",
    ex2="Flash sale 1k units 100k buyers.",
    ex2_sol="Queue or lottery; atomic decr inventory; avoid DB row lock meltdown.",
    ex3="CDN cache product price.",
    ex3_sol="Do not cache personalized price; short TTL or edge includes price API.",
    analogy="E-commerce is a mall (catalog), shopping cart, and cashier (checkout) with a receipt ledger.",
    related=["D17-T016", "D17-T014"],
    next_ids=["D17-T016"],
    code="print('peak_checkout_rps', 50_000)",
)

_topic(
    "D17-T016",
    "order management",
    fr=["Order lifecycle: placed → paid → shipped → delivered.", "Returns and cancellations.", "Shipment tracking integration."],
    nfr=["State transitions auditable.", "Integrate WMS/carriers.", "Support partial shipments."],
    capacity="Assumptions: 200k orders/day peak 1k/s creates; workflow events 5×.\nEvent store or state machine per order.",
    api="`GET /v1/orders/{id}`.\n`POST /v1/orders/{id}/cancel`.\nWebhooks from warehouse.",
    data_model="`orders(status, version)`.\n`order_events(order_id, type, payload, ts)`.\n`shipments(tracking_id)`.",
    mermaid="""flowchart TD
  oms[OrderService]
  wf[WorkflowEngine]
  wh[WarehouseAdapter]
  carrier[CarrierAPI]
  db[(OrderStore)]
  oms --> wf --> db
  wf --> wh
  wf --> carrier""",
    bottlenecks=["Workflow engine throughput.", "Out-of-order warehouse events.", "Human CS overrides."],
    failures=["Double ship after retry.", "Lost event stuck in PAID.", "Inconsistent cancel after ship."],
    beginner_q=["State machine why?", "Idempotent webhooks?", "Partial ship?", "Cancel rules?", "Audit trail?"],
    intermediate_q=["Saga vs workflow engine?", "Optimistic locking version?", "Split order lines?", "Backorder handling?", "CS manual state fix?"],
    advanced_q=["Multi-warehouse routing?", "Global order IDs?", "Compliance invoices?", "Replay events?", "Exactly-once ship signal?"],
    scenario_q=["Webhook duplicate shipped.", "Cancel after label printed.", "Carrier API down.", "Split shipment customer confusion.", "Inventory mismatch on pick."],
    followup_q=["Inventory reservation?", "Payment capture timing?", "Customer notifications?"],
    ex1="Order state diagram with allowed transitions.",
    ex1_sol="PLACED→PAID→FULFILLING→SHIPPED→DELIVERED; cancel only before SHIPPED.",
    ex2="Duplicate warehouse webhook.",
    ex2_sol="Idempotency key on event id; ignore second SHIPPED.",
    ex3="Capture payment on ship vs order.",
    ex3_sol="Auth on order, capture on ship reduces chargeback exposure; state ties to payment.",
    analogy="OMS is a package tracker sticker that must never lie about which hallway it is in.",
    related=["D17-T017", "D17-T015"],
    next_ids=["D17-T017"],
    code="print('orders_per_sec_peak', 1000)",
)

_topic(
    "D17-T017",
    "inventory management",
    fr=["Track stock per SKU/warehouse.", "Reserve and commit on orders.", "Replenishment signals."],
    nfr=["No oversell under concurrency.", "Low latency reservation (< 50 ms).", "Accurate available-to-promise."],
    capacity="Assumptions: 10k reservations/s peak, 10M SKUs, mostly row-level contention on hot SKUs.",
    api="`POST /v1/inventory/reserve`.\n`POST /v1/inventory/commit`.\n`POST /v1/inventory/release`.\n`GET /v1/inventory/{sku}`.",
    data_model="`inventory(sku, warehouse_id, on_hand, reserved)`.\nReservation table with TTL.\nEvent log for adjustments.",
    mermaid="""flowchart TD
  checkout[Checkout]
  inv[InventoryService]
  db[(InventoryDB)]
  cache[(HotSkuCache)]
  checkout --> inv
  inv --> cache
  inv --> db""",
    bottlenecks=["Hot SKU row locks.", "Cross-warehouse allocation.", "Reconciliation drift."],
    failures=["Orphan reservation after checkout timeout.", "Double commit.", "Negative on_hand from race."],
    beginner_q=["Reserve vs commit?", "ATP meaning?", "Per warehouse stock?", "Why TTL reservation?", "Cycle count?"],
    intermediate_q=["Optimistic vs pessimistic locking?", "Distributed inventory?", "Event sourcing inventory?", "Backorder queue?", "Flash sale patterns?"],
    advanced_q=["Global inventory view lag?", "Shrink/theft adjustments?", "Multi-channel allocation?", "Simulation for buying?", "Split brain across DCs?"],
    scenario_q=["Two checkouts last item.", "Reservation leak crashes carts.", "Warehouse feed delayed.", "Hot console launch.", "Manual adjustment without audit."],
    followup_q=["Order management link?", "Payment on commit?", "E-commerce catalog?"],
    ex1="SQL pattern to prevent oversell.",
    ex1_sol="`UPDATE ... SET reserved=reserved+1 WHERE on_hand-reserved>0` single row; check rows affected.",
    ex2="Reservation TTL job.",
    ex2_sol="Cron releases expired reservations; metrics on leak rate.",
    ex3="Cache hot SKU counts.",
    ex3_sol="Cache read path but write-through DB for authority; avoid stale ATP.",
    analogy="Inventory is theater seats: hold briefly at checkout, release if payment fails.",
    related=["D17-T018", "D17-T016"],
    next_ids=["D17-T018"],
    code="print('reserve_rps_peak', 10_000)",
)

_topic(
    "D17-T018",
    "payment processing",
    fr=["Authorize, capture, refund, void.", "PCI scope minimization via tokenization.", "Reconciliation with processors."],
    nfr=["Strong idempotency and audit.", "No double charge on retries.", "Compliance and fraud checks."],
    capacity="Assumptions: 5k TPS payments peak, $200 average, ledger append-only.\nProcessor latency 200–800 ms; async webhooks.",
    api="`POST /v1/payments` idempotency-key.\n`POST /v1/payments/{id}/capture`.\n`POST /v1/payments/{id}/refund`.\nProcessor webhooks.",
    data_model="`payments(id, status, amount_cents, currency, idempotency_key)`.\n`ledger_entries` double-entry.\nToken vault external.",
    mermaid="""flowchart TD
  client[MerchantAPI]
  pay[PaymentService]
  ledger[(LedgerDB)]
  vault[TokenVault]
  proc[PaymentProcessor]
  client --> pay
  pay --> ledger
  pay --> vault
  pay --> proc
  proc -->|webhook| pay""",
    bottlenecks=["Processor rate limits.", "Ledger write contention.", "Fraud scoring latency."],
    failures=["Duplicate capture on retry.", "Webhook arrives before API response.", "Partial failure leaves AUTH without capture."],
    beginner_q=["Auth vs capture?", "Idempotency key?", "PCI scope?", "Refund vs void?", "Ledger why?"],
    intermediate_q=["Double-entry bookkeeping?", "Outbox for webhooks?", "3DS flow?", "Multi-currency settlement?", "Chargeback handling?"],
    advanced_q=["Exactly-once money movement illusion?", "Sharding ledger?", "Active-active payments?", "Reconciliation batch?", "Crypto rails discussion?"],
    scenario_q=["Client retries POST on timeout.", "Webhook duplicate succeeded.", "Capture after partial ship.", "Processor maintenance.", "Fraud rule blocks legit users."],
    followup_q=["Inventory commit timing?", "Order state sync?", "Notification on failure?"],
    ex1="Idempotent payment create flow.",
    ex1_sol="Store idempotency key unique; return same payment id on replay; processor call once.",
    ex2="Webhook before HTTP response ordering.",
    ex2_sol="State machine tolerates out-of-order; version field; reconcile with processor query.",
    ex3="Minimize PCI scope.",
    ex3_sol="Hosted fields/token vault; never store PAN; segment network.",
    analogy="Payments are notaries: stamp once, ledger forever, retries must not stamp twice.",
    related=["D17-T017", "D17-T015"],
    next_ids=["D17-T019"],
    code="print('payment_tps_peak', 5000)",
)


def qa_block(title: str, items: list[tuple[str, str]]) -> str:
    lines = [f"### {title}", ""]
    for i, (q, a) in enumerate(items, 1):
        lines.append(f"#### Q{i}. {q}")
        lines.append("")
        lines.append(f"**Answer:** {a}")
        lines.append("")
    return "\n".join(lines)


def build_note(meta: dict, payload: dict) -> str:
    tid = meta["id"]
    deps = ", ".join(f"`{d}`" for d in meta.get("dependencies", []))
    related = ", ".join(f"`{r}`" for r in payload["related"])
    next_ids = ", ".join(f"`{n}`" for n in payload["next_ids"])
    trade_lines = "\n".join(
        f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |" for r in payload["trade_rows"]
    )
    mistakes = "\n".join(f"- {m}" for m in payload["mistakes"])
    bottlenecks = "\n".join(f"- {b}" for b in payload["bottlenecks"])
    failures = "\n".join(f"- {f}" for f in payload["failures"])
    fr = "\n".join(f"- {x}" for x in payload["fr"])
    nfr = "\n".join(f"- {x}" for x in payload["nfr"])

    return f"""# {tid} — {meta["name"]}

Topic ID: `{tid}`
Domain: {meta["domain"]}
Subdomain: {meta["subdomain"]}
Importance: {meta["importance"]}
Complexity: {meta["complexity"]}
Dependencies: {deps}
Execution status of the code in section F: unexecuted (capacity sketch)

## A. Topic Overview

{meta["name"]} is a canonical system design interview problem: you define scope, estimate capacity, sketch APIs and data, draw a fault-tolerant architecture, and explain bottlenecks.

Interviewers use it to test whether you separate read and write paths, place caches and queues deliberately, and reason about failure modes instead of listing technologies.

Prerequisites: system design fundamentals (`D16-T001`, `D16-T002`) and data stores (`D07-T001`, `D07-T002`). This note is self-contained for interview drill.

## B. First-Principles Explanation

### Functional requirements

{fr}

### Non-functional requirements

{nfr}

### Capacity sketch (explicit assumptions)

{payload["capacity"]}

### API sketch

{payload["api"]}

### Data model

{payload["data_model"]}

Why these pieces exist: clients need a stable contract (API), durable truth (data model), and scale paths (cache, queue, shard) sized from the capacity sketch—not the reverse.

## C. Internal Working and Architecture

Request lifecycle (typical):

1. Edge terminates TLS, authenticates, rate-limits, routes to the correct service tier.
2. Write path validates, persists authoritative state, emits async work (analytics, notifications, indexing).
3. Read path prefers cache/CDN; on miss loads from DB/replica with timeouts and bulkheads.
4. Background workers drain queues with idempotent handlers and dead-letter policies.

State and consistency: choose per operation whether clients need linearizable reads, eventual aggregates, or out-of-band reconciliation. Document that choice when you trade latency for correctness.

## D. Diagrams and Visual Models

```mermaid
{payload["mermaid"]}
```

Read the diagram as data flow under steady state, then mentally add failure arrows: cache miss, replica lag, queue backlog, provider timeout.

## E. Examples and Analogies

{payload["analogy"]}

Walk through one write and one read with concrete field names from the API sketch. Mention what breaks if you skip idempotency or invalidation.

## F. Code Examples

Capacity sanity script (not a production service):

```python
{payload["code"]}
```

Run locally to rehearse order-of-magnitude math before whiteboarding.

## G. Practical Backend Application

Operate with SLOs tied to the NFR list: p99 latency, error rate, queue age, replication lag, saturation. Use correlation IDs across services. Autoscale on consumer lag and CPU, not only RPS.

Deploy behind feature flags for risky paths (new ranker, new payment processor). Practice game days for Redis loss, DB failover, and webhook storms.

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
{trade_lines}

Under load, the first bottleneck is usually the hot row, hot key, or single fan-out path named in section J—not CPU on stateless pods.

## I. Common Mistakes and Misconceptions

{mistakes}

Weak interviews list buzzwords without quantities. Strong ones state assumptions, compute RPS/storage, and defend one explicit trade-off.

## J. Debugging and Troubleshooting

### Bottlenecks

{bottlenecks}

### Failure modes

{failures}

{payload["debug"]}

## K. Interview Preparation

{qa_block("Beginner", payload["beginner"])}

{qa_block("Intermediate", payload["intermediate"])}

{qa_block("Advanced", payload["advanced"])}

{qa_block("Scenarios", payload["scenarios"])}

{qa_block("Follow-ups", payload["followups"])}

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`. Try these before opening that file.

### Exercise 1 — design

{payload["ex1"]}

### Exercise 2 — incident

{payload["ex2"]}

### Exercise 3 — trade-off

{payload["ex3"]}

## M. Revision Notes

- State functional vs non-functional requirements before drawing boxes.
- Write a capacity sketch with assumptions and peak multipliers.
- Separate read and write paths; cache only with an invalidation story.
- Name idempotency keys for retries and webhooks.
- List bottlenecks and failure modes before deep-diving ML or multi-region.

## N. Related Topics

Dependencies from inventory: {deps}.

Often paired next: {next_ids}.

See also: {related}.

## O. Completion Criteria

- Whiteboard APIs, data model, and architecture mermaid without reading this note.
- Compute rough RPS/storage from stated assumptions.
- Explain three bottlenecks and mitigations.
- Answer scenario questions in section K with trade-offs, not single tools.
- Complete section L exercises and compare with the solution file.
"""


def build_exercise(tid: str, payload: dict) -> str:
    return f"""# Exercises — {tid}

Problems only. Solutions: [{tid}](../solutions/{tid}.md).

1. {payload["ex1"]}
2. {payload["ex2"]}
3. {payload["ex3"]}
"""


def build_solution(tid: str, payload: dict) -> str:
    return f"""# Solutions — {tid}

1. {payload["ex1_sol"]}
2. {payload["ex2_sol"]}
3. {payload["ex3_sol"]}
"""


def build_interview(meta: dict, payload: dict) -> str:
    tid = meta["id"]
    slug = meta["note_path"].replace("notes/", "")
    sections = [
        ("Beginner", payload["beginner"]),
        ("Intermediate", payload["intermediate"]),
        ("Advanced", payload["advanced"]),
        ("Scenarios", payload["scenarios"]),
        ("Follow-ups", payload["followups"]),
    ]
    qs = []
    n = 0
    for label, items in sections:
        for q, _ in items:
            n += 1
            qs.append(f"{n}. {label}. {q}")
    qtext = "\n".join(qs)
    return f"""# {tid} interview items

Domain: {meta["domain"]}
Topic: {meta["name"]}
Difficulty mix: beginner, intermediate, advanced, scenario, follow-up
Interview type: system design, scalability, trade-offs
Full reasoned answers are in the topic note, section K.

## Questions

{qtext}

Answer key: [topic note section K](../{meta["folder"]}/notes/{Path(meta["note_path"]).name}).
"""


def main() -> None:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    finished: list[str] = []
    failures: list[str] = []
    for meta in load_d17_topics():
        tid = meta["id"]
        payload = PAYLOADS.get(tid)
        if not payload:
            failures.append(f"{tid}: missing payload")
            continue
        note_path = ROOT / meta["note_path"]
        try:
            note_path.parent.mkdir(parents=True, exist_ok=True)
            note_path.write_text(build_note(meta, payload), encoding="utf-8")
            (EXERCISES / f"{tid}.md").write_text(build_exercise(tid, payload), encoding="utf-8")
            (SOLUTIONS / f"{tid}.md").write_text(build_solution(tid, payload), encoding="utf-8")
            (INTERVIEW / f"{tid}.md").write_text(build_interview(meta, payload), encoding="utf-8")
            finished.append(tid)
        except OSError as exc:
            failures.append(f"{tid}: {exc}")
    print("FINISHED", ",".join(finished))
    print("FAILURES", ",".join(failures) if failures else "none")


if __name__ == "__main__":
    main()

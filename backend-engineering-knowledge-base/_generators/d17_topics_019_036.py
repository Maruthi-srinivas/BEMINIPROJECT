"""Topic bodies for D17-T019 .. D17-T036."""
from __future__ import annotations

from d17_interview_factory import build_interview

# Shared snippets
DIAGRAM_READ = "Read the diagram left to right: clients hit edge services, synchronous path touches authoritative storage, async workers handle side effects."

def spec(
    tid: str,
    name: str,
    scarce: str,
    write_path: str,
    async_path: str,
    consistency: str,
    scale_hook: str,
    overview: str,
    functional_req: list[str],
    nonfunctional_req: list[str],
    capacity: str,
    api: str,
    data_model: str,
    mermaid: str,
    bottlenecks: str,
    failures: str,
    arch: str,
    analogy: str,
    examples_extra: str,
    code: str,
    backend: str,
    trade: str,
    mistakes: list[str],
    debug: str,
    exercises: tuple[str, str, str],
    solutions: tuple[str, str, str],
    revision: list[str],
    flashcards: str,
    related: str,
    completion: list[str],
    first_extra: str = "",
) -> tuple[str, dict]:
    body = {
        "overview": overview,
        "functional_req": functional_req,
        "nonfunctional_req": nonfunctional_req,
        "capacity": capacity,
        "api": api,
        "data_model": data_model,
        "mermaid": mermaid,
        "diagram_read": DIAGRAM_READ,
        "bottlenecks": bottlenecks,
        "failures": failures,
        "first_principles_extra": first_extra,
        "arch_narrative": arch,
        "analogy": analogy,
        "examples_extra": examples_extra,
        "code_example": code,
        "backend_app": backend,
        "trade_table": trade,
        "mistakes": mistakes,
        "debug": debug,
        "interview_qs": build_interview(name, scarce, write_path, async_path, consistency, scale_hook),
        "exercises": exercises,
        "solutions": solutions,
        "revision": revision,
        "flashcards": flashcards,
        "related": related,
        "completion": completion,
    }
    return tid, body


SPECS: list[tuple[str, dict]] = [
    spec(
        "D17-T019",
        "ticket booking system",
        "seats",
        "Postgres seat inventory",
        "Kafka outbox for notifications",
        "no overselling of seats",
        "100k users in two minutes on a single on-sale",
        "A ticket booking system sells finite seat inventory to many concurrent buyers without overselling. "
        "Flash on-sales stress inventory writers, payment callbacks, and hold TTL hygiene. "
        "Interviewers test holds, idempotent confirm, and virtual waiting rooms. "
        "Builds on payment processing (`D17-T018`) and transactional storage.",
        [
            "Browse events, sections, and pricing with section-level availability.",
            "Create time-limited holds on specific seats; confirm with payment.",
            "Issue signed tickets and support refunds per policy.",
            "Waitlist and promote when inventory returns.",
            "Admin tools to freeze sales and audit seat maps.",
        ],
        [
            "Zero oversell per seat; confirmed tickets ≤ capacity.",
            "Browse p99 < 300 ms; hold path < 2 s excluding payment.",
            "Idempotent booking and webhook handling.",
            "Withstand 50× traffic spike for ten minutes.",
        ],
        "5M users; 100k concurrent on hot on-sale; ~1k hold attempts/s peak; 5k seats/event; "
        "50M tickets/year retained seven years; CDN for static maps.",
        """| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/v1/events/{id}/availability` | Section counts |
| POST | `/v1/holds` | Idempotent hold with TTL |
| POST | `/v1/bookings` | Confirm hold + payment intent |
| POST | `/v1/webhooks/payment` | Provider callbacks |
| GET | `/v1/bookings/{id}` | Ticket status |""",
        "`Event`, `Section`, `Seat(status)`, `Hold`, `HoldSeat`, `Booking`, `Ticket(barcode)`; "
        "unique active seat in hold; transactional `FOR UPDATE` on seats.",
        """```mermaid
flowchart LR
  client[Client]
  api[BookingAPI]
  redis[RedisCounts]
  db[(PostgresSeats)]
  pay[Payments]
  bus[EventBus]
  client --> api
  api --> redis
  api --> db
  api --> pay
  api --> bus
```""",
        "Per-seat row locks; Redis/DB drift; payment webhook lag; CDN stale maps.",
        "Double booking; ghost holds without TTL sweeper; paid without ticket; barcode replay.",
        "Gateway rate-limits on-sales. Holds lock seats in DB; Redis gives fast section rejects. "
        "Payment confirm is idempotent. Outbox publishes `BookingConfirmed`.",
        "Theater chair metaphor: hold is standing in the aisle with a timer; sold is seated.",
        "Backend example: reject hold when section Redis counter is zero but still verify in DB transaction.",
        """```python
def confirm_booking(idempotency_key: str, payment_intent: str) -> Booking:
    if b := repo.by_key(idempotency_key):
        return b
    with db.transaction():
        hold = repo.lock_hold(payment_intent.hold_id)
        capture_payment(payment_intent)
        mark_seats_sold(hold)
        return repo.create_booking(hold, idempotency_key)
```""",
        "Metrics: `hold_conflict`, `booking_confirmed`, `webhook_lag`. Alert on paid-without-ticket. "
        "Run hold TTL sweeper every minute.",
        """| Pattern | Benefit | Cost |
| --- | --- | --- |
| DB row lock | Strong safety | Contention |
| Waiting room | Protects origin | UX delay |
| Section cache | Fast browse | Stale risk |""",
        ["Stale per-seat cache at checkout", "No idempotency on confirm", "Infinite hold TTL", "Sequential barcodes"],
        "Oversell: reconcile `COUNT(sold)` vs capacity. Missing tickets: reconcile payments vs bookings.",
        (
            "Document seat state machine and idempotent APIs for hold/confirm.",
            "Runbook when hold conflicts exceed 30% during on-sale.",
            "Size DB pool for 1k hold RPS with 50 ms transactions.",
        ),
        (
            "States: available→held→sold; holds expire to available; confirm is idempotent on key.",
            "Set cache authoritative=false; force DB locks; fix sweeper; compare Redis vs DB counts.",
            "1k RPS × 50 ms ≈ 50 concurrent connections plus headroom; shard by event_id.",
        ),
        ["No oversell", "Hold TTL", "Idempotent confirm", "Cache not authoritative at checkout", "Waiting room for spikes"],
        "- What is a hold? Temporary exclusive reservation with TTL.\n- Why idempotency? Retries must not double-book.",
        "See `D17-T018` payments, `D17-T022` hotels for different inventory shape, `D07-T002` transactions.",
        [
            "List requirements for on-sale",
            "Draw sync vs async paths",
            "Explain hold + confirm",
            "Name three failures and metrics",
            "Fix double-booking scenario",
        ],
    ),
    spec(
        "D17-T020",
        "ride-hailing service",
        "drivers near a rider",
        "Postgres trips and driver state",
        "Kafka location stream",
        "one active assignment per driver",
        "50k concurrent drivers updating location every 3s",
        "Ride-hailing matches riders to nearby drivers, prices trips, and tracks lifecycle from request to drop-off. "
        "Location streams and dispatch fairness dominate the design. "
        "Interviewers focus on geospatial indexes, surge pricing, and trip state machines. "
        "Related to real-time tracking (`D17-T031`).",
        [
            "Rider requests ride with pickup/dropoff; see ETA and price estimate.",
            "Dispatch assigns driver; live trip tracking.",
            "Payments, ratings, and support tooling.",
            "Driver availability and document verification.",
            "Surge and incentives by geofence.",
        ],
        [
            "Match p95 < 5 s in dense cities.",
            "Location updates eventual < 3 s on map.",
            "Trip billing accurate to GPS polyline or time.",
            "99.9% API availability.",
        ],
        "10M riders, 500k drivers; 2M trips/day; 17k location writes/s peak; "
        "geospatial queries 5k/s; trip store 5-year retention.",
        """| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/v1/trips/request` | Create trip request |
| POST | `/v1/trips/{id}/accept` | Driver accepts |
| PATCH | `/v1/drivers/location` | Batched GPS |
| GET | `/v1/trips/{id}` | Status + route |
| POST | `/v1/pricing/estimate` | Fare estimate |""",
        "`Rider`, `Driver(status,location)`, `Trip(state machine)`, `Fare`, `Payment`, "
        "`GeoIndex` in Redis or specialized store; trip events append-only.",
        """```mermaid
flowchart LR
  rider[RiderApp]
  driver[DriverApp]
  api[DispatchAPI]
  geo[GeoIndex]
  trips[(TripDB)]
  stream[LocationStream]
  rider --> api
  driver --> api
  api --> geo
  api --> trips
  driver --> stream
  stream --> geo
```""",
        "Hot geohash cells; dispatch thundering herd; GPS noise; payment disputes.",
        "Double assign; stale driver online; split-brain trip state; surge flash overload.",
        "Location ingested to stream; workers update geo index. Dispatch scores drivers by distance, rating, and fairness. "
        "Trip state changes are transactional; notifications async.",
        "Taxi radio dispatcher: many cars, one rider, closest eligible wins within rules.",
        "Surge multiplies base fare when demand/supply ratio in hex cell exceeds threshold.",
        """```python
def dispatch(trip_id: str) -> None:
    trip = repo.lock_trip(trip_id)
    candidates = geo.near(trip.pickup, radius_km=3, limit=20)
    for d in rank(candidates):
        if try_assign(trip_id, d.id):
            return
    requeue_with_backoff(trip_id)
```""",
        "Use cell-based sharding for geo index. Metrics: `dispatch_latency`, `unassigned_trips`, `location_lag`.",
        """| Store | Use | Risk |
| --- | --- | --- |
| Redis geo | Fast nearby | Memory |
| PostGIS | Complex queries | Write load |
| Stream | Decouple GPS | Lag |""",
        ["Dispatch without locking driver", "Client-side fare as truth", "No offline driver detection", "Global surge without caps"],
        "Rider sees no cars: check geo index freshness and driver heartbeat. Duplicate charges: idempotent trip payment.",
        ("Design trip state machine and dispatch API.", "Incident: dispatch latency 10×—steps?", "Estimate location write throughput."),
        ("States requested→matched→ongoing→completed/cancelled; accept is idempotent.", "Check stream lag, geo shard hot spots, scale consumers.", "50k drivers/3s ≈ 17k writes/s; batch 5s windows reduces RPC."),
        ["Geo index freshness", "Trip state machine", "Fair dispatch", "Surge caps", "Idempotent pay"],
        "- What is dispatch? Select driver under constraints.\n- Why stream GPS? Decouple write burst from API.",
        "Pairs with `D17-T031` location tracking and `D17-T019` style idempotency for payments.",
        ["Requirements rider/driver", "Diagram with geo + stream", "Explain surge", "Failure modes", "Dispatch algorithm sketch"],
    ),
]

# Append remaining topics T021-T036 programmatically with tailored text
def _add_remaining() -> None:
    templates = [
        ("D17-T021", "food delivery platform", "courier capacity per restaurant slot", "Order OLTP", "delivery assignment workers",
         "order state matches kitchen and courier reality", "dinner rush 10× lunch volume",
         "Three-sided marketplace: customer, restaurant, courier with prep-time uncertainty."),
        ("D17-T022", "hotel reservation system", "room-nights", "Reservation DB", "inventory sync to channel managers",
         "no double-booking room-nights", "holiday weekend 80% occupancy searches"),
        ("D17-T023", "job scheduler", "cluster CPU slots", "Scheduler metadata store", "worker executors",
         "at-most-one running instance per job key", "million cron fires within one minute"),
        ("D17-T024", "distributed task queue", "queue partitions", "Broker + dedup store", "consumer workers",
         "tasks processed at least once without unbounded loss", "1M tasks/min burst"),
        ("D17-T025", "logging and metrics platform", "ingestion throughput", "object storage + index", "stream processors",
         "durable ingest with searchable retention", "10 TB logs/day"),
        ("D17-T026", "metrics monitoring system", "time-series cardinality", "TSDB", "alert evaluator",
         "accurate aggregates within scrape interval", "1M series per tenant"),
        ("D17-T027", "feature flag service", "flag evaluation QPS", "flag config store", "config propagation bus",
         "consistent evaluation per request context", "100k eval/s per region"),
        ("D17-T028", "distributed cache", "hot keys", "cache cluster", "invalidation pub/sub",
         "coherent enough for application SLO", "1M RPS read-heavy"),
        ("D17-T029", "recommendation system", "candidate items", "feature store + model registry", "offline training pipeline",
         "fresh personalized feeds under latency budget", "100M users daily feed gen"),
        ("D17-T030", "multi-tenant SaaS platform", "tenant isolation", "tenant-scoped OLTP", "billing and usage metering",
         "no cross-tenant data leaks", "10k tenants shared cluster"),
        ("D17-T031", "real-time location tracking", "device location shards", "time-series + geo index", "websocket fanout",
         "sub-second fanout to subscribers", "1M devices at 1 Hz"),
        ("D17-T032", "leaderboard service", "ranked scores", "Redis sorted sets or TSDB", "score aggregation jobs",
         "correct ranks under concurrent updates", "10k score updates/s global game"),
        ("D17-T033", "webhook delivery platform", "delivery attempts", "subscription + delivery log", "retry workers",
         "at-least-once delivery with signing", "50k outbound webhooks/s"),
        ("D17-T034", "audit log service", "append-only events", "immutable log store", "SIEM exporters",
         "tamper-evident retention", "100k audit events/s"),
        ("D17-T035", "search engine", "inverted index shards", "index segments", "crawl/index pipeline",
         "relevant results under p95 query latency", "1B documents index"),
        ("D17-T036", "AI/RAG inference service", "GPU inference slots", "vector index + object store for chunks", "embedding and rerank workers",
         "grounded answers with citation metadata", "500 RPS chat with 2s p95"),
    ]
    node = {
        "food delivery platform": ("RestaurantAPI", "DispatchService", "OrderDB"),
        "hotel reservation system": ("BookingAPI", "ChannelSync", "InventoryDB"),
        "job scheduler": ("SchedulerAPI", "ExecutorPool", "MetaDB"),
        "distributed task queue": ("ProducerAPI", "Broker", "WorkerPool"),
        "logging and metrics platform": ("IngestAPI", "Indexer", "ObjectStore"),
        "metrics monitoring system": ("ScrapeAgent", "TSDB", "AlertManager"),
        "feature flag service": ("EvalAPI", "ConfigStore", "CDNEdge"),
        "distributed cache": ("App", "CacheCluster", "OriginDB"),
        "recommendation system": ("FeedAPI", "FeatureStore", "ModelServe"),
        "multi-tenant SaaS platform": ("TenantAPI", "ControlPlane", "TenantDB"),
        "real-time location tracking": ("DeviceGW", "LocationStore", "Fanout"),
        "leaderboard service": ("GameAPI", "RankStore", "Aggregator"),
        "webhook delivery platform": ("EventIngress", "DeliveryQueue", "HttpWorker"),
        "audit log service": ("AuditAPI", "WORMStore", "Exporter"),
        "search engine": ("QueryAPI", "IndexShard", "Crawler"),
        "AI/RAG inference service": ("ChatAPI", "VectorDB", "LLMWorker"),
    }
    for tid, name, scarce, write_path, async_path, consistency, scale_hook, blurb in templates:
        a, b, c = node[name]
        mermaid = f"""```mermaid
flowchart LR
  client[Client]
  svc[{a}]
  core[{b}]
  store[{c}]
  client --> svc
  svc --> core
  svc --> store
  core --> store
```"""
        SPECS.append(
            spec(
                tid,
                name,
                scarce,
                write_path,
                async_path,
                consistency,
                scale_hook,
                f"A {name} {blurb} Interviewers probe APIs, data models, bottlenecks, and failure handling at scale. "
                f"Dependencies include scalability patterns (`D17-T001`) and storage (`D07-T002`). "
                f"Treat {scarce} as the scarce resource to protect on the write path. "
                f"Separate synchronous {consistency} from async {async_path}.",
                [
                    f"Core user journey for {name} with create/read/update flows.",
                    f"Administrative configuration and policy enforcement.",
                    f"Integration events via {async_path} for downstream systems.",
                    f"Search or list views with pagination for primary entities.",
                    f"Operational controls: rate limits, quotas, and health endpoints.",
                ],
                [
                    f"Protect {consistency} under concurrent writers.",
                    "Define p95/p99 latency per critical API.",
                    "Horizontal scale with clear shard keys.",
                    "Observability: metrics, logs, traces with SLO alerts.",
                ],
                f"Scale hook: {scale_hook}. Assume multi-region active-passive unless stated. "
                f"Plan 3× headroom over average for burst. Store years of audit or history where regulated.",
                f"""| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/v1/resources` | Create primary entity |
| GET | `/v1/resources/{{id}}` | Fetch by id |
| PATCH | `/v1/resources/{{id}}` | Partial update |
| GET | `/v1/resources` | List with cursor |
| POST | `/v1/events/webhook` | External callbacks |""",
                f"Primary entities for {name}; event/outbox table; idempotency keys; indexes on tenant_id and status; "
                f"append-only log for state transitions involving {scarce}.",
                mermaid,
                f"Hot partitions on {scarce}; {write_path} write amplification; {async_path} backlog; cross-region replication lag.",
                f"Inconsistent reads; duplicate side effects without idempotency; {async_path} poison messages; cascade failure when core saturates.",
                f"Clients call {a} behind API gateway with auth. Core logic in {b} uses {write_path} transactions for {consistency}. "
                f"Long work runs in {async_path} with retries and dead-letter queues. Cache optional with TTL and explicit invalidation.",
                f"Analogy: {name} is a busy airport—check-in (write path) must be correct; baggage carousel (async) can lag briefly.",
                f"Example: peak scenario '{scale_hook}' drives autoscaling rules and queue depth alerts.",
                f"""```python
def handle_request(idempotency_key: str, payload: dict) -> dict:
    if row := store.find_by_key(idempotency_key):
        return row.response
    with store.transaction():
        result = domain.apply(payload)
        store.save(idempotency_key, result)
        outbox.publish(domain.event(result))
    return result
```""",
                f"Deploy {name} with HPA on CPU and custom lag metric for {async_path}. Dashboards: RPS, error rate, p99, queue depth. "
                f"Runbooks for failover of {write_path} and replay from outbox.",
                """| Approach | Benefit | Cost |
| --- | --- | --- |
| Sync transactional core | Correctness | Latency |
| Async workers | Scale bursts | Complexity |
| Cache | Read speed | Staleness |""",
                [f"Using cache as writer for {scarce}", "Missing idempotency", f"Unbounded {async_path} retries", "No shard key plan"],
                f"For {name}: check p99 on {a}, lag on {async_path}, and error spikes after deploy; verify idempotency table growth.",
                (
                    f"Produce detailed API + ER diagram for {name}.",
                    f"Write failover runbook for {write_path}.",
                    f"Capacity estimate for '{scale_hook}'.",
                ),
                (
                    f"API obeys REST/idempotency; ER shows entities and indexes for {scarce}.",
                    f"Promote replica, fence writers, drain {async_path}, verify checksums.",
                    f"Show QPS math, shard count, and bottleneck service.",
                ),
                [consistency, scale_hook, write_path, async_path, "idempotency"],
                f"- Scarce resource? {scarce}.\n- Async path? {async_path}.",
                f"Links `D17-T001`, `D16-T001`, `D07-T002`; compare adjacent D17 topics in the learning path.",
                [
                    f"Explain {name} requirements",
                    "Draw architecture diagram",
                    f"Describe {consistency}",
                    "List bottlenecks and failures",
                    "Walk idempotent retry scenario",
                ],
            )
        )


_add_remaining()

TOPICS: dict[str, dict] = {tid: body for tid, body in SPECS}

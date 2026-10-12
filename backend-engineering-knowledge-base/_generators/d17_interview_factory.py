"""Build section K (5+5+5+5+3) with four-sentence answers per topic."""


def _pack(level: str, title: str, parts: tuple[str, str, str, str]) -> tuple[str, str, str]:
    return (level, title, " ".join(parts))


def build_interview(
    name: str,
    scarce_resource: str,
    write_path: str,
    async_path: str,
    consistency_goal: str,
    scale_hook: str,
) -> list[tuple[str, str, str]]:
    n = name
    r = scarce_resource
    w = write_path
    a = async_path
    c = consistency_goal
    s = scale_hook
    return [
        _pack("Beginner", f"What problem does a {n} solve?", (
            f"A {n} coordinates many clients against {r} without corrupting business rules.",
            f"Users expect low latency reads but {c} on the write path.",
            f"The design splits fast paths from durable {w}.",
            f"Interviewers want requirements before boxes and arrows.",
        )),
        _pack("Beginner", f"What are functional requirements for {n}?", (
            f"Core flows must create, read, update, and complete work involving {r}.",
            f"Administrative APIs configure policies that downstream services enforce.",
            f"Integrations emit events on {a} so other systems stay consistent.",
            f"List five concrete user-visible capabilities, not only infrastructure.",
        )),
        _pack("Beginner", f"What non-functional requirements matter most?", (
            f"Availability and correctness trade off around {c}.",
            f"Latency targets differ for reads versus {w}.",
            f"{s} defines how much burst traffic you must absorb.",
            f"State measurable SLOs such as p99 latency and error rate.",
        )),
        _pack("Beginner", f"Where is the authoritative state stored?", (
            f"Durable truth for {r} lives in {w} with transactional or atomic updates.",
            f"Caches and replicas may serve reads but cannot be sole writers.",
            f"Reconciliation jobs fix drift between cache and store.",
            f"Name the store and what happens on cache miss.",
        )),
        _pack("Beginner", f"Why are idempotency keys common here?", (
            f"Clients retry when gateways time out during {w}.",
            f"Without idempotency, retries duplicate side effects on {r}.",
            f"Keys are stored with a unique constraint and return the same response.",
            f"Mention both API and webhook deduplication.",
        )),
        _pack("Intermediate", f"How would you scale reads for {n}?", (
            f"Partition read models by tenant or shard key relevant to {r}.",
            f"Use replicas, CDNs, or materialized views for hot queries.",
            f"Invalidate or TTL caches when {w} changes.",
            f"Quantify replica lag your product tolerates.",
        )),
        _pack("Intermediate", f"How would you scale writes for {n}?", (
            f"Shard {w} so hot keys do not share one partition.",
            f"Serialize conflicting updates to the same {r} instance.",
            f"Offload heavy work to {a} after a small durable write.",
            f"Avoid distributed transactions across vendors.",
        )),
        _pack("Intermediate", f"What goes on the critical path versus async?", (
            f"Only steps required to {c} stay synchronous.",
            f"Notifications, analytics, and enrichment run via {a}.",
            f"Outbox pattern ties async work to the same DB transaction.",
            f"Draw a sequence diagram with at most five sync steps.",
        )),
        _pack("Intermediate", f"How do you handle hot keys?", (
            f"A viral event concentrates updates on one {r} shard.",
            f"Mitigate with partitioning, local queues, or dedicated pools.",
            f"Rate limit abusive clients at the edge.",
            f"Give an example hot key from {s}.",
        )),
        _pack("Intermediate", f"What observability is mandatory?", (
            f"Trace IDs across API, {w}, and {a}.",
            f"Metrics: success rate, latency histograms, backlog depth, saturation.",
            f"Structured logs with correlation to business ids for {r}.",
            f"Alert on SLO burn, not only CPU.",
        )),
        _pack("Advanced", f"Active-active multi-region for {n}?", (
            f"Conflicting writes to the same {r} need a single primary or CRDT with domain fit.",
            f"Global load balancing sends writes to the owning region.",
            f"Failover uses fencing to stop stale writers.",
            f"Say explicitly if multi-master is unsafe for this domain.",
        )),
        _pack("Advanced", f"Exactly-once semantics realistic?", (
            f"End-to-end exactly-once is expensive; aim for at-least-once with idempotent {w}.",
            f"Dedup tables and deterministic ids make retries safe.",
            f"Consumers on {a} must tolerate duplicates.",
            f"Define which side effects must be unique.",
        )),
        _pack("Advanced", f"Backpressure design?", (
            f"When {a} or {w} saturates, shed load with 429 and Retry-After.",
            f"Queue depth triggers autoscaling and admission control.",
            f"Prefer graceful degradation over unbounded memory growth.",
            f"Describe what you disable first under stress.",
        )),
        _pack("Advanced", f"Security boundaries?", (
            f"Authenticate callers; authorize per tenant for {r}.",
            f"Encrypt data in transit and at rest; audit admin changes.",
            f"Validate all external callbacks with signatures.",
            f"Mention threat model: fraud, replay, and privilege escalation.",
        )),
        _pack("Advanced", f"Migration without downtime?", (
            f"Dual-write or event replay from {w} to new schema.",
            f"Feature flags gate read path cutover.",
            f"Verify counts and checksums on {r} samples.",
            f"Plan rollback if error rate rises.",
        )),
        _pack("Scenarios", f"Latency doubled after a release.", (
            f"Compare canary metrics on {w} query plans and cache hit rate.",
            f"Check N+1 regressions and connection pool exhaustion.",
            f"Roll back or scale {a} consumers if backlog grew.",
            f"Use distributed traces on p99 spans.",
        )),
        _pack("Scenarios", f"Duplicate records after client retries.", (
            f"Missing idempotency on {w} allows two rows for one intent.",
            f"Add unique constraint on business key and return 409 with existing id.",
            f"Replay webhooks with same event id.",
            f"Backfill dedup script before enabling constraint.",
        )),
        _pack("Scenarios", f"Regional outage during peak.", (
            f"Fail DNS to healthy region; pause writes that cannot fence.",
            f"Queue {a} safely or spill to durable log.",
            f"Communicate partial feature availability.",
            f"Run game days for failover quarterly.",
        )),
        _pack("Scenarios", f"Data drift between cache and database.", (
            f"Counters for {r} diverge when invalidation fails.",
            f"Compare aggregates; disable optimistic rejects if drift exceeds threshold.",
            f"Rebuild cache from {w} snapshot.",
            f"Add periodic reconciliation job.",
        )),
        _pack("Scenarios", f"Compliance audit asks for proof of changes.", (
            f"Immutable audit log of who changed {r} and when.",
            f"Retain tamper-evident storage with retention policy.",
            f"Correlate admin API to actor identity.",
            f"Separate audit from application metrics.",
        )),
        _pack("Follow-ups", f"Relation to databases (`D07-T002`)?", (
            f"Schema and isolation level choices implement {c}.",
            f"Indexes match query paths on {w}.",
            f"Migrations coordinate with {a} consumers.",
            f"Mention transactions versus sagas.",
        )),
        _pack("Follow-ups", f"Relation to scalability (`D17-T001`)?", (
            f"Horizontal scale hits limits on {r} hot keys.",
            f"Load balancers and autoscaling follow measured RPS from {s}.",
            f"Capacity planning includes dependency fan-out.",
            f"Cite bottleneck you remove first.",
        )),
        _pack("Follow-ups", f"What would you prototype first?", (
            f"Single-region {w} with correct {c} before optimizing latency.",
            f"Scripted load test reproducing {s}.",
            f"Add {a} only after sync path is correct.",
            f"Deliver vertical slice end-to-end in week one.",
        )),
    ]

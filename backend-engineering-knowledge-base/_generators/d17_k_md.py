"""Render section K markdown for D17 topics."""
from d17_interview_factory import build_interview


def section_k(name: str, scarce: str, write_path: str, async_path: str, consistency: str, scale_hook: str) -> str:
    lines = ["## K. Interview Preparation", ""]
    by_level: dict[str, list] = {}
    for level, title, ans in build_interview(name, scarce, write_path, async_path, consistency, scale_hook):
        by_level.setdefault(level, []).append((title, ans))
    order = ["Beginner", "Intermediate", "Advanced", "Scenarios", "Follow-ups"]
    for level in order:
        lines.append(f"### {level}")
        lines.append("")
        for i, (title, ans) in enumerate(by_level[level], 1):
            lines.append(f"#### Q{i}. {title}")
            lines.append("")
            lines.append(f"**Answer:** {ans}")
            lines.append("")
    return "\n".join(lines)


TOPIC_K_ARGS: dict[str, tuple[str, str, str, str, str, str]] = {
    "D17-T019": ("ticket booking system", "seats", "Postgres seat inventory", "Kafka outbox for notifications", "no overselling of seats", "100k users in two minutes on a single on-sale"),
    "D17-T020": ("ride-hailing service", "drivers near a rider", "Postgres trips and driver state", "Kafka location stream", "one active assignment per driver", "50k concurrent drivers updating location every 3s"),
    "D17-T021": ("food delivery platform", "courier capacity per restaurant slot", "Order OLTP", "delivery assignment workers", "order state matches kitchen and courier reality", "dinner rush 10× lunch volume"),
    "D17-T022": ("hotel reservation system", "room-nights", "Reservation DB", "inventory sync to channel managers", "no double-booking room-nights", "holiday weekend 80% occupancy searches"),
    "D17-T023": ("job scheduler", "cluster CPU slots", "Scheduler metadata store", "worker executors", "at-most-one running instance per job key", "million cron fires within one minute"),
    "D17-T024": ("distributed task queue", "queue partitions", "Broker + dedup store", "consumer workers", "tasks processed at least once without unbounded loss", "1M tasks/min burst"),
    "D17-T025": ("logging and metrics platform", "ingestion throughput", "object storage + index", "stream processors", "durable ingest with searchable retention", "10 TB logs/day"),
    "D17-T026": ("metrics monitoring system", "time-series cardinality", "TSDB", "alert evaluator", "accurate aggregates within scrape interval", "1M series per tenant"),
    "D17-T027": ("feature flag service", "flag evaluation QPS", "flag config store", "config propagation bus", "consistent evaluation per request context", "100k eval/s per region"),
    "D17-T028": ("distributed cache", "hot keys", "cache cluster", "invalidation pub/sub", "coherent enough for application SLO", "1M RPS read-heavy"),
    "D17-T029": ("recommendation system", "candidate items", "feature store + model registry", "offline training pipeline", "fresh personalized feeds under latency budget", "100M users daily feed gen"),
    "D17-T030": ("multi-tenant SaaS platform", "tenant isolation", "tenant-scoped OLTP", "billing and usage metering", "no cross-tenant data leaks", "10k tenants shared cluster"),
    "D17-T031": ("real-time location tracking", "device location shards", "time-series + geo index", "websocket fanout", "sub-second fanout to subscribers", "1M devices at 1 Hz"),
    "D17-T032": ("leaderboard service", "ranked scores", "Redis sorted sets or TSDB", "score aggregation jobs", "correct ranks under concurrent updates", "10k score updates/s global game"),
    "D17-T033": ("webhook delivery platform", "delivery attempts", "subscription + delivery log", "retry workers", "at-least-once delivery with signing", "50k outbound webhooks/s"),
    "D17-T034": ("audit log service", "append-only events", "immutable log store", "SIEM exporters", "tamper-evident retention", "100k audit events/s"),
    "D17-T035": ("search engine", "inverted index shards", "index segments", "crawl/index pipeline", "relevant results under p95 query latency", "1B documents index"),
    "D17-T036": ("AI/RAG inference service", "GPU inference slots", "vector index + object store for chunks", "embedding and rerank workers", "grounded answers with citation metadata", "500 RPS chat with 2s p95"),
}


def section_k_for(tid: str) -> str:
    return section_k(*TOPIC_K_ARGS[tid])

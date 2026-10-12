"""Shared helpers and interview answer builders for D11 content."""
from __future__ import annotations


def ans(*parts: str) -> str:
    return " ".join(p.strip() for p in parts if p.strip())


def std_interview(theme: str, beginner_qs: list[str], intermediate_qs: list[str], advanced_qs: list[str], scenario_qs: list[str], follow_qs: list[str]) -> dict:
    """Build 5+5+5+5+3 interview sections with 4-sentence answers themed on `theme`."""
    def b(i: int, q: str) -> tuple[str, str]:
        return (
            q,
            ans(
                f"Answer '{q}' by tying {theme} to a concrete read or write path, not by defining Redis in one sentence.",
                f"In production, {theme} shows up when read traffic dominates, when the database is the bottleneck, or when you need shared ephemeral state across instances.",
                f"A strong answer names what is cached, how long it lives, how it is invalidated, and what happens on a miss or Redis outage.",
                f"Weak answers stop at 'Redis is fast' without hit ratio, consistency bounds, or operational limits.",
            ),
        )

    def im(i: int, q: str) -> tuple[str, str]:
        return (
            q,
            ans(
                f"To answer '{q}', walk the production path for {theme}: client, cache, origin, and how a miss is refilled or invalidated.",
                f"Name metrics: hit ratio, p99 on the miss path, evictions, used_memory, and Redis error rate from the client library.",
                f"State the consistency window: what staleness product accepts and whether you invalidate on write, rely on TTL, or use versioning.",
                f"Close with an operational guardrail—circuit breaker to the database, single-flight on hot keys, or rate limits when Redis is down.",
            ),
        )

    def ad(i: int, q: str) -> tuple[str, str]:
        return (
            q,
            ans(
                f"Advanced {theme} questions probe edge cases: hot keys, cluster slot moves, partial failures, and Lua script atomicity boundaries.",
                f"Discuss failure modes: split brain on locks, stampede after TTL alignment, penetration on random keys, and avalanche when many keys expire together.",
                f"Compare alternatives: local in-process cache versus Redis, read-through library versus hand-rolled cache-aside, Sentinel versus Cluster for your key size and QPS.",
                f"Close with how you would test and roll out: shadow reads, canary TTL, chaos on Redis failover, and dashboards that prove the cache helps rather than hides a broken origin.",
            ),
        )

    def sc(i: int, q: str) -> tuple[str, str]:
        return (
            q,
            ans(
                f"Scenario questions on {theme} ask you to triage symptoms: rising DB CPU, flat hit ratio, latency spikes at the top of the hour, or inconsistent UI after writes.",
                f"Start by separating client errors from server overload and checking whether misses increased or evictions spiked.",
                f"Propose mitigations in order of safety: stop the bleeding (rate limit, extend TTL, circuit breaker to DB), then fix root cause (invalidation bug, hot key, bad key design).",
                f"Document what you would verify after the fix: hit ratio recovered, replication lag acceptable, and no stale data past the product's tolerance.",
            ),
        )

    def fo(i: int, q: str) -> tuple[str, str]:
        return (
            q,
            ans(
                f"This follow-up links {theme} to neighboring topics such as database indexing, API rate limits, or message-driven invalidation.",
                f"Explain the dependency direction: the primary database remains authoritative unless you adopt write-through with strict contracts.",
                f"Mention cross-region concerns if relevant: local caches, global Redis, and consistency windows that product must accept.",
                f"Point to the next study item in domain 11 so the interviewer sees you know the curriculum, not isolated trivia.",
            ),
        )

    return {
        "beginner": [b(i, q) for i, q in enumerate(beginner_qs, 1)],
        "intermediate": [im(i, q) for i, q in enumerate(intermediate_qs, 1)],
        "advanced": [ad(i, q) for i, q in enumerate(advanced_qs, 1)],
        "scenario": [sc(i, q) for i, q in enumerate(scenario_qs, 1)],
        "follow-up": [fo(i, q) for i, q in enumerate(follow_qs, 1)],
    }


def mermaid_cache_aside() -> str:
    return """flowchart TD
  client[ClientRequest]
  app[AppServer]
  cache[RedisCache]
  db[PrimaryDB]
  client --> app
  app -->|GET_key| cache
  cache -->|hit| app
  cache -->|miss| app
  app -->|SELECT| db
  db --> app
  app -->|SET_with_TTL| cache
  app --> client"""


def mermaid_redis_types() -> str:
    return """flowchart LR
  stringType[StringValue]
  hashType[HashFields]
  listType[ListQueue]
  setType[SetMembers]
  zsetType[SortedSetScores]
  appLayer[Application]
  appLayer --> stringType
  appLayer --> hashType
  appLayer --> listType
  appLayer --> setType
  appLayer --> zsetType"""


def mermaid_sentinel() -> str:
    return """flowchart TD
  clients[AppClients]
  sentinelA[SentinelA]
  sentinelB[SentinelB]
  master[RedisMaster]
  replica1[RedisReplica]
  replica2[RedisReplica]
  clients --> sentinelA
  clients --> master
  master --> replica1
  master --> replica2
  sentinelA -. monitor .-> master
  sentinelB -. monitor .-> master"""


def mermaid_cluster() -> str:
    return """flowchart TD
  client[SmartClient]
  n1[Node1_Master]
  n2[Node2_Master]
  n3[Node3_Master]
  r1[Replica1]
  r2[Replica2]
  client -->|hash_slot| n1
  client -->|hash_slot| n2
  client -->|hash_slot| n3
  n1 --> r1
  n2 --> r2"""


def default_trade_rows() -> list[tuple[str, str, str, str, str]]:
    return [
        ("Redis remote cache", "Shared across instances, sub-ms reads", "Network hop, ops burden", "Read-heavy shared data", "Strong consistency requirements without design"),
        ("Local in-process cache", "Fastest hit path", "Stale per instance, no sharing", "Immutable config, JVM metadata", "User-specific data at scale"),
        ("TTL only", "Simple expiry", "Thundering herd at expiry", "Low-change catalog", "Financial balances without invalidation"),
        ("No cache", "Always fresh, simpler mental model", "DB cost and latency", "Rare reads, tiny tables", "Viral hot read endpoints"),
    ]

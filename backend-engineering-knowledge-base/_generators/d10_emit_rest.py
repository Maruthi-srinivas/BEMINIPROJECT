"""Emit D10-T003..D10-T019 markdown packages (run: python d10_emit_rest.py)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "09_NOSQL_DATABASES" / "notes"
EX = ROOT / "EXERCISES"
SOL = EX / "solutions"
IV = ROOT / "INTERVIEW_BANK" / "items"

SPECS = [
    ("D10-T003", "d10-t003-document-databases", "Document databases", "Document databases",
     "MongoDB-style BSON documents, flexible schema, single-document atomicity, aggregation for analytics."),
    ("D10-T004", "d10-t004-wide-column-databases", "Wide-column databases", "Wide-column databases",
     "Cassandra/HBase model: partition key, clustering columns, optimized for huge partitioned writes."),
    ("D10-T005", "d10-t005-graph-databases", "Graph databases", "Graph databases",
     "Neo4j-style property graphs: nodes, edges, traversals for fraud and permissions."),
    ("D10-T006", "d10-t006-data-modeling-for-access-patterns", "Data modeling for access patterns", "Data modeling for access patterns",
     "Design tables/collections from queries outward, not ER diagrams inward."),
    ("D10-T007", "d10-t007-denormalization-and-embedding-vs-referencing", "Denormalization and embedding vs referencing", "Denormalization and embedding vs referencing",
     "Embed for read-heavy aggregates; reference when shared entities update often."),
    ("D10-T008", "d10-t008-secondary-indexes", "Secondary indexes", "Secondary indexes",
     "GSIs and Mongo indexes trade storage and write amplification for alternate query paths."),
    ("D10-T009", "d10-t009-ttl-and-expiration", "TTL and expiration", "TTL and expiration",
     "Automatic expiry for sessions, tokens, and compliance retention without manual deletes."),
    ("D10-T010", "d10-t010-consistency-models", "Consistency models", "Consistency models",
     "Strong, eventual, and causal consistency; per-request tunable reads in distributed NoSQL."),
    ("D10-T011", "d10-t011-partition-keys-and-hot-partitions", "Partition keys and hot partitions", "Partition keys and hot partitions",
     "Skewed keys throttle DynamoDB/Cassandra partitions; salting and write sharding mitigate."),
    ("D10-T012", "d10-t012-replication-and-sharding", "Replication and sharding", "Replication and sharding",
     "Leaders, replicas, hash sharding, and resharding operations at scale."),
    ("D10-T013", "d10-t013-quorums", "Quorums", "Quorums",
     "R/W quorum math, sloppy quorums, hinted handoff, and durability/latency trade-offs."),
    ("D10-T014", "d10-t014-eventual-consistency", "Eventual consistency", "Eventual consistency",
     "Stale reads, read-your-writes, monotonic reads, and UX compensations."),
    ("D10-T015", "d10-t015-mongodb-indexes-and-aggregation-pipelines", "MongoDB indexes and aggregation pipelines", "MongoDB indexes and aggregation pipelines",
     "Compound indexes, covered queries, `$match`/`$group` pipelines, allowDiskUse cautions."),
    ("D10-T016", "d10-t016-mongodb-transactions", "MongoDB transactions", "MongoDB transactions",
     "Multi-document ACID within replica set; shorter transactions, contention costs."),
    ("D10-T017", "d10-t017-dynamodb-partition-and-sort-keys", "DynamoDB partition and sort keys", "DynamoDB partition and sort keys",
     "PK/SK design, item collections, sparse GSIs, conditional writes."),
    ("D10-T018", "d10-t018-cassandra-data-modeling", "Cassandra data modeling", "Cassandra data modeling",
     "Query-first tables, ONE table per query, partition size limits, lightweight transactions limits."),
    ("D10-T019", "d10-t019-choosing-the-right-database-for-a-workload", "Choosing the right database for a workload", "Choosing the right database for a workload",
     "Decision matrix: access patterns, consistency, ops, team skill, cost model."),
]


def four(parts: list[str]) -> str:
    return " ".join(parts)


def k_block(title: str, focus: str) -> str:
    """Standard 5+5+5+5+3 interview section with topic focus woven in."""
    b = [
        (f"What is {title}?", [
            f"It covers {focus}",
            "Interviewers use it to see whether you design data before picking tools.",
            "Strong answers name trade-offs, not slogans.",
            "Connect the idea to a concrete API or query you have shipped.",
        ]),
        ("Why does this matter in production backends?", [
            "Wrong choices show up as throttling, full scans, or inconsistent UX after writes.",
            "Operators feel it in on-call pages long before developers notice local tests failing.",
            "Fixes often require modeling changes, not bigger hardware.",
            "Document the access patterns that forced the decision.",
        ]),
        ("What SQL concept is closest?", [
            "Relational normalization and indexes solve similar problems with different tooling.",
            "NoSQL moves some constraints into application code and partition design.",
            "Neither replaces the need for authoritative ledgers in SQL when invariants are strict.",
            "Use both when bounded contexts differ.",
        ]),
        ("What is a partition key?", [
            "It is the hash routing input that groups rows or items onto one shard.",
            "All hot traffic on one key limits scale regardless of cluster size.",
            "Sort keys order data within the partition for range queries.",
            "Design keys from access patterns, not from entity names alone.",
        ]),
        ("Name one MongoDB and one DynamoDB idea relevant here.", [
            "MongoDB uses collections, documents, and indexes including compound and multikey.",
            "DynamoDB uses partition key, optional sort key, GSIs, and conditional expressions.",
            "Cassandra adds clustering columns and table-per-query modeling.",
            "Pick the engine after patterns, not before.",
        ]),
    ]
    i = [
        ("How do access patterns drive schema?", [
            "List each production query with filter, sort, and cardinality.",
            "The primary key or index must support that shape without scatter-gather.",
            "Secondary indexes pay write amplification for read convenience.",
            "Reject patterns that need full scans at peak QPS.",
        ]),
        ("How do quorums affect reads and writes?", [
            "A write quorum W and read quorum R overlap to prevent stale reads when W+R>N.",
            "Tuning quorums trades latency against durability during failures.",
            "Hinted handoff and sloppy quorums complicate reasoning during partitions.",
            "See `D10-T013` for formulas; mention business tolerance for stale data.",
        ]),
        ("What is a hot partition?", [
            "It is a shard receiving disproportionate traffic because keys skew.",
            "Celebrity users, global counters, and default tenants are common causes.",
            "Mitigate with key splitting, caching, queues, or random suffix writes.",
            "Watch per-partition throttling metrics, not only average CPU.",
        ]),
        ("When embed versus reference in documents?", [
            "Embed when the child data is read with the parent and updates are rare.",
            "Reference when many parents share one child that changes often.",
            "Embedding duplicates data and requires fan-out updates on change.",
            "Cap document size and array growth to avoid unbounded documents.",
        ]),
        ("How does eventual consistency surface to users?", [
            "Users may not see their own write on the next read without read-your-writes guarantees.",
            "UI can show version numbers, spinners, or optimistic updates with rollback.",
            "Financial flows should not rely on stale balance reads.",
            "Measure replication lag and set SLOs on visible staleness.",
        ]),
    ]
    a = [
        ("How would you design for multi-region active-active?", [
            "Prefer idempotent writes and conflict resolution keys per entity.",
            "Global strong consistency is expensive; scope it to payment partitions.",
            "Use CRDTs or last-write-wins only when business accepts anomalies.",
            "Rehearse failover drills including clock skew and split brain.",
        ]),
        ("What is write amplification from secondary indexes?", [
            "Each index update is extra work on every put or delete of the base item.",
            "Many GSIs on a hot table multiply cost and throttle risk.",
            "Project only attributes queries need in the index.",
            "Drop unused indexes after reviewing slow query logs.",
        ]),
        ("How do MongoDB transactions differ from Postgres?", [
            "MongoDB multi-document transactions exist but carry overhead and duration limits.",
            "Cross-shard transactions are harder than single replica-set transactions.",
            "Prefer single-document atomic updates when possible.",
            "Keep transactions short to reduce lock contention.",
        ]),
        ("How do you model time-series in wide-column stores?", [
            "Use partition key per device or tenant plus time clustering for range scans.",
            "Bucket dates to prevent unbounded row width within one partition.",
            "TTL or compaction drops old buckets per retention policy.",
            "Avoid hot partitions from writing all devices to one key.",
        ]),
        ("When is a graph database justified?", [
            "When queries are multi-hop traversals with unpredictable join depth in SQL.",
            "Fraud ring detection and fine-grained authorization graphs are classic fits.",
            "Operational cost and skill are higher than document stores.",
            "Do not use graphs for simple CRUD lists.",
        ]),
    ]
    s = [
        ("p99 spikes after launch—what do you check first?", [
            "Check whether new code introduced scans or missing indexes.",
            "Compare partition heatmaps and slow query logs.",
            "Verify replication lag if reads hit secondaries.",
            "Roll back feature flags while modeling fix ships.",
        ]),
        ("Users see stale data right after update—why?", [
            "Reads may target a replica lagging the primary or a cache without invalidation.",
            "Eventual consistency without read-your-writes causes this symptom.",
            "Fix with consistent read, primary read after write, or version checks.",
            "Document expected staleness in API contracts.",
        ]),
        ("Throttling on one DynamoDB partition key—mitigation?", [
            "Split logical key with suffix buckets and aggregate in application layer.",
            "Cache read-heavy configuration with short TTL.",
            "Move counters to sharded keys or a queue-based writer.",
            "Avoid monotonic keys on global counters without sharding.",
        ]),
        ("MongoDB collection passed 16 MB document limit—what now?", [
            "Split arrays into separate collections or bucket documents by time.",
            "Stop unbounded push into embedded arrays on every event.",
            "Use capped patterns or archive cold events to object storage.",
            "Add pagination APIs that do not require whole-document loads.",
        ]),
        ("Choosing Cassandra versus DynamoDB for a feed—how?", [
            "List read and write patterns, multi-region needs, and team experience.",
            "Cassandra offers tunable consistency and self-hosted control.",
            "DynamoDB offers managed scaling with strict partition discipline.",
            "Either fails with a celebrity hot partition without key design.",
        ]),
    ]
    f = [
        ("Link to `D10-T001` SQL vs NoSQL?", [
            "SQL keeps invariants; NoSQL optimizes keyed access paths.",
            "This topic is the detailed slice of that broader trade-off.",
            "Interviewers chain them in system design loops.",
            "Always state what remains in SQL.",
        ]),
        ("Link to `D07-T002` normalization?", [
            "Normalization reduces update anomalies in relational schemas.",
            "NoSQL denormalization trades update cost for read speed.",
            "Choose per field based on change frequency.",
            "Money fields often stay normalized.",
        ]),
        ("Link to observability?", [
            "Trace database calls with partition key tags where safe.",
            "Alert on throttle, scan, and lag metrics per store.",
            "SLO dashboards beat guessing after deploys.",
            "Correlate p99 with query plans, not only CPU.",
        ]),
    ]
    lines = ["## K. Interview Preparation", ""]
    for title, qs in [
        ("Beginner", b),
        ("Intermediate", i),
        ("Advanced", a),
        ("Scenarios", s),
        ("Follow-ups", f),
    ]:
        lines.append(f"### {title}")
        lines.append("")
        for n, (q, ans) in enumerate(qs, 1):
            lines.append(f"#### Q{n}. {q}")
            lines.append("")
            lines.append(f"**Answer:** {four(ans)}")
            lines.append("")
    return "\n".join(lines)


def mermaid_for(slug: str) -> str:
    if "graph" in slug:
        return "graph LR\n  user((User))--follows-->user2((User))\n  user--posted-->post((Post))"
    if "quorum" in slug or "replication" in slug:
        return "flowchart LR\n  c[Client]-->l[Leader]\n  l-->r1[Replica]\n  l-->r2[Replica]"
    if "partition" in slug or "hot" in slug:
        return "flowchart TD\n  w[Writes]-->p1[Hot partition]\n  w-->p2[Cold partition]\n  w-->p3[Cold partition]"
    return "flowchart LR\n  api[API]-->store[(NoSQL store)]\n  api-->sql[(SQL authority)]"


def build_note(tid: str, slug: str, title: str, subdomain: str, blurb: str) -> str:
    deps = {
        "D10-T003": ["D10-T002", "D10-T001", "D07-T001", "D07-T002"],
        "D10-T004": ["D10-T003", "D10-T001", "D07-T001", "D07-T002"],
        "D10-T005": ["D10-T004", "D10-T001", "D07-T001", "D07-T002"],
        "D10-T006": ["D10-T005", "D10-T001", "D07-T001", "D07-T002"],
        "D10-T007": ["D10-T006", "D10-T001", "D07-T001", "D07-T002"],
        "D10-T008": ["D10-T007", "D10-T001", "D07-T001", "D07-T002"],
        "D10-T009": ["D10-T008", "D10-T001", "D07-T001", "D07-T002"],
        "D10-T010": ["D10-T009", "D10-T001", "D07-T001", "D07-T002"],
        "D10-T011": ["D10-T010", "D10-T001", "D07-T001", "D07-T002"],
        "D10-T012": ["D10-T011", "D10-T001", "D07-T001", "D07-T002"],
        "D10-T013": ["D10-T012", "D10-T001", "D07-T001", "D07-T002"],
        "D10-T014": ["D10-T013", "D10-T001", "D07-T001", "D07-T002"],
        "D10-T015": ["D10-T014", "D10-T001", "D07-T001", "D07-T002"],
        "D10-T016": ["D10-T015", "D10-T001", "D07-T001", "D07-T002"],
        "D10-T017": ["D10-T016", "D10-T001", "D07-T001", "D07-T002"],
        "D10-T018": ["D10-T017", "D10-T001", "D07-T001", "D07-T002"],
        "D10-T019": ["D10-T018", "D10-T001", "D07-T001", "D07-T002"],
    }
    default_deps = ["D10-T001", "D07-T001", "D07-T002"]
    importance = {
        "D10-T007": "core",
        "D10-T008": "core",
        "D10-T015": "core",
        "D10-T016": "core",
    }.get(tid, "common")
    d = deps.get(tid, default_deps)
    dep_s = ", ".join(f"`{x}`" for x in d)
    k = k_block(title, blurb)
    return f"""# {tid} — {title}

Topic ID: `{tid}`
Domain: NoSQL Databases
Subdomain: {subdomain}
Importance: {importance}
Complexity: intermediate
Dependencies: {dep_s}
Execution status of the code in section F: illustrative

## A. Topic Overview

{blurb} Document databases (MongoDB), wide-column systems (Cassandra), key-value caches (Redis), and managed items (DynamoDB) all appear in backend interviews together with SQL authority for money and identity.

Production symptoms of misunderstanding this topic include throttled partitions, collection scans, unbounded embedded arrays, and stale reads after writes. Interviewers expect you to connect the concept to partition keys, quorums, and explicit access patterns.

Prerequisites: `D10-T001` and relational basics (`D07-T001`, `D07-T002`). Pair study with hands-on query plans in your chosen engine.

## B. First-Principles Explanation

Distributed storage must route each request to the correct shard, replicate for availability, and choose how many copies must agree before acknowledging IO. {blurb} The CAP trade space explains behavior during partitions: many NoSQL systems favor availability with tunable consistency.

Modeling starts from queries: primary keys, sort keys, indexes, and document shape exist to make those queries bounded work. Joins across arbitrary keys are intentionally expensive so the hot path stays predictable.

## C. Internal Working and Architecture

Clients send operations with a key or query predicate. The coordinator hashes partition keys, consults metadata for shard ownership, and forwards to replicas. Leaders accept writes; followers catch up asynchronously unless strong consistency is requested per operation.

Secondary indexes and aggregation pipelines are separate internal structures that must be maintained on each write. TTL subsystems schedule expiration compactions. Metrics expose per-partition load so operators detect hot keys.

## D. Diagrams and Visual Models

```mermaid
{mermaid_for(slug)}
```

Use the diagram as a talking point: identify the bottleneck shard and the authoritative store for invariants.

## E. Examples and Analogies

Analogy: designing highways before neighborhoods—you decide where traffic must flow, then place on-ramps (indexes) rather than paving every possible side street.

MongoDB example: `db.orders.find({{ userId: 1, status: "open" }}).sort({{ createdAt: -1 }}).limit(20)` requires a compound index on `(userId, status, createdAt)` or the planner scans.

DynamoDB example: `PK=USER#1`, `SK=ORDER#2025-10-12` groups a user's orders for range queries within one partition.

## F. Code Examples

```javascript
// MongoDB: indexed find (illustrative)
db.products.createIndex({{ sku: 1 }}, {{ unique: true }});
db.products.find({{ sku: "ABC-123" }}); // should use IXSCAN
```

```text
# DynamoDB item keys (illustrative)
PK = TENANT#t1#USER#u9
SK = PROFILE
attrs: displayName, email, version
```

Do not run against production. Validate with `explain()` or DynamoDB returned metrics in dev.

## G. Practical Backend Application

Wrap the store behind repositories that encode key naming, consistent reads for authz, and idempotent writes. Use outbox or CDC to keep SQL authoritative rows and NoSQL read models aligned.

For multi-tenant SaaS, include `tenantId` in every partition key. Cap document sizes and array lengths in validation middleware before writes reach the database.

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Document embed | One round trip reads | Fan-out updates | Read-heavy aggregates | Shared mutable child |
| Wide-column partition | Huge write throughput | Query rigidity | Feeds, metrics | Ad hoc analytics |
| GSI / secondary index | Alternate access path | Write amplification | Needed query shape | Many unused indexes |
| Strong consistency read | Fresh data | Higher latency | Balances, authz | Best-effort social likes |
| TTL expiry | Automatic cleanup | Delayed deletion | Sessions, logs | Immediate legal delete proof |

## I. Common Mistakes and Misconceptions

- Designing keys from nouns (`User`) instead of access patterns (`USER#id#ORDERS`).
- Ignoring hot partitions on global counters or default tenants.
- Treating eventual consistency as "broken" instead of specifying read guarantees.
- Building MongoDB aggregations without `$match` early or indexes supporting `$match`.
- Using DynamoDB scans in request path because the console made it easy in dev.

## J. Debugging and Troubleshooting

Symptoms: throttling, rising p99, stale UI, or replication lag alarms.

Diagnosis:

1. Capture the exact query and verify index or key condition usage.
2. Inspect per-partition metrics for heat skew.
3. Check replica lag and whether reads use secondaries.
4. Compare error spikes to deploys and new secondary indexes building.

Metrics: throttled requests, scan count, index build progress, conditional check failures.

{k}

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`.

### Exercise 1 — design

Write three access patterns for this topic's subdomain and propose keys or indexes for MongoDB and DynamoDB. Acceptance: no scan-heavy hot path.

### Exercise 2 — debugging

Given throttling on a single partition key, propose two mitigations and how to validate them in metrics. Acceptance: mention sharding or caching, not "scale up" alone.

### Exercise 3 — trade-off

Pick SQL versus this NoSQL feature for a workload described in section A and defend consistency choices. Acceptance: name authoritative store and stale-read UX.

## M. Revision Notes

- {blurb}
- Partition keys and indexes come from access patterns.
- Hot partitions and quorums appear together in incidents.
- MongoDB, DynamoDB, and Cassandra names signal modeling style, not magic scale.
- Keep money and identity invariants in SQL unless you implement sagas deliberately.

## N. Related Topics

Neighbors in domain 10: prior and next topic ids in the learning path. Cross-domain: `D07-T002`, `D08-T001`, `D11-T001`.

## O. Completion Criteria

- Whiteboard keys/indexes for three queries without scans.
- Explain one hot-partition incident and mitigation.
- Describe quorum or consistency choice for a payment-adjacent read.
- Compare embed versus reference for a shared entity.
- Answer scenario questions in section K without hand-waving.
"""


def interview_titles(title: str, blurb: str) -> list[str]:
    """23 question titles for interview bank (matches k_block order)."""
    base_b = [
        f"What is {title}?",
        "Why does this matter in production backends?",
        "What SQL concept is closest?",
        "What is a partition key?",
        "Name one MongoDB and one DynamoDB idea relevant here.",
    ]
    base_i = [
        "How do access patterns drive schema?",
        "How do quorums affect reads and writes?",
        "What is a hot partition?",
        "When embed versus reference in documents?",
        "How does eventual consistency surface to users?",
    ]
    base_a = [
        "How would you design for multi-region active-active?",
        "What is write amplification from secondary indexes?",
        "How do MongoDB transactions differ from Postgres?",
        "How do you model time-series in wide-column stores?",
        "When is a graph database justified?",
    ]
    base_s = [
        "p99 spikes after launch—what do you check first?",
        "Users see stale data right after update—why?",
        "Throttling on one DynamoDB partition key—mitigation?",
        "MongoDB collection passed document size limits—what now?",
        "Choosing Cassandra versus DynamoDB for a feed—how?",
    ]
    base_f = [
        "Link to `D10-T001` SQL vs NoSQL?",
        "Link to `D07-T002` normalization?",
        "Link to observability?",
    ]
    return base_b + base_i + base_a + base_s + base_f


def write_aux(tid: str, slug: str, title: str, blurb: str) -> None:
    (EX / f"{tid}.md").write_text(
        f"# Exercises — {tid}\n\nSolutions: [solutions/{tid}.md](solutions/{tid}.md).\n\n"
        f"1. Design keys/indexes for three access patterns ({title}).\n"
        f"2. Debug single-partition throttling.\n"
        f"3. Trade SQL vs NoSQL for a workload in section A.\n",
        encoding="utf-8",
    )
    (SOL / f"{tid}.md").write_text(
        f"# Solutions for {tid}\n\n"
        "## Exercise 1\n\nSee section K scenarios; sample keys: tenant-prefixed PK, compound Mongo index matching filter+sort.\n\n"
        "## Exercise 2\n\nSplit hot key with hash suffix buckets; validate via partition metrics and reduced throttle events.\n\n"
        "## Exercise 3\n\nKeep ledger SQL; use NoSQL for read models with versioned snapshots and defined staleness.\n",
        encoding="utf-8",
    )
    titles = interview_titles(title, blurb)
    levels = (
        ["Beginner"] * 5
        + ["Intermediate"] * 5
        + ["Advanced"] * 5
        + ["Scenario"] * 5
        + ["Follow-up"] * 3
    )
    qs = [f"{i + 1}. {levels[i]}. {titles[i]}" for i in range(23)]
    (IV / f"{tid}.md").write_text(
        f"# {tid} interview items\n\nTopic: {title}\n\n## Questions\n\n" + "\n".join(qs[:23])
        + f"\n\nAnswer key: [section K](../../09_NOSQL_DATABASES/notes/{slug}.md).\n",
        encoding="utf-8",
    )


HAND_AUTHORED_SLUGS = {
    "d10-t001-sql-vs-nosql-trade-offs",
    "d10-t002-key-value-stores",
    "d10-t003-document-databases",
    "d10-t011-partition-keys-and-hot-partitions",
}


def main() -> None:
    NOTES.mkdir(parents=True, exist_ok=True)
    for tid, slug, title, subdomain, blurb in SPECS:
        if slug not in HAND_AUTHORED_SLUGS:
            (NOTES / f"{slug}.md").write_text(
                build_note(tid, slug, title, subdomain, blurb), encoding="utf-8"
            )
        write_aux(tid, slug, title, blurb)
        print("wrote", tid)


if __name__ == "__main__":
    main()

"""D07-T001 .. D07-T008 topic bodies."""
from d07_common import bank_from_sections, bullets, mk_body

BODIES: dict = {}

_iv = {}  # placeholder to satisfy linter

# --- D07-T001 ---
_b1 = [
    (
        "What is a relational database?",
        "A relational database stores data in tables made of rows and columns with a declared schema. "
        "Relationships between entities are expressed with keys and enforced with constraints, not only in application code. "
        "Clients query with SQL or a query builder that compiles to SQL. "
        "The engine guarantees transactional semantics when you use explicit transactions.",
    ),
    (
        "What does non-relational mean in practice?",
        "Non-relational stores trade the uniform table model for models tuned to access patterns: documents, wide columns, key-value, or graphs. "
        "Many relax multi-row ACID guarantees or expose them only per partition or per document. "
        "Schema may be flexible or enforced at write time depending on the product. "
        "They are chosen when scale, latency, or shape of data fits the model better than normalized tables.",
    ),
    (
        "Name two differences between SQL and NoSQL marketing labels.",
        "SQL is a language; relational is a data model. "
        "Some NoSQL databases still offer SQL interfaces or strong consistency options. "
        "NoSQL originally meant not only SQL, not no SQL forever. "
        "Interview answers should name concrete trade-offs, not slogans.",
    ),
    (
        "Where does the application sit in the data path?",
        "The service opens connections, begins transactions, and issues reads and writes through a driver. "
        "The database enforces constraints, locks or MVCC rules, and durability to disk. "
        "Caches and search indexes are separate systems that must be kept consistent with policy. "
        "Choosing relational versus non-relational changes how you handle joins, migrations, and failure modes.",
    ),
    (
        "What is a single reason to keep using a relational database in 2026?",
        "Complex reporting, money movement, and multi-entity invariants still map cleanly to normalized tables plus SQL. "
        "Mature tooling for migrations, backups, and operational playbooks reduces risk. "
        "You can add read replicas and partitioning without abandoning the model. "
        "If your queries need ad hoc joins and aggregations, relational remains the default correct answer.",
    ),
]
_b2 = [
    (
        "How do you decide between PostgreSQL and MongoDB for a new product?",
        "List the dominant read and write paths and whether they need multi-row atomic updates. "
        "If orders, inventory, and payments must move together, a relational transaction is simpler than compensating sagas across documents. "
        "If the payload is a nested document read as a whole and rarely joined, a document store can reduce impedance mismatch. "
        "Prototype the hardest query on both and measure, including migration and backup cost, not only hello-world latency.",
    ),
    (
        "What is the impedance mismatch problem?",
        "Object-oriented application code wants graphs of objects; relational storage wants flat rows and foreign keys. "
        "ORMs map between them but can hide N+1 queries and surprise transactions. "
        "Document databases store JSON-like trees that match some APIs closely. "
        "The mismatch is managed with schema design, DTOs, and explicit query layers, not ignored.",
    ),
    (
        "Can a system use both relational and non-relational databases?",
        "Yes, polyglot persistence is common: PostgreSQL for ledger data, Redis for locks, Elasticsearch for search. "
        "Each store becomes a source of truth for what it owns; cross-store consistency needs outbox events or batch reconciliation. "
        "Operational complexity rises with every additional datastore. "
        "Add a second database only when the benefit is measured, not because a blog post recommended it.",
    ),
    (
        "How does schema flexibility differ?",
        "Relational schemas are declared with DDL and enforced on insert and update. "
        "Document stores may allow any shape per document but still need application validation for compatibility. "
        "Flexible schema speeds early development and slows queries that lack stable fields. "
        "Migrations in relational systems are explicit versioned scripts; in document systems they are often lazy backfills.",
    ),
    (
        "What question exposes a weak 'NoSQL for scale' answer?",
        "Ask what happens to a financial transfer that touches balance and audit tables. "
        "If the candidate cannot explain atomic commit or an alternative saga with idempotency, scale talk is hand waving. "
        "Scale has axes: read QPS, write QPS, data size, and operational headcount. "
        "Pick the store that fits the invariant, then scale that design with replicas, pooling, and query tuning.",
    ),
]
_b3 = [
    (
        "How does CAP apply to database choice?",
        "CAP describes partitions in distributed systems: when the network splits, you choose between strong consistency and availability for that window. "
        "Single-node PostgreSQL avoids partition trade-offs until you add replicas and failover. "
        "Many distributed NoSQL systems let you pick per-request consistency levels. "
        "Interviewers want you to connect CAP to replication lag and read-your-writes, not recite the acronym alone.",
    ),
    (
        "What is BASE as contrasted with ACID?",
        "BASE (basically available, soft state, eventual consistency) describes systems that accept temporary divergence for availability. "
        "ACID transactions keep invariants inside one database boundary. "
        "Eventual consistency can be correct if business rules tolerate lag and you have reconciliation. "
        "Payment ledgers usually stay ACID; view counters may be eventual.",
    ),
    (
        "When is a graph database the right relational alternative?",
        "When traversals along many relationships are the hot path and recursive SQL becomes painful. "
        "Social feeds, permission graphs, and fraud rings are classic examples. "
        "Graph stores optimize pointer chasing; they are weaker for bulk tabular reporting. "
        "You can model graphs in relational tables too; choose graph when traversal performance dominates.",
    ),
    (
        "What operational signals differ between stores?",
        "Relational ops focus on vacuum or autovacuum, bloat, connection counts, and replication lag. "
        "Document and wide-column ops add compaction, tombstones, and repair jobs. "
        "Backup formats and restore time targets differ by orders of magnitude. "
        "Runbooks must match the engine you picked, not a generic 'database' checklist.",
    ),
    (
        "How do you migrate from document to relational later?",
        "Extract stable entities into tables, keep JSON blobs only for truly schemaless attributes. "
        "Backfill with idempotent jobs and verify row counts and checksums per entity. "
        "Dual-write or CDC until cutover, then freeze writes to the old collection. "
        "The cost is why teams normalize early for core domains even if edges stay document-shaped.",
    ),
]
_b4 = [
    (
        "Marketing wants Mongo because 'JSON matches the API' but finance needs SQL reports. What do you propose?",
        "Keep money and reporting entities in PostgreSQL with strict types and migrations. "
        "Store marketing content or CMS blobs in a document DB if it truly reduces release friction. "
        "Expose a read model or materialized view for finance instead of querying the document store ad hoc. "
        "Document the system of record per entity so audits know which database to subpoena.",
    ),
    (
        "Latency on reads spiked after choosing Redis as the primary database. What went wrong?",
        "Redis is an in-memory data structure server, not a durable system of record for all entities. "
        "Persistence modes and eviction under memory pressure can lose or stall data. "
        "The fix is to put authoritative rows in PostgreSQL and use Redis for cache or ephemeral state. "
        "Measure hit ratio, memory limits, and RPO before trusting Redis for anything financial.",
    ),
    (
        "A startup copied a big-tech polyglot diagram. Incidents multiply. Why?",
        "Each database adds failure domains, backup jobs, security patches, and on-call expertise. "
        "Without staff to operate Cassandra, Elasticsearch, and Postgres, pages go unresolved. "
        "Start with one relational database until metrics prove a second store is required. "
        "Extract services and datastores after boundaries are clear, not before.",
    ),
    (
        "Team argues Dynamo-style always beats SQL. What benchmark do you run?",
        "Pick three production queries: a join report, a point read, and a write with a uniqueness constraint. "
        "Run them with realistic data size and concurrent writers on both candidates. "
        "Include failover drill time and cost of fixing a bad migration. "
        "Whichever wins on the metrics you actually SLO on gets the job.",
    ),
    (
        "Compliance requires row-level audit who changed what. Does NoSQL help?",
        "Relational audit tables with append-only rows and triggers or application-level audit are well understood. "
        "Some document stores offer change streams but cross-document transactions may be limited. "
        "Immutable event logs in Kafka plus relational projections are a common hybrid. "
        "Choose the design regulators can query with standard SQL during an audit.",
    ),
]
_b5 = [
    (
        "How does this connect to schema design in D07-T002?",
        "Once you pick relational storage, tables, types, and schemas become the contract between services and DBAs. "
        "NoSQL still needs logical schemas even if physical storage is flexible. "
        "The choice of store determines how painful migrations and joins will be later. "
        "Read D07-T002 before debating indexes on a store you have not modeled.",
    ),
    (
        "How does this connect to transactions in D07-T011?",
        "Relational databases expose multi-statement transactions as a first-class feature. "
        "Many non-relational systems scope atomicity to a single document or partition. "
        "Your store choice bounds how you implement transfers and inventory holds. "
        "If you need ACID across rows, start relational or accept distributed transaction complexity.",
    ),
    (
        "How does caching relate to picking SQL versus NoSQL?",
        "Caching is orthogonal: Redis does not replace a relational source of truth. "
        "Document stores are not a cache layer unless you explicitly treat them as ephemeral. "
        "Cache invalidation policy must reference the authoritative database. "
        "See domain 11 for Redis patterns after you know what is canonical in domain 7.",
    ),
]

_t001 = mk_body(
    overview=(
        "Relational databases organize data into tables with declared types and enforce relationships with keys and constraints. "
        "Non-relational databases optimize for alternative models and often for horizontal scale at the cost of narrower transactional guarantees. "
        "Backend engineers choose between them based on invariants, query shapes, team skills, and operational budget—not slogans. "
        "Interviews use this topic to see whether you can name trade-offs before jumping to microservices and sharding."
    ),
    first_principles=(
        "Persistent storage must survive process crashes. A database engine pages data to disk, replays logs, and exposes a concurrency model. "
        "Relational theory (Codd) adds structure: relations, tuples, and declarative queries. SQL is the mainstream language for that model. "
        "NoSQL families emerged when single-node SQL hit limits or when nested documents matched product shapes. "
        "The first-principles question is always: what must be true after a crash, under concurrency, and during a partition—and which engine proves those properties cheapest."
    ),
    internal=(
        "A relational engine parses SQL, plans joins and index scans, acquires locks or MVCC snapshots, and writes WAL records before acknowledging commit. "
        "A document engine stores BSON or JSON on disk with optional secondary indexes and replication per shard. "
        "Key-value engines hash keys to partitions; wide-column engines sort rows by partition key plus clustering columns. "
        "Your service sees a connection pool, sessions, and transactions; the difference is what the server can atomically combine in one commit."
    ),
    mermaid="""flowchart TD
  app[ApplicationService]
  decide{DominantAccessPattern}
  rdb[(RelationalPrimary)]
  doc[(DocumentStore)]
  cache[(CacheEphemeral)]
  app --> decide
  decide -->|multiRowInvariants| rdb
  decide -->|wholeDocumentReads| doc
  app --> cache
  cache -->|cacheMiss| rdb""",
    examples=(
        "Analogy: relational is a spreadsheet with strict column types and referential checks; document is a folder of JSON files with optional indexes. "
        "Neither analogy replaces knowing your queries. "
        "Backend example: user profiles as documents can work; wallet balances belong in rows with `numeric` and transactional updates. "
        "Do not store authoritative money in a cache. Do not run cross-shard joins without accepting latency."
    ),
    sql_title="compare models with the same entity",
    sql="""-- unexecuted
CREATE TABLE accounts (
  id         bigint PRIMARY KEY,
  owner_id   bigint NOT NULL,
  balance    numeric(18,2) NOT NULL CHECK (balance >= 0)
);

-- document store equivalent is one JSON blob per owner with embedded accounts array;
-- updating one account balance without touching siblings needs careful atomic operators.""",
    practical=(
        "Start new services on one relational database unless a written ADR documents a different store. "
        "Put connection strings in secrets; use pooling (`D07-T025`). "
        "Log slow queries and migration versions. "
        "When product asks for a second database, require a failing metric on the first and a rollback plan."
    ),
    tradeoffs=bullets(
        [
            "| Relational | ACID, joins, mature ops | migration rigidity | ledgers, ERP | giant opaque blobs only |",
        ]
    )
    + "\n\n"
    + "| Choice | Benefit | Cost | Choose when | Avoid when |\n| --- | --- | --- | --- | --- |\n"
    + "| Relational | ACID, SQL joins | vertical scale limits first | money, reporting | only unstructured media |\n"
    + "| Document | flexible nested shape | cross-doc transactions limited | CMS, catalogs | multi-row invariants |\n"
    + "| Key-value | O(1) lookups | no ad hoc queries | sessions, rate limits | complex analytics |\n"
    + "| Wide-column | huge write throughput | modeling learning curve | time series at scale | heavy ad hoc joins |",
    mistakes=bullets(
        [
            "Picking MongoDB because JSON 'matches the API' while finance needs SQL aggregates.",
            "Treating Redis as the system of record for balances.",
            "Assuming NoSQL means no schema—clients still need compatible fields.",
            "Ignoring backup and restore drills for the chosen engine.",
            "Sharding before normalization and query tuning on a single node.",
        ]
    ),
    debugging=bullets(
        [
            "Symptom: inconsistent reads across services—map each entity to its system of record.",
            "Symptom: ORM generates huge joins—check whether document shape would help or indexes are missing.",
            "Compare p95 latency with cache off to see if the database choice is the bottleneck.",
            "Review ADRs and runbooks: if only Postgres is documented, new stores are accidental.",
        ]
    ),
    beginner=_b1,
    intermediate=_b2,
    advanced=_b3,
    scenarios=_b4,
    followups=_b5,
    exercises="""### Exercise 1 — design

Pick a ride-hailing app: users, trips, payments. State which entities live in PostgreSQL versus a document store and why. Acceptance: at least one entity must use multi-row ACID justification.

### Exercise 2 — trade-off

Your team proposes Cassandra for a 500-row configuration table. Write a one-page argument for or against. Acceptance: mention operational cost and query pattern, not only throughput.

### Exercise 3 — migration

You inherit MongoDB for orders but need SQL reporting. Outline a dual-write cutover plan. Acceptance: idempotent backfill, verification metrics, and freeze window.""",
    exercise_items=[
        "Design relational vs document split for ride-hailing with ACID justification.",
        "Argue for or against Cassandra for a tiny configuration table.",
        "Outline Mongo-to-SQL reporting migration with dual-write.",
    ],
    solutions=[
        "Keep users, trips, payments, and payouts in PostgreSQL with foreign keys and transactions. "
        "Store marketing banners or unstructured driver notes as documents if needed. "
        "Trips updating payment status and driver availability need one transactional boundary.",
        "Reject Cassandra for 500 static rows: ops overhead and CQL modeling cost exceed benefit. "
        "PostgreSQL with a single table and cache is simpler; Cassandra wins on huge write-heavy time series, not config.",
        "Backfill orders into relational tables nightly with checksum counts; dual-write new orders to both; "
        "compare totals; freeze Mongo writes; switch readers to SQL views; decommission after retention window.",
    ],
    bank_questions=bank_from_sections(_b1, _b2, _b3, _b4, _b5),
    revision=bullets(
        [
            "Relational = tables + keys + SQL + multi-row transactions.",
            "NoSQL = model fit and scale trade-offs, not 'no rules'.",
            "Polyglot persistence needs explicit sources of truth.",
            "Benchmark real queries and ops cost, not slogans.",
        ]
    ),
    completion=bullets(
        [
            "Explain when relational storage is non-negotiable.",
            "Name two NoSQL families and a valid use case each.",
            "Describe polyglot persistence risks.",
            "Push back on store choice with metrics and invariants.",
        ]
    ),
)
BODIES["D07-T001"] = _t001

# Additional topics D07-T002 .. D07-T008 are appended in follow-up edits to keep generator modular.

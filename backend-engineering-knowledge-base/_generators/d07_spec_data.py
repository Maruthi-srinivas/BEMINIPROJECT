"""Topic-specific registrations for D07-T002 .. D07-T031."""
from __future__ import annotations

from d07_common import fact_block


def _facts(overrides: dict[int, str], base: list[str] | None = None) -> list[str]:
    b = (base or GENERIC)[:]
    for idx, sent in overrides.items():
        b[idx] = sent
    if len(b) != 92:
        raise ValueError(f"expected 92 facts, got {len(b)}")
    return b


GENERIC = fact_block(
    "Database topics affect every backend service that persists state.",
    "Correct mental models prevent data corruption under concurrency.",
    "Schema and transaction choices are hard to reverse without migrations.",
    "Interviewers probe whether you connect theory to on-call reality.",
    "Production debugging starts with identifying the system of record.",
    "Logs and metrics should name the database role: primary or replica.",
    "Slow queries often trace to missing indexes or bad join order.",
    "Connection storms look like database outages but are client misconfig.",
    "Teams forget that DDL can lock tables during careless migrations.",
    "Assuming default isolation is SERIALIZABLE causes surprise anomalies.",
    "Application retries must be idempotent when constraints fail.",
    "Caching without invalidation creates ghost reads for users.",
    "Backups are worthless without tested restore procedures.",
    "Replication is not sharding; conflating them breaks capacity plans.",
    "Incidents show up as 500s, timeouts, or silent wrong balances.",
    "Compare primary versus replica lag during read inconsistency tickets.",
    "EXPLAIN output tells you whether the planner chose a seq scan.",
    "Check max_connections and pool exhaustion before blaming CPU.",
    "Correlate deploy time with migration version and lock waits.",
    "Use statement timeouts to fail fast instead of wedging pools.",
    "Product wants features; you translate them into constraints and indexes.",
    "Teach stakeholders that data rules live in the database when possible.",
    "Show how a constraint prevents an entire class of bugs.",
    "Estimate migration downtime using row counts and lock models.",
    "Illustrative SQL in notes is unexecuted but should be valid dialect.",
    "Use parameterized queries in real services, not string concatenation.",
    "Foreign keys document relationships for the next engineer.",
    "CHECK constraints encode domain rules close to storage.",
    "Pools reuse TCP connections and amortize authentication.",
    "Pool size times pod count must stay below database max_connections.",
    "Long transactions hold connections and block pool recycling.",
    "Monitor hikaricp or pgBouncer wait metrics in production.",
    "Backward-incompatible DDL needs expand-contract deploy steps.",
    "Blocking migrations should run in maintenance windows or online tools.",
    "Feature flags do not rollback applied DDL automatically.",
    "Document forward-only migrations with compensating application logic.",
    "Success means p95 query latency within SLO after change.",
    "Deadlock rate should not spike after a concurrency change.",
    "Replication lag p99 within budget for stale-tolerant reads.",
    "Constraint violation rate should be near zero for happy paths.",
    "PostgreSQL uses MVCC; MySQL InnoDB does with different DDL behavior.",
    "Isolation semantics differ slightly; read the manual per engine.",
    "Never assume Oracle locking on Postgres without testing.",
    "Session-level settings can change isolation for one transaction.",
    "Asynchronous replicas apply WAL after commit on primary.",
    "Read-your-writes fails if you read a lagging replica too soon.",
    "Critical reads after a write should target the primary.",
    "Lag-aware routers help dashboards but not payment confirmation.",
    "MVCC keeps snapshot versions per transaction id or xmin xmax.",
    "UPDATE creates new row versions; old versions need vacuum.",
    "HOT updates avoid index churn when indexed columns unchanged.",
    "Serializable isolation uses SSI or predicate locks depending on engine.",
    "Network partitions can promote a replica while primary still writes.",
    "Split brain duplicates primary unless fencing stops old writer.",
    "Idempotent consumers heal duplicate messages after failover.",
    "Cross-shard transactions need two-phase commit or sagas.",
    "Spin up test database in CI and apply migration chain.",
    "Run EXPLAIN on golden queries when indexes change.",
    "Assert migration checksum and rollback script presence.",
    "Concurrency integration tests catch lost updates early.",
    "Load test with pool size matching production per instance.",
    "Inspect recent deploy, pool metrics, and slow query log.",
    "Capture pg_stat_activity for blocking queries.",
    "Roll back application if migration is forward-only broken.",
    "Reconcile financial totals against ledger constraints.",
    "Halt batch jobs that double-apply partial migrations.",
    "Compare row counts before and after backfill scripts.",
    "Restore from PITR if DDL corrupted constraints mid-flight.",
    "Put cluster in read-only, fix schema, replay missed writes.",
    "Keep runbook steps in the incident channel for audit.",
    "Explain risk of data loss if shortcuts ship without review.",
    "Offer phased rollout with measurable rollback triggers.",
    "Pair extra QA time with any isolation level change.",
    "Send post-write reads to primary until lag under threshold.",
    "Stamp session with last_write_lsn for replica routing if available.",
    "Invalidate caches on write path before acknowledging client.",
    "Page if replica lag exceeds minutes for user-facing reads.",
    "The next topic in domain seven builds on this foundation.",
    "API pagination should use indexed columns for stability.",
    "Map SQLSTATE or vendor codes to stable HTTP errors.",
    "Emit db.client.operation spans with sanitized statements.",
    "Dashboard pool usage, deadlocks, replication lag, and bloat.",
    "Shard keys should be chosen before volume makes resharding painful.",
    "Index-only scans may still hit the heap when the visibility map is stale.",
    "Prepared statements conflict with transaction-level pool modes.",
    "Logical dumps differ from physical backups in restore time and PITR.",
    "Autovacuum tuning must match update-heavy table churn.",
    "Partial indexes shrink size when queries always filter status.",
    "Covering indexes trade disk for fewer heap lookups on hot reads.",
    "SERIALIZABLE workloads need application retry on serialization failures.",
    "Retention documentation belongs in privacy policies and ops runbooks.",
    "Document expected query shapes beside every new index in code review.",
)


def register_specs(add) -> None:
    # D07-T002 Tables, rows, columns, schemas
    add(
        "D07-T002",
        "tables, rows, columns, and schemas",
        """flowchart TD
  catalog[DatabaseCatalog]
  schema[SchemaNamespace]
  table[TableDefinition]
  row[TableRow]
  catalog --> schema
  schema --> table
  table --> row""",
        """-- unexecuted
CREATE SCHEMA app;
CREATE TABLE app.users (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);""",
        "Tables hold rows; columns define typed attributes; schemas namespace objects inside a database catalog.",
        "Physical storage is pages and tuples; logical model is relations. DDL declares the contract applications rely on.",
        "System catalogs store metadata. The planner reads statistics on columns to estimate cardinality.",
        "A user row is a tuple; altering column type is a migration, not a runtime cast in SQL text.",
        "Version schemas with migrations. Never rely on implicit defaults across environments.",
        ["Confusing database with schema name.", "Using text for everything.", "No NOT NULL on required fields.", "Skipping comments on odd columns.", "Different DDL in staging and prod."],
        ["Verify \\d+ or information_schema matches code.", "Check search_path in Postgres.", "Compare migration history table.", "Inspect ORM-generated DDL vs actual."],
        ["Table = rows + columns.", "Schema namespaces objects.", "DDL is versioned.", "Types matter for money."],
        ["Draw catalog hierarchy.", "Write CREATE TABLE with types.", "Explain search_path.", "Find drift between envs."],
        ["Add migration for new nullable column with backfill plan.", "Document why timestamptz not timestamp.", "Find orphan tables without FKs."],
        ["Nullable column migration.", "timestamptz vs timestamp.", "Orphan table audit."],
        ["Use DEFAULT then backfill then SET NOT NULL.", "timestamptz stores UTC; timestamp without zone is ambiguous.", "List tables without FK to core entities."],
        _facts({24: "CREATE SCHEMA separates tenant or module tables from public.", 25: "IDENTITY columns replace serial for standard SQL."}),
    )

    # D07-T003 Primary and foreign keys
    add(
        "D07-T003",
        "primary and foreign keys",
        """flowchart LR
  parent[ParentTablePK]
  child[ChildTableFK]
  parent -->|ON_DELETE_rule| child""",
        """-- unexecuted
CREATE TABLE orders (
  id bigint PRIMARY KEY,
  customer_id bigint NOT NULL REFERENCES customers(id) ON DELETE RESTRICT
);""",
        "Primary keys uniquely identify rows; foreign keys enforce referential integrity between tables.",
        "Keys are constraints backed by indexes. The engine rejects orphan child rows on insert.",
        "FK checks run on child insert/update and parent delete/update depending on rules.",
        "Order lines reference orders; deleting an order may CASCADE or RESTRICT per policy.",
        "Choose ON DELETE RESTRICT for money links; CASCADE only for pure ownership trees.",
        ["FK missing on obvious relations.", "Random UUID without index.", "Deleting parents with RESTRICT surprise.", "Natural keys that change.", "Composite PK without ORM support."],
        ["Read FK violation SQLSTATE.", "Check missing index on FK column.", "Trace orphan rows with LEFT JOIN null.", "Review ON DELETE rules."],
        ["PK uniqueness.", "FK referential integrity.", "ON DELETE behaviors.", "Index FK columns."],
        ["Explain RESTRICT vs CASCADE.", "Write FK migration.", "Find orphans.", "Pick PK type."],
        ["Add FK with validation on existing data.", "Choose ON DELETE for comments.", "Benchmark FK index on child."],
        ["Add FK safely.", "ON DELETE policy.", "FK index benchmark."],
        ["Validate rows, CREATE INDEX CONCURRENTLY, then ADD CONSTRAINT.", "RESTRICT for shared parents; CASCADE for owned children.", "Child FK column must be indexed for joins."],
        _facts({0: "A primary key uniquely identifies each row in a table.", 1: "Foreign keys require matching parent key values.", 2: "Referential integrity is enforced at commit time.", 3: "ON DELETE CASCADE removes children when parent deleted."}),
    )

    # D07-T004 Candidate, composite, surrogate keys
    add(
        "D07-T004",
        "candidate, composite, and surrogate keys",
        """flowchart TD
  natural[NaturalCandidateKey]
  surrogate[SurrogateSurrogateKey]
  composite[CompositeKey]
  natural -->|may_change| surrogate
  composite -->|multiColumn| table[Table]""",
        """-- unexecuted
CREATE TABLE order_items (
  order_id bigint NOT NULL,
  line_no int NOT NULL,
  sku text NOT NULL,
  PRIMARY KEY (order_id, line_no)
);""",
        "Candidate keys are minimal sets of columns that uniquely identify a row. Surrogate keys are system-generated ids.",
        "Composite keys combine columns when no single column is unique. Surrogates stabilize references when natural keys change.",
        "Uniqueness constraints and PK indexes implement key choice. ORMs prefer single-column surrogates.",
        "Email as natural key breaks when users change email; surrogate user id stays stable.",
        "Use composite PK for junction tables; surrogate bigint for most entity roots.",
        ["Using email as PK.", "UUID without generation strategy.", "Composite PK in APIs.", "Duplicate candidates.", "Snowflake in JS number field."],
        ["Find duplicate natural keys before UNIQUE.", "Check index width on composite.", "API exposes stable id.", "Migration rekeys with mapping table."],
        ["Candidate = unique minimal.", "Surrogate = opaque id.", "Composite = multi-column.", "Stability matters."],
        ["Compare natural vs surrogate.", "Design junction PK.", "Plan email change.", "Explain wide composite index cost."],
        ["Migrate email PK to surrogate.", "Design M:N junction keys.", "Document id generation."],
        ["Email PK migration.", "M:N junction.", "Id generation doc."],
        ["Add id column, backfill, dual-write FKs, drop email PK.", "Junction uses (a_id,b_id) PK.", "Use bigint or UUID v7; JSON ids as strings."],
        _facts({0: "A candidate key is any minimal unique identifier for a row.", 1: "A primary key is the chosen candidate key.", 2: "Composite keys use multiple columns together.", 3: "Surrogate keys are meaningless outside the database."}),
    )

    # D07-T005 Constraints and data integrity
    add(
        "D07-T005",
        "constraints and data integrity",
        """flowchart TD
  app[Application]
  db[(DatabaseConstraints)]
  app -->|INSERT| db
  db -->|violation| reject[RejectOrRollback]""",
        """-- unexecuted
ALTER TABLE accounts
  ADD CONSTRAINT balance_non_negative CHECK (balance >= 0),
  ADD CONSTRAINT email_lowercase CHECK (email = lower(email));""",
        "Constraints encode invariants in the database: NOT NULL, UNIQUE, CHECK, FK, and exclusion constraints.",
        "Integrity at the database survives buggy clients and ad hoc SQL. Application checks are not enough alone.",
        "Constraint checks run per row or per statement depending on type. DEFERRABLE constraints wait until commit.",
        "Non-negative balance CHECK stops negative withdrawals even if service math bugs.",
        "Prefer constraints over triggers when declarative rules suffice.",
        ["Validation only in API.", "CHECK that duplicates app logic wrongly.", "Overly strict CHECK blocking legit data.", "Missing NOT NULL.", "Unnamed constraints hard to migrate."],
        ["Map SQLSTATE 23514 to 400.", "Name constraints for migrations.", "Find violations with NOT VALID then VALIDATE.", "Compare app vs DB rules."],
        ["NOT NULL, UNIQUE, CHECK, FK.", "DB is last line of defense.", "Name constraints.", "DEFERRABLE rare but useful."],
        ["Add CHECK safely.", "Explain DEFERRABLE.", "Map errors to HTTP.", "Find duplicate rules."],
        ["Add CHECK NOT VALID on big table.", "Design UNIQUE partial index.", "Remove duplicate app validation."],
        ["CHECK NOT VALID.", "Partial UNIQUE.", "Dedupe validation."],
        ["ADD CONSTRAINT ... NOT VALID; VALIDATE later.", "UNIQUE WHERE deleted_at IS NULL for soft delete.", "Keep canonical rule in DB."],
        _facts({0: "NOT NULL rejects missing required values.", 1: "UNIQUE prevents duplicate combinations.", 2: "CHECK enforces boolean predicates per row.", 3: "Foreign keys tie child values to parents."}),
    )

    # D07-T006 Normalization
    f_norm = _facts(
        {
            0: "First normal form requires atomic column values without repeating groups.",
            1: "Second normal form removes partial dependencies on part of a composite key.",
            2: "Third normal form removes transitive dependencies on non-key attributes.",
            3: "BCNF requires every determinant to be a candidate key.",
            4: "Normalization reduces update anomalies and duplicate facts.",
            5: "Denormalization is a later deliberate trade for read performance.",
            6: "Interviewers want examples of anomalies, not only definitions.",
            7: "OLTP schemas are usually at least 3NF for core entities.",
            24: "Split phone_list column into phone_numbers table for 1NF.",
            25: "Move city_from_zip out of orders if zip determines city (3NF).",
            48: "MVCC does not remove need for normalized write paths.",
            60: "Reports wrong city when zip table stale—check 3NF decomposition.",
        }
    )
    add(
        "D07-T006",
        "normalization through BCNF",
        """flowchart TD
  unnormalized[RepeatingGroups]
  oneNF[FirstNF]
  twoNF[SecondNF]
  threeNF[ThirdNF]
  unnormalized --> oneNF --> twoNF --> threeNF""",
        """-- unexecuted
-- Violation: orders(customer_id, product_a, product_b) repeating products
CREATE TABLE order_lines (
  order_id bigint NOT NULL,
  line_no int NOT NULL,
  product_id bigint NOT NULL,
  qty int NOT NULL CHECK (qty > 0),
  PRIMARY KEY (order_id, line_no)
);""",
        "Normalization decomposes tables to eliminate redundancy and update anomalies through 1NF, 2NF, 3NF, and BCNF.",
        "Functional dependencies drive decomposition. Each normal form fixes a specific anomaly class.",
        "FDs are declared or discovered from keys. Decomposition must be lossless and dependency-preserving when possible.",
        "Storing city only by zip in orders creates transitive dependency on zip if zip determines city.",
        "Normalize write paths first; denormalize reads with measured need (`D07-T007`).",
        ["Skipping 1NF with JSON arrays in columns.", "3NF confusion with star schema.", "Over-normalizing read-heavy dashboards.", "BCNF overkill for tiny tables.", "No FK after split."],
        ["Find update anomalies in prod data.", "Check redundant city columns.", "Verify join reconstructs facts.", "Document FDs in ADR."],
        ["1NF atomic.", "2NF no partial FD.", "3NF no transitive FD.", "BCNF all determinants are keys."],
        ["Fix 1NF violation.", "Explain transitive FD.", "When BCNF differs from 3NF.", "Lossless join test."],
        ["Decompose orders with repeating products.", "Identify 3NF violation in sample schema.", "Argue when star schema is OK."],
        ["Decompose repeating products.", "Find 3NF violation.", "Star schema trade-off."],
        ["Create order_lines with PK (order_id,line_no).", "Extract zip->city to zips table.", "Star schema for warehouse, not OLTP writes."],
        f_norm,
    )

    # D07-T007 Denormalization
    add(
        "D07-T007",
        "denormalization",
        """flowchart LR
  norm[NormalizedWrites]
  denorm[DenormalizedReadModel]
  norm -->|ETL_or_trigger| denorm""",
        """-- unexecuted
ALTER TABLE orders ADD COLUMN customer_name text;
-- maintained by trigger or application on customer update""",
        "Denormalization duplicates data to speed reads or simplify queries at the cost of update complexity.",
        "It trades write simplicity for read performance after normalization removed redundancy.",
        "Materialized views, summary columns, and read models are common forms.",
        "Caching order customer_name avoids join on hot read if updates are rare.",
        "Measure join cost before denormalizing; keep source of truth normalized.",
        ["Denormalize without update path.", "Two truths diverge.", "Trigger storms on bulk update.", "Premature denorm.", "No refresh for matview."],
        ["Compare join EXPLAIN before/after.", "Reconcile denorm column drift.", "Refresh materialized view job.", "Audit trigger latency."],
        ["Denorm = controlled redundancy.", "Source of truth stays normalized.", "Refresh strategy required.", "Measure first."],
        ["Design summary column updates.", "Use matview CONCURRENTLY.", "When not to denorm.", "Detect drift."],
        ["Add customer_name to orders safely.", "Refresh strategy for dashboard matview.", "Rollback denorm experiment."],
        ["customer_name denorm.", "Matview refresh.", "Rollback denorm."],
        ["Backfill, trigger on customer update, monitor drift job.", "CONCURRENTLY refresh on schedule.", "Drop column if join p95 fine after index."],
        _facts({0: "Denormalization copies data that could be joined instead.", 1: "It speeds reads when joins are hot and writes are cold.", 2: "Updates must touch all copies or async reconcile.", 3: "Eventual consistency is acceptable only if product agrees."}),
    )

    # D07-T008 Relationships
    add(
        "D07-T008",
        "one-to-one, one-to-many, and many-to-many relationships",
        """flowchart TD
  oneToOne[OneToOne]
  oneToMany[OneToMany]
  manyToMany[ManyToMany]
  manyToMany --> junction[JunctionTable]""",
        """-- unexecuted
CREATE TABLE user_profiles (
  user_id bigint PRIMARY KEY REFERENCES users(id),
  bio text
);
CREATE TABLE tag_map (
  post_id bigint REFERENCES posts(id),
  tag_id bigint REFERENCES tags(id),
  PRIMARY KEY (post_id, tag_id)
);""",
        "Cardinality shapes keys and junction tables: 1:1 shares PK or unique FK, 1:N uses FK on many side, M:N uses junction.",
        "Relationships are constraints plus access patterns. ORM annotations must match DDL.",
        "1:1 optional profile uses user_id PK/FK. M:N needs composite PK on junction.",
        "Posts to tags use tag_map; never encode multiple tag ids in one column.",
        "Draw ER diagram before migrations; name junction tables clearly.",
        ["M:N without junction.", "FK on wrong side.", "1:1 with separate ids unlinked.", "Cascade deletes on M:N hub.", "Nullable FK when required."],
        ["LEFT JOIN finds missing profiles.", "Count junction duplicates.", "Check FK direction.", "ORM join table name."],
        ["1:1 PK/FK.", "1:N FK on many.", "M:N junction.", "Cardinality drives DDL."],
        ["Model M:N.", "Optional 1:1.", "ON DELETE on junction.", "Query both directions."],
        ["Add tag_map migration.", "Refactor broken M:N array column.", "Document cardinality ADR."],
        ["tag_map migration.", "Fix array M:N.", "Cardinality ADR."],
        ["Create junction with composite PK.", "Migrate array to junction with backfill.", "ADR lists cardinalities per entity."],
        _facts({0: "One-to-many places the foreign key on the many side.", 1: "One-to-one often shares primary key with parent.", 2: "Many-to-many requires a junction table with two foreign keys.", 3: "Cardinality affects delete rules and index design."}),
    )

    # D07-T009 Joins and subqueries
    add(
        "D07-T009",
        "joins and subqueries",
        """flowchart LR
  a[TableA]
  b[TableB]
  a -->|INNER_JOIN| b
  a -->|LEFT_JOIN| b""",
        """-- unexecuted
SELECT o.id, c.email
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.created_at >= now() - interval '7 days';

SELECT id FROM orders WHERE customer_id IN (
  SELECT id FROM customers WHERE country = 'IN'
);""",
        "Joins combine rows from related tables; subqueries nest SELECT for filtering, projection, or existence tests.",
        "Join algorithms: nested loop, hash join, merge join. Indexes on join keys matter.",
        "INNER JOIN keeps matches; LEFT JOIN preserves left rows with NULLs for missing right.",
        "Correlated subqueries can be rewritten to joins for planner flexibility.",
        "Prefer explicit JOIN syntax; filter early with WHERE on indexed columns.",
        ["Implicit join in WHERE only.", "Cartesian product bug.", "Correlated subquery per row.", "SELECT * in hot path.", "Join on non-indexed text."],
        ["EXPLAIN nested loop vs hash.", "Check row estimate errors.", "Rewrite IN subquery to JOIN.", "Find missing FK index."],
        ["INNER vs OUTER.", "Join on FK indexed.", "Subquery vs JOIN.", "Predicate pushdown."],
        ["Write LEFT JOIN report.", "Rewrite correlated subquery.", "Explain cartesian product.", "Pick semi-join."],
        ["Optimize slow join report.", "Convert IN to EXISTS.", "Add covering index for join."],
        ["Join report tune.", "IN to EXISTS.", "Covering join index."],
        ["Index customer_id and created_at.", "EXISTS stops at first match.", "Include email in index only if covering justified."],
        _facts({0: "INNER JOIN returns rows with matches in both tables.", 1: "LEFT OUTER JOIN keeps all left rows.", 2: "Subqueries can appear in FROM, WHERE, and SELECT.", 3: "Correlated subqueries reference outer rows per iteration."}),
    )

    # D07-T010 Aggregations
    add(
        "D07-T010",
        "aggregations and grouping",
        """flowchart TD
  rows[RowSet]
  group[GROUP_BY]
  agg[AggregateFuncs]
  rows --> group --> agg""",
        """-- unexecuted
SELECT customer_id, COUNT(*) AS order_count, SUM(total_cents) AS revenue
FROM orders
WHERE status = 'paid'
GROUP BY customer_id
HAVING SUM(total_cents) > 10000;""",
        "Aggregations collapse many rows via COUNT, SUM, AVG, MIN, MAX; GROUP BY defines buckets; HAVING filters groups.",
        "Aggregates compute after WHERE filters rows. HAVING filters after grouping.",
        "Planner may use index-only scans or hash aggregate. Statistics affect group cardinality estimates.",
        "Revenue per customer uses GROUP BY customer_id; HAVING removes small totals.",
        "Use FILTER clause or conditional aggregates instead of multiple queries when possible.",
        ["HAVING where WHERE belongs.", "Non-aggregated column missing from GROUP BY.", "NULL in SUM.", "Distinct inside aggregate confusion.", "Huge GROUP BY without index."],
        ["Check GROUP BY list.", "Compare estimate vs actual rows.", "Use EXPLAIN ANALYZE on aggregate.", "Watch sort vs hash aggregate."],
        ["WHERE before GROUP BY.", "HAVING after.", "NULL ignored by COUNT(col).", "Index group key if huge."],
        ["Fix invalid GROUP BY.", "Explain FILTER.", "When ROLLUP needed.", "Distinct aggregate cost."],
        ["Write HAVING report.", "Add partial index for status filter.", "Compare COUNT(*) vs COUNT(col)."],
        ["HAVING report.", "Partial index.", "COUNT variants."],
        ["HAVING filters groups after aggregation.", "Index (status, customer_id) if selective.", "COUNT(*) counts rows; COUNT(col) ignores nulls."],
        _facts({0: "GROUP BY creates one output row per distinct group key.", 1: "HAVING filters groups after aggregation.", 2: "WHERE filters rows before aggregation.", 3: "NULL values are ignored by COUNT(column) but not COUNT(*)."}),
    )

    # D07-T011 Transactions
    add(
        "D07-T011",
        "transactions",
        """flowchart TD
  begin[BEGIN]
  work[Statements]
  commit[COMMIT]
  rollback[ROLLBACK]
  begin --> work
  work -->|success| commit
  work -->|error| rollback""",
        """-- unexecuted
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;""",
        "A transaction groups statements into one atomic unit that commits or rolls back entirely.",
        "BEGIN starts a transaction boundary; COMMIT makes changes durable; ROLLBACK undoes work.",
        "Savepoints nest partial rollback. Drivers map autocommit versus explicit transactions.",
        "Transfer moves money between accounts in one transaction or neither side updates.",
        "Keep transactions short; hold locks only while necessary.",
        ["Long transactions.", "Autocommit surprise in ORM.", "Nested transaction confusion.", "Side effects outside TX.", "Commit after external API."],
        ["pg_stat_activity xact_start.", "Find idle in transaction.", "Set statement_timeout.", "Log rollback reason."],
        ["BEGIN/COMMIT/ROLLBACK.", "Short transactions.", "Savepoints rare.", "One business action per TX."],
        ["Implement transfer TX.", "Explain autocommit.", "When savepoint.", "Idle in transaction fix."],
        ["Wrap transfer in TX with constraints.", "Add statement_timeout.", "Test rollback on violation."],
        ["Transfer transaction.", "statement_timeout.", "Rollback test."],
        ["Use single TX; CHECK prevents negative balance.", "ALTER DATABASE ... statement_timeout.", "Expect rollback on FK violation."],
        _facts({0: "Transactions begin with BEGIN or an implicit session.", 1: "COMMIT makes all changes durable together.", 2: "ROLLBACK undoes work since BEGIN.", 3: "Atomicity means all or nothing for the unit."}),
    )

    # D07-T012 ACID
    f_acid = _facts(
        {
            0: "Atomicity means a transaction's changes all commit or all roll back.",
            1: "Consistency means constraints hold before and after each transaction.",
            2: "Isolation means concurrent transactions do not observe each other's partial work.",
            3: "Durability means committed data survives crashes after WAL fsync.",
            4: "ACID is a bundle; weakening one letter changes application assumptions.",
            5: "Consistency in ACID is about constraints, not CAP consistency.",
            6: "Interviewers contrast ACID OLTP with BASE eventually consistent stores.",
            7: "Durability depends on synchronous_commit and replication settings.",
        }
    )
    add(
        "D07-T012",
        "ACID properties",
        """flowchart TD
  A[Atomicity]
  C[Consistency]
  I[Isolation]
  D[Durability]
  A --> C --> I --> D""",
        """-- unexecuted
-- Atomicity + consistency example
BEGIN;
INSERT INTO orders (id, total_cents) VALUES (1, 5000);
INSERT INTO order_lines (order_id, line_no, amount_cents) VALUES (1, 1, 5000);
COMMIT;""",
        "ACID: Atomicity, Consistency, Isolation, Durability—properties of transactional database processing.",
        "Atomicity is undo on failure; consistency is valid state per constraints; isolation is concurrency control; durability is log replay.",
        "WAL provides durability; lock/MVCC provides isolation; constraint checks provide consistency.",
        "Order header and lines commit together—atomicity. Negative balance rejected—consistency.",
        "Tune isolation and synchronous_commit knowing which ACID letter you relax.",
        ["Confusing CAP C with ACID C.", "Assuming cross-db ACID.", "No constraints then claiming C.", "async commit for money.", "Long TX breaking I."],
        ["Check synchronous_commit.", "Find partial commits across services.", "Verify constraints exist.", "Measure commit latency."],
        ["Four letters defined.", "C is constraints.", "Durability = WAL.", "Not same as CAP."],
        ["Explain each letter with example.", "When async commit OK.", "Cross-service atomicity limits.", "Map to Postgres settings."],
        ["Document ACID boundaries for payment service.", "Choose sync commit policy.", "Add missing constraints."],
        ["Payment ACID boundary.", "sync commit policy.", "Add constraints."],
        ["Single DB TX for ledger; sagas across services.", "synchronous_commit on for money.", "ADD CONSTRAINT for balances."],
        f_acid,
    )

    # D07-T013 Isolation levels
    f_iso = _facts(
        {
            0: "READ UNCOMMITTED allows dirty reads in theory; Postgres treats it as READ COMMITTED.",
            1: "READ COMMITTED sees only committed data per statement snapshot.",
            2: "REPEATABLE READ keeps one snapshot for the whole transaction.",
            3: "SERIALIZABLE prevents serializable anomalies using SSI or locking.",
            4: "Higher isolation reduces anomalies but increases retries and blocking.",
            5: "Default in Postgres is READ COMMITTED; in MySQL InnoDB REPEATABLE READ.",
            6: "Set isolation per transaction when needed, not globally without review.",
            7: "Anomalies map to isolation level: dirty, non-repeatable, phantom.",
        }
    )
    add(
        "D07-T013",
        "SQL isolation levels",
        """flowchart TD
  ru[ReadUncommitted]
  rc[ReadCommitted]
  rr[RepeatableRead]
  ser[Serializable]
  ru --> rc --> rr --> ser""",
        """-- unexecuted
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT balance FROM accounts WHERE id = 1;
-- same balance if re-selected in this transaction
COMMIT;""",
        "Isolation levels define which concurrency anomalies a transaction may see.",
        "ANSI levels form a ladder of stricter behavior. Engines implement with locks or MVCC snapshots.",
        "Postgres uses snapshots; RR prevents non-repeatable reads; serializable adds predicate checks.",
        "Inventory hold may need REPEATABLE READ or SERIALIZABLE to avoid double sell.",
        "Pick lowest isolation that preserves invariants; test under concurrency.",
        ["Always SERIALIZABLE for speed myth.", "Ignoring default per engine.", "Phantom under RR in some engines.", "No retry on serialization_failure.", "Long RR holding versions."],
        ["Log isolation level per TX.", "Watch serialization_failure rate.", "Compare statement vs transaction snapshot.", "Load test concurrent updates."],
        ["Four ANSI levels.", "Postgres RC default.", "RR snapshot.", "Serializable strongest."],
        ["Pick level for inventory.", "Explain RR vs RC.", "Handle 40001 retry.", "Engine differences."],
        ["Set isolation for stock decrement.", "Add retry on serialization failure.", "Document default per service."],
        ["Stock decrement isolation.", "Retry policy.", "Document defaults."],
        ["Use SELECT ... FOR UPDATE or SERIALIZABLE.", "Exponential backoff on SQLSTATE 40001.", "README lists BEGIN ISOLATION per use case."],
        f_iso,
    )

    # D07-T014 Anomalies
    f_anom = _facts(
        {
            0: "A dirty read sees uncommitted changes from another transaction.",
            1: "A non-repeatable read sees different values when reading the same row twice.",
            2: "A phantom read sees new rows matching a predicate on a re-scan.",
            3: "Lost update occurs when two writers overwrite without proper isolation or locking.",
            4: "READ COMMITTED prevents dirty reads in Postgres.",
            5: "REPEATABLE READ prevents non-repeatable reads in Postgres.",
            6: "SERIALIZABLE or careful locking prevents phantoms for critical predicates.",
            7: "Optimistic schemes detect lost updates with version columns.",
        }
    )
    add(
        "D07-T014",
        "dirty, non-repeatable, and phantom reads",
        """flowchart TD
  dirty[DirtyRead]
  nrr[NonRepeatableRead]
  phantom[PhantomRead]
  dirty -->|prevented_by| rc[ReadCommitted]
  nrr -->|prevented_by| rr[RepeatableRead]
  phantom -->|prevented_by| ser[Serializable]""",
        """-- unexecuted
-- Session A
BEGIN; UPDATE accounts SET balance = balance - 50 WHERE id = 1; -- not committed
-- Session B (READ COMMITTED) should not see -50 until commit""",
        "Dirty, non-repeatable, and phantom reads are isolation anomalies defined by ANSI SQL concurrency.",
        "They describe what concurrent schedules allow. MVCC and locks map levels to prevented anomalies.",
        "Dirty read is uncommitted data. Non-repeatable is two reads, different committed value. Phantom is new rows in range.",
        "Double booking can be phantom if second transaction inserts overlapping reservation.",
        "Match anomaly to business risk; choose isolation or explicit locks.",
        ["Calling all races dirty reads.", "Thinking RR stops all phantoms everywhere.", "No version column on optimistic path.", "SELECT FOR UPDATE forgotten.", "Read replica for just-written row."],
        ["Reproduce with two sessions.", "Check isolation setting.", "Use version column mismatch.", "Route critical read to primary."],
        ["Three anomaly definitions.", "Map to isolation.", "Lost update related.", "Postgres specifics."],
        ["Demonstrate phantom.", "Fix lost update.", "Explain dirty read.", "Replica stale vs anomaly."],
        ["Script two-session anomaly demo.", "Add version optimistic lock.", "Document read-after-write."],
        ["Two-session demo.", "Optimistic version.", "Read-after-write."],
        ["Use repeatable read or serializable in test.", "UPDATE ... WHERE version = :v.", "Primary read after POST."],
        f_anom,
    )

    # D07-T015 Locks and deadlocks
    add(
        "D07-T015",
        "locks and deadlocks",
        """flowchart TD
  t1[Txn1LockRowA]
  t2[Txn2LockRowB]
  t1 -->|waits_B| t2
  t2 -->|waits_A| deadlock[Deadlock]""",
        """-- unexecuted
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
-- holds row lock until commit
COMMIT;""",
        "Locks serialize access to rows, pages, or tables. Deadlocks are cyclic wait graphs detected by the engine.",
        "Row-level locks accompany UPDATE/DELETE/SELECT FOR UPDATE. Deadlock detector aborts one transaction.",
        "Lock modes: shared vs exclusive. Predicate locks appear in serializable isolation.",
        "Use consistent lock ordering to avoid deadlocks. Keep lock duration minimal.",
        "Log deadlock graphs; retry aborted transactions with backoff.",
        ["Table lock from DDL.", "FOR UPDATE everywhere.", "Deadlock as 500 without retry.", "Lock order random.", "Advisory locks forgotten."],
        ["pg_locks view.", "deadlock_timeout logs.", "Retry SQLSTATE 40P01.", "Find missing index causing table lock."],
        ["Row locks.", "Deadlock cycle.", "FOR UPDATE.", "Consistent ordering."],
        ["Explain deadlock log.", "Design lock order.", "Retry policy.", "DDL lock impact."],
        ["Fix deadlock in transfer code.", "Add retry middleware.", "Reduce lock scope."],
        ["Fix transfer deadlock.", "Retry middleware.", "Shrink locks."],
        ["Lock accounts in id order.", "Retry on 40P01.", "Shorten transaction."],
        _facts({0: "Locks prevent incompatible concurrent access to resources.", 1: "Deadlocks form when transactions wait on each other in a cycle.", 2: "The database chooses a victim transaction to abort.", 3: "SELECT FOR UPDATE takes row-level exclusive locks."}),
    )

    # D07-T016 Optimistic vs pessimistic
    add(
        "D07-T016",
        "optimistic versus pessimistic concurrency control",
        """flowchart TD
  pessimistic[SELECT_FOR_UPDATE]
  optimistic[VersionColumnCheck]
  pessimistic -->|blocks| writers
  optimistic -->|retries| writers""",
        """-- unexecuted
-- optimistic
UPDATE products SET stock = stock - 1, version = version + 1
WHERE id = 10 AND version = :expected_version;
-- if rowcount 0, someone else won""",
        "Pessimistic control locks rows before update; optimistic control checks at commit time with versions or timestamps.",
        "Pessimistic prevents conflicts early; optimistic assumes conflicts are rare and retries.",
        "FOR UPDATE is pessimistic. Version column with rowcount check is optimistic.",
        "High contention inventory uses pessimistic row locks; low contention profiles use optimistic.",
        "Expose conflict as 409 to clients for optimistic retries.",
        ["Optimistic without retry.", "Pessimistic on whole table.", "Lost update with neither.", "Version not incremented.", "Long FOR UPDATE."],
        ["Rowcount zero on update.", "Lock waits in pg_stat.", "409 rate spike.", "Compare conflict rate."],
        ["Lock early vs check late.", "Version column.", "409 conflict.", "Contention drives choice."],
        ["Pick strategy for seats.", "Implement version update.", "When pessimistic required.", "Test concurrent cart."],
        ["Add version to entity.", "Benchmark FOR UPDATE vs optimistic.", "Client retry contract."],
        ["Version column.", "Benchmark strategies.", "Retry contract."],
        ["ALTER ADD version int default 0.", "Load test 100 concurrent decrements.", "Document If-Match style headers."],
        _facts({0: "Pessimistic concurrency locks resources before modifying them.", 1: "Optimistic concurrency assumes conflicts are rare and validates at write time.", 2: "Version columns enable compare-and-swap style updates.", 3: "High contention favors pessimistic row locks."}),
    )

    # D07-T017 MVCC
    f_mvcc = _facts(
        {
            0: "Multi-Version Concurrency Control keeps multiple row versions for concurrent readers and writers.",
            1: "Readers take snapshots without blocking writers in typical MVCC engines.",
            2: "UPDATE creates a new row version and marks the old dead until vacuum.",
            3: "Transaction ids or timestamps decide which versions are visible.",
            4: "Vacuum reclaims dead tuples and prevents transaction id wraparound.",
            5: "Long transactions block vacuum and cause bloat.",
            6: "MVCC implements isolation without readers locking writers.",
            7: "Snapshot too old errors appear when versions are gone on some engines.",
            48: "MVCC is how Postgres implements READ COMMITTED and REPEATABLE READ snapshots.",
            49: "xmin and xmax system columns track row version visibility.",
            50: "HOT updates avoid new index entries when indexed columns unchanged.",
            51: "Autovacuum tuning matters for write-heavy tables under MVCC.",
        }
    )
    add(
        "D07-T017",
        "MVCC",
        """flowchart TD
  writer[WriterCreatesNewVersion]
  reader[ReaderUsesSnapshot]
  old[DeadTuples]
  writer --> old
  reader -->|sees_visible| snapshot[Snapshot]
  old -->|vacuum| reclaim[ReclaimSpace]""",
        """-- unexecuted
-- conceptual visibility (not valid SQL)
-- tx snapshot sees rows where xmin committed before snapshot and xmax not visible""",
        "MVCC lets readers and writers proceed with snapshots of row versions instead of always blocking.",
        "Each update is a new version chained logically; visibility rules pick which version a transaction sees.",
        "Vacuum or purge processes reclaim space from dead versions no snapshot needs.",
        "Under MVCC, a long report transaction does not block checkout writes, but bloat can slow both.",
        "Monitor bloat, autovacuum, and transaction age; keep transactions short.",
        ["Thinking MVCC removes need for locks on writes.", "Disabling autovacuum.", "SELECT * in RR forever.", "Ignoring bloat.", "Mixing MVCC with naive application caches."],
        ["pg_stat_user_tables n_dead_tup.", "autovacuum lag.", "txid age.", "EXPLAIN shows heap fetches."],
        ["Versions not overwrite.", "Snapshots.", "Vacuum required.", "Writes still lock row."],
        ["Explain xmin/xmax conceptually.", "Bloat symptom.", "Vacuum vs full vacuum.", "SSI vs MVCC."],
        ["Tune autovacuum on hot table.", "Find long idle transactions.", "Explain snapshot isolation."],
        ["Autovacuum tune.", "Idle TX hunt.", "Snapshot explainer."],
        ["Lower autovacuum scale factor on hot table.", "Terminate idle in transaction.", "Draw reader snapshot diagram."],
        f_mvcc,
    )

    # D07-T018 Indexes
    f_idx = _facts(
        {
            0: "An index is an auxiliary data structure speeding lookups at the cost of write overhead.",
            1: "B-tree is the default ordered index supporting range scans.",
            2: "Sequential scan reads whole table when selectivity is poor or stats wrong.",
            3: "Indexes help WHERE, JOIN, and ORDER BY on matching leading columns.",
            4: "Unused indexes slow writes and consume disk.",
            5: "Selectivity estimates come from ANALYZE statistics.",
            24: "CREATE INDEX CONCURRENTLY builds without blocking writes in Postgres.",
            25: "Partial indexes filter rows with a WHERE clause on the index definition.",
        }
    )
    add(
        "D07-T018",
        "database indexes",
        """flowchart TD
  query[QueryPredicate]
  planner[Planner]
  index[IndexScan]
  seq[SeqScan]
  query --> planner
  planner -->|selective| index
  planner -->|not| seq""",
        """-- unexecuted
CREATE INDEX CONCURRENTLY idx_orders_customer_created
  ON orders (customer_id, created_at DESC);""",
        "Indexes accelerate finding rows by key or range; every index adds maintenance on writes.",
        "B-trees store sorted keys pointing to heap tuples or primary key. Hash indexes suit equality only.",
        "Planner compares estimated cost of index scan versus sequential scan.",
        "customer_id filter on orders uses btree on customer_id.",
        "Index columns you filter and join; verify with EXPLAIN, drop unused indexes.",
        ["Index every column.", "Wrong column order.", "Function on column unindexed.", "Stale stats.", "Duplicate indexes."],
        ["EXPLAIN shows Seq Scan.", "pg_stat_user_indexes idx_scan zero.", "Run ANALYZE.", "Check correlation."],
        ["B-tree default.", "Write cost.", "Selectivity.", "CONCURRENTLY build."],
        ["Pick index columns.", "Explain seq vs index.", "Find unused index.", "Partial index use."],
        ["Add index for slow query.", "Drop duplicate.", "ANALYZE after bulk load."],
        ["Add index.", "Drop duplicate.", "ANALYZE bulk."],
        ["Match WHERE and ORDER BY leading columns.", "Keep cheaper index.", "ANALYZE orders after import."],
        f_idx,
    )

    # D07-T019 Composite and covering
    add(
        "D07-T019",
        "composite and covering indexes",
        """flowchart LR
  cols[LeadingColumns]
  include[INCLUDEColumns]
  cols --> indexOnly[IndexOnlyScan]""",
        """-- unexecuted
CREATE INDEX idx_orders_cover ON orders (customer_id, created_at)
  INCLUDE (total_cents, status);""",
        "Composite indexes order multiple columns; covering indexes INCLUDE extra columns to enable index-only scans.",
        "Leftmost prefix rule: index (a,b) helps WHERE a and WHERE a,b, not alone b.",
        "INCLUDE columns are payload not part of sort key but available from index.",
        "Dashboard query reading customer_id, created_at, total_cents may be index-only with INCLUDE.",
        "Design index order matching equality filters before range sorts.",
        ["Column order reversed.", "INCLUDE everything.", "Index-only myth without vacuum.", "Redundant single-col indexes.", "Wide indexes bloating cache."],
        ["EXPLAIN Index Only Scan.", "Check visibility map.", "Compare index size.", "Prefix rule test."],
        ["Leading column rule.", "INCLUDE payload.", "Index-only needs VM.", "Equality before range."],
        ["Design composite for query.", "Explain prefix.", "When INCLUDE helps.", "Drop redundant."],
        ["Cover hot reporting query.", "Reorder composite.", "Measure index size."],
        ["Cover query.", "Reorder composite.", "Index size."],
        ["INCLUDE totals for index-only.", "Put equality cols first.", "Watch idx_blks_hit."],
        _facts({0: "Composite indexes specify column order that matters for prefix matching.", 1: "Covering indexes include non-key columns to avoid heap lookups.", 2: "Index-only scans require visibility map freshness in Postgres.", 3: "Too many included columns enlarge the index."}),
    )

    # D07-T020 Clustered vs non-clustered
    add(
        "D07-T020",
        "clustered versus non-clustered indexes",
        """flowchart TD
  clustered[ClusteredIndexOrderIsTable]
  nonclustered[NonClusteredSeparateStructure]
  clustered --> heap[HeapOrClusteredStorage]
  nonclustered --> lookup[LookupToHeap]""",
        """-- unexecuted
-- SQL Server style (illustrative)
-- CREATE CLUSTERED INDEX cx ON orders(created_at);
-- Postgres: CLUSTER command reorders heap once; PK is logical not clustered by default""",
        "Clustered indexes define physical row order; non-clustered indexes are separate structures pointing to rows.",
        "SQL Server clustered index is the table order. Postgres uses heap with separate indexes; CLUSTER is one-time rewrite.",
        "InnoDB clusters by primary key. Too many secondary indexes increase write amplification.",
        "Choose clustering key aligned with range scans if engine supports it.",
        "Know your engine: interview answers must not confuse Postgres heap with SQL Server clustered.",
        ["Thinking Postgres PK is clustered like SQL Server.", "CLUSTER in prod without window.", "Random UUID PK clustering.", "Many secondary on wide PK.", "Ignoring fillfactor."],
        ["Check amname index type.", "Heap vs index read in EXPLAIN.", "Page splits on insert pattern.", "CLUSTER one-off plan."],
        ["Engine-specific clustering.", "Postgres heap default.", "InnoDB PK clustered.", "CLUSTER not continuous."],
        ["Compare Postgres vs SQL Server.", "Pick clustering key.", "UUID insert penalty.", "Explain lookup."],
        ["Document engine clustering model.", "Mitigate UUID PK fragmentation.", "When CLUSTER helps."],
        ["Engine doc.", "UUID mitigation.", "CLUSTER case."],
        ["State Postgres uses heap + indexes.", "Use uuid v7 or sequential.", "CLUSTER during maintenance."],
        _facts({0: "A clustered index determines physical storage order on some engines.", 1: "Non-clustered indexes are separate trees pointing to row locators.", 2: "PostgreSQL tables are heap-organized with separate indexes.", 3: "InnoDB stores rows in primary key order."}),
    )

    # D07-T021 B-tree and hash
    add(
        "D07-T021",
        "B-tree and hash indexes",
        """flowchart TD
  btree[BTreeOrdered]
  hash[HashEquality]
  btree --> range[RangeScans]
  hash --> eq[EqualityOnly]""",
        """-- unexecuted
CREATE INDEX idx_users_email ON users USING btree (email);
CREATE INDEX idx_sessions_token ON sessions USING hash (token);""",
        "B-tree indexes support ordering, range predicates, and sorting; hash indexes support equality lookups only.",
        "B-tree nodes branch by key order with balanced height. Hash maps key to bucket.",
        "Postgres hash indexes are valid but btree is default for most cases.",
        "email = $1 uses btree or hash; created_at > $1 needs btree.",
        "Default to btree unless proven equality-only workload with hash support.",
        ["Hash for range query.", "Btree on low cardinality alone.", "Wrong opclass for text.", "GiST confusion.", "Reindex after corruption."],
        ["EXPLAIN Index Scan type.", "Operator class mismatch.", "Cardinality estimate 1.", "Compare btree vs hash on eq."],
        ["Btree ordered.", "Hash eq only.", "Opclass matters.", "GiST for geo separate."],
        ["Pick btree vs hash.", "Explain balance.", "When hash wins.", "Reindex need."],
        ["Benchmark eq lookup.", "Fix range on hash mistake.", "Document opclass."],
        ["Eq benchmark.", "Fix hash mistake.", "Opclass doc."],
        ["Hash only for = queries.", "Add btree for ranges.", "Use varchar_pattern_ops for LIKE prefix."],
        _facts({0: "B-tree indexes keep keys sorted for range and ordering operations.", 1: "Hash indexes map keys to buckets for equality comparisons.", 2: "Most OLTP queries need B-tree because of range and ORDER BY.", 3: "Operator classes define how values compare for indexing."}),
    )

    # D07-T022 Query plans
    add(
        "D07-T022",
        "query execution plans",
        """flowchart TD
  parse[Parse]
  rewrite[Rewrite]
  plan[Plan]
  execute[Execute]
  parse --> rewrite --> plan --> execute""",
        """-- unexecuted
EXPLAIN (FORMAT TEXT)
SELECT * FROM orders WHERE customer_id = 42;""",
        "The optimizer chooses access paths: join order, scan types, and aggregate methods to minimize estimated cost.",
        "Statistics on table size and column distribution feed cost model. Bad stats yield bad plans.",
        "Plans are trees of nodes: Seq Scan, Index Scan, Hash Join, Sort, Aggregate.",
        "Sudden seq scan on big table often means stale stats or wrong parameter sniffing.",
        "Refresh stats, adjust indexes, or rewrite query when plan regresses.",
        ["Trust cost without ANALYZE.", "Generic plan cache issues.", "Nested loop on huge inner.", "Sort spill to disk.", "Ignore join order."],
        ["Compare EXPLAIN before/after.", "pg_stat_statements mean time.", "Track plan hash changes.", "Work_mem spills."],
        ["Planner uses stats.", "Nodes: scan join sort.", "Estimates can be wrong.", "Plans can change."],
        ["Read EXPLAIN tree.", "Fix bad nested loop.", "When materialize.", "Stats refresh."],
        ["Interpret plan for slow query.", "Fix join order with stats.", "Increase work_mem cautiously."],
        ["Interpret plan.", "Fix join order.", "work_mem tune."],
        ["Identify Seq Scan on millions.", "ANALYZE; add index.", "Watch external sort in ANALYZE."],
        _facts({0: "The planner estimates costs using statistics and hardware constants.", 1: "Sequential scan reads all pages when index is not cheaper.", 2: "Hash join builds a hash table on the inner side for equi-joins.", 3: "Nested loop joins are cheap when the inner side is small per outer row."}),
    )

    # D07-T023 EXPLAIN
    f_explain = _facts(
        {
            0: "EXPLAIN shows the planned node tree without executing the query.",
            1: "EXPLAIN ANALYZE executes the query and adds actual row counts and timings.",
            2: "Buffers option shows cache hits versus disk reads per node.",
            3: "Actual rows differing greatly from estimates signals stats or correlation issues.",
            4: "Never run EXPLAIN ANALYZE on destructive statements in production without care.",
            5: "Use BUFFERS to see whether index scans are cache-friendly.",
            24: "EXPLAIN (ANALYZE, BUFFERS) is the standard Postgres tuning trio.",
            25: "Planning time matters for very fast queries called millions of times.",
        }
    )
    add(
        "D07-T023",
        "EXPLAIN and EXPLAIN ANALYZE",
        """flowchart TD
  explain[EXPLAIN]
  analyze[EXPLAIN_ANALYZE]
  buffers[BUFFERS]
  explain --> planOnly[PlanOnly]
  analyze --> actual[ActualRowsAndTime]
  buffers --> io[CacheVsDisk]""",
        """-- unexecuted
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT o.id, c.email
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.created_at >= now() - interval '30 days';""",
        "EXPLAIN displays the planner's intended operations; EXPLAIN ANALYZE runs the query and measures reality.",
        "Compare estimated versus actual rows at each node to find misestimates. BUFFERS reveals I/O.",
        "ANALYZE on production writes if the query mutates; use transactions rolled back or staging copies.",
        "Thirty-day order report: check nested loop vs hash join and buffer hits.",
        "Capture plans in CI for golden queries; investigate regressions after migrations.",
        ["ANALYZE on DELETE in prod.", "Only looking at total time.", "Ignoring misestimate nodes.", "No FORMAT JSON for tools.", "Running on different data size."],
        ["Find node where actual >> estimate.", "shared hit vs read.", "Loop count on nested loop.", "Save plan baseline."],
        ["EXPLAIN safe plan.", "ANALYZE executes.", "BUFFERS for I/O.", "Misestimate diagnosis."],
        ["Read ANALYZE output.", "Use BUFFERS.", "Safe prod workflow.", "JSON plans."],
        ["Document plan for top query.", "Fix misestimate.", "Add plan test."],
        ["Plan doc.", "Fix misestimate.", "Plan test."],
        ["Store EXPLAIN in repo.", "ANALYZE table or increase stats target.", "Assert Index Scan in test."],
        f_explain,
    )

    # D07-T024 Slow queries
    add(
        "D07-T024",
        "slow query optimization",
        """flowchart TD
  identify[IdentifySlowQuery]
  explain[EXPLAIN_ANALYZE]
  fix[IndexOrRewrite]
  verify[VerifySLO]
  identify --> explain --> fix --> verify""",
        """-- unexecuted
-- find candidates
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;""",
        "Slow query work finds high-latency statements, explains plans, and fixes access paths or SQL shape.",
        "pg_stat_statements aggregates mean time and calls. Logs capture duration thresholds.",
        "Fixes: indexes, stats, partition pruning, rewrite joins, pagination cursors.",
        "OFFSET million rows is slow; keyset pagination on indexed column is fast.",
        "Optimize top queries by total time (mean * calls), not only mean.",
        ["Index without measuring.", "Cache hides need.", "ORM N+1.", "Select star.", "Functions on indexed col."],
        ["pg_stat_statements total time.", "EXPLAIN ANALYZE.", "Find N+1 in traces.", "Check lock waits."],
        ["Measure first.", "Total time ranking.", "Keyset pagination.", "N+1 fix."],
        ["Optimize top stmt.", "Fix N+1.", "Replace OFFSET.", "Add partial index."],
        ["Plan for pg_stat_statements top query.", "Fix ORM fetch join.", "Keyset API."],
        ["Top stmt plan.", "Fetch join.", "Keyset API."],
        ["Index per EXPLAIN.", "JOIN FETCH or batch IN.", "WHERE id > :cursor ORDER BY id LIMIT."],
        _facts({0: "Slow queries are identified by latency, total time, and business criticality.", 1: "pg_stat_statements ranks queries by cumulative cost.", 2: "Missing indexes often show as sequential scans on large tables.", 3: "ORM N+1 appears as many similar fast queries."}),
    )

    # D07-T025 Connection pooling
    add(
        "D07-T025",
        "connection pooling",
        """flowchart TD
  pods[AppPods]
  pool[Pooler]
  db[(Database)]
  pods --> pool --> db""",
        """-- unexecuted
-- application pool sizing rule of thumb: cores * 2 + spindle_count (adjust per workload)
-- PgBouncer pool_mode = transaction for serverless""",
        "Connection pooling reuses database sessions to avoid handshake overhead and max_connections exhaustion.",
        "Poolers like PgBouncer multiplex many clients to fewer server connections.",
        "Transaction pooling returns server connection after each transaction; session features break.",
        "Thousand Kubernetes pods each opening 10 connections can exceed Postgres max_connections.",
        "Size pools per instance; use pooler; monitor waiting threads.",
        ["Pool per request.", "Huge max pool size.", "Session pooling with temp tables.", "No pooler at scale.", "Idle connections forever."],
        ["too many clients already.", "Pool wait metrics.", "pg_stat_activity count.", "Pgbouncer SHOW POOLS."],
        ["Reuse connections.", "PgBouncer modes.", "max_connections math.", "Short transactions."],
        ["Size pool.", "Pick pool mode.", "Fix storm.", "Graceful drain."],
        ["Calculate pool for 50 pods.", "Choose transaction vs session pooling.", "Drill failover."],
        ["Pool calc.", "Pool mode.", "Failover drill."],
        ["50 pods * 5 conns = 250; pooler to 100 server conns.", "Transaction mode for stateless API.", "Drain pools before failover."],
        _facts({0: "Each database connection consumes memory on the server.", 1: "Pools amortize SSL and authentication costs.", 2: "PgBouncer transaction pooling suits short stateless queries.", 3: "Session pooling is required for prepared statements and temp tables per session."}),
    )

    # D07-T026 Migrations
    add(
        "D07-T026",
        "migrations and schema evolution",
        """flowchart TD
  v1[SchemaV1]
  mig[MigrationScript]
  v2[SchemaV2]
  v1 --> mig --> v2""",
        """-- unexecuted
ALTER TABLE users ADD COLUMN display_name text;
-- expand-contract: add nullable, backfill, set NOT NULL, drop old""",
        "Migrations version DDL changes alongside application code for reproducible environments.",
        "Expand-contract avoids incompatible deploy ordering: add new column, dual-write, backfill, switch reads, drop old.",
        "Tools: Flyway, Liquibase, Alembic, Rails migrations. Track history table.",
        "Adding NOT NULL instantly on huge table locks; use multi-step expand.",
        "Test migrations on copy; measure lock duration; plan rollback.",
        ["Blocking ACCESS EXCLUSIVE.", "No down migration.", "Data loss ALTER.", "Different order prod vs dev.", "Heavy backfill in TX."],
        ["lock_timeout.", "pg_stat_progress_create_index.", "Row count estimate.", "Migration table version."],
        ["Versioned DDL.", "Expand-contract.", "Online index.", "Backward compatible deploy."],
        ["Plan NOT NULL migration.", "Online index create.", "Rollback story.", "Lock minimization."],
        ["Write expand-contract for rename.", "CONCURRENTLY index migration.", "Flyway ordering."],
        ["Rename expand-contract.", "Concurrent index.", "Flyway order."],
        ["Add column, backfill job, switch code, drop old.", "CREATE INDEX CONCURRENTLY.", "Vxxx before app deploy."],
        _facts({0: "Migrations apply ordered DDL scripts to evolve schema.", 1: "Backward-compatible deploys require expand-contract patterns.", 2: "Long locks from ALTER TABLE can take sites offline.", 3: "Index creation should use CONCURRENTLY on Postgres for large tables."}),
    )

    # D07-T027 Backup and PITR
    add(
        "D07-T027",
        "backup, restore, and point-in-time recovery",
        """flowchart TD
  base[BaseBackup]
  wal[WALArchive]
  pitr[PITRRestore]
  base --> pitr
  wal --> pitr""",
        """-- unexecuted
-- recovery target example (conceptual)
-- restore_command pulls WAL until '2026-10-12 12:00:00+00'""",
        "Backups capture base images; continuous archiving of WAL enables point-in-time recovery to a timestamp.",
        "RPO is how much data you may lose; RTO is how fast you restore. Test restores quarterly.",
        "Logical dumps (pg_dump) differ from physical base backups for speed and PITR.",
        "Accidental DROP needs PITR or replica lag snapshot, not yesterday's dump only.",
        "Encrypt backups; restrict access; automate restore drills.",
        ["Backups never tested.", "WAL archiving off.", "Same region only.", "No PITR target practice.", "Dump-only for huge DB."],
        ["Restore drill timer.", "Missing WAL segments.", "Backup age alert.", "pg_dump size time."],
        ["Base + WAL = PITR.", "RPO/RTO.", "Test restore.", "Logical vs physical."],
        ["Run restore drill.", "Explain RPO.", "Pick backup tool.", "Handle DROP TABLE."],
        ["Document PITR runbook.", "Calculate RPO with WAL lag.", "Encrypt S3 backups."],
        ["PITR runbook.", "RPO calc.", "Backup encryption."],
        ["Step-by-step restore to staging.", "RPO = max WAL gap.", "SSE-KMS on backup bucket."],
        _facts({0: "Physical backups copy data files at a point in time.", 1: "WAL records every change after the backup for replay.", 2: "Point-in-time recovery replays WAL to a target timestamp.", 3: "Untested backups are a false sense of security."}),
    )

    # D07-T028 Replication and failover
    f_rep = _facts(
        {
            0: "Replication copies data from primary to standby for read scaling and high availability.",
            1: "Streaming replication ships WAL records to replicas asynchronously or synchronously.",
            2: "Failover promotes a replica when the primary is unhealthy.",
            3: "Replication is not sharding; each replica holds a full copy of the dataset.",
            4: "Split-brain happens if two nodes think they are primary.",
            5: "Fencing or STONITH stops the old primary from accepting writes.",
            6: "RPO near zero needs synchronous replication with latency cost.",
            7: "Logical replication replicates row changes for upgrades or subsets.",
            52: "Sharding splits data across nodes; replication duplicates the same data.",
            53: "You shard when one node cannot hold or serve the dataset.",
            54: "Cross-shard queries need federation or application-side aggregation.",
            55: "Migrations from single node to sharded are painful; plan early.",
        }
    )
    add(
        "D07-T028",
        "replication and failover",
        """flowchart TD
  primary[Primary]
  wal[WALStream]
  replica[Replica]
  failover[FailoverController]
  primary --> wal --> replica
  failover -->|promote| replica""",
        """-- unexecuted
-- check replication lag (Postgres)
SELECT now() - pg_last_xact_replay_timestamp() AS replay_lag;""",
        "Replication maintains standby copies; failover redirects writes when the primary fails.",
        "Physical streaming replication is byte-for-byte; logical replication publishes changes.",
        "Patroni, orchestrators, and cloud RDS handle promotion and DNS updates.",
        "Async replication may lose last seconds of writes on failover—know RPO.",
        "Do not confuse replication with sharding (`D07-T029`).",
        ["Two primaries after split brain.", "Failover without app retry.", "DNS TTL too long.", "Replica promotion without rewind.", "Testing only sync in prod."],
        ["replay lag metric.", "pg_is_in_recovery().", "Connection errors spike.", "Timeline mismatch."],
        ["Replica full copy.", "Async vs sync.", "Failover automation.", "Not sharding."],
        ["Explain lag.", "Design failover.", "Split brain prevent.", "vs sharding."],
        ["Run failover game day.", "Document RPO.", "Compare logical vs physical."],
        ["Failover game day.", "RPO doc.", "Logical vs physical."],
        ["Promote replica in staging; measure downtime.", "State seconds of async loss.", "Logical for version upgrade."],
        f_rep,
    )

    # D07-T029 Partitioning and sharding
    f_shard = _facts(
        {
            0: "Partitioning splits one logical table into physical chunks inside one database instance.",
            1: "Sharding splits data across multiple database instances or nodes.",
            2: "Partition pruning skips irrelevant partitions for faster queries.",
            3: "Shard key choice is hard to change; pick a stable high-cardinality key.",
            4: "Cross-shard joins are expensive; design queries shard-local.",
            5: "Replication copies entire databases; sharding divides responsibility.",
            6: "Vitess, Citus, and application routers implement sharding.",
            7: "Global uniqueness may need UUID or snowflake per shard.",
            52: "Do not shard before indexing and query tuning on one node.",
            53: "Hot shards occur when shard key is skewed.",
            54: "Rebalancing shards is an operational migration project.",
            55: "Two-phase commit across shards is rare; prefer sagas.",
        }
    )
    add(
        "D07-T029",
        "partitioning and sharding",
        """flowchart TD
  logical[LogicalTable]
  part[PartitionsSameInstance]
  shardA[ShardA]
  shardB[ShardB]
  logical --> part
  logical -->|scale_out| shardA
  logical -->|scale_out| shardB""",
        """-- unexecuted
CREATE TABLE orders (
  id bigint,
  created_at timestamptz NOT NULL,
  customer_id bigint NOT NULL
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2026_10 PARTITION OF orders
  FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');""",
        "Partitioning divides tables by range, list, or hash on one server; sharding spreads partitions across nodes.",
        "Pruning limits scans to relevant partitions. Sharding adds network routing and cross-shard pain.",
        "Declarative partitioning in Postgres attaches child tables. Sharding needs a router layer.",
        "Time-based orders partition by month; user_id shard when single node maxed despite tuning.",
        "Shard only after proven single-node limits; keep cross-shard transactions rare.",
        ["Sharding day one.", "Bad shard key.", "Cross-shard join reports.", "No rebalance plan.", "Confuse partition with shard."],
        ["EXPLAIN partition pruning.", "Shard heatmap.", "Router misroute.", "Orphan shard data."],
        ["Partition same node.", "Shard multi node.", "Pruning.", "Shard key."],
        ["Design time partition.", "When to shard.", "Avoid cross shard TX.", "Rebalance."],
        ["Add monthly partitions.", "Pick tenant shard key.", "Document router."],
        ["Monthly partitions.", "Tenant shard key.", "Router doc."],
        ["CREATE next month partition job.", "tenant_id hash mod N.", "Router library choice ADR."],
        f_shard,
    )

    # D07-T030 Read replicas
    add(
        "D07-T030",
        "read replicas and read/write splitting",
        """flowchart TD
  write[WritePathPrimary]
  read[ReadPathReplica]
  app[Application]
  app --> write
  app --> read""",
        """-- unexecuted
-- application pseudo
-- route SELECT reports to replica DSN
-- route INSERT/UPDATE/DELETE to primary DSN""",
        "Read replicas serve SELECT traffic; primaries handle writes. Splitting reduces primary load with lag trade-offs.",
        "Lag means stale reads. Critical read-after-write must hit primary or use session tracking.",
        "Connection pools often have two DSNs: writer and reader.",
        "Dashboard analytics on replica; payment confirmation on primary.",
        "Monitor lag; circuit-break replica reads when lag high.",
        ["Replica for just-written balance.", "Sticky session ignored.", "Round-robin all reads.", "Lag not alerted.", "Replica serves writes by mistake."],
        ["replay lag.", "User sees old avatar.", "Writer DSN on SELECT bug.", "Load imbalance on one replica."],
        ["Writes primary.", "Reads replica with lag.", "Read-your-writes.", "Lag alerts."],
        ["Design split.", "Fix stale read bug.", "Lag circuit breaker.", "Load balance replicas."],
        ["Implement rw split.", "Add lag metric alert.", "Session stickiness after write."],
        ["RW split.", "Lag alert.", "Post-write stickiness."],
        ["Two pools in config.", "Alert lag > 5s.", "Primary for 30s after user mutation."],
        _facts({0: "Read replicas apply the same WAL as the primary with delay.", 1: "Read/write splitting routes mutations to the primary only.", 2: "Applications must tolerate stale reads on replicas or route carefully.", 3: "Multiple replicas load-balance read traffic horizontally."}),
    )

    # D07-T031 Archival
    add(
        "D07-T031",
        "data archival and retention",
        """flowchart TD
  hot[HotPrimaryData]
  archive[ColdArchiveStore]
  purge[PurgePerPolicy]
  hot -->|age_threshold| archive
  hot --> purge""",
        """-- unexecuted
INSERT INTO orders_archive SELECT * FROM orders
WHERE created_at < now() - interval '2 years';
DELETE FROM orders WHERE created_at < now() - interval '2 years';""",
        "Archival moves cold data to cheaper storage; retention policies define legal and product delete schedules.",
        "Deletes in batches with indexes on created_at. Archival tables or object storage with metadata.",
        "GDPR erasure may conflict with audit retention—legal defines precedence.",
        "Two-year orders move to archive table or S3 parquet; primary stays fast.",
        "Automate jobs; verify counts; document retention in privacy policy.",
        ["DELETE full table lock.", "No archive before delete.", "Restore untested.", "PII in archive unencrypted.", "Retention without legal review."],
        ["Row counts before/after.", "Job duration.", "Orphan files in bucket.", "FK blocking delete."],
        ["Hot vs cold.", "Batch delete.", "Legal retention.", "Archive format."],
        ["Design retention job.", "GDPR vs audit.", "Partition drop vs delete.", "Restore archive."],
        ["Batch archive job.", "Retention ADR.", "Partition detach old month."],
        ["Batch archive.", "Retention ADR.", "Detach partition."],
        ["DELETE ... LIMIT 10000 loop.", "Legal sign-off on periods.", "DETACH PARTITION instead of DELETE."],
        _facts({0: "Archival reduces primary database size and cost for cold data.", 1: "Retention policies define how long data must be kept or deleted.", 2: "Regulations may require deletion while audits require retention balances.", 3: "Partition detach can drop old data quickly without row-by-row delete."}),
    )

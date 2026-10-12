"""Twenty core interview QAs per topic (D09-T007..D09-T018); follow-ups added by std_k."""
from __future__ import annotations

# Each entry: (question, s1, s2, s3, s4)


def _t007():
    return [
        ("What is a heap page in PostgreSQL?", "A fixed-size block (commonly 8KB, block size is compile-time) holding line pointers and tuples.", "The buffer manager caches pages in shared_buffers.", "Updates may insert new tuples or HOT chains on the same page.", "Indexes reference heap tuple identifiers via TIDs."),
        ("What is TOAST?", "The Oversized-Attribute Storage Technique stores wide varlena values out-of-line.", "A side table linked from the main heap tuple holds chunks.", "Compression may apply before storage depending on strategy.", "It keeps main pages from exceeding usable space."),
        ("When does PostgreSQL toast a value?", "When a row would exceed the page threshold after insert or update.", "Large text, jsonb, and bytea are common candidates.", "The decision is automatic based on type and size.", "Storage strategy can be tuned per column."),
        ("Name TOAST storage strategies.", "PLAIN refuses out-of-line storage.", "EXTENDED tries compression then out-of-line.", "EXTERNAL keeps uncompressed external storage.", "MAIN keeps in-line if possible else external."),
        ("Why is SELECT * risky on wide tables?", "It pulls toasted columns into memory even if unused.", "Network and application memory costs jump.", "Index-only scans cannot avoid fetching toasted columns if selected.", "Explicit column lists help performance."),
        ("What is a line pointer?", "An entry in the page header array pointing to tuple offset.", "Dead line pointers remain until vacuum.", "They enable indirection when tuples move within page.", "ItemId is the internal name in docs."),
        ("How does UPDATE move tuples?", "If no space on page, the row may move to another page with new TID.", "Indexes must be updated unless HOT applies.", "Moving tuples is expensive for indexed tables.", "fillfactor and HOT reduce moves."),
        ("What is toast_tuple_target?", "A per-column tuning knob for when to toast.", "Lowering it toasts earlier.", "Raising keeps more in-line at page cost.", "Defaults vary; test with your row width."),
        ("Can TOAST tables bloat?", "Yes, dead toast chunks need vacuum like heap.", "Wide json churn creates toast bloat.", "Monitor toast rel size via pg_total_relation_size.", "Vacuum parent helps toast cleanup."),
        ("Difference heap TID vs ctid?", "ctid exposed in SQL is block and offset.", "It changes when row moves.", "Do not use as primary key.", "Useful for debugging version chains."),
        ("Page header contents?", "Checksum if enabled, free space pointers, line pointer count.", "Layout documented in internals guides.", "Corruption detected via checksum failures.", "Zero_damaged_pages GUC affects behavior on error."),
        ("ALTER COLUMN SET STORAGE effect?", "Changes strategy for future writes.", "Does not rewrite existing data immediately.", "May need rewrite migration for full effect.", "Plan maintenance for large tables."),
        ("JSONB storage note?", "jsonb is varlena binary format often toasted when large.", "GIN indexes target jsonb paths separately.", "Small jsonb may stay in-line.", "Design payloads to avoid accidental megabytes."),
        ("TOAST and replication?", "Physical replication carries WAL for toast pages like heap.", "Logical replication sends decoded column values.", "Large values increase replication bandwidth.", "Compression affects size on disk not logical content."),
        ("Read path for toasted column?", "Fetch heap tuple, follow toast pointer, read chunks.", "May be multiple I/Os.", "Caching helps repeated reads.", "Keep hot columns narrow."),
        ("Write path for growing column?", "May trigger toast and new chunk rows.", "Generates WAL for heap and toast.", "Can be slower than small updates.", "Batch large writes off critical path if possible."),
        ("Scenario: sudden table growth after json feature?", "Check average row width and toast size.", "Archive old json off-row to object store.", "Add constraints on payload size.", "Vacuum after cleanup."),
        ("Scenario: slow SELECT id only on wide table?", "Should not fetch toast if column not projected.", "Verify query only selects id.", "If ORM loads all fields, fix mapping.", "Heap-only scan still reads page headers."),
        ("Scenario: pg_attribute shows storage external?", "Future writes prefer external toast.", "Large values skip main page.", "Good for rare huge blobs.", "Bad for frequently filtered huge text in heap."),
        ("Scenario: page checksum error?", "Hardware or storage fault.", "Restore from backup.", "Investigate disk subsystem.", "Do not ignore repeated checksum failures."),
    ]


def _t008():
    return [
        ("Default index type in PostgreSQL?", "B-tree via USING btree.", "Handles =, <, >, and sorted scans.", "Most OLTP indexes are btree.", "Other types need explicit USING."),
        ("When use GIN?", "Inverted indexes for composite items like tsvector, jsonb paths, arrays.", "Fast @> and @@ style ops with right opclass.", "Build and size can be large.", "Good for read-heavy search."),
        ("When use GiST?", "Geometric and custom datatypes with GiST opclasses.", "Lossy for some types with recheck.", "Extensible framework.", "Not default for integers."),
        ("When use BRIN?", "Block range indexes for very large naturally correlated data.", "Tiny index size stores min/max per range.", "Ideal for time-series append if queries align.", "Useless if data unordered within column."),
        ("B-tree multicolumn order?", "Leftmost column most important for mixed queries.", "Cannot skip leading column in typical btree usage.", "Order columns by selectivity and query patterns.", "INCLUDE adds payload columns on leaf."),
        ("CREATE INDEX CONCURRENTLY?", "Builds without blocking writes long-term.", "Two scans and validation phase.", "Can fail leaving invalid index.", "Use on production large tables."),
        ("Index-only scan requirements?", "Index must cover columns and visibility map says all-visible.", "Vacuum maintains visibility map.", "Still may need heap fetch if map not set.", "See D09-T005."),
        ("GIN vs GiST for full text?", "GIN common for tsvector search.", "GiST can be smaller with different perf.", "Benchmark with real corpus.", "Maintenance differs."),
        ("BRIN correlation?", "Works when physical order matches key order.", "Cluster or load sorted data.", "After heavy updates correlation may degrade.", "Reindex BRIN if needed."),
        ("Unused index detection?", "pg_stat_user_indexes idx_scan near zero over window.", "Drop cautiously after workload cover.", "FK may need index.", "Duplicate indexes waste writes."),
        ("Partial index use?", "Indexes subset with WHERE clause.", "Smaller and selective.", "Must match query predicate.", "Great for active-only rows."),
        ("Hash index note?", "Historically limited; btree usually preferred.", "Check version docs for hash improvements.", "Not default choice.", "Equality-only if used."),
        ("Index bloat cause?", "Dead heap tuples leave dead index entries until vacuum.", "Heavy churn without vacuum.", "REINDEX CONCURRENTLY on supported versions.", "Fix churn first."),
        ("Covering index benefit?", "Avoid heap visits for included columns.", "Reduces I/O on read-heavy.", "Larger index size.", "Trade write amplification."),
        ("Expression index?", "Index on function of column.", "Must match query expression exactly.", "Useful for lower(email).", "Planner must see same expr."),
        ("Scenario: jsonb @> slow?", "Missing GIN jsonb_path_ops or jsonb_ops index.", "EXPLAIN shows seq scan.", "Add appropriate GIN.", "ANALYZE after."),
        ("Scenario: BRIN not used?", "Poor correlation or wrong stats.", "EXPLAIN analyze all partitions.", "Consider btree on recent partition.", "Reload sorted."),
        ("Scenario: duplicate indexes?", "Same columns twice wastes writes.", "Drop one after verify.", "Migration tools sometimes create extras.", "Audit pg_indexes."),
        ("Scenario: index valid false?", "CONCURRENTLY build failed.", "Drop invalid index.", "Retry during low traffic.", "Check logs for deadlock."),
        ("Scenario: FK without index on child?", "Deletes on parent slow.", "Add btree on child FK cols.", "Standard schema review item.", "Critical at scale."),
    ]


def _t009():
    return [
        ("What does the planner output?", "A plan tree: nodes for scans, joins, aggregates.", "EXPLAIN shows estimated costs and rows.", "EXPLAIN ANALYZE executes and shows actuals.", "BUFFERS adds cache hit detail."),
        ("Cost units meaning?", "Abstract units not milliseconds.", "Compare relative plans.", "seq_page_cost and random_page_cost scale IO.", "cpu_operator_cost scales CPU."),
        ("Join algorithms?", "Nested loop good for small outer.", "Hash join builds hash table on inner.", "Merge join needs sorted inputs.", "Planner picks based on stats."),
        ("When nested loop wins?", "Small cardinality on outer side.", "Index on inner join key.", "OLTP point lookups.", "Bad when outer huge without index."),
        ("Materialize node?", "Caches subquery results.", "Costs memory.", "Used when replanning expensive.", "Watch work_mem limits."),
        ("Join order search?", "Exhaustive for few relations.", "genetic optimizer for many tables (geqo_threshold).", "Bad stats cause wrong order.", "Increase stats or hint carefully."),
        ("Prepared statements planning?", "Generic vs custom plans depending on version and settings.", "First executions may differ from later.", "pg_prepared_statements view shows plans.", "ORMs use prepares heavily."),
        ("Partition pruning?", "Constraints eliminate child tables.", "Must have provable predicates.", "Default partition may defeat prune.", "D09-T014."),
        ("Parallel gather?", "Leader collects partial results.", "Workers scan partitions of table.", "Increases CPU use.", "max_parallel_workers_per_gather caps."),
        ("Row estimate errors?", "Stale stats or correlated predicates.", "ANALYZE and extended stats help.", "NDV errors on skewed columns.", "D09-T010."),
        ("enable_seqscan off?", "Forces index if available.", "Debugging only.", "Hides real production choice.", "Do not leave on globally."),
        ("Bitmap scan?", "Combines index tid bitmaps before heap visit.", "Useful for medium selectivity.", "Multiple indexes can bitmap AND/OR.", "Reduces random heap hits."),
        ("Subquery flattening?", "Planner may join instead of nested loop subselect.", "Rewrite rules transform SQL.", "Same semantics different plan.", "EXPLAIN shows structure."),
        ("CTE materialization?", "WITH may be inlined or materialized per version/planner.", "NOT MATERIALIZED hints on supported versions.", "Affects performance surprises.", "Test after upgrades."),
        ("Scenario: sudden seq scan on big table?", "Stats dropped or predicate not indexable.", "Check pg_stats and indexes.", "ANALYZE.", "Add or fix index."),
        ("Scenario: hash join huge memory?", "Inner side large; work_mem exceeded to disk.", "Increase work_mem cautiously.", "Rewrite to nest loop with index.", "Batch processing."),
        ("Scenario: bad plan after upgrade?", "Planner changes between versions.", "Re-analyze all.", "Compare EXPLAIN.", "Report regression with details."),
        ("Scenario: OR conditions slow?", "May become bitmap or multiple scans.", "Consider UNION ALL rewrite.", "Partial indexes per branch.", "Measure both."),
        ("Scenario: LIMIT without order?", "Planner may choose fast partial plan.", "Add ORDER BY if needed.", "Different plan cost.", "Not a bug."),
        ("Scenario: geqo plan unstable?", "Many joins.", "Raise geqo_threshold or simplify SQL.", "Split queries.", "Stats quality matters."),
    ]


def _t010():
    return [
        ("What does ANALYZE collect?", "Per-column ndistinct, null fraction, most common values, histogram bounds.", "Stored in pg_stats.", "Sample size driven by default_statistics_target.", "Autovacuum can trigger analyze."),
        ("Why stale stats hurt?", "Underestimated rows choose nested loop over hash.", "Overestimated rows skip useful indexes.", "Plans flip after analyze.", "Monitor last_analyze."),
        ("default_statistics_target?", "Controls sample rows per column.", "Higher improves estimates, slower analyze.", "Per-column SET STATISTICS.", "Typical range 100-1000 documented."),
        ("Extended statistics?", "Multivariate ndistinct and dependencies on supported versions.", "CREATE STATISTICS for correlated columns.", "Helps AND of correlated filters.", "Requires analyze to populate."),
        ("n_distinct sign meaning?", "Positive absolute count; negative fraction of table.", "-1 often means unique.", "Planner scales with table growth.", "Check after bulk load."),
        ("MCV list?", "Most common values with frequencies.", "Helps equality predicates.", "Limited list length.", "Skewed status column example."),
        ("Histogram use?", "Range queries estimate selectivity.", "Bucket boundaries in pg_stats.", "Uneven buckets for skew.", "Combine with MCV."),
        ("ANALYZE vs VACUUM?", "Analyze updates planner stats.", "Vacuum reclaims tuples and can analyze.", "Both maintenance.", "Different goals."),
        ("Sampling bias?", "Small tables fully scanned.", "Very large tables sampled.", "Sudden data change needs manual analyze.", "After COPY analyze."),
        ("Security of pg_stats?", "Column-level privileges can hide stats.", "Leaks possible via functional dependencies awareness.", "Treat as sensitive on secret columns.", "Document access."),
        ("autovacuum analyze trigger?", "Insert/update/delete thresholds.", "scale_factor similar to vacuum.", "Can be per table.", "Tune hot tables."),
        ("pg_stats not matching reality?", "Stats are estimates.", "EXPLAIN ANALYZE shows actual.", "Increase target on problem columns.", "Consider extended stats."),
        ("Global stats extensions?", "pg_stat_statements for query runtime not column stats.", "Do not confuse.", "Both needed for tuning.", "Different catalogs."),
        ("Partition stats?", "Per child table stats.", "Parent may not have own rows.", "Analyze children after load.", "Pruning uses child stats."),
        ("Scenario: plan good in test bad prod?", "Prod data skew larger.", "Raise statistics on skewed col.", "Extended stats.", "Rebenchmark."),
        ("Scenario: analyze takes hours?", "Huge table high target.", "Lower target temporarily.", "Analyze sample partitions.", "Maintenance window."),
        ("Scenario: new enum value all rows?", "MCV outdated until analyze.", "Run analyze after backfill.", "Plans may seq scan.", "Expected until refreshed."),
        ("Scenario: join estimate off by 1000x?", "Correlated filters.", "CREATE STATISTICS.", "Rewrite join order.", "ANALYZE verbose."),
        ("Scenario: autovacuum analyze never?", "Table autovacuum disabled.", "Zero changes threshold not met.", "Manual analyze.", "Fix flags."),
        ("Scenario: security hide stats?", "REVOKE on column still may leak via plans.", "Use views carefully.", "Understand limits.", "Compliance review."),
    ]


def _t011():
    return [
        ("Default isolation in PostgreSQL?", "READ COMMITTED for new sessions unless changed.", "Each statement sees new snapshot in RC.", "Documented in SQL standard section with PostgreSQL notes.", "Not SERIALIZABLE by default."),
        ("REPEATABLE READ behavior?", "Single snapshot for transaction.", "Sees consistent reads.", "Serialization anomalies for write skew possible without SSI.", "Upgrade to SERIALIZABLE for strictness."),
        ("SERIALIZABLE in PostgreSQL?", "Uses Serializable Snapshot Isolation.", "May raise serialization_failure.", "Apps must retry.", "Stronger than RR for some anomalies."),
        ("Row lock on UPDATE?", "Locks updated row until transaction ends.", "Other updates wait or deadlock.", "SELECT does not lock row.", "FOR UPDATE locks explicitly."),
        ("SELECT FOR UPDATE?", "Locks rows for upcoming update.", "Prevents concurrent writers.", "Can skip locked rows with SKIP LOCKED.", "Queue workers pattern."),
        ("Deadlock detection?", "Cycle in lock waits aborted one txn.", "Error returned to client.", "Retry with backoff.", "Keep lock order consistent."),
        ("Predicate locking?", "Part of SSI for phantoms.", "Not full table locks.", "Tracks rw-dependencies.", "Documented anomaly prevention."),
        ("Read phenomena under RC?", "Non-repeatable read possible across statements.", "Phantom reads possible.", "Dirty read prevented.", "Know your isolation choice."),
        ("Lost update prevention?", "Use UPDATE with WHERE checks row version.", "Or SELECT FOR UPDATE.", "Optimistic locking column.", "Not automatic on plain UPDATE race."),
        ("DDL locking?", "Stronger locks than DML.", "ACCESS EXCLUSIVE blocks reads/writes on table.", "Short DDL preferred.", "Use lock_timeout."),
        ("Advisory vs row locks?", "Advisory app-defined.", "Row locks tied to tuples.", "Different namespaces.", "D09-T012 advisory."),
        ("idle in transaction locks?", "Held until commit.", "Blocks vacuum and DDL.", "Set timeouts.", "Pooler may not help session state."),
        ("Foreign key locking?", "Checks lock referenced rows.", "Deadlocks possible parent child order.", "Index FK columns.", "Understand insert order."),
        ("Scenario: serialization_failure spike?", "SSI conflicts under concurrent bookings.", "Retry logic required.", "Reduce transaction scope.", "Consider advisory serialize hot sku."),
        ("Scenario: deadlock on two updates?", "Opposite lock order.", "Fix application lock ordering.", "Log deadlock graphs.", "Short transactions."),
        ("Scenario: migration ACCESS EXCLUSIVE?", "Blocks app traffic.", "Use concurrent index create.", "Schedule low traffic.", "Statement_timeout on clients."),
        ("Scenario: phantom inventory?", "RR without SSI allows anomaly class.", "Use SERIALIZABLE or explicit locks.", "Test concurrency.", "Business acceptance."),
        ("Scenario: SKIP LOCKED workers?", "Each worker grabs different rows.", "Good job queue.", "Ensure idempotent processing.", "Index pending status."),
        ("Scenario: repeatable read report wrong?", "User expects statement fresh data.", "Wrong isolation level chosen.", "Switch to RC.", "Educate product."),
        ("Scenario: lock wait timeout?", "lock_timeout fired.", "Find blocker in pg_locks.", "Kill or fix slow txn.", "Tune timeout."),
    ]


def _t012():
    return [
        ("What are advisory locks?", "User-defined lock IDs in shared memory.", "pg_advisory_lock family functions.", "Not tied to table rows.", "Coordination primitive."),
        ("Session vs transaction scope?", "Session locks until unlock or disconnect.", "Transaction locks release at commit.", "Choose to avoid leaks.", "Document which you use."),
        ("pg_try_advisory_lock?", "Non-blocking attempt returns false if busy.", "Use backoff in apps.", "Better than waiting forever.", "Combine with metrics."),
        ("Two-key locks?", "pg_advisory_lock(int, int) namespaces pairs.", "Avoid collisions between teams.", "Document key registry.", "Ops runbook entry."),
        ("Pooler interaction?", "Transaction pooling resets session between txns.", "Session advisory locks unsafe in txn pool mode.", "Use session pool or DB-side jobs.", "D09-T015."),
        ("Versus row locks?", "Row locks enforce data integrity on tuples.", "Advisory for app-level mutex.", "Do not replace FK constraints.", "Complement when appropriate."),
        ("Deadlocks with advisory?", "Possible if circular wait.", "Same deadlock detector.", "Order lock acquisition.", "Keep critical sections short."),
        ("Monitoring?", "pg_locks locktype advisory.", "Join to activity.", "Alert long waits.", "Dashboard optional."),
        ("Cron duplicate runs?", "Try lock at job start.", "Skip if false.", "Prevents double billing.", "Classic pattern."),
        ("Migration singleton?", "Advisory lock during schema migration.", "Second deploy waits or exits.", "Better than table lock sometimes.", "Release on failure carefully."),
        ("64-bit keys?", "pg_advisory_lock(bigint) on supported APIs.", "More namespace space.", "Still document owners.", "Avoid random keys."),
        ("Unlock on exception?", "Session lock persists after error unless transaction-level.", "Use transaction locks or finally unlock.", "Connection return to pool dangerous.", "Test failure paths."),
        ("Scenario: two pods both lead?", "Missing advisory gate.", "Add try lock.", "One wins one backs off.", "Kubernetes lease alternative."),
        ("Scenario: lock stuck after crash?", "Session ended releases session locks.", "Transaction locks rolled back.", "Zombie rare.", "Restart backend if needed."),
        ("Scenario: same key two services?", "Collision causes mutual exclusion bugs.", "Central key registry.", "Prefix service id in high key.", "Code review."),
        ("Scenario: pgbouncer txn mode jobs?", "Locks do not span client txns as expected.", "Move job to session mode pool.", "Or use row locks.", "Architecture fix."),
        ("Scenario: performance of advisory?", "Lightweight compared to row lock storm.", "Still serializes section.", "Keep work tiny.", "Measure throughput."),
        ("Scenario: logical decoding and advisory?", "Locks not replicated.", "Each node independent.", "Do not rely cross-node.", "Use distributed lock service if needed."),
        ("Scenario: testing locks?", "Two psql sessions try lock.", "Verify second blocks or try false.", "Automate in integration test.", "Document expected."),
        ("Scenario: upgrade forgot unlock?", "Deploy stuck until disconnect.", "Use lock_timeout on acquisition.", "Health check fails.", "Fix finally blocks."),
    ]


def _t013():
    return [
        ("Physical streaming replication?", "Standby receives WAL stream and applies redo.", "Byte-level copy of cluster files logically via WAL.", "Hot standby allows reads on replica.", "Requires wal_level replica or higher."),
        ("Logical replication?", "Decodes WAL to row changes.", "Publication and subscription.", "Selective tables.", "wal_level logical required."),
        ("Replication slot?", "Prevents WAL removal until consumer acks.", "Monitor lag bytes.", "Orphan slot fills disk.", "pg_replication_slots view."),
        ("Synchronous replication?", "synchronous_standby_names waits for standby flush.", "Increases commit latency.", "Reduces data loss window.", "Policy per transaction possible on supported versions."),
        ("Primary vs standby promotion?", "Standby promoted to read-write.", "Timeline may increment.", "Clients reconnect.", "D09-T018."),
        ("Logical conflict?", "Subscriber may conflict on apply.", "Policies: error, skip, overwrite depending on config.", "Design keys carefully.", "Test failovers."),
        ("Initial sync logical?", "COPY snapshot then stream.", "Large tables take time.", "Monitor subscription state.", "Plan bandwidth."),
        ("Cascade replication?", "Chained standbys supported physically.", "Logical cascades possible with design.", "Lag accumulates.", "Topology planning."),
        ("Archive vs streaming?", "Archive is file copy for PITR.", "Streaming is continuous.", "Often both.", "D09-T017."),
        ("Read-only connection to primary?", "Always writable primary.", "Route reads to replicas with lag awareness.", "Proxy or driver target.", "D09-T016."),
        ("pg_hba and replication?", "Replication role connects for streaming.", "Security credentials.", "SSL common.", "Least privilege."),
        ("Timeline history?", "Promotion creates new timeline.", "pg_control tracks.", "Avoid split brain.", "Fencing old primary."),
        ("Scenario: slot lag terabytes?", "Consumer down.", "Drop or fix consumer.", "Emergency wal space.", "Alert early."),
        ("Scenario: logical schema drift?", "Subscriber missing column.", "Replication stops.", "Migrate subscriber first.", "Version contracts."),
        ("Scenario: async replica stale read?", "User complains stale UI.", "Route critical reads to primary.", "Or sync replica.", "Product decision."),
        ("Scenario: wal_level change?", "Requires restart typically.", "Plan maintenance.", "Cannot enable logical instantly.", "Read docs."),
        ("Scenario: cross-version replication?", "Supported within major version bands documented.", "Test upgrades.", "Logical may differ.", "Follow compatibility matrix."),
        ("Scenario: network partition primary standby?", "Async diverges.", "Sync may block commits.", "Failover policy chooses RPO.", "Runbook."),
        ("Scenario: subscription on production primary load?", "Decoding consumes resources.", "Monitor CPU.", "Dedicated replica for logical.", "Scale."),
        ("Scenario: promote during heavy write?", "Brief unavailability.", "Clients retry.", "Pooler flush.", "Practice drill."),
    ]


def _t014():
    return [
        ("Declarative partitioning?", "CREATE TABLE parent PARTITION BY.", "Children hold data.", "Planner prunes.", "PostgreSQL 10+ feature evolution documented."),
        ("RANGE vs LIST vs HASH?", "RANGE for time ids.", "LIST for enum regions.", "HASH for even split unclear range.", "Choose by query pattern."),
        ("Partition key requirement?", "Queries should filter on key for prune.", "Updates moving rows change partition.", "Unique constraints include key.", "Design early."),
        ("ATTACH PARTITION?", "Adds existing table as partition.", "Validates constraints.", "Fast for prebuilt data.", "ETL pattern."),
        ("DETACH PARTITION?", "Removes child for archival.", "Can CONCURRENTLY on supported versions.", "Keeps data file.", "Drop later."),
        ("Default partition?", "Catches non-matching rows.", "Prune may scan default always.", "Monitor overflow.", "Avoid catch-all growth."),
        ("Global unique index?", "Must include partition key.", "Enforce per child uniqueness.", "Design ids with time component.", "Common interviews."),
        ("Partition-wise join?", "Optimizer may join matching children.", "Needs compatible partitioning.", "Performance win.", "Not automatic always."),
        ("Maintenance per child?", "Vacuum and analyze per partition.", "Smaller units faster.", "Drop old monthly partition cheap.", "Ops win."),
        ("Constraint exclusion?", "Legacy name for prune concept.", "Check constraints on children.", "Planner proves exclusion.", "Still relevant term."),
        ("Too many partitions?", "Planning memory and open file cost.", "Hundreds ok, millions bad.", "Balance granularity.", "Benchmark open."),
        ("Scenario: query scans all partitions?", "Missing predicate on key.", "Fix SQL or add constraint.", "EXPLAIN shows all children.", "Common bug."),
        ("Scenario: insert wrong partition?", "No child accepts row.", "Error or default.", "Fix bounds.", "Migration."),
        ("Scenario: FK to partitioned table?", "Supported with limitations per version.", "Check docs.", "May reference parent.", "Test DDL."),
        ("Scenario: monthly roll automation?", "CREATE next month attach.", "Detach old to cold storage.", "Scripted job.", "Calendar runbook."),
        ("Scenario: partition key update?", "Row move between children expensive.", "Avoid updating key.", "Delete insert pattern.", "Design keys stable."),
        ("Scenario: stats on parent?", "Parent often empty.", "Analyze children.", "Autovacuum per child.", "Monitor each."),
        ("Scenario: BRIN on partitioned?", "Per child BRIN for time.", "Tiny indexes.", "Align load order.", "D09-T008."),
        ("Scenario: backup per partition?", "Logical copy one child.", "Physical still cluster.", "Archival detach then pg_dump.", "Hybrid."),
        ("Scenario: cross-partition aggregate?", "May gather all children.", "Parallel per child.", "Ensure prune.", "Aggregate precompute."),
    ]


def _t015():
    return [
        ("Why use PgBouncer?", "Multiplex many clients to fewer PostgreSQL backends.", "Reduces memory and process count.", "Hides connection churn from server.", "Common in microservices."),
        ("Session pooling mode?", "Server connection tied to client for client lifetime.", "Full PostgreSQL session features work.", "Less multiplexing benefit.", "Good for migrations."),
        ("Transaction pooling mode?", "Server connection assigned per transaction only.", "High density.", "Breaks session state across transactions.", "Stateless APIs."),
        ("Statement pooling mode?", "Rare; per statement.", "Very restrictive.", "Few apps compatible.", "Most use transaction."),
        ("Prepared statements issue?", "Named prepares bind to server session.", "Txn pooling may switch sessions.", "Disable server prepare or use session mode.", "Driver flags matter."),
        ("SET and temp tables?", "Lost between transactions in txn pool.", "Use session mode if needed.", "Or SET LOCAL per txn.", "Architectural constraint."),
        ("LISTEN NOTIFY?", "Requires persistent session.", "Incompatible with txn pooling for listeners.", "Dedicated session pool.", "Document."),
        ("Pool sizing?", "default_pool_size and max_client_conn.", "Server max_connections still caps.", "Leave headroom for admin.", "Monitor waits."),
        ("Odyssey pgcat alternatives?", "Same concepts different impl.", "Compare features.", "Still need mode discipline.", "Vendor eval."),
        ("RDS Proxy note?", "Managed pooling layer.", "Similar session semantics questions.", "IAM auth integration.", "Cloud specific."),
        ("Health checks?", "Pooler pings server.", "Removes bad backends.", "Apps see disconnect retry.", "Runbook."),
        ("TLS termination?", "Pooler may SSL to clients and server.", "Cert management.", "Compliance.", "Latency small."),
        ("Scenario: broken search_path?", "Txn pool resets session.", "Set each transaction.", "Or session mode.", "Migration fix."),
        ("Scenario: idle clients maxed?", "max_client_conn hit.", "Not same as server limit.", "Scale pooler.", "Client backoff."),
        ("Scenario: N+1 with pool?", "Still N queries.", "Pool does not batch SQL.", "Fix app.", "Do not blame pooler."),
        ("Scenario: admin DDL via pool?", "Use session mode direct.", "Avoid txn pool for long DDL.", "Separate admin URL.", "Ops practice."),
        ("Scenario: prepared plan leak?", "Many unique prepares exhaust memory.", "Use unnamed or disable.", "ORM config.", "Monitor."),
        ("Scenario: latency added?", "Small hop through pooler.", "Worth vs fork cost.", "Measure p99.", "Co-locate."),
        ("Scenario: multi-tenant pools?", "Pool per tenant vs shared.", "Isolation versus efficiency.", "Noisy neighbor.", "Architecture."),
        ("Scenario: failover VIP?", "Pooler must point new primary.", "DNS or config reload.", "With D09-T018.", "Automate."),
    ]


def _t016():
    return [
        ("Define replication lag?", "Standby replay LSN behind primary flush.", "Measured bytes or time.", "pg_stat_replication shows.", "User-visible staleness."),
        ("replay_lag vs write_lag?", "write_lag network to standby OS.", "flush_lag standby disk.", "replay_lag applied to queries.", "Different bottlenecks."),
        ("Causes of lag?", "Network bandwidth.", "Standby CPU replay.", "Heavy queries on standby.", "Maintenance vacuum on standby."),
        ("max_standby_streaming_delay?", "Cancel standby queries conflicting with apply.", "Or pause apply causing lag.", "Tune trade-off.", "Document behavior."),
        ("Synchronous commit lag?", "Waits for remote flush.", "Not lag but latency.", "Different metric.", "RPO improvement."),
        ("Monitoring?", "Alert lag bytes threshold.", "Grafana from pg_stat_replication.", "Time since replay timestamp.", "Business SLO."),
        ("Read routing?", "Stale reads if async.", "Critical reads to primary.", "Lag-aware routing libraries.", "Product choice."),
        ("Lag during bulk load?", "WAL spike.", "Replica may fall behind.", "Throttle load or pause reads.", "Expected."),
        ("Slot lag?", "Logical consumer slow.", "WAL retained.", "Disk risk on primary.", "D09-T013."),
        ("Replay pause?", "Hot standby conflict policy.", "Queries canceled.", "Lag grows.", "Fix long standby queries."),
        ("Scenario: replica p99 high?", "Replay or query contention.", "Check replay lag first.", "Separate read workload.", "Hardware."),
        ("Scenario: lag zero but stale?", "Clock skew metric wrong.", "Use LSN bytes.", "Application cache.", "Not replication."),
        ("Scenario: promote with lag?", "Lose last seconds data async.", "Accept RPO.", "Force sync for zero.", "Runbook."),
        ("Scenario: cross-region lag?", "Physics latency.", "Async only realistic.", "Global app design.", "CDN not DB."),
        ("Scenario: vacuum on primary affects lag?", "More WAL generated.", "Indirectly yes.", "Bulk vacuum plan.", "Monitor."),
        ("Scenario: small instance replica?", "Undersized replay CPU.", "Scale replica.", "Match primary class.", "Cost."),
        ("Scenario: monitoring replay timestamp null?", "Not in recovery or not streaming.", "Check recovery mode.", "Connectivity.", "Fix replica."),
        ("Scenario: lag alert flapping?", "Threshold too tight.", "Use smoothed metric.", "Bursty workload.", "Tune."),
        ("Scenario: read your writes?", "Need primary or sync.", "Laggy replica fails.", "Session stickiness.", "Design."),
        ("Scenario: logical lag?", "Subscription apply delay.", "Different views.", "pg_stat_subscription.", "Fix apply errors."),
    ]


def _t017():
    return [
        ("pg_basebackup purpose?", "Physical cluster copy for standby or PITR base.", "Includes data files and backup_label.", "Taken online with WAL continuity.", "Foundation of physical DR."),
        ("WAL archive for PITR?", "Continuous segment archive to storage.", "Restore base then replay to target time.", "RPO gap if archive missing.", "Test chain."),
        ("pg_dump vs physical?", "Logical SQL or custom format portable.", "Physical faster restore huge DB.", "Choose per RTO RPO.", "Often both."),
        ("recovery_target_time?", "Stop replay at timestamp in recovery.conf parameters on version-specific config.", "Verify timezone.", "Document procedure per version.", "Practice restore."),
        ("Backup validation?", "Restore to scratch monthly.", "Untested backup is hope.", "Automate verify.", "Compliance."),
        ("Tablespace backup?", "Include all dirs.", "Missing tablespace breaks restore.", "Inventory paths.", "Ops checklist."),
        ("Encryption?", "Encrypt backups at rest.", "TLS in transit.", "Key management.", "Security review."),
        ("Retention?", "GFS rotation.", "Legal hold.", "WAL retention matches.", "Cost."),
        ("Snapshot storage backup?", "Crash consistent if quiesced or use fs snapshot APIs.", "Still need WAL.", "Cloud EBS snapshots common.", "Freeze or use backup tool."),
        ("Point-in-time limits?", "Cannot recover before oldest base.", "WAL must cover window.", "Gap means failure.", "Monitor archive."),
        ("Scenario: restore missing WAL?", "Recovery stops.", "Find segment in archive.", "Re-seed from new base.", "Postmortem."),
        ("Scenario: pg_dump during peak?", "Load and locks.", "Use replica logical dump.", "Schedule off peak.", "Directory format parallel."),
        ("Scenario: corrupt base backup?", "Checksum verify.", "Retake backup.", "Multiple copies.", "Detect early."),
        ("Scenario: RTO 15 minutes?", "Pre-staged standby promotion faster than restore.", "HA not backup substitute.", "Combine strategies.", "D09-T018."),
        ("Scenario: accidental DROP?", "PITR to before drop.", "Need WAL and base.", "Promote recovered instance.", "Swap DNS."),
        ("Scenario: major version upgrade backup?", "Logical or pg_upgrade path.", "Test restore on new major.", "Plan rollback.", "Docs."),
        ("Scenario: partial table restore?", "Logical dump table.", "Physical is whole cluster.", "Choose tool.", "Time."),
        ("Scenario: backup locks?", "pg_dump ACCESS SHARE.", "Long dump on busy table ok mostly.", "Replication slots.", "Monitor."),
        ("Scenario: cloud auto backup?", "Vendor PITR window.", "Understand retention.", "Exit strategy.", "Test export."),
        ("Scenario: ransomware?", "Immutable offsite backups.", "Air gap.", "Separate credentials.", "Incident plan."),
    ]


def _t018():
    return [
        ("HA goal?", "Survive primary failure with minimal downtime.", "Often RPO RTO targets.", "Combines replication monitoring promotion.", "Not only backup."),
        ("Patroni style?", "DCS etcd consul for leader election.", "Automates failover.", "Fencing old primary.", "Common pattern."),
        ("VIP or DNS switch?", "Clients point to stable name.", "TTL affects failover speed.", "Pooler reload config.", "App retry."),
        ("Split brain risk?", "Two primaries write diverge.", "STONITH or fencing.", "Never promote twice blindly.", "Runbook."),
        ("Synchronous standby in HA?", "Zero data loss goal.", "Commit latency cost.", "Quorum commit policies.", "Regional design."),
        ("Witness node?", "Break tie in quorum.", "Lightweight.", "Not data store.", "Election only."),
        ("Health checks?", "HTTP API patroni.", "Load balancer checks.", "False positive causes flip.", "Tune carefully."),
        ("Failback?", "Return to old primary after fix.", "Rebuild as replica.", "Re-sync data.", "Planned."),
        ("Multi-region HA?", "Async replication lag.", "Manual promotion cross region.", "Global traffic routing.", "Complex."),
        ("Managed cloud HA?", "Multi-AZ automatic.", "Less control.", "Understand failover impact.", "Vendor SLA."),
        ("Application retries?", "Transient connection errors on failover.", "Exponential backoff.", "Idempotent writes.", "Required."),
        ("Connection pooler on failover?", "Must drain and reconnect.", "Session loss.", "Brief outage window.", "Coordinate."),
        ("Scenario: brain split after network?", "Two writers.", "Data divergence.", "Fencing required.", "Restore from backup worst case."),
        ("Scenario: failover test quarterly?", "Measure actual RTO.", "Document gaps.", "Fix DNS TTL.", "Compliance."),
        ("Scenario: promoted standby too old?", "Async lag lost commits.", "Business accepts RPO.", "Use sync for critical.", "Communicate."),
        ("Scenario: etcd down patroni?", "No automatic failover.", "Monitor DCS.", "Redundant DCS.", "Ops."),
        ("Scenario: load balancer stale primary?", "Writes hit dead node.", "Health check fix.", "Multiple LB layers.", "Urgent."),
        ("Scenario: rolling upgrade HA?", "Switchover planned.", "Reduce downtime.", "Version compatibility.", "Test."),
        ("Scenario: disaster whole region?", "DR region promote.", "DNS global.", "Large RPO if async.", "Insurance."),
        ("Scenario: human operator promote mistake?", "Runbook approvals.", "Break glass credentials.", "Audit log.", "Training."),
    ]


CORES = {
    "D09-T007": _t007(),
    "D09-T008": _t008(),
    "D09-T009": _t009(),
    "D09-T010": _t010(),
    "D09-T011": _t011(),
    "D09-T012": _t012(),
    "D09-T013": _t013(),
    "D09-T014": _t014(),
    "D09-T015": _t015(),
    "D09-T016": _t016(),
    "D09-T017": _t017(),
    "D09-T018": _t018(),
}

"""D09-T006..D09-T018 specs."""
from d09_pack_rest import BASE_DEPS, PACK  # noqa: F401
from d09_pack_rest import _topic, follow_wal, para, std_k, tbl

PACK2: list[dict] = []

# D09-T006
PACK2.append(
    _topic(
        "D09-T006",
        "Dead tuples and table bloat",
        "d09-t006-dead-tuples-and-table-bloat.md",
        ["D09-T005", *BASE_DEPS],
        "d09_t006_bloat.sql",
        "SELECT schemaname, relname, n_live_tup, n_dead_tup, pg_size_pretty(pg_total_relation_size(relid)) AS total FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 10;",
        para("Dead tuples are obsolete row versions MVCC keeps until vacuum.", "Bloat is wasted space in heap and indexes.", "HOT updates avoid new index entries when conditions allow.", "fillfactor reserves page space for HOT chains."),
        para("UPDATE-heavy workloads create dead tuples faster than vacuum reclaims.", "Indexes point to all versions until vacuum cleans.", "Table size on disk can grow while live rows stay flat.", "Monitoring n_dead_tup is the first signal."),
        para("HOT requires updated columns not indexed and free space on same page.", "Page splits and wide indexes reduce HOT rate.", "pgstattuple extension gives page-level detail on supported installs.", "REINDEX or pg_repack address index bloat separately."),
        """```mermaid
flowchart TD
  update[UpdateRow]
  dead[DeadTupleLeft]
  hot{HOTPossible}
  indexChurn[IndexUpdate]
  update --> dead
  dead --> hot
  hot -->|no| indexChurn
  hot -->|yes| samePage[SamePageChain]
```""",
        para("Bloat is attic junk after remodel; vacuum sweeps.", "HOT is updating a sticky note on the same page.", "Do not assume autovacuum alone fixes index bloat.", "Do not lower fillfactor everywhere blindly."),
        para("Tune autovacuum on hot tables.", "Reduce update width and indexed columns.", "Use partial indexes carefully.", "Schedule repack for large bloat after fixing leaks."),
        tbl("| lower fillfactor | More HOT room | More empty space | HOT-heavy narrow updates | Sequential scan heavy |", "| aggressive vacuum | Less dead data | IO | Steady OLTP | Batch ETL windows |"),
        "- Blaming vacuum for app txn leaks.\n- REINDEX without fixing churn.\n- Ignoring index bloat.",
        "pg_total_relation_size grows; n_dead_tup high; autovacuum running but file huge—check index sizes and HOT ratio.",
        std_k(
            "bloat",
            [
                ("What is a dead tuple?", "Row version no longer visible to any snapshot.", "Still occupies space.", "Vacuum reclaims.", "Created by UPDATE/DELETE."),
                ("What is table bloat?", "Disk larger than live data needs.", "Dead tuples and fragmentation.", "May remain after vacuum.", "FULL/repack shrinks file."),
                ("What is HOT?", "Heap-only tuple update on same page without new index entries.", "Needs free space and no indexed changed cols.", "Reduces index churn.", "Not always possible."),
                ("fillfactor purpose?", "Leaves page free space for updates.", "Default often 100 for analytics tables.", "Lower for hot narrow updates.", "Trade scan efficiency."),
                ("Heap vs index bloat?", "Heap vacuum reclaims tuples.", "Indexes may bloat separately.", "REINDEX fixes index.", "Both matter."),
                ("Measure bloat?", "n_dead_tup ratio.", "pgstattuple/pg_squeeze tools.", "Compare live vs size.", "Trend over time."),
                ("Why bloat after DELETE?", "Space marked reusable not returned to OS.", "Normal vacuum behavior.", "FULL if must shrink file.", "Plan maintenance."),
                ("Long txn effect?", "Blocks vacuum horizon.", "Dead tuples accumulate.", "Classic bloat cause.", "Fix sessions."),
                ("Wide rows impact?", "Fewer tuples per page.", "More IO per update.", "TOAST for large values.", "D09-T007."),
                ("Autovacuum not enough?", "Thresholds too loose.", "IO throttled.", "Table too large single worker.", "Tune or manual."),
                ("pg_repack vs FULL?", "Repack online with locks brief.", "FULL exclusive lock.", "Choose per SLA.", "Both rewrite."),
                ("Update same column indexed?", "Disables HOT for that col.", "Index always new entry.", "Design indexes.", "Covering indexes cost."),
                ("Monitoring alerts?", "dead_tup fraction.", "Table size growth rate.", "Autovacuum age.", "Disk usage."),
                ("Partitioning help?", "Smaller vacuum units.", "Drop old partitions.", "D09-T014.", "Archival pattern."),
                ("ORM save() every field?", "Updates all columns.", "Breaks HOT.", "Patch only changes.", "Performance win."),
                ("Scenario: 100GB table 5M live rows?", "Massive bloat or wide rows.", "Check dead ratio.", "Repack plan.", "Fix update pattern."),
                ("Scenario: index bigger than heap?", "Index bloat or redundant indexes.", "REINDEX.", "Drop unused.", "Analyze queries."),
                ("Scenario: vacuum runs but size flat?", "Expected without FULL.", "Check bloat tools.", "Accept or repack.", "Educate stakeholders."),
                ("Scenario: HOT ratio zero?", "Indexed updates or no page space.", "Lower fillfactor.", "Reduce indexed cols.", "Measure pg_stat."),
                ("Scenario: nightly job DELETE millions?", "Spike dead tuples.", "Run vacuum after.", "Partition drops.", "Batch deletes."),
            ],
        ),
        "Report top dead tuple tables.", "Explain missing HOT on indexed update.", "Choose fillfactor for hot narrow table.",
        ["Dead tuples from MVCC.", "Vacuum reclaims.", "HOT reduces index work.", "Bloat is disk overhead.", "fillfactor tuning."],
        "After `D09-T005`. With `D09-T007` storage.",
        ["Define dead tuple.", "Explain HOT prerequisites.", "Read n_dead_tup stats.", "Contrast vacuum vs FULL shrink.", "Propose ORM fix for bloat."],
        "1. Dead tuple report.\n2. HOT failure analysis.\n3. fillfactor trade-off.",
        "### Exercise 1\nList tables where n_dead_tup > n_live_tup.\n\n### Exercise 2\nIndexed UPDATE prevents HOT; suggest schema change.\n\n### Exercise 3\nfillfactor 70 on hot table: more HOT, larger heap scans—document.",
    )
)

# Remaining topics 007-018 in compact generator
_META = [
    (
        "D09-T007",
        "Heap storage and TOAST",
        "d09-t007-heap-storage-and-toast.md",
        ["D09-T006", *BASE_DEPS],
        "d09_t007_toast.sql",
        "SELECT attname, attstorage, attlen FROM pg_attribute WHERE attrelid = 'large_payload'::regclass;",
        "Heap pages store line pointers to tuples; oversized varlena values go to TOAST side tables with compression and out-of-line storage strategies.",
        "Page layout includes header, line pointers, tuple data; updates can move tuples within or across pages.",
        "TOAST strategies: plain, extended, external, main; ALTER COLUMN STORAGE sets preference.",
        """```mermaid
flowchart TD
  heapPage[HeapPage]
  tuple[HeapTuple]
  toast[TOASTTable]
  heapPage --> tuple
  tuple -->|oversized| toast
```""",
        "TOAST is overflow parking for wide values.", "Large JSON blobs often toast.", "Do not SELECT * on huge columns casually.", "toast_tuple_target tunable per column.",
        "Watch table bloat on toast tables.", "Index only needed JSON keys.", "Use appropriate text/json types.", "Consider external object store for blobs.",
        tbl("| compress TOAST | Saves space | CPU | Large text/json | Hot tiny reads |"),
        "- Fetching * on wide rows.\n- Ignoring toast table bloat.\n- Wrong storage strategy.",
        "Slow selects on wide rows; check column lengths and EXPLAIN buffers.",
    ),
    (
        "D09-T008",
        "B-tree, GIN, GiST and BRIN indexes",
        "d09-t008-b-tree-gin-gist-and-brin-indexes.md",
        ["D09-T007", *BASE_DEPS],
        "d09_t008_indexes.sql",
        "SELECT indexrelid::regclass, idx_scan, idx_tup_read FROM pg_stat_user_indexes ORDER BY idx_scan DESC LIMIT 10;",
        "B-tree is default for equality and range; GIN for inverted multi-entry (full text, jsonb paths); GiST for geometric and custom opclasses; BRIN for very large naturally ordered tables.",
        "Each index type has different build, size, and query patterns.",
        "Planner chooses index scans based on stats and costs (D09-T009).",
        """```mermaid
flowchart LR
  query[QueryPredicate]
  btree[BtreeIndex]
  gin[GINIndex]
  gist[GiSTIndex]
  brin[BRINIndex]
  query --> btree
  query --> gin
  query --> gist
  query --> brin
```""",
        "B-tree is sorted catalog; GIN is book index terms; BRIN is coarse map of ranges.", "Match index to operator class.", "Do not GIN everything.", "Partial indexes reduce size.",
        "Audit unused indexes via idx_scan.", "Create concurrent indexes on prod.", "Understand INCLUDE columns on btree where supported.", "REINDEX after bulk load corruption.",
        tbl("| GIN on jsonb | Fast containment | Large build | JSON queries | Low selectivity |"),
        "- Wrong opclass.\n- Duplicate indexes.\n- Missing index on FK.",
        "Seq scan on huge table—check stats and index presence.",
    ),
    (
        "D09-T009",
        "Query planner and optimizer",
        "d09-t009-query-planner-and-optimizer.md",
        ["D09-T008", *BASE_DEPS],
        "d09_t009_planner.sql",
        "EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE user_id = 1 AND created_at > now() - interval '7 days';",
        "Planner generates paths: sequential scan, index scan, joins (nested loop, hash, merge).",
        "Cost model uses cpu_operator_cost, seq_page_cost, random_page_cost—not magic constants; tune carefully.",
        "Statistics drive row estimates (D09-T010).",
        """```mermaid
flowchart TD
  sql[SQLQuery]
  rewrite[RewriteRules]
  paths[GeneratePaths]
  cost[EstimateCosts]
  plan[ChosenPlan]
  sql --> rewrite --> paths --> cost --> plan
```""",
        "Planner picks cheapest estimated plan, not always correct.", "EXPLAIN ANALYZE compares estimate vs actual.", "Do not spam enable_seqscan off.", "Join order matters.",
        "Fix bad plans with stats, indexes, query rewrite.", "Use pg_stat_statements.", "Consider prepared plan stability.", "Partition pruning D09-T014.",
        tbl("| generic plan | Stable | Wrong for skew | ORMs | Data skew |"),
        "- Blaming planner without ANALYZE.\n- Missing stats on join columns.",
        "Estimated rows 1 actual 1M—update stats or increase statistics target.",
    ),
    (
        "D09-T010",
        "Statistics and ANALYZE",
        "d09-t010-statistics-and-analyze.md",
        ["D09-T009", *BASE_DEPS],
        "d09_t010_analyze.sql",
        "SELECT attname, n_distinct, most_common_vals FROM pg_stats WHERE tablename = 'orders' AND attname = 'status';",
        "ANALYZE samples table to build histograms and distinct counts in pg_stats.",
        "Planner uses stats for selectivity estimates.",
        "default_statistics_target and extended statistics (dependencies, multivariate) improve hard cases on supported versions.",
        """```mermaid
flowchart TD
  analyze[ANALYZECommand]
  sample[RandomSample]
  pgstats[pg_stats]
  planner[PlannerEstimates]
  analyze --> sample --> pgstats --> planner
```""",
        "Stats are guesses from samples; stale stats cause bad plans.", "Autovacuum can analyze.", "Do not disable analyze.", "After bulk load run ANALYZE.",
        "Monitor last_analyze.", "Increase target on skewed columns.", "Use extended stats for correlated cols.", "Security: hide stats with column privileges.",
        tbl("| higher statistics_target | Better estimates | Slower analyze | Skewed columns | Tiny tables |"),
        "- Never analyzing after migration.\n- Trusting n_distinct -1 blindly.",
        "Plan flip after deploy—check stats freshness.",
    ),
    (
        "D09-T011",
        "Isolation and row-level locking",
        "d09-t011-isolation-and-row-level-locking.md",
        ["D09-T010", *BASE_DEPS],
        "d09_t011_isolation.sql",
        "SHOW transaction_isolation; SELECT * FROM pg_locks WHERE NOT granted;",
        "PostgreSQL default isolation is READ COMMITTED; REPEATABLE READ and SERIALIZABLE available.",
        "Writers take row-level locks; SELECT FOR UPDATE locks explicitly.",
        "SSI implements true serializable on supported versions with serialization_failure retries.",
        """```mermaid
flowchart TD
  txn[Transaction]
  snap[Snapshot]
  rowlock[RowLockOnWrite]
  txn --> snap
  txn --> rowlock
```""",
        "MVCC handles read consistency; locks handle write conflicts.", "Deadlocks detected automatically.", "Do not mix isolation levels randomly.", "Advisory locks separate D09-T012.",
        "Set isolation per transaction needs.", "Retry on serialization_failure.", "Keep transactions short.", "Use lock timeouts.",
        tbl("| SELECT FOR UPDATE | Prevents lost updates | Blocks readers of those rows | Checkout flows | Read-mostly |"),
        "- Expecting RR without phantom policy knowledge.\n- Long locks from app bugs.",
        "pg_locks not granted—find blocker pid.",
    ),
    (
        "D09-T012",
        "Advisory locks",
        "d09-t012-advisory-locks.md",
        ["D09-T011", *BASE_DEPS],
        "d09_t012_advisory.sql",
        "SELECT pg_try_advisory_lock(42); SELECT pg_advisory_unlock(42);",
        "Advisory locks are application-defined mutexes in shared memory.",
        "Session or transaction scoped variants exist.",
        "Use for job coordination—not substitute for row locks on business data.",
        """```mermaid
flowchart TD
  app[ApplicationWorker]
  advlock[pg_advisory_lock]
  app --> advlock
```""",
        "Like numbered bathroom keys for workers.", "Poolers break session locks in transaction mode.", "Always unlock or use transaction level.", "Do not collide on key namespaces.",
        "Namespace keys per service.", "Use try locks with backoff.", "Document key ranges.", "Monitor lock waits.",
        tbl("| advisory lock | Lightweight coordination | App discipline required | Cron dedup | Financial row updates |"),
        "- Same lock id across services.\n- Forgetting unlock on error paths with session locks.",
        "Stuck job—check pg_locks for advisory.",
    ),
    (
        "D09-T013",
        "Streaming and logical replication",
        "d09-t013-streaming-and-logical-replication.md",
        ["D09-T012", *BASE_DEPS],
        "d09_t013_replication.sql",
        "SELECT application_name, state, sent_lsn, write_lsn, flush_lsn, replay_lsn FROM pg_stat_replication;",
        "Physical streaming ships WAL to standbys; logical decoding ships row changes via publications.",
        "Requires wal_level replica or logical as documented.",
        "Slots retain WAL for consumers.",
        """```mermaid
flowchart LR
  primary[Primary]
  walstream[WALStream]
  standby[PhysicalStandby]
  logical[LogicalSubscriber]
  primary --> walstream --> standby
  primary --> logical
```""",
        "Streaming is byte-for-byte redo; logical is change events.", "Do not delete slots casually.", "Failover promotes standby D09-T018.", "Conflicts on logical apply possible.",
        "Monitor replication lag.", "Sync replicas for RPO.", "Test failover.", "Publication row filters on supported versions.",
        tbl("| logical replication | Selective tables | Conflicts to handle | CDC to warehouses | Full DB clone |"),
        "- wal_level too low.\n- Orphan slots filling disk.",
        "replay_lsn stuck—network or conflict.",
    ),
    (
        "D09-T014",
        "Table partitioning",
        "d09-t014-table-partitioning.md",
        ["D09-T013", *BASE_DEPS],
        "d09_t014_partition.sql",
        "SELECT relname, relkind FROM pg_class WHERE relname LIKE 'events_%';",
        "Declarative partitioning by RANGE, LIST, or HASH splits one logical table into partitions.",
        "Planner prunes partitions when constraints prove safety.",
        "Attach/detach for archival patterns.",
        """```mermaid
flowchart TD
  parent[PartitionedParent]
  p2024[Partition2024]
  p2025[Partition2025]
  parent --> p2024
  parent --> p2025
```""",
        "Like filing cabinets by year.", "Must include partition key in constraints.", "Global unique indexes need include partition key.", "Wrong prune causes scan all children.",
        "Choose key aligned to queries.", "Default partition catch-all carefully.", "Maintenance per child.", "Exchange partition for bulk load.",
        tbl("| range by time | Easy drop old data | Many partitions | Event logs | Small uniform table |"),
        "- Too many partitions.\n- Missing constraint exclusion.",
        "Slow query—EXPLAIN shows all partitions scanned.",
    ),
    (
        "D09-T015",
        "Connection poolers",
        "d09-t015-connection-poolers.md",
        ["D09-T014", *BASE_DEPS],
        "d09_t015_pooler.md",
        "-- PgBouncer concepts: pool_mode session, transaction, statement",
        "PgBouncer and similar poolers multiplex clients onto fewer PostgreSQL backends.",
        "Modes: session (full features), transaction (reset between txn), statement (rare).",
        "Prepared statements and temp tables break in transaction pooling without care.",
        """```mermaid
flowchart TD
  apps[ManyAppConnections]
  pooler[PgBouncer]
  pg[PostgreSQLBackends]
  apps --> pooler --> pg
```""",
        "Pooler is nightclub line controlling entry.", "Not a query cache.", "Size server max_connections to pool defaults.", "Use session mode for migrations.",
        "Place pooler close to DB.", "Disable server-side prepare in txn mode for some drivers.", "Monitor wait queues.", "Separate pools per service.",
        tbl("| transaction pooling | High density | Breaks session state | Stateless APIs | LISTEN/NOTIFY chat |"),
        "- Pool mode mismatch with ORM.", "Oversized server pools defeating pooler.",
        "Broken prepared statements—check pool mode.",
    ),
    (
        "D09-T016",
        "Replication lag",
        "d09-t016-replication-lag.md",
        ["D09-T015", *BASE_DEPS],
        "d09_t016_lag.sql",
        "SELECT now() - pg_last_xact_replay_timestamp() AS replay_delay;",
        "Lag is bytes behind LSN or time since last replay on standby.",
        "Causes: network, replay CPU, hot standby conflicts, long queries on standby.",
        "Synchronous_commit and synchronous_standby_names reduce commit visibility lag at cost.",
        """```mermaid
flowchart TD
  primaryLSN[PrimaryFlushLSN]
  replayLSN[StandbyReplayLSN]
  gap[LagBytesOrTime]
  primaryLSN --> gap
  replayLSN --> gap
```""",
        "Lag is debt between primary and replica truth.", "Read your writes needs routing.", "Do not use laggy replica for critical reads without acceptance.", "Monitor continuously.",
        "Alert on lag thresholds.", "Cap standby max_standby_streaming_delay.", "Hardware match replay.", "Load balance reads carefully.",
        tbl("| async replica | Cheap | Stale reads | Analytics | Strong consistency reads |"),
        "- Ignoring lag during failover.", "Heavy queries on standby slowing replay.",
        "User sees old data—check replica routing.",
    ),
    (
        "D09-T017",
        "Backup and recovery",
        "d09-t017-backup-and-recovery.md",
        ["D09-T016", *BASE_DEPS],
        "d09_t017_backup.sql",
        "SELECT * FROM pg_control_checkpoint(); -- pair with base backups and WAL archive",
        "Physical base backup (pg_basebackup) plus WAL archive enables PITR.",
        "Logical backups (pg_dump) are portable but different RPO/RTO.",
        "Test restores regularly; backups untested are guesses.",
        """```mermaid
flowchart LR
  base[BaseBackup]
  walarch[WALArchive]
  restore[RestorePITR]
  base --> restore
  walarch --> restore
```""",
        "Base backup is snapshot; WAL is forward journal.", "RPO defined by archive gap.", "Do not store only on same disk.", "Encryption and access control matter.",
        "Automate backups.", "Monitor archive failures.", "Document recovery runbook.", "Align with D09-T018 failover.",
        tbl("| pg_dump logical | Simple | Slow restore big DB | Small/medium | Multi-TB OLTP |"),
        "- No WAL archive with PITR claim.", "Deleting WAL needed for recovery.",
        "Restore drill fails—find missing WAL segment.",
    ),
    (
        "D09-T018",
        "High availability and failover",
        "d09-t018-high-availability-and-failover.md",
        ["D09-T017", *BASE_DEPS],
        "d09_t018_ha.sql",
        "SELECT pg_is_in_recovery(), pg_last_wal_receive_lsn();",
        "HA combines replication, monitoring, and promotion of standby to primary.",
        "Tools like Patroni, repmgr, or cloud RDS Multi-AZ automate failover.",
        "Split-brain prevented with leader election and STONITH/fencing.",
        """```mermaid
flowchart TD
  primary[Primary]
  standby[Standby]
  monitor[HAController]
  monitor --> primary
  monitor --> standby
  standby -->|promote| newPrimary[NewPrimary]
```""",
        "Failover is changing who is primary, not magic sync.", "Clients must reconnect via VIP or service discovery.", "Test failover quarterly.", "Synchronous replicas affect commit latency.",
        "Define RTO/RPO.", "Use connection strings with targets.", "Avoid dual-primary.", "Pooler must follow new primary.",
        tbl("| sync replication | Zero data loss goal | Latency | Financial primary | Distant DR only async |"),
        "- Promoting stale standby.", "DNS TTL too long.",
        "Outage after failover—apps point to old primary IP.",
    ),
]

from d09_k_cores import CORES  # noqa: E402

for m in _META:
    tid, name, slug, deps, sqlf, sql, ov, fr, intr, mmd, ex, pr, tb, mis, dbg = m
    if tid == "D09-T015":
        sql = "SELECT 1; -- poolers are configured outside SQL; document PgBouncer pool_mode in ops repo"
    core = CORES[tid]
    PACK2.append(
        _topic(
            tid,
            name,
            slug,
            list(deps),
            sqlf,
            sql,
            para(ov),
            para(fr),
            para(intr),
            mmd,
            para(ex),
            para(pr),
            tbl(tb) if tb.startswith("|") else tbl(tb),
            mis,
            dbg,
            std_k(tid, core),
            f"Run lab SQL for {tid} and document observations.",
            f"Debug scenario related to {name}.",
            f"Trade-off essay for {name}.",
            [f"{name} key point {x}" for x in range(1, 6)],
            f"Links around `{tid}` in PostgreSQL internals path.",
            [
                f"Explain {name} in production.",
                "Read lab SQL output.",
                "Name one failure mode.",
                "Name one trade-off.",
                "Answer five beginner interview questions.",
            ],
            f"1. Lab.\n2. Debug.\n3. Trade-off for {tid}.",
            f"### Solutions {tid}\nSee section K and note body; tailor to your cluster version.",
        )
    )

"""D09-T003..D09-T018 topic specs for build_d09_remaining.add."""
from __future__ import annotations


def para(*s: str) -> str:
    return " ".join(s)


def qa(q: str, s1: str, s2: str, s3: str, s4: str):
    return (q, para(s1, s2, s3, s4))


def tbl(*rows: str) -> str:
    head = "| Choice | Benefit | Cost | Choose when | Avoid when |\n| --- | --- | --- | --- | --- |\n"
    return head + "\n".join(rows)


def ib(lines: list[str]) -> str:
    return "\n".join(f"{i}. {t}" for i, t in enumerate(lines, 1))


def k23(questions: list[tuple[str, str, str, str, str]]) -> dict:
    assert len(questions) == 23
    return {
        "beginner": [qa(q, *a) for q, *a in questions[0:5]],
        "intermediate": [qa(q, *a) for q, *a in questions[5:10]],
        "advanced": [qa(q, *a) for q, *a in questions[10:15]],
        "scenarios": [qa(q, *a) for q, *a in questions[15:20]],
        "followups": [qa(q, *a) for q, *a in questions[20:23]],
    }


# Shared answer patterns for follow-ups reused with topic-specific tail
def follow_wal():
    return [
        ("How does this topic relate to WAL?", "Data page changes are logged before or as part of durability rules.", "Commit records wait on WAL persistence according to synchronous_commit.", "Replicas and PITR read the same WAL stream.", "See D09-T003 for record types and writers."),
        ("How does vacuum interact?", "Vacuum reclaims dead heap tuples and freezes xids.", "It does not replace WAL for durability.", "Heavy vacuum increases I/O alongside WAL writes.", "See D09-T005."),
        ("How do poolers change the picture?", "Poolers do not bypass WAL or storage on the server.", "They change how many backends run concurrent SQL.", "Session features may break under transaction pooling.", "See D09-T015."),
    ]


PACK: list[dict] = []

# --- D09-T003 WAL ---
PACK.append(
    {
        "id": "D09-T003",
        "name": "WAL (Write-Ahead Logging)",
        "subdomain": "WAL (Write-Ahead Logging)",
        "file": "d09-t003-wal-write-ahead-logging.md",
        "deps": ["D09-T002", "D09-T001", "D07-T001", "D07-T002", "D08-T001", "D08-T002"],
        "sql_file": "d09_t003_wal.sql",
        "sql": "SELECT pg_current_wal_lsn(), pg_walfile_name(pg_current_wal_lsn());\nSHOW wal_level;\nSHOW synchronous_commit;",
        "overview": para(
            "Write-Ahead Logging (WAL) is PostgreSQL's durability journal: changes to heap and index pages are described in append-only WAL before the corresponding data files are considered committed.",
            "Each WAL record has a Log Sequence Number (LSN) ordering all changes.",
            "On commit, the transaction waits until its commit record is flushed to disk subject to synchronous_commit policy.",
            "WAL also feeds physical replication and point-in-time recovery (D09-T013, D09-T017).",
        ),
        "first": para(
            "If PostgreSQL wrote data files first and crashed mid-write, pages could be torn or inconsistent.",
            "Logging intent to WAL allows crash recovery to replay or undo work from the last consistent checkpoint (D09-T004).",
            "Backends insert WAL into shared WAL buffers; the WAL writer flushes buffers to segment files under pg_wal.",
            "The rule is log first, then apply changes to shared buffers, then eventually checkpoint dirty pages to data files.",
        ),
        "internal": para(
            "WAL records describe heap/index modifications, commits, aborts, and structural changes.",
            "full_page_writes (when enabled) can log entire page images after checkpoint to guard against partial page writes—default varies by version; confirm on your cluster.",
            "wal_level controls how much is logged: minimal, replica, or logical (names and semantics documented per version).",
            "synchronous_commit trades durability latency: off or local modes may acknowledge before remote flush depending on settings.",
            "Archiving copies completed segments for backup chains.",
        ),
        "mermaid": """```mermaid
flowchart LR
  backend[BackendDML]
  walbuf[SharedWALBuffers]
  walwriter[WALWriter]
  walfiles[WALSegmentFiles]
  databuf[SharedDataBuffers]
  datafiles[DataFiles]
  backend --> walbuf
  walbuf --> walwriter
  walwriter --> walfiles
  backend --> databuf
  databuf --> datafiles
```""",
        "examples": para(
            "Analogy: WAL is a numbered ledger; data files are the warehouse shelves updated after the ledger entry exists.",
            "Bulk load with UNLOGGED tables skips WAL for the table but loses crash safety for that data.",
            "Do not delete pg_wal manually while the server runs.",
            "Do not assume synchronous_commit=on means zero data loss on all replicas—that depends on replication sync policy.",
        ),
        "practical": para(
            "Monitor WAL generation rate, disk space on the WAL volume, and replication lag bytes behind LSN.",
            "Separate WAL to fast durable storage on busy primaries when possible.",
            "Tune checkpoint and wal_compression settings on supported versions to reduce spikes—verify documentation.",
            "Logical decoding reads WAL for change streams.",
        ),
        "table": tbl(
            "| sync commit on | Stronger durability per txn | Higher commit latency | OLTP needing default safety | Extreme low-latency with accepted risk |",
            "| wal_level logical | CDC possible | More WAL volume | Event outbox patterns | Pure read replicas only |",
            "| UNLOGGED tables | Faster loads | Data lost on crash | Staging rebuilds | Financial ledger core tables |",
        ),
        "mistakes": "- Deleting WAL breaks recovery and replication.\n- Confusing WAL size with table bloat.\n- Setting wal_level too low then enabling logical replication without restart planning.\n- Ignoring archive_command failures until disk fills.",
        "debug": "Symptoms: disk full on pg_wal, replication stuck, recovery pause. Check pg_stat_archiver, oldest WAL needed for slots, `pg_ls_waldir` size. Mitigate: increase retention policy, fix archiver, relieve slot consumers.",
        "k": k23(
            [
                ("What is WAL?", "An append-only log of database changes.", "It provides crash-safe redo.", "Commit waits on WAL flush per policy.", "LSNs order all records."),
                ("What is an LSN?", "A byte offset-like pointer into the WAL stream.", "It monotonically increases for new records.", "Replication tracks sent and replay LSNs.", "Functions like pg_current_wal_lsn expose it."),
                ("Which process writes WAL files?", "Backends insert into WAL buffers.", "The WAL writer flushes to segments.", "Checkpointer does not replace WAL persistence.", "Archiver copies completed segments if configured."),
                ("Why log before data files?", "To recover after crash without torn pages dominating.", "Redo applies logged changes from checkpoint forward.", "Undo uses clog status for in-flight txns.", "This is the write-ahead rule."),
                ("What does synchronous_commit control?", "How eagerly commit waits for WAL durability.", "Off can return before flush for single-node policy.", "Remote commit waits may involve synchronous standby names.", "Exact behavior is version-documented."),
                ("What is wal_level for?", "It selects how much detail WAL contains.", "replica enables physical replication.", "logical enables logical decoding.", "Changing it typically requires restart."),
                ("What are WAL segments?", "Fixed-size files under pg_wal.", "The server recycles or archives them.", "Retention ties to replication slots and checkpoints.", "Never manually delete active segments."),
                ("How does WAL relate to MVCC?", "WAL logs physical page changes.", "MVCC visibility is separate tuple logic.", "Both apply on commit paths.", "Readers use snapshots not WAL directly."),
                ("What is full_page_write?", "Logging full page images after checkpoint.", "Guards against partial page writes on some storage.", "Can increase WAL volume after checkpoint.", "Setting default varies; check your version."),
                ("How do you measure WAL pressure?", "WAL bytes per second, segment creation rate.", "Compare to disk IOPS on WAL device.", "Watch checkpoint and bgwriter together.", "Use pg_stat_wal on supported versions."),
                ("Can you disable WAL per table?", "UNLOGGED tables skip WAL for their data.", "They truncate on crash recovery.", "Not for production durable data.", "Temporary tables also avoid durable WAL for user data."),
                ("What happens if WAL disk fills?", "Writes and commits block.", "Database may halt DML.", "Replication stalls.", "Emergency space or archive fix required."),
                ("How does logical decoding use WAL?", "Decoder reads WAL with a replication slot.", "Slots retain WAL until consumed.", "Lagging consumers hold disk.", "See D09-T013."),
                ("What is group commit?", "Batching commit WAL flushes for throughput.", "Reduces fsync syscalls under load.", "Still preserves transaction order rules.", "Implementation details vary by version."),
                ("Difference WAL vs redo in recovery?", "WAL is the continuous log.", "Recovery replays WAL after checkpoint REDO point.", "Checkpoint bounds work.", "See D09-T004."),
                ("Primary disk OK but replica lagging in bytes?", "Network or replay speed on standby.", "Compare pg_wal_lsn_diff on primary.", "Hot standby conflicts rare.", "See D09-T016."),
                ("After storage glitch, checksum failures?", "WAL replay may not fix bad pages if already corrupted.", "Use backups and PITR.", "data checksums help detect early.", "See D09-T017."),
                ("Bulk insert WAL huge?", "Expected for durable tables.", "Use COPY tuning, drop indexes, or staging UNLOGGED then insert.", "Commit batching still logs.", "Measure before disabling durability."),
                ("Archive command failing silently?", "pg_stat_archiver shows failures.", "WAL accumulates if not recycled.", "Monitoring required.", "Fix permissions and path."),
                ("App wants fsync=off equivalent?", "synchronous_commit off is not identical but trades safety.", "Never disable fsync at OS level for PostgreSQL without expert review.", "Understand RPO impact.", "Document business acceptance."),
                *follow_wal(),
            ]
        ),
        "ex1": "Query pg_current_wal_lsn and wal_level on a lab instance. Acceptance: explain LSN versus filename.",
        "ex2": "Disk full on pg_wal—list checks for archiver and replication slots.",
        "ex3": "Trade synchronous_commit off for a metrics table—state RPO impact.",
        "rev": ["WAL before durable commit.", "LSN orders changes.", "WAL writer flushes buffers.", "wal_level enables replication modes.", "Never delete live WAL."],
        "related": "Follows `D09-T002`. Leads to `D09-T004` checkpoints, `D09-T013` replication.",
        "completion": ["State write-ahead rule.", "Name WAL writer role.", "Explain synchronous_commit trade-off.", "Relate WAL to physical replication.", "Read current WAL LSN from SQL."],
        "ex_md": "1. LSN lab.\n2. pg_wal full diagnosis.\n3. synchronous_commit trade-off.",
        "sol_md": "### Exercise 1\nLSN is logical position; pg_walfile_name maps to segment file.\n\n### Exercise 2\nCheck pg_stat_archiver, replication slots, max_wal_size, disk mount.\n\n### Exercise 3\nCommits may be lost on crash before flush; acceptable only if product accepts that RPO.",
        "ib": ib(
            [
                "Beginner. What is WAL?",
                "Beginner. What is LSN?",
                "Beginner. Who flushes WAL files?",
                "Beginner. Why log first?",
                "Beginner. synchronous_commit?",
                "Intermediate. wal_level?",
                "Intermediate. WAL segments?",
                "Intermediate. WAL and MVCC?",
                "Intermediate. full_page_writes?",
                "Intermediate. Measure WAL pressure?",
                "Advanced. UNLOGGED tables?",
                "Advanced. WAL disk full?",
                "Advanced. Logical decoding?",
                "Advanced. Group commit?",
                "Advanced. WAL vs recovery redo?",
                "Scenario. Replica byte lag?",
                "Scenario. Checksum failures?",
                "Scenario. Bulk insert WAL?",
                "Scenario. Archive failures?",
                "Scenario. synchronous_commit off request?",
                "Follow-up. WAL relation?",
                "Follow-up. Vacuum relation?",
                "Follow-up. Poolers relation?",
            ]
        ),
    }
)

# Additional topics D09-T004..T018: compact specs
def _topic(
    tid: str,
    name: str,
    slug: str,
    deps: list[str],
    sql_file: str,
    sql: str,
    overview: str,
    first: str,
    internal: str,
    mermaid: str,
    examples: str,
    practical: str,
    table: str,
    mistakes: str,
    debug: str,
    k_questions: list,
    ex1: str,
    ex2: str,
    ex3: str,
    rev: list[str],
    related: str,
    completion: list[str],
    ex_md: str,
    sol_md: str,
    ib_lines: list[str],
) -> dict:
    return {
        "id": tid,
        "name": name,
        "subdomain": name,
        "file": slug,
        "deps": deps,
        "sql_file": sql_file,
        "sql": sql,
        "overview": overview,
        "first": first,
        "internal": internal,
        "mermaid": mermaid,
        "examples": examples,
        "practical": practical,
        "table": table,
        "mistakes": mistakes,
        "debug": debug,
        "k": k23(k_questions),
        "ex1": ex1,
        "ex2": ex2,
        "ex3": ex3,
        "rev": rev,
        "related": related,
        "completion": completion,
        "ex_md": ex_md,
        "sol_md": sol_md,
        "ib": ib(ib_lines),
    }


def std_k(prefix: str, core: list[tuple[str, str, str, str, str]]) -> list:
    """23 questions: 20 topic-specific + 3 followups from follow_wal pattern with prefix."""
    f = follow_wal()
    assert len(core) == 20
    return core + f


BASE_DEPS = ["D09-T001", "D07-T001", "D07-T002", "D08-T001", "D08-T002"]

PACK.append(
    _topic(
        "D09-T004",
        "Checkpoints and crash recovery",
        "d09-t004-checkpoints-and-crash-recovery.md",
        ["D09-T003", *BASE_DEPS],
        "d09_t004_checkpoint.sql",
        "SELECT name, setting, unit FROM pg_settings WHERE name LIKE 'checkpoint%' OR name IN ('max_wal_size','min_wal_size');\nSELECT * FROM pg_control_checkpoint();",
        para(
            "Checkpoints mark consistent recovery points in PostgreSQL.",
            "The checkpointer process writes a checkpoint record to WAL and flushes dirty data pages.",
            "Crash recovery replays WAL from the last checkpoint REDO location.",
            "Checkpoint frequency interacts with WAL size settings whose defaults vary by version.",
        ),
        para(
            "After a crash, shared buffers are empty; disk may lag committed work.",
            "Recovery runs in startup: replay WAL redo, then accept connections.",
            "Checkpoints bound how much WAL must be replayed.",
            "Spreading checkpoint I/O avoids thundering herds but tuning is workload-specific.",
        ),
        para(
            "Checkpointer triggers on time, WAL volume, and manual CHECKPOINT.",
            "Background writer trickles dirty pages; checkpoint forces a wave.",
            "pg_control_checkpoint shows timeline and REDO pointer.",
            "Recovery also handles two-phase commit and invalid pages via full_page_writes when enabled.",
        ),
        """```mermaid
flowchart TD
  crash[SystemCrash]
  startup[PostmasterStartup]
  redo[ReplayWALFromCheckpoint]
  consistent[DatabaseConsistent]
  crash --> startup
  startup --> redo
  redo --> consistent
```""",
        para("Checkpoint is a save point in a game—replay only the journal after that mark.", "CHECKPOINT command forces flush for admins.", "Do not confuse with transaction COMMIT.", "Long recovery means infrequent checkpoints or huge WAL since last one."),
        para("Tune max_wal_size and checkpoint_timeout together on your version.", "Monitor checkpoint_write_time and buffers_checkpoint.", "Plan maintenance windows after unclean shutdown.", "Use pg_resetwal only as last resort with documentation."),
        tbl(
            "| frequent checkpoints | Less recovery time | More I/O spikes | Fast restart SLAs | Already I/O bound |",
            "| rare checkpoints | Smoother writes | Long recovery | Write-heavy steady load | Strict RTO after crash |",
        ),
        "- Thinking COMMIT equals checkpoint.\n- Killing checkpointer.\n- Ignoring recovery pause after power loss.",
        "Symptoms: long startup, spike IO every checkpoint_timeout. Inspect logs for checkpoint starting/ending, pg_stat_bgwriter.",
        std_k(
            "checkpoint",
            [
                ("What is a checkpoint?", "A point where dirty buffers are flushed and WAL marks consistency.", "Recorded in WAL and control file.", "Bounds recovery work.", "Triggered by time or WAL volume."),
                ("Which process runs checkpoints?", "The checkpointer auxiliary process.", "Distinct from WAL writer.", "Can be observed in pg_stat_activity.", "Manual CHECKPOINT also works."),
                ("What is crash recovery?", "Replaying WAL after unclean shutdown.", "Starts from last checkpoint REDO.", "Then database opens.", "May take minutes if WAL long."),
                ("How do checkpoints affect WAL size?", "Recycling rules depend on max_wal_size and min_wal_size.", "More WAL since last checkpoint lengthens recovery.", "Settings vary by version.", "Monitor disk."),
                ("What is the REDO pointer?", "LSN where recovery begins.", "Shown in pg_control_checkpoint.", "Moves forward each checkpoint.", "Ties to WAL filenames."),
                ("Background writer vs checkpoint?", "Bgwriter trickles writes.", "Checkpoint flushes broadly.", "Both touch buffers.", "Spikes often checkpoint."),
                ("full_page_writes role in recovery?", "Protects against partial page writes.", "Logs page images after checkpoint.", "Increases WAL after checkpoint.", "Confirm setting on cluster."),
                ("How long will recovery take?", "Proportional to WAL since checkpoint.", "Hardware and replay parallelism matter.", "Test on staging.", "Not fixed formula."),
                ("Does standby recovery differ?", "Standby replays continuous WAL.", "Same redo engine.", "Lag is bytes behind.", "See replication topics."),
                ("What after filesystem full during checkpoint?", "Database may stop.", "Needs space to complete.", "Preventive monitoring.", "Emergency resize."),
                ("Power loss during COMMIT?", "Committed if WAL flushed per policy.", "Uncommitted rolled back.", "Data pages may lag WAL.", "Recovery reconciles."),
                ("pg_resetwal when?", "Only corrupted control when experts guide.", "Risk data loss.", "Not routine tuning.", "Backups first."),
                ("Checkpoint spikes on metrics?", "Normal if periodic.", "Problem if constant.", "Tune or spread IO.", "Separate WAL disk helps."),
                ("Relation to PITR?", "Base backup plus WAL archive.", "Checkpoint in backup label.", "See D09-T017.", "RPO/RTO planning."),
                ("Two-phase commit recovery?", "Prepared xacts replayed.", "Rare in app layers.", "Logged in WAL.", "Ops must resolve in-doubt."),
                ("Scenario: 30 min startup after crash?", "Huge WAL since checkpoint.", "Increase checkpoint frequency cautiously.", "Check hardware.", "Validate max_wal_size."),
                ("Scenario: checkpoint every few seconds?", "Too aggressive tuning.", "IO saturation.", "Relax timeout.", "Measure end-to-end."),
                ("Scenario: replica diverged?", "Not checkpoint alone—timeline fork.", "Use replication docs.", "May need rebuild.", "D09-T013."),
                ("Scenario: data checksum error on recovery?", "Page corruption.", "Restore backup.", "Hardware check.", "D09-T017."),
                ("Scenario: manual CHECKPOINT before maintenance?", "Reduces recovery window.", "Causes IO spike.", "Schedule low traffic.", "Good practice."),
            ],
        ),
        "Read pg_control_checkpoint and explain REDO location.",
        "Correlate checkpoint logs with IO spikes.",
        "Tune max_wal_size vs recovery time trade-off.",
        ["Checkpoint bounds recovery.", "Checkpointer flushes dirty pages.", "Recovery replays WAL.", "Distinct from COMMIT.", "Watch checkpoint metrics."],
        "After `D09-T003`. Before `D09-T005`.",
        ["Explain recovery after crash.", "Read pg_control_checkpoint.", "Contrast checkpoint and commit.", "Name checkpointer.", "Identify checkpoint spike metrics."],
        "1. REDO pointer lab.\n2. IO spike correlation.\n3. max_wal_size trade-off.",
        "### Exercise 1\nREDO LSN is start of replay; compare to pg_current_wal_lsn before crash tests on lab only.\n\n### Exercise 2\nMatch log 'checkpoint starting' to pg_stat_bgwriter buffers_checkpoint.\n\n### Exercise 3\nLarger max_wal_size spreads checkpoints but lengthens recovery—document RTO.",
        ib(
            [
                "Beginner. What is a checkpoint?",
                "Beginner. Which process checkpoints?",
                "Beginner. Crash recovery?",
                "Beginner. Checkpoints and WAL size?",
                "Beginner. REDO pointer?",
                "Intermediate. Bgwriter vs checkpoint?",
                "Intermediate. full_page_writes?",
                "Intermediate. Recovery duration?",
                "Intermediate. Standby recovery?",
                "Intermediate. Filesystem full?",
                "Advanced. Power loss at COMMIT?",
                "Advanced. pg_resetwal?",
                "Advanced. Checkpoint spikes?",
                "Advanced. PITR link?",
                "Advanced. 2PC recovery?",
                "Scenario. 30 min startup?",
                "Scenario. Checkpoints every few seconds?",
                "Scenario. Replica diverged?",
                "Scenario. Checksum on recovery?",
                "Scenario. CHECKPOINT before maintenance?",
                "Follow-up. WAL relation?",
                "Follow-up. Vacuum relation?",
                "Follow-up. Poolers relation?",
            ]
        ),
    )
)

# D09-T005 Vacuum
PACK.append(
    _topic(
        "D09-T005",
        "Vacuum and autovacuum",
        "d09-t005-vacuum-and-autovacuum.md",
        ["D09-T004", *BASE_DEPS],
        "d09_t005_vacuum.sql",
        "SELECT relname, n_dead_tup, last_vacuum, last_autovacuum, autovacuum_count FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 10;\nSHOW autovacuum;",
        para(
            "VACUUM reclaims space from dead tuples left by MVCC and advances freezing to prevent transaction id wraparound.",
            "Autovacuum automates vacuum and analyze based on table statistics and GUC thresholds.",
            "VACUUM is not usually blocking for SELECT; it can conflict with long transactions holding horizons.",
            "VACUUM FULL rewrites tables exclusively and locks heavily—different operation.",
        ),
        para(
            "Dead tuples remain until vacuum marks space reusable on pages.",
            "Freeze sets xmin to frozen markers so old xids need not be consulted.",
            "Autovacuum launcher schedules workers when dead tuple fraction crosses scale_factor thresholds (defaults vary by version).",
            "ANALYZE often runs with autovacuum to refresh planner stats (D09-T010).",
        ),
        para(
            "Vacuum scans heap pages, removes dead line pointers, freezes when eligible, updates visibility map and free space map.",
            "Index vacuuming reclaims dead index tuples pointing to dead heap entries.",
            "autovacuum_vacuum_cost_delay throttles vacuum I/O under load.",
            "Manual VACUUM (VERBOSE, ANALYZE) used in incidents; schedule for large tables.",
        ),
        """```mermaid
flowchart TD
  dead[DeadTuplesAccumulate]
  launcher[AutovacuumLauncher]
  worker[AutovacuumWorker]
  reclaim[ReclaimAndFreeze]
  dead --> launcher
  launcher --> worker
  worker --> reclaim
```""",
        para("Vacuum is garbage collection for row versions.", "Autovacuum is the cron-like scheduler.", "Do not disable autovacuum cluster-wide.", "Do not run VACUUM FULL routinely for bloat."),
        para("Watch n_dead_tup, autovacuum_count, wraparound warnings in logs.", "Tune per-table storage parameters for hot tables.", "Use idle_in_transaction_session_timeout to help horizons.", "Pair with index bloat monitoring."),
        tbl("| autovacuum on | Hands-off maintenance | Background IO | OLTP default | Known batch windows only |", "| aggressive vacuum | Lower bloat | More IO | Write-heavy | IO-starved disk |"),
        "- Disabling autovacuum.\n- VACUUM FULL as first knob.\n- Ignoring wraparound warnings.",
        "Rising dead tuples, emergency autovacuum, xid age alerts—find blockers in pg_stat_activity.",
        std_k(
            "vacuum",
            [
                ("What does VACUUM do?", "Removes dead tuple space and freezes old xids.", "Updates FSM and visibility map.", "Does not always shrink file size on disk.", "Standard bloat tool."),
                ("What is autovacuum?", "Automatic scheduler for vacuum/analyze.", "Launcher plus workers.", "Governed by GUC and per-table params.", "Should stay enabled."),
                ("VACUUM vs VACUUM FULL?", "Regular vacuum reclaims pages in place.", "FULL rewrites table exclusively.", "FULL locks table.", "FULL for extreme shrink needs."),
                ("What triggers autovacuum vacuum?", "Dead tuple thresholds vs reltuples.", "Formula uses scale_factor and threshold.", "Defaults vary.", "Per-table overrides exist."),
                ("Why vacuum blocked?", "Long xmin horizon from old transactions.", "Replication slots can delay cleanup on logical.", "Find idle in transaction.", "End offending sessions."),
                ("What is freezing?", "Marking tuples frozen to stop xid aging.", "Prevents wraparound.", "vacuum_freeze settings matter.", "Monitor datfrozenxid."),
                ("Index vacuum?", "Cleans dead index entries.", "Needed for index bloat.", "Runs with heap vacuum.", "REINDEX separate tool."),
                ("Does vacuum block reads?", "Generally no exclusive lock for standard vacuum.", "FULL blocks writes.", "DDL may conflict.", "MVCC still applies."),
                ("autovacuum analyze?", "Updates planner statistics.", "Important after bulk changes.", "See D09-T010.", "Can be tuned separately."),
                ("Cost delay?", "Throttles vacuum IO.", "Prevents starvation tuning mistake if too high.", "Balance with bloat.", "Per-table possible."),
                ("Wraparound vacuum?", "Forced when xids age.", "Priority over regular.", "Can surprise IO.", "Prevent with routine vacuum."),
                ("Visibility map role?", "Tracks all-visible pages.", "Enables index-only scans.", "Vacuum maintains.", "D09-T007 related."),
                ("Manual vacuum when?", "After bulk delete.", "Before major DDL.", "When stats show lag.", "Not instead of fixing txn leaks."),
                ("Vacuum and replication?", "Primary vacuum normal.", "Standby replays WAL.", "Hot standby conflicts rare.", "Logical slots hold xmin."),
                ("Monitoring queries?", "pg_stat_user_tables n_dead_tup.", "pg_stat_progress_vacuum.", "Logs autovacuum duration.", "Dashboard trends."),
                ("Scenario: autovacuum never runs?", "autovacuum off or zero workers.", "Table marked not autovacuumed.", "Fix config.", "Manual vacuum interim."),
                ("Scenario: table 80% dead?", "Update-heavy without vacuum.", "Tune autovacuum params.", "Fix long txns.", "Consider fillfactor."),
                ("Scenario: disk not shrinking?", "Vacuum reclaims space inside file.", "Need VACUUM FULL or pg_repack.", "Understand difference.", "Plan lock window."),
                ("Scenario: emergency autovacuum loop?", "Xid age critical.", "Let it finish.", "Add capacity.", "Postmortem txn leaks."),
                ("Scenario: vacuum slow on huge table?", "Cost delay high.", "Partition table.", "Off-peak run.", "Parallel vacuum options per version."),
            ],
        ),
        "Query top n_dead_tup tables.",
        "Find xmin blocker for stalled vacuum.",
        "Tune autovacuum for one hot table.",
        ["Vacuum reclaims dead tuples.", "Autovacuum automates.", "Freeze prevents wraparound.", "FULL is exclusive rewrite.", "Watch n_dead_tup."],
        "After `D09-T004`. Links `D09-T006` bloat.",
        ["Explain autovacuum triggers.", "Contrast VACUUM and FULL.", "Read pg_stat_user_tables vacuum columns.", "Name wraparound risk.", "Find vacuum blockers."],
        "1. n_dead_tup report.\n2. Blocker session.\n3. Per-table autovacuum tuning.",
        "### Exercise 1\nIdentify tables with high n_dead_tup and stale last_autovacuum.\n\n### Exercise 2\nCorrelate pg_stat_activity.xmin with vacuum not progressing.\n\n### Exercise 3\nLower scale_factor on hot table; document IO impact.",
    )
)

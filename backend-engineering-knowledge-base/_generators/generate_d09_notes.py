#!/usr/bin/env python3
"""Generate D09-T001..D09-T018 notes, exercises, solutions, interview bank items."""
from __future__ import annotations

import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "08_POSTGRESQL_INTERNALS" / "notes"
EX_DIR = ROOT / "EXERCISES"
SOL_DIR = EX_DIR / "solutions"
IB_DIR = ROOT / "INTERVIEW_BANK" / "items"
EXAMPLES_DIR = EX_DIR / "examples"


def para(*sentences: str) -> str:
    return " ".join(sentences)


def section_k(answers: dict[str, list[str]]) -> str:
    """answers keys: beginner, intermediate, advanced, scenarios, followups (5,5,5,5,3)."""
    out = ["## K. Interview Preparation", ""]
    levels = [
        ("Beginner", "beginner", 5),
        ("Intermediate", "intermediate", 5),
        ("Advanced", "advanced", 5),
        ("Scenarios", "scenarios", 5),
        ("Follow-ups", "followups", 3),
    ]
    for title, key, n in levels:
        out.append(f"### {title}")
        out.append("")
        qs = answers[key]
        assert len(qs) == n, f"{key} needs {n} items, got {len(qs)}"
        for i, (q, a) in enumerate(qs, 1):
            out.append(f"#### Q{i}. {q}")
            out.append("")
            out.append(f"**Answer:** {a}")
            out.append("")
    return "\n".join(out)


def write_bundle(topic: dict) -> None:
    tid = topic["id"]
    note_path = NOTES_DIR / topic["filename"]
    note_path.parent.mkdir(parents=True, exist_ok=True)

    header = textwrap.dedent(
        f"""# {tid} — {topic["name"]}

Topic ID: `{tid}`
Domain: PostgreSQL Internals
Subdomain: {topic["subdomain"]}
Importance: advanced
Complexity: advanced
Dependencies: {", ".join(f"`{d}`" for d in topic["dependencies"])}
Execution status of the code in section F: reference SQL (verify on your PostgreSQL version)

"""
    )

    body = topic["sections"]
    note = header + body + "\n" + section_k(topic["k"]) + "\n" + topic["tail"]
    note_path.write_text(note, encoding="utf-8")

    ex = textwrap.dedent(
        f"""# Exercises — {tid}

Problems only. Solutions: [{tid}](../solutions/{tid}.md).

{topic["exercises_md"]}
"""
    )
    (EX_DIR / f"{tid}.md").write_text(ex, encoding="utf-8")

    sol = textwrap.dedent(
        f"""# Solutions — {tid}

{topic["solutions_md"]}
"""
    )
    (SOL_DIR / f"{tid}.md").write_text(sol, encoding="utf-8")

    ib = textwrap.dedent(
        f"""# {tid} interview items

Domain: PostgreSQL Internals
Topic: {topic["name"]}
Difficulty mix: beginner, intermediate, advanced, scenario, follow-up
Interview type: internals, operations, debugging, trade-off
Full reasoned answers are in the topic note, section K.

## Questions

{topic["ib_questions"]}

Answer key: [topic note section K](../../08_POSTGRESQL_INTERNALS/notes/{topic["filename"]}).
"""
    )
    (IB_DIR / f"{tid}.md").write_text(ib, encoding="utf-8")

    if topic.get("example_sql"):
        EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)
        (EXAMPLES_DIR / topic["example_file"]).write_text(topic["example_sql"], encoding="utf-8")


# Shared tail template pieces
def tail_lmn(id_: str, related: str, completion: list[str]) -> str:
    ex_block = textwrap.dedent(
        f"""## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{id_}.md`. Try these before opening that file.

"""
    )
    return (
        ex_block
        + "\n".join(topic_exercises_l[id_])
        + "\n\n## M. Revision Notes\n\n"
        + "\n".join(f"- {b}" for b in revision_bullets[id_])
        + "\n\n## N. Related Topics\n\n"
        + related
        + "\n\n## O. Completion Criteria\n\n"
        + "\n".join(f"- {c}" for c in completion)
        + "\n"
    )


topic_exercises_l: dict[str, list[str]] = {}
revision_bullets: dict[str, list[str]] = {}


def register_exercises(tid: str, ex1: str, ex2: str, ex3: str, rev: list[str]):
    topic_exercises_l[tid] = [
        f"### Exercise 1 — implementation\n\n{ex1}",
        f"### Exercise 2 — debugging\n\n{ex2}",
        f"### Exercise 3 — trade-off\n\n{ex3}",
    ]
    revision_bullets[tid] = rev


TOPICS: list[dict] = []

# --- D09-T001 ---
register_exercises(
    "D09-T001",
    "On a lab instance, list PostgreSQL background processes with `SELECT pid, backend_type, state FROM pg_stat_activity WHERE backend_type IS NOT NULL;` and map each type you see to the architecture diagram in section D. Acceptance: you can explain postmaster versus backend versus at least three auxiliary process types.",
    "A service reports `FATAL: sorry, too many clients already`. Trace how connection limits relate to `max_connections`, reserved slots for superuser, and whether a pooler sits in front. Acceptance: you name the process that accepts connections and one knob that changes the limit (values vary by version and config).",
    "You can add more app servers or raise `max_connections`. Compare memory impact of one backend per connection versus PgBouncer session pooling for a read-heavy API. Acceptance: you mention shared_buffers per cluster not per connection, and that each backend has private memory.",
    [
        "Postmaster supervises; backends run client SQL.",
        "Shared memory holds buffers, locks, and WAL buffers.",
        "Checkpointer, background writer, WAL writer, autovacuum are separate aux processes.",
        "One client connection maps to one backend process (before poolers).",
    ],
)

TOPICS.append(
    {
        "id": "D09-T001",
        "name": "PostgreSQL architecture",
        "subdomain": "PostgreSQL architecture",
        "filename": "d09-t001-postgresql-architecture.md",
        "dependencies": ["D07-T001", "D07-T002", "D08-T001", "D08-T002"],
        "example_file": "d09_t001_architecture.sql",
        "example_sql": "-- D09-T001: architecture introspection\nSELECT pid, backend_type, state, wait_event_type, wait_event\nFROM pg_stat_activity\nWHERE backend_type IS NOT NULL\nORDER BY backend_type, pid;\n\nSHOW max_connections;\nSHOW shared_buffers;\n",
        "sections": textwrap.dedent(
            """## A. Topic Overview

PostgreSQL is a multi-process database server. A supervising **postmaster** listens for connections, forks or allocates **backend** processes for clients, and manages auxiliary workers for checkpointing, WAL persistence, buffer eviction, and vacuum.

The architecture exists because isolating work in processes keeps a bug or stuck query from tearing down the entire server, and because the operating system scheduler can reason about CPU and memory per backend. Shared state lives in **shared memory** (buffer pool, lock tables, WAL buffers) while SQL execution state stays mostly private to each backend.

In production you see this when tuning `max_connections`, diagnosing which process is waiting on I/O, or explaining why connection storms hurt memory. Interviewers use architecture to anchor MVCC, WAL, vacuum, and poolers in something concrete instead of abstract SQL.

Prerequisites: relational basics (`D07-T001`, `D07-T002`) and general database storage concepts (`D08-T001`, `D08-T002`). Later PostgreSQL topics assume you know which process owns checkpoints versus client queries.

## B. First-Principles Explanation

A database server must do three jobs at once: accept many clients, keep data durable on disk, and serve reads from memory when possible. PostgreSQL splits those jobs across processes coordinated through shared memory and signals.

When a client connects, the postmaster accepts the TCP session and starts a new backend process (or uses a pre-existing pool outside the server). That backend parses SQL, plans it, executes it, and returns rows. Meanwhile other processes flush dirty buffers, write WAL, and advance checkpoints without blocking every client in one giant thread pool lock.

Shared memory holds the **buffer cache** copy of data pages, so backends read and modify the same pages safely using lightweight locks and MVCC rules described in `D09-T002`. WAL records go to shared WAL buffers before the **WAL writer** asks the kernel to persist them, which is `D09-T003`.

Why not threads only? PostgreSQL historically chose processes for portability and fault isolation. A runaway backend can often be terminated with `pg_terminate_backend` while siblings continue. The trade-off is higher per-connection overhead than a threaded design, which is why poolers (`D09-T015`) are common.

## C. Internal Working and Architecture

Major components:

- **Postmaster**: parent process; listens on ports; forks backends; does not run user SQL itself.
- **Backend processes**: one per active server session (unless using external pooling that multiplexes).
- **Background writer**: writes dirty shared buffers to data files ahead of demand to smooth I/O.
- **Checkpointer**: writes a consistent checkpoint record and flushes dirty pages at checkpoint time (`D09-T004`).
- **WAL writer**: flushes WAL buffers to WAL files on disk.
- **Autovacuum launcher** and **workers**: schedule and run vacuum/analyze (`D09-T005`).
- Optional: **logical replication workers**, **parallel query** workers, **archiver** when WAL archiving is enabled.

A simple read path:

1. Backend receives `SELECT`.
2. Planner chooses a plan (`D09-T009`).
3. Executor asks the buffer manager for pages; on miss, reads from OS cache or disk.
4. Visibility rules decide which row versions are visible (`D09-T002`).
5. Results return to the client; backend waits for the next message.

Connection state is per backend (GUC settings, prepared statements, portals, temporary tables). Shared catalogs and user data pages are global in shared buffers. Temporary files for sorts and hashes are per backend on disk.

Memory: `shared_buffers` is cluster-wide. Each backend also allocates **work_mem** (per operation, not per statement globally) and maintenance memory for vacuum or index builds. Raising `max_connections` linearly increases worst-case private memory if every session runs heavy sorts at once.

## D. Diagrams and Visual Models

```mermaid
flowchart TD
  clients[ClientApplications]
  postmaster[Postmaster]
  backendA[BackendSessionA]
  backendB[BackendSessionB]
  sharedMem[SharedMemoryBuffersLocksWAL]
  bgwriter[BackgroundWriter]
  checkpointer[Checkpointer]
  walwriter[WALWriter]
  autovac[AutovacuumWorkers]
  datafiles[DataFilesAndWALOnDisk]
  clients --> postmaster
  postmaster --> backendA
  postmaster --> backendB
  backendA --> sharedMem
  backendB --> sharedMem
  bgwriter --> sharedMem
  checkpointer --> sharedMem
  walwriter --> sharedMem
  autovac --> sharedMem
  sharedMem --> datafiles
  walwriter --> datafiles
  checkpointer --> datafiles
```

Read top-down: clients never touch data files directly; backends mutate shared buffers under WAL and MVCC rules; auxiliary processes persist and recycle storage.

## E. Examples and Analogies

Analogy: the postmaster is a hotel front desk that assigns a dedicated concierge (backend) per guest. Housekeeping (vacuum), the night audit (checkpoint), and the security log book (WAL) run as separate staff who share the same building (shared memory) but do not each guest's errands.

Backend example: during a deploy, traffic doubles and connection latency spikes. `pg_stat_activity` shows hundreds of backends in `idle in transaction`. Architecture explains that each idle session still consumes a process and memory even when not running queries, which pushes you toward shorter transactions or a pooler.

Do not assume the postmaster runs queries; connecting tools to the postmaster PID is wrong. Do not set `max_connections` to thousands without modeling memory and using a pooler. Do not confuse **background writer** with **checkpointer**—both touch buffers, but checkpoints define recovery boundaries.

## F. Code Examples

File: `examples/d09_t001_architecture.sql`

Dependencies: PostgreSQL client (`psql`) and read access to `pg_stat_activity`.

```sql
SELECT pid, backend_type, state, wait_event_type, wait_event
FROM pg_stat_activity
WHERE backend_type IS NOT NULL
ORDER BY backend_type, pid;

SHOW max_connections;
SHOW shared_buffers;
```

How to run: `psql -f examples/d09_t001_architecture.sql` from the knowledge-base root (or the copy under `EXERCISES/examples/`).

Expected output: a row set listing `client backend`, `autovacuum worker`, `checkpointer`, etc., plus GUC values that depend on your `postgresql.conf` and version.

Important lines: `backend_type` distinguishes client backends from auxiliary processes. `SHOW max_connections` is cluster-wide, not per database. `shared_buffers` is allocated once in shared memory.

Edge cases: RDS and managed offerings sometimes hide or rename process types but still expose `pg_stat_activity`. Some extensions add background workers; they appear with their own `backend_type` labels depending on version.

This example is reference SQL; run it on your instance to capture real numbers.

## G. Practical Backend Application

Microservices often open a connection per request unless a pool is configured. Architecture explains why a traffic spike becomes a **process** spike and why ORM defaults like "connection per HTTP request" need bounds.

Use `pg_stat_activity` in runbooks: which app user owns slow queries, whether the checkpointer is stuck waiting on storage, whether autovacuum workers are absent during bloat growth. Pair with OS metrics: each backend is a process in `top`.

Error handling: `too many clients` is a capacity signal, not retry forever. Observability: export counts by `state` and `wait_event_type`. Security: the postmaster runs as the database OS user; compromising a backend still should not escalate without misconfiguration.

Scaling: vertical scale increases CPUs for parallel query and faster checkpoints; horizontal read scale often uses replicas (`D09-T013`) rather than infinite connections to one primary.

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Process per connection | Isolation, simple model | RAM and fork cost | Moderate connections, strong session semantics | Thousands of chatty clients without a pooler |
| High shared_buffers | More hits in buffer cache | Eviction pressure, long recovery | Read-heavy, warm working set | Tiny RAM VMs with oversized cache |
| Many auxiliary workers | Maintenance keeps pace | CPU and I/O contention | Large tables with autovacuum tuned | Single-disk hosts already saturated |
| No pooler | Full PostgreSQL feature set per session | Connection storms | Admin tools, migrations | Serverless-style massive concurrency |

Failure modes: connection exhaustion, one backend holding an idle transaction blocking vacuum, storage saturation slowing every process via shared disks.

## I. Common Mistakes and Misconceptions

- Believing PostgreSQL uses one thread per connection internally on all platforms—it is process-based for regular backends.
- Thinking killing the postmaster is safe—it takes down the cluster; terminate individual backends instead.
- Assuming `shared_buffers` should be "most of RAM" on every host; OS cache also matters and optimal ratios vary by workload and version guidance.
- Confusing **background writer** activity with checkpoint completion—check `pg_stat_bgwriter` and checkpoint logs for the full picture.
- Ignoring that temporary tables and prepared statements bind to a session, which breaks transaction pooling modes (`D09-T015`).

Weak interview answers list process names without what they share or persist. Strong answers tie backends to WAL, buffers, and connection limits.

## J. Debugging and Troubleshooting

Symptoms: sudden `too many clients`, elevated load with no slow query, memory climbing with idle sessions, postmaster respawning children rapidly.

Diagnosis:

1. `SELECT count(*), state FROM pg_stat_activity GROUP BY 1;`
2. Check `max_connections` and reserved connections for superuser (setting names and defaults vary by version).
3. Map application pool size × instances to actual backends.
4. Inspect `wait_event` for IO or LWLock contention shared by all backends.

Immediate mitigation: reduce app concurrency, terminate idle in transaction sessions, enable or resize a pooler. Long-term: session timeouts, right-size pools, fix connection leaks in app code.

Metrics: connections used / max, autovacuum worker presence, checkpoint write time, backend CPU per database.

"""
        ),
        "k": {
            "beginner": [
                (
                    "What is the postmaster in PostgreSQL?",
                    para(
                        "The postmaster is the root server process that listens for inbound connections and starts backend processes to handle them.",
                        "It also supervises auxiliary processes such as the checkpointer, background writer, WAL writer, and autovacuum launcher.",
                        "If the postmaster exits, the entire database instance stops, which is why operators restart the service rather than killing the postmaster PID casually.",
                        "Interviewers expect you to separate the postmaster from client backends because only backends execute SQL for sessions.",
                    ),
                ),
                (
                    "What does a backend process do?",
                    para(
                        "A backend is the process that serves one client connection session from login until disconnect.",
                        "It parses SQL, invokes the planner and executor, reads and modifies shared buffer pages under MVCC rules, and returns results.",
                        "Session-local state such as temporary tables, prepared statements, and some GUC settings live with that backend.",
                        "When the client disconnects, that backend process ends, which is why long-lived idle connections still consume a process slot.",
                    ),
                ),
                (
                    "What is stored in shared memory?",
                    para(
                        "Shared memory holds the buffer pool copies of relation pages, lock manager state, WAL buffers, and various global counters and caches.",
                        "All backends read and update these structures concurrently using lightweight locks and atomic operations.",
                        "Because buffers are shared, one backend can read a page another backend cached, avoiding redundant disk reads.",
                        "Private SQL execution memory such as sort workspaces is not shared; it is allocated per backend according to settings like work_mem.",
                    ),
                ),
                (
                    "Name two auxiliary processes besides client backends.",
                    para(
                        "The checkpointer and WAL writer are common examples: the checkpointer establishes recovery checkpoints and flushes dirty data pages at checkpoint boundaries.",
                        "The WAL writer flushes WAL from shared WAL buffers to WAL segment files on disk.",
                        "Other auxiliaries include the background writer, autovacuum launcher and workers, and optional archiver or logical replication workers.",
                        "Listing names plus one sentence of responsibility shows you understand how persistence and maintenance happen outside user queries.",
                    ),
                ),
                (
                    "Why does PostgreSQL use processes instead of only threads?",
                    para(
                        "Process isolation limits blast radius: a stuck or corrupted backend can often be terminated without ending every session.",
                        "The model maps cleanly to Unix process APIs and historically improved portability across platforms.",
                        "Each connection maps to identifiable OS resources, which simplifies observability in pg_stat_activity and system tools.",
                        "The cost is higher per-connection overhead than some threaded databases, which is a motivation for external connection poolers.",
                    ),
                ),
            ],
            "intermediate": [
                (
                    "How does a SELECT interact with the buffer cache?",
                    para(
                        "The executor requests pages through the buffer manager, which searches shared buffers for the relation block.",
                        "On a hit, PostgreSQL reads the page from shared memory without disk I/O; on a miss, it reads from the filesystem into a victim buffer frame.",
                        "Visibility checks on heap tuples happen after the page is in memory, using transaction snapshots rather than reading a separate version store.",
                        "Repeated scans benefit from pages already warmed by other backends or earlier queries in the same session.",
                    ),
                ),
                (
                    "What is the relationship between backends and max_connections?",
                    para(
                        "max_connections caps how many regular client backends may connect at once, in addition to reserved slots for superuser access in typical configurations.",
                        "Each active session consumes one slot and one backend process unless an external pooler multiplexes many clients onto fewer server sessions.",
                        "Raising the limit without poolers increases worst-case memory because each backend can allocate private work areas.",
                        "Exact defaults and reserved connection behavior should be confirmed on your version and vendor documentation rather than assumed.",
                    ),
                ),
                (
                    "What do the background writer and checkpointer both do, and how do they differ?",
                    para(
                        "Both can write dirty shared buffers to table files, reducing work needed later.",
                        "The background writer trickles dirty pages out continuously to smooth I/O and help backends find clean victims during reads.",
                        "The checkpointer runs at checkpoint events, flushes a consistent set of pages, and writes checkpoint records that bound crash recovery work.",
                        "Confusing the two leads to mis-tuning: checkpoint spikes relate to checkpoint settings; steady write load may be background writer activity.",
                    ),
                ),
                (
                    "Where does autovacuum fit architecturally?",
                    para(
                        "The autovacuum launcher is a permanent auxiliary process that schedules autovacuum worker processes based on table statistics and policy.",
                        "Workers are regular backends in the sense of executing SQL internally, but they run maintenance commands like VACUUM and ANALYZE.",
                        "They compete for I/O and locks like any backend, which is why heavy write workloads need deliberate autovacuum tuning.",
                        "Without autovacuum workers, MVCC dead tuple accumulation and statistics drift become operational problems even if user queries still run.",
                    ),
                ),
                (
                    "How would you prove which process is consuming CPU on a PostgreSQL host?",
                    para(
                        "Correlate pg_stat_activity.pid with OS tools such as top or ps to see command line and CPU per backend.",
                        "Filter by state and query text to find active SQL versus idle sessions that still hold a process.",
                        "Auxiliary processes appear with distinct backend_type values, helping separate checkpointer WAL activity from a runaway client query.",
                        "Managed services may restrict OS access, in which case wait_event fields and pg_stat statements views become the primary lens.",
                    ),
                ),
            ],
            "advanced": [
                (
                    "Explain how parallel query workers relate to the session backend.",
                    para(
                        "The leader backend for a parallel plan spawns additional background worker processes to scan or compute portions of the plan.",
                        "Workers cooperate through dynamic shared memory areas and still belong logically to the issuing query.",
                        "They are not extra client connections, but they consume CPU and memory and appear in activity views while the query runs.",
                        "max_parallel_workers and per-gather limits cap parallelism; raising them without CPU headroom can slow other sessions.",
                    ),
                ),
                (
                    "What happens at a high level when the postmaster receives SIGTERM?",
                    para(
                        "PostgreSQL initiates a controlled shutdown: active backends are signaled to finish, checkpoints run, and shared memory is released cleanly.",
                        "Immediate shutdown modes exist for operators but risk longer recovery if a checkpoint cannot complete.",
                        "Applications see connection errors during shutdown and must reconnect to a surviving instance or wait for restart.",
                        "Exact signal handling and shutdown modes are documented per version; automation should use pg_ctl or service managers rather than kill -9 on the postmaster.",
                    ),
                ),
                (
                    "Why can idle in transaction sessions hurt the whole cluster?",
                    para(
                        "They hold a backend slot, preventing new connections when near max_connections.",
                        "They may hold row-level locks and prevent vacuum from removing tuple versions those transactions still need to see.",
                        "They can block DDL or maintenance that conflicts with their open transaction snapshot.",
                        "Application connection pools that leak transactions into idle state are a common root cause seen in pg_stat_activity.",
                    ),
                ),
                (
                    "How does shared_buffers interact with the operating system page cache?",
                    para(
                        "PostgreSQL reads and writes its own buffer pool in shared memory, but underlying files are still cached by the OS.",
                        "Double caching can occur if both shared_buffers and OS cache hold the same pages, wasting RAM on some workloads.",
                        "On the other hand, OS cache helps when tools read files directly or when shared_buffers is modest.",
                        "Tuning guidance evolved across versions; measure hit ratios and total memory pressure instead of copying a single rule of thumb.",
                    ),
                ),
                (
                    "What architectural constraint motivates connection poolers?",
                    para(
                        "Forking or allocating a backend per client connection does not scale to tens of thousands of short HTTP-style connections.",
                        "Each backend carries memory for parsing, portals, and potential sorts, so connection storms exhaust RAM before CPU saturates.",
                        "Poolers multiplex many clients onto fewer server sessions, trading some PostgreSQL session semantics for efficiency.",
                        "Transaction-level pooling cannot safely carry all session features, which is a design trade-off revisited in D09-T015.",
                    ),
                ),
            ],
            "scenarios": [
                (
                    "After a deploy, API latency rises and PostgreSQL shows 500 backends mostly idle. What architectural knob do you check first?",
                    para(
                        "Compare application instance count times pool max to max_connections and actual pg_stat_activity counts.",
                        "Idle backends still consume processes and memory even when wait_event is ClientRead.",
                        "If each microservice opens a pool of 50 and you scaled replicas, you may have multiplied connections without a central pooler.",
                        "Mitigation is lowering per-app pool size, introducing PgBouncer, or raising max_connections only after memory modeling.",
                    ),
                ),
                (
                    "Disk utilisation is 100% but queries look idle. Which aux processes could still be writing?",
                    para(
                        "Checkpointer and background writer flushes spike during checkpoints or heavy dirty buffer volume.",
                        "WAL writer persists WAL buffers, and autovacuum workers rewrite pages during vacuum.",
                        "Archiver processes copy WAL if archiving is enabled, adding read load on WAL devices.",
                        "Use pg_stat_bgwriter, checkpoint logs, and pg_stat_progress_vacuum to attribute I/O to maintenance versus queries.",
                    ),
                ),
                (
                    "A developer wants to run long migrations from laptops with VPN disconnects. What process lifecycle issue appears?",
                    para(
                        "A disconnect terminates the backend running the migration unless using a detached session tool on the server.",
                        "Partial transactions roll back on disconnect unless using asynchronous job patterns or running from a stable bastion session.",
                        "Connection poolers may reassign sessions, breaking temp tables and SET commands mid-migration.",
                        "Architecture suggests running DDL from controlled sessions with statement_timeout and lock_timeout set explicitly.",
                    ),
                ),
                (
                    "You see many parallel workers for one query and other APIs time out. Is this a planner bug?",
                    para(
                        "Parallelism is requested by the planner when benefits outweigh costs; one heavy gather can consume most CPUs.",
                        "Other backends still run but queue longer at the OS scheduler, appearing as latency spikes.",
                        "You can reduce max_parallel_workers_per_gather or statement-level parallel hints depending on version and extensions.",
                        "The architectural fix is capacity planning: separate OLAP workloads, throttle parallelism, or use resource groups where available.",
                    ),
                ),
                (
                    "Monitoring alerts on postmaster restarts every hour. What subsystems do you inspect?",
                    para(
                        "Frequent restarts point to OOM kills, panics, or external orchestration failing health checks.",
                        "Check OS logs for SIGKILL, disk full on WAL or data directory, and shared memory allocation failures at startup.",
                        "Review postgresql log for FATAL/panic lines preceding exit.",
                        "Architecture knowledge tells you children cannot outlive a dead postmaster, so clients see widespread connection resets.",
                    ),
                ),
            ],
            "followups": [
                (
                    "How does architecture connect to MVCC?",
                    para(
                        "MVCC tuple visibility is evaluated inside backend executors reading shared buffer pages.",
                        "No separate version server exists; old row versions remain in heap pages until vacuum removes them.",
                        "Because all backends share buffers, visibility rules must be cheap per tuple using xmin/xmax transaction ids and snapshots.",
                        "See D09-T002 for the visibility rules themselves.",
                    ),
                ),
                (
                    "Which process is responsible for WAL durability?",
                    para(
                        "Backends insert WAL records into shared WAL buffers during data-changing operations.",
                        "The WAL writer process flushes those buffers to WAL files; commit waits until the transaction's WAL is persisted according to synchronous_commit policy.",
                        "Checkpointer and archiver interact with WAL segments but do not replace WAL writer persistence.",
                        "Details are in D09-T003 and checkpoint interaction in D09-T004.",
                    ),
                ),
                (
                    "Why mention poolers in an architecture topic?",
                    para(
                        "Poolers change the one-client-one-backend picture clients experience.",
                        "They sit between applications and the postmaster, opening fewer server sessions and reusing them.",
                        "That affects session GUCs, prepared statements, and LISTEN/NOTIFY semantics depending on pooling mode.",
                        "D09-T015 covers transaction versus session pooling trade-offs explicitly.",
                    ),
                ),
            ],
        },
        "exercises_md": """1. Map `pg_stat_activity.backend_type` rows to process roles using section D.
2. Diagnose `too many clients already` using connection math and pool settings.
3. Compare raising `max_connections` versus adding PgBouncer for a read API.""",
        "solutions_md": """### Exercise 1

Expect rows such as `client backend`, `checkpointer`, `walwriter`, `background writer`, `autovacuum launcher`, and `autovacuum worker`. Client backends run app SQL; checkpointer establishes recovery checkpoints; WAL writer persists WAL; background writer trickles dirty buffers; autovacuum processes run maintenance.

### Exercise 2

Compute app_instances × pool_max_connections. Compare to `SHOW max_connections` minus reserved superuser slots (verify on your version). If sum exceeds available slots, either lower app pools, add a pooler, or increase limit after memory review. The accepting process is the postmaster path that creates backends.

### Exercise 3

Raising max_connections increases simultaneous backends and worst-case private memory (work_mem per operation, catalog caches). PgBouncer keeps fewer server backends while multiplexing clients, reducing process count, but session-level features may break in transaction pooling. Read-heavy APIs with short queries often favor a pooler plus moderate server connections.""",
        "ib_questions": """1. Beginner. What is the postmaster?
2. Beginner. What does a backend process do?
3. Beginner. What lives in shared memory?
4. Beginner. Name two auxiliary processes.
5. Beginner. Why processes instead of only threads?
6. Intermediate. How does SELECT use the buffer cache?
7. Intermediate. How do backends relate to max_connections?
8. Intermediate. Background writer versus checkpointer?
9. Intermediate. Where does autovacuum fit?
10. Intermediate. How do you map CPU to a backend PID?
11. Advanced. How do parallel workers relate to the leader backend?
12. Advanced. What happens on controlled shutdown?
13. Advanced. Why is idle in transaction harmful?
14. Advanced. shared_buffers versus OS page cache?
15. Advanced. Why connection poolers exist architecturally?
16. Scenario. 500 mostly idle backends after deploy.
17. Scenario. Disk saturated with idle-looking queries.
18. Scenario. VPN disconnect during migration.
19. Scenario. One parallel query starves others.
20. Scenario. Postmaster restarting hourly.
21. Follow-up. Architecture and MVCC?
22. Follow-up. Which pieces persist WAL?
23. Follow-up. Why discuss poolers here?""",
        "tail": tail_lmn(
            "D09-T001",
            "Understand this before: `D07-T001`, `D07-T002`, `D08-T001`.\n\nThis topic supports: `D09-T002` MVCC, `D09-T003` WAL, `D09-T015` poolers.\n\nOften confused with: threaded database engines and application-side pools only.",
            [
                "Draw postmaster, backends, shared memory, and three aux processes.",
                "Explain why idle sessions still consume backends.",
                "Use pg_stat_activity to attribute CPU or waits to a PID.",
                "Relate max_connections to app pool sizing.",
                "Describe one failure mode of connection storms.",
            ],
        ),
    }
)

# NOTE: Additional topics D09-T002..T018 are appended by extend script run.


def main() -> None:
    for t in TOPICS:
        write_bundle(t)
    import build_d09_remaining

    build_d09_remaining.build_all()
    ids = ["D09-T001"] + build_d09_remaining.ALL_IDS
    print("Wrote", len(ids), "topics:", ", ".join(ids))


if __name__ == "__main__":
    main()

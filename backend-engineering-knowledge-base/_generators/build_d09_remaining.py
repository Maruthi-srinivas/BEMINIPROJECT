"""Build D09-T002..T018 markdown bundles from inline definitions."""
from __future__ import annotations

import importlib.util
from pathlib import Path

GEN = Path(__file__).parent / "generate_d09_notes.py"
spec = importlib.util.spec_from_file_location("gen", GEN)
gen = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(gen)

para = gen.para
register_exercises = gen.register_exercises
tail_lmn = gen.tail_lmn
write_bundle = gen.write_bundle


def sections(
    overview: str,
    first: str,
    internal: str,
    mermaid: str,
    examples: str,
    code_block: str,
    practical: str,
    table: str,
    mistakes: str,
    debug: str,
) -> str:
    return f"""## A. Topic Overview

{overview}

## B. First-Principles Explanation

{first}

## C. Internal Working and Architecture

{internal}

## D. Diagrams and Visual Models

{mermaid}

## E. Examples and Analogies

{examples}

## F. Code Examples

{code_block}

## G. Practical Backend Application

{practical}

## H. Advantages, Limitations and Trade-offs

{table}

## I. Common Mistakes and Misconceptions

{mistakes}

## J. Debugging and Troubleshooting

{debug}
"""


def std_table(rows: str) -> str:
    return (
        "| Choice | Benefit | Cost | Choose when | Avoid when |\n"
        "| --- | --- | --- | --- | --- |\n" + rows
    )


def code_sql(fname: str, sql: str) -> str:
    return f"""File: `examples/{fname}`

Dependencies: PostgreSQL client (`psql`).

```sql
{sql.strip()}
```

How to run: `psql -f examples/{fname}` (copy under `EXERCISES/examples/`).

Expected output: depends on cluster data and version; use as a lab script, not golden-file output.

Important lines: treat comments in the SQL as hints for what to observe in `EXPLAIN` or catalog views.

Edge cases: roles need permission to read catalogs; managed vendors may restrict some views.

Reference SQL; execute on your PostgreSQL version to validate behavior.
"""


def ib_from_k(k: dict) -> str:
    lines: list[str] = []
    n = 1
    for level in ("beginner", "intermediate", "advanced", "scenarios", "followups"):
        for q, _a in k[level]:
            lines.append(f"{n}. {q}")
            n += 1
    return "\n".join(lines)


def add(spec: dict) -> None:
    if not spec.get("ib"):
        spec["ib"] = ib_from_k(spec["k"])
    register_exercises(spec["id"], spec["ex1"], spec["ex2"], spec["ex3"], spec["rev"])
    spec["sections"] = sections(
        spec["overview"],
        spec["first"],
        spec["internal"],
        spec["mermaid"],
        spec["examples"],
        code_sql(spec["sql_file"], spec["sql"]),
        spec["practical"],
        spec["table"],
        spec["mistakes"],
        spec["debug"],
    )
    spec["tail"] = tail_lmn(spec["id"], spec["related"], spec["completion"])
    spec["filename"] = spec["file"]
    spec["dependencies"] = spec["deps"]
    spec["exercises_md"] = spec["ex_md"]
    spec["solutions_md"] = spec["sol_md"]
    spec["ib_questions"] = spec["ib"]
    spec["example_file"] = spec["sql_file"]
    spec["example_sql"] = spec["sql"]
    write_bundle(spec)


def qa(q, s1, s2, s3, s4):
    return (q, para(s1, s2, s3, s4))


ALL_IDS: list[str] = []


def build_all() -> None:
    # D09-T002 MVCC
    add(
        {
            "id": "D09-T002",
            "name": "MVCC and tuple visibility",
            "subdomain": "MVCC and tuple visibility",
            "file": "d09-t002-mvcc-and-tuple-visibility.md",
            "deps": ["D09-T001", "D07-T001", "D07-T002", "D08-T001", "D08-T002"],
            "sql_file": "d09_t002_mvcc.sql",
            "sql": """
-- xmin/xmax on a live row (catalog example)
SELECT ctid, xmin, xmax, * FROM pg_class WHERE relname = 'pg_class' LIMIT 3;
BEGIN;
SELECT txid_current();
ROLLBACK;
""",
            "overview": para(
                "Multi-Version Concurrency Control (MVCC) lets PostgreSQL readers and writers overlap without readers blocking writers on row locks for ordinary SELECT.",
                "Each row version is a heap tuple tagged with inserting and deleting transaction ids (xmin, xmax) plus hint bits for visibility.",
                "Snapshots taken at statement or transaction start decide which tuple versions a session may see.",
                "Interviewers probe MVCC before WAL, vacuum, and isolation because it explains anomalies, bloat, and why UPDATE creates new row versions.",
            ),
            "first": para(
                "If every reader locked rows that writers need, OLTP throughput would collapse.",
                "PostgreSQL keeps old row versions in place until vacuum reclaims them, while new versions are inserted for UPDATE and DELETE marks old versions dead.",
                "A transaction snapshot contains a set of visible transaction ids and bounds; the executor tests each tuple against that snapshot.",
                "Readers never overwrite committed data in place for user tables; writers create new tuples and chain via ctid when needed.",
            ),
            "internal": para(
                "Heap tuples store xmin (creator xid) and xmax (deleter or updater xid, or invalid).",
                "Hint bits cache commit status to avoid repeated clog lookups once known.",
                "Snapshots come from procarray and snapshot machinery; isolation level changes when snapshots are taken (Repeatable Read holds one snapshot for the transaction).",
                "Subtransactions complicate cmin/cmax command ids inside a transaction for self-visibility rules.",
                "Transaction id wraparound is a cluster-wide risk if vacuum cannot freeze old xmin horizons—see D09-T005.",
            ),
            "mermaid": """```mermaid
flowchart TD
  txnBegin[TransactionBegin]
  snap[BuildSnapshot]
  readRow[ReadHeapTuple]
  visCheck{VisibleToSnapshot}
  returnRow[ReturnVersion]
  skipRow[SkipOrSeekNext]
  txnBegin --> snap
  snap --> readRow
  readRow --> visCheck
  visCheck -->|yes| returnRow
  visCheck -->|no| skipRow
  skipRow --> readRow
```""",
            "examples": para(
                "Analogy: a spreadsheet where edits append new rows with timestamps instead of erasing history; readers choose the latest row their timestamp allows.",
                "UPDATE id=1 SET balance=balance-10 creates a new tuple; the old tuple gets xmax set; SELECT may still see the old value in an older snapshot.",
                "Do not assume DELETE removes bytes immediately—space is reclaimed by vacuum.",
                "Do not confuse MVCC with no locking: writers still take row-level locks on conflicting updates.",
            ),
            "practical": para(
                "Long transactions (open snapshots) delay vacuum and cause bloat—common ORM anti-pattern.",
                "Read-only replicas apply WAL and evaluate visibility on the standby similarly for queries.",
                "Serializable isolation adds SSI predicates on top of MVCC—see D09-T011.",
                "Debugging visibility often pairs pg_stat_activity.xmin with autovacuum blocked reasons.",
            ),
            "table": std_table(
                "| MVCC reads | No read locks on stable snapshots | Old versions consume space | Read-heavy OLTP | Write-heavy without vacuum |\n"
                "| Repeatable Read snapshot | Consistent reads in txn | Phantom policy differs from ANSI expectations in historical docs | Reporting in one txn | Long txn holding horizon |\n"
                "| Row locks on write | Prevents lost updates | Waits and deadlocks possible | Concurrent updates | Hot row counters without strategies |"
            ),
            "mistakes": "- Saying MVCC means no locks.\n- Thinking DELETE frees disk instantly.\n- Ignoring xmin horizon from idle transactions.\n- Assuming READ COMMITTED and REPEATABLE READ behave identically across databases.",
            "debug": "Symptoms: growing table size with stable row counts, vacuum never catching up. Check `pg_stat_activity` for old xmin, `pg_stat_all_tables.n_dead_tup`, long `idle in transaction`. Mitigate: end transactions, lower statement timeouts, tune autovacuum.",
            "k": {
                "beginner": [
                    qa("What problem does MVCC solve?", "It allows concurrent reads while writes proceed by keeping multiple row versions.", "Readers use snapshots instead of locking every row they read.", "Writers create new versions rather than overwriting visible data in place.", "This increases throughput for typical OLTP mixed workloads."),
                    qa("What are xmin and xmax on a heap tuple?", "xmin records which transaction inserted the row version.", "xmax records which transaction deleted or updated it out of visibility, when set.", "Visibility routines compare them to the active snapshot.", "Hint bits cache whether xmin/xmax transactions committed or aborted."),
                    qa("What is a snapshot?", "A snapshot captures which transactions are visible to a statement or transaction.", "It includes xmin/xmax bounds and in-progress xid sets as of snapshot build time.", "Executors ask whether a tuple is visible to that snapshot.", "Different isolation levels take snapshots at different times."),
                    qa("Does SELECT take row locks in PostgreSQL?", "A plain SELECT does not take row-exclusive locks for read consistency under MVCC.", "It reads tuple versions visible to its snapshot.", "Writers still lock rows they modify.", "SELECT FOR UPDATE explicitly locks rows for later update."),
                    qa("What happens on UPDATE?", "PostgreSQL writes a new row version and marks the old version dead with xmax.", "Indexes may need new entries unless HOT applies—see D09-T006.", "Until vacuum runs, both versions occupy space.", "Concurrent readers in older snapshots may still see the old version."),
                ],
                "intermediate": [
                    qa("How does READ COMMITTED differ from REPEATABLE READ for snapshots?", "READ COMMITTED takes a new snapshot for each statement in PostgreSQL.", "REPEATABLE READ holds the first snapshot for the whole transaction.", "That changes whether a second SELECT in the same txn can see commits from others.", "Neither eliminates the need to handle write conflicts on updates."),
                    qa("What are hint bits?", "They are status flags on tuples caching commit knowledge for xmin/xmax.", "They reduce repeated access to the commit log once known.", "They can be set when visibility is first determined.", "They must be treated as hints; visibility still follows snapshot rules."),
                    qa("Why can long transactions cause bloat?", "Vacuum cannot remove dead tuples still visible to any open snapshot horizon.", "An idle in transaction session pins xmin and blocks freezing old pages.", "Dead tuples accumulate even if current queries need few rows.", "Ending long transactions is often the real fix, not only autovacuum tuning."),
                    qa("What is ctid?", "ctid is the physical tuple identifier (block, offset) of a row version.", "It can change when a row is rewritten by vacuum full or cluster.", "Applications should not use ctid as a stable primary key.", "It helps explain chains of row versions on updates."),
                    qa("How does DELETE interact with MVCC?", "DELETE sets xmax on visible versions rather than erasing bytes immediately.", "Space becomes reusable on that page after vacuum.", "Concurrent snapshots may still see the row until their snapshot predates the delete commit.", "Foreign keys and triggers still run under normal locking rules."),
                ],
                "advanced": [
                    qa("What is transaction id wraparound?", "Transaction ids are 32-bit and eventually exhaust if not frozen.", "Vacuum (freeze) marks old tuples as frozen so xmin horizons advance safely.", "If autovacuum cannot keep up, the cluster may refuse new transactions to protect data integrity.", "Monitoring age of oldest xmin and emergency autovacuum settings is an operational duty."),
                    qa("How do subtransactions affect visibility?", "cmin and cmax track command ids within a transaction for tuple visibility among statements in the same txn.", "Savepoints create subtransactions with their own ids.", "Visibility must handle whether a tuple inserted earlier in the same txn is visible to later commands.", "This is internal but explains odd self-visibility edge cases in advanced debugging."),
                    qa("Does MVCC apply on replicas?", "Standbys replay WAL and have their own snapshots for queries on hot standbys when enabled.", "Visibility is evaluated on the standby's data pages like on the primary.", "Replication lag means snapshots may see older global state relative to primary commits.", "Hot standby conflicts can cancel queries if they pin vacuum on primary—rare but documented."),
                    qa("How does SERIALIZABLE differ from MVCC alone?", "Serializable Snapshot Isolation adds predicate locking and serialization failures.", "MVCC still stores versions; SSI detects rw-dependencies that could break serializability.", "Applications may see serialization_failure and must retry.", "It is stricter than REPEATABLE READ for certain anomaly classes."),
                    qa("Why can COUNT(*) be expensive under MVCC?", "Each version must be checked for visibility per snapshot.", "Large tables with many dead tuples slow scans even if live rows are few.", "Vacuum reduces dead tuples; partial indexes do not remove visibility work on heap.", "Approximate counts or maintained counters are common patterns at scale."),
                ],
                "scenarios": [
                    qa("Dashboard COUNT grows but business rows stable—MVCC angle?", "Likely dead tuples from updates without adequate vacuum or blocked horizon.", "Check n_dead_tup and last_autovacuum.", "Find long transactions holding snapshots.", "Fix workload or autovacuum before adding hardware."),
                    qa("Two SELECTs in one txn return different row counts—why?", "If isolation is READ COMMITTED, each statement gets a new snapshot.", "Commits between statements become visible.", "REPEATABLE READ would keep counts stable unless the txn itself writes.", "This is expected PostgreSQL behavior, not a broken replica."),
                    qa("ORM keeps transaction open during external API call—impact?", "Snapshot horizon pinned; vacuum cannot prune dead tuples those transactions could still see.", "Table and index bloat accelerate.", "Connection pool may exhaust backends.", "Pattern: commit before external IO or use outbox/async."),
                    qa("UPDATE hot row every millisecond—what MVCC symptom?", "Rapid creation of dead tuples and index churn.", "Throughput may plateau due to vacuum and WAL volume.", "Consider queue aggregation, advisory serialization, or alternative storage patterns.", "Row-level locks also serialize writers on that key."),
                    qa("After bulk UPDATE, disk doubled—next step?", "Confirm dead tuple count via pg_stat_all_tables.", "Run manual VACUUM (not FULL first) during low traffic.", "Ensure no long snapshots block.", "Plan autovacuum cost limits if vacuum cannot keep pace."),
                ],
                "followups": [
                    qa("Link MVCC to WAL?", "Every tuple change generates WAL like any page modification.", "MVCC semantics are about visibility; WAL is about durability and replication.", "See D09-T003 for commit WAL records.", "Both interact during crash recovery replay."),
                    qa("Link MVCC to vacuum?", "Vacuum reclaims dead tuple space and freezes xids.", "Without vacuum MVCC versions accumulate.", "See D09-T005 and D09-T006.", "Autovacuum is the automated piece."),
                    qa("Link MVCC to locking topic?", "MVCC avoids reader-writer blocking for plain reads.", "Writers still lock updated rows; DDL takes stronger locks.", "See D09-T011.", "SELECT FOR UPDATE bridges MVCC reads with explicit locks."),
                ],
            },
            "ex1": "Inspect xmin/xmax on catalog rows and run `SELECT txid_current()` inside a rolled-back transaction. Acceptance: explain xmin versus snapshot.",
            "ex2": "Given rising dead tuples and an `idle in transaction` session, explain why vacuum cannot shrink the table yet.",
            "ex3": "Choose READ COMMITTED vs REPEATABLE READ for a financial report txn. Acceptance: mention statement-level vs transaction-level snapshots.",
            "rev": ["xmin/xmax tag row versions.", "Snapshots pick visible tuples.", "UPDATE creates new versions.", "Vacuum reclaims dead tuples.", "Long txns block horizons."],
            "related": "Builds on `D09-T001`. Leads to `D09-T005` vacuum, `D09-T011` isolation.",
            "completion": ["Explain UPDATE visibility without erasing old bytes.", "Relate idle transactions to bloat.", "Contrast READ COMMITTED and REPEATABLE READ snapshots.", "Describe xmin wraparound risk at high level.", "Read xmin/xmax from a catalog query."],
            "ex_md": "1. Catalog xmin/xmax lab.\n2. Dead tuples with idle in transaction.\n3. Isolation level for reporting txn.",
            "sol_md": "### Exercise 1\nxmin is inserter xid; xmax marks deleting/updating xid. Snapshot compares against active xids.\n\n### Exercise 2\nVacuum cannot remove tuples still visible to the idle snapshot horizon.\n\n### Exercise 3\nREPEATABLE READ if the report must not see mid-txn commits; READ COMMITTED if statement-fresh data is OK.",
            "ib": "\n".join(
                f"{n}. {t}"
                for n, t in enumerate(
                    [
                        "Beginner. MVCC problem?",
                        "Beginner. xmin and xmax?",
                        "Beginner. What is a snapshot?",
                        "Beginner. SELECT row locks?",
                        "Beginner. What happens on UPDATE?",
                        "Intermediate. READ COMMITTED vs REPEATABLE READ?",
                        "Intermediate. Hint bits?",
                        "Intermediate. Long transactions and bloat?",
                        "Intermediate. What is ctid?",
                        "Intermediate. DELETE and MVCC?",
                        "Advanced. Xid wraparound?",
                        "Advanced. Subtransactions visibility?",
                        "Advanced. MVCC on replicas?",
                        "Advanced. SERIALIZABLE vs MVCC?",
                        "Advanced. COUNT cost under MVCC?",
                        "Scenario. Stable rows, growing table?",
                        "Scenario. Two COUNTs differ in one txn?",
                        "Scenario. ORM txn during HTTP?",
                        "Scenario. Hot row updates?",
                        "Scenario. Disk after bulk UPDATE?",
                        "Follow-up. MVCC and WAL?",
                        "Follow-up. MVCC and vacuum?",
                        "Follow-up. MVCC and locking?",
                    ],
                    start=1,
                )
            ),
        }
    )
    ALL_IDS.append("D09-T002")

    from d09_pack_rest import PACK
    from d09_pack_006_018 import PACK2

    for spec in PACK + PACK2:
        add(spec)
        ALL_IDS.append(spec["id"])


if __name__ == "__main__":
    build_all()
    print("built", len(ALL_IDS), "topics")

# --- definitions appended below ---

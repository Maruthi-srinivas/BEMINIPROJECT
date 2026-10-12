#!/usr/bin/env python3
"""Generate all D07-T001..D07-T031 artifacts from structured specs."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_GEN = Path(__file__).resolve().parent
if str(_GEN) not in sys.path:
    sys.path.insert(0, str(_GEN))

from d07_common import bank_from_sections, bullets, fact_block, mk_body

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "00_INDEX" / "inventory.json"


def load_topics() -> list[dict]:
    data = json.loads(INV.read_text(encoding="utf-8"))
    out = [t for t in data["topics"] if re.match(r"D07-T(\d+)$", t["id"])]
    out.sort(key=lambda t: int(t["id"].split("-T")[1]))
    return [t for t in out if 1 <= int(t["id"].split("-T")[1]) <= 31]


def a(*parts: str) -> str:
    text = " ".join(p.strip() for p in parts if p.strip())
    if len([s for s in text.split(".") if s.strip()]) < 4:
        raise ValueError(f"need 4 sentences: {text[:80]}")
    return text


def iv_pack(focus: str, facts: list[str]) -> tuple:
    f = facts
    beginner = [
        (f"What is the core idea behind {focus}?", a(f[0], f[1], f[2], f[3])),
        (f"Why do backend teams care about {focus}?", a(f[4], f[5], f[6], f[7])),
        (f"Name one mistake juniors make with {focus}.", a(f[8], f[9], f[10], f[11])),
        (f"How does {focus} show up in production incidents?", a(f[12], f[13], f[14], f[15])),
        (f"What should you read in logs when debugging {focus}?", a(f[16], f[17], f[18], f[19])),
    ]
    intermediate = [
        (f"How would you explain {focus} to a product manager?", a(f[20], f[21], f[22], f[23])),
        (f"What SQL or schema detail best teaches {focus}?", a(f[24], f[25], f[26], f[27])),
        (f"How does {focus} interact with connection pooling?", a(f[28], f[29], f[30], f[31])),
        (f"When does {focus} block a release?", a(f[32], f[33], f[34], f[35])),
        (f"What metric proves you solved a {focus} problem?", a(f[36], f[37], f[38], f[39])),
    ]
    advanced = [
        (f"How does {focus} differ between PostgreSQL and MySQL?", a(f[40], f[41], f[42], f[43])),
        (f"How does {focus} change under replication lag?", a(f[44], f[45], f[46], f[47])),
        (f"How does {focus} relate to MVCC?", a(f[48], f[49], f[50], f[51])),
        (f"What is a distributed-systems failure mode for {focus}?", a(f[52], f[53], f[54], f[55])),
        (f"How would you test {focus} in CI?", a(f[56], f[57], f[58], f[59])),
    ]
    scenarios = [
        (f"On-call: p95 latency doubled after a deploy touching {focus}. First three steps?", a(f[60], f[61], f[62], f[63])),
        (f"Finance reports wrong totals linked to {focus}. What do you verify?", a(f[64], f[65], f[66], f[67])),
        (f"A migration failed mid-way affecting {focus}. How do you recover?", a(f[68], f[69], f[70], f[71])),
        (f"Team wants to skip {focus} to ship faster. Your response?", a(f[72], f[73], f[74], f[75])),
        (f"Read replica serves stale data involving {focus}. Mitigation?", a(f[76], f[77], f[78], f[79])),
    ]
    followups = [
        (f"How does {focus} connect to the next topic in domain 7?", a(f[80], f[81], f[82], f[83])),
        (f"How does {focus} connect to API design?", a(f[84], f[85], f[86], f[87])),
        (f"How does {focus} connect to observability?", a(f[88], f[89], f[90], f[91])),
    ]
    return beginner, intermediate, advanced, scenarios, followups


# Each spec: focus, mermaid (no spaces in node IDs), sql, overview, fp, internal, examples, practical,
# mistakes (5), debugging (4), revision (4), completion (4), exercises (3 blocks), solutions (3), facts (92 strings)
SPECS: dict[str, dict] = {}


def add(
    tid: str,
    focus: str,
    mermaid: str,
    sql: str,
    overview: str,
    fp: str,
    internal: str,
    examples: str,
    practical: str,
    mistakes: list[str],
    debugging: list[str],
    revision: list[str],
    completion: list[str],
    ex_blocks: list[str],
    ex_items: list[str],
    solutions: list[str],
    facts: list[str],
) -> None:
    if len(facts) != 92:
        raise ValueError(f"{tid} needs 92 fact sentences, got {len(facts)}")
    b, i, adv, sc, fu = iv_pack(focus, facts)
    ex_text = "\n\n".join(f"### Exercise {n + 1}\n\n{blk}" for n, blk in enumerate(ex_blocks))
    SPECS[tid] = mk_body(
        overview=overview,
        first_principles=fp,
        internal=internal,
        mermaid=mermaid,
        examples=examples,
        sql_title=focus,
        sql=sql,
        practical=practical,
        tradeoffs="| Choice | Benefit | Cost | Choose when | Avoid when |\n| --- | --- | --- | --- | --- |\n"
        + "| Apply topic pattern | predictable behavior | design time | core domain data | quick hacks |\n"
        + "| Defer topic pattern | faster prototype | incident debt | throwaway demos | money and compliance |",
        mistakes=bullets(mistakes),
        debugging=bullets(debugging),
        beginner=b,
        intermediate=i,
        advanced=adv,
        scenarios=sc,
        followups=fu,
        exercises=ex_text,
        exercise_items=ex_items,
        solutions=solutions,
        bank_questions=bank_from_sections(b, i, adv, sc, fu),
        revision=bullets(revision),
        completion=bullets(completion),
    )


# --- Topic fact sentences (4+ per interview answer built via `a()`) ---
# For brevity each "fact" is one sentence; iv_pack groups them in fours.

F_REL = fact_block(
    "Relational databases store rows in tables with declared types.",
    "SQL is the standard way to query and mutate relational data.",
    "Foreign keys express relationships and enable referential integrity.",
    "Transactions group changes that must succeed or fail together.",
    "Choosing a datastore shapes how you enforce business invariants.",
    "Wrong store choice shows up as reconciliation jobs and data bugs.",
    "Interviews test whether you know trade-offs, not buzzwords.",
    "Production systems often use one relational primary plus caches.",
    "Teams pick Mongo only for JSON shape without checking joins.",
    "Using Redis as primary for money loses durability guarantees.",
    "Assuming NoSQL has no schema creates client compatibility bugs.",
    "Skipping backups for new engines invites total data loss.",
    "Incidents appear as duplicate charges or lost updates.",
    "Cross-service inconsistency often means two sources of truth.",
    "ORM N+1 queries masquerade as database slowness.",
    "Check which database owns each entity during triage.",
    "Logs should include db instance, migration version, and query id.",
    "Slow query logs reveal missing indexes before store changes.",
    "Compare p95 with cache disabled to isolate the datastore.",
    "Alert on replication lag when reads use replicas.",
    "Product wants speed; you explain audit and reporting needs.",
    "Relational models make finance SQL straightforward.",
    "Document stores complicate ad hoc joins across collections.",
    "Show a one-page data map with systems of record.",
    "CREATE TABLE shows constraints that document stores lack.",
    "CHECK and FOREIGN KEY encode rules close to data.",
    "Illustrative SQL teaches invariants better than slogans.",
    "Parameterized inserts keep examples honest at boundaries.",
    "Pools reduce connection overhead but do not fix bad queries.",
    "Too many connections exhaust max_connections on Postgres.",
    "Pool sizing must match CPU cores and transaction length.",
    "Monitor pool wait time alongside query latency.",
    "Releases block when migrations are backward incompatible.",
    "Long-running migrations need expand-contract patterns.",
    "Feature flags cannot fix a broken schema rollback.",
    "Ship DDL in small steps with reversible steps documented.",
    "Success metric: correct balances after concurrent transfers.",
    "Track error rate on constraint violations after deploy.",
    "Replication lag below SLO for read-your-writes paths.",
    "p95 query time within budget for top ten endpoints.",
    "Postgres has richer types and stricter SQL than MySQL.",
    "MySQL InnoDB also offers MVCC but dialect differs.",
    "Always check isolation and replication semantics per engine.",
    "Do not assume Oracle behaviors on open-source engines.",
    "Replicas apply WAL asynchronously unless synchronous commit.",
    "Stale reads on replicas violate read-your-writes expectations.",
    "Route critical reads to primary or use lag-aware routing.",
    "Lag metrics should gate marketing pages, not payments.",
    "MVCC gives snapshot reads without blocking writers.",
    "Vacuum or purge reclaims old row versions in Postgres.",
    "Long transactions block cleanup and increase bloat.",
    "Isolation choice still matters even with MVCC.",
    "Split-brain during failover can duplicate writes.",
    "Leader election must be coordinated with fencing.",
    "Clients must retry idempotently after partition heals.",
    "Distributed transactions across shards are expensive.",
    "CI should apply migrations to ephemeral database containers.",
    "Run EXPLAIN on representative queries in migration tests.",
    "Contract tests assert constraint names and error codes.",
    "Load tests with realistic concurrency catch isolation bugs.",
    "Rollback migration script exists before merge.",
    "Check deploy dashboards and recent DDL first.",
    "Capture EXPLAIN for top slow queries after deploy.",
    "Compare error rates on deadlocks and timeouts.",
    "Finance totals must match ledger sums per account.",
    "Look for double application of migrations.",
    "Verify batch jobs idempotency keys after partial failure.",
    "Re-run reconciliation with frozen writes if needed.",
    "Restore from backup if DDL left table inconsistent.",
    "Use transactional DDL where supported or lock writes.",
    "Document rollback steps in the migration ticket.",
    "Skipping design review invites production firefighting.",
    "Insist on ADR with measured bottleneck before new store.",
    "Offer timeline impact with risk spelled out.",
    "Ship behind feature flag only after schema ready.",
    "Route payment reads to primary until lag drops.",
    "Expose read-after-write token to clients if needed.",
    "Cache invalidation must follow primary writes.",
    "Monitor replica lag alerting on call.",
    "Next topic deepens schema and keys for relational modeling.",
    "Store choice without schema design is incomplete.",
    "Continue the learning path in table and key topics.",
    "APIs must not leak internal surrogate keys without stability.",
    "Pagination cursors should use indexed columns.",
    "Error responses map constraint violations to 409.",
    "Trace spans should tag db.system and db.statement fingerprint.",
    "Metrics: pool usage, deadlocks, replication lag.",
    "Logs must correlate query latency with endpoint name.",
    "Distributed caches are not substitutes for transactional stores.",
    "Read models can be rebuilt from event logs when designed intentionally.",
    "Schema diagrams should live in version control beside migrations.",
    "Choosing a database is a multi-year operational commitment.",
)

add(
    "D07-T001",
    "relational versus non-relational databases",
    """flowchart TD
  svc[ApiService]
  choice{NeedsMultiRowACID}
  pg[(PostgresPrimary)]
  mongo[(DocumentDB)]
  svc --> choice
  choice -->|yes| pg
  choice -->|nestedDocsOnly| mongo""",
    """-- unexecuted
CREATE TABLE ledger_entries (
  id bigserial PRIMARY KEY,
  account_id bigint NOT NULL REFERENCES accounts(id),
  amount_cents bigint NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);""",
    "Relational and non-relational databases differ in data model, query language, and transactional boundaries. "
    "Backend engineers pick a primary store based on invariants, not hype.",
    "Storage engines must survive crashes and concurrent writers. Relational theory adds structure; NoSQL optimizes alternate access paths.",
    "SQL databases parse queries, plan index scans, and commit WAL records. Document engines index JSON and replicate per shard.",
    "Wallet balances belong in relational rows; CMS pages may be documents.",
    "Default to PostgreSQL until metrics justify another store. Document ADRs for exceptions.",
    [
        "Choosing NoSQL to avoid migrations.",
        "Ignoring backup drills.",
        "Polyglot persistence without owners per entity.",
        "Sharding before tuning queries.",
        "Using cache as system of record.",
    ],
    [
        "Map each entity to its database during incidents.",
        "Compare latency with cache off.",
        "Inspect slow query log after store change.",
        "Verify migration version matches code.",
    ],
    [
        "Relational for multi-row invariants.",
        "NoSQL is a family of models.",
        "One primary source of truth per entity.",
        "Measure before adding stores.",
    ],
    [
        "Explain ACID need for payments.",
        "Name two NoSQL models.",
        "Describe polyglot risks.",
        "Challenge store hype with metrics.",
    ],
    [
        "Design store split for ride-hailing with ACID justification.",
        "Argue for/against wide-column for tiny config table.",
        "Outline document-to-SQL migration with dual-write.",
    ],
    [
        "Ride-hailing ACID split design.",
        "Cassandra for 500-row config critique.",
        "Dual-write Mongo to SQL reporting migration.",
    ],
    [
        "Trips and payments in PostgreSQL; marketing blobs optional document.",
        "Reject Cassandra; use Postgres plus cache for tiny config.",
        "Backfill, dual-write, verify counts, freeze, cutover.",
    ],
    F_REL,
)

from d07_spec_data import register_specs  # noqa: E402

register_specs(add)

try:
    from d07_bodies_p1 import BODIES as _P1_BODIES  # noqa: WPS433

    if "D07-T001" in _P1_BODIES:
        SPECS["D07-T001"] = _P1_BODIES["D07-T001"]
except ImportError:
    pass

BODIES: dict = SPECS


def build_note(t: dict, body: dict) -> str:
    tid = t["id"]
    num = int(tid.split("-T")[1])
    deps = ", ".join(f"`{d}`" for d in t.get("dependencies", [])[:4])
    prev = f"`D07-T{num-1:03d}`" if num > 1 else "`D05-T002`"
    nxt = f"`D07-T{num+1:03d}`" if num < 31 else "`D08-T001`"
    return f"""# {tid} — {t['name']}

Topic ID: `{tid}`
Domain: Database Fundamentals
Subdomain: {t['subdomain']}
Importance: {t['importance']}
Complexity: {t['complexity']}
Dependencies: {deps}
SQL in section F: unexecuted (illustrative only)

## A. Topic Overview

{body['overview']}

Prerequisites: {prev}. Next in the database track: {nxt}.

## B. First-Principles Explanation

{body['first_principles']}

## C. Internal Working and Architecture

{body['internal']}

## D. Diagrams and Visual Models

```mermaid
{body['mermaid']}
```

Read the diagram as a logical model for this topic; engine details vary by product.

## E. Examples and Analogies

{body['examples']}

## F. Code Examples

{body['code_section']}

## G. Practical Backend Application

{body['practical']}

## H. Advantages, Limitations and Trade-offs

{body['tradeoffs']}

## I. Common Mistakes and Misconceptions

{body['mistakes']}

## J. Debugging and Troubleshooting

{body['debugging']}

## K. Interview Preparation

{body['interview']}

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`. Try these before opening that file.

{body['exercises']}

## M. Revision Notes

{body['revision']}

## N. Related Topics

Understand this before: {prev}.

This topic supports: {nxt}.

Often confused with: adjacent domain-7 topics—read section N of neighbors when unsure.

Interviewers combine this with `D05-T021` pooling and `D07-T023` EXPLAIN.

## O. Completion Criteria

{body['completion']}
"""


def main() -> None:
    topics = load_topics()
    finished: list[str] = []
    failures: list[str] = []
    for t in topics:
        tid = t["id"]
        try:
            if tid not in BODIES:
                raise KeyError("no body")
            body = BODIES[tid]
            note_path = ROOT / t["note_path"]
            note_path.parent.mkdir(parents=True, exist_ok=True)
            note_path.write_text(build_note(t, body), encoding="utf-8")
            (ROOT / "EXERCISES" / f"{tid}.md").write_text(
                f"# Exercises — {tid}\n\nProblems only. Solutions: [{tid}](../solutions/{tid}.md).\n\n"
                + "\n".join(f"{i}. {x}" for i, x in enumerate(body["exercise_items"], 1))
                + "\n",
                encoding="utf-8",
            )
            (ROOT / "EXERCISES" / "solutions" / f"{tid}.md").write_text(
                "# Solutions for " + tid + "\n\nOpen this only after attempting the exercises.\n\n"
                + "\n\n".join(
                    f"## Exercise {i}\n\n{s}" for i, s in enumerate(body["solutions"], 1)
                )
                + "\n",
                encoding="utf-8",
            )
            rel = "../" + t["note_path"].replace("\\", "/")
            (ROOT / "INTERVIEW_BANK" / "items" / f"{tid}.md").write_text(
                f"# {tid} interview items\n\nDomain: Database Fundamentals\nTopic: {t['subdomain']}\n\n"
                "## Questions\n\n"
                + "\n".join(f"{i}. {q}" for i, q in enumerate(body["bank_questions"], 1))
                + f"\n\nAnswer key: [topic note section K]({rel}).\n",
                encoding="utf-8",
            )
            finished.append(tid)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{tid}: {exc}")
    print("FINISHED", ",".join(finished))
    print("FAILURES", "; ".join(failures) if failures else "none")


if __name__ == "__main__":
    main()

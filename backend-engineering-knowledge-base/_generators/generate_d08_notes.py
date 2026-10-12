#!/usr/bin/env python3
"""Generate D08-T001..D08-T023 notes, exercises, solutions, interview bank items."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "00_INDEX" / "inventory.json"
NOTES_DIR = ROOT / "07_ADVANCED_SQL" / "notes"
EX_DIR = ROOT / "EXERCISES"
SOL_DIR = EX_DIR / "solutions"
IB_DIR = ROOT / "INTERVIEW_BANK" / "items"

DOMAIN = "SQL — Advanced Topics"


def load_topics():
    data = json.loads(INV.read_text(encoding="utf-8"))
    return [t for t in data["topics"] if t["id"].startswith("D08-T")]


def slug_from_path(note_path: str) -> str:
    return Path(note_path).stem


def join_s(*parts: str) -> str:
    return " ".join(p.strip() for p in parts if p.strip())


def render_section_k(blocks: dict) -> str:
    out = ["## K. Interview Preparation", ""]
    for level, title in [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
        ("scenarios", "Scenarios"),
        ("followups", "Follow-ups"),
    ]:
        out.append(f"### {title}")
        out.append("")
        qs = blocks[level]
        for i, (q, a) in enumerate(qs, 1):
            out.append(f"#### Q{i}. {q}")
            out.append("")
            out.append(f"**Answer:** {a}")
            out.append("")
    return "\n".join(out)


def render_note(t: dict, body: dict) -> str:
    tid = t["id"]
    name = t["name"]
    deps = ", ".join(f"`{d}`" for d in t.get("dependencies", [])) or "none"
    slug = slug_from_path(t["note_path"])
    lines = [
        f"# {tid} — {name}",
        "",
        f"Topic ID: `{tid}`",
        f"Domain: {DOMAIN}",
        f"Subdomain: {t['subdomain']}",
        f"Importance: {t['importance']}",
        f"Complexity: {t['complexity']}",
        f"Dependencies: {deps}",
        "Execution status of the code in section F: not executed (illustrative PostgreSQL-style SQL)",
        "",
        "## A. Topic Overview",
        "",
        body["overview"],
        "",
        "## B. First-Principles Explanation",
        "",
        body["first_principles"],
        "",
        "## C. Internal Working and Architecture",
        "",
        body["internal"],
        "",
        "## D. Diagrams and Visual Models",
        "",
        body.get("diagram_intro", "The diagram below summarizes the main flow for this topic."),
        "",
        body["mermaid"],
        "",
        (body.get("diagram_after", "") + "\n" if body.get("diagram_after") else ""),
        "## E. Examples and Analogies",
        "",
        body["examples"],
        "",
        "## F. Code Examples",
        "",
        body["code_section"],
        "",
        "## G. Practical Backend Application",
        "",
        body["backend"],
        "",
        "## H. Advantages, Limitations and Trade-offs",
        "",
        body["tradeoffs"],
        "",
        "## I. Common Mistakes and Misconceptions",
        "",
        body["mistakes"],
        "",
        "## J. Debugging and Troubleshooting",
        "",
        body["debugging"],
        "",
        render_section_k(body["interview"]),
        "## L. Practical Exercises",
        "",
        f"Solutions are in `EXERCISES/solutions/{tid}.md`. Try these before opening that file.",
        "",
        body["exercises"],
        "",
        "## M. Revision Notes",
        "",
        body["revision"],
        "",
        "## N. Related Topics",
        "",
        body["related"],
        "",
        "## O. Completion Criteria",
        "",
        body["completion"],
        "",
    ]
    return "\n".join(lines)


def render_exercise(tid: str, items: list[str]) -> str:
    return "\n".join(
        [
            f"# Exercises — {tid}",
            "",
            f"Problems only. Solutions: [{tid}](../solutions/{tid}.md).",
            "",
        ]
        + [f"{i}. {item}" for i, item in enumerate(items, 1)]
        + [""]
    )


def render_solution(tid: str, parts: list[str]) -> str:
    out = [
        f"# Solutions for {tid}",
        "",
        "Open this only after attempting the exercises in the topic note.",
        "",
    ]
    for i, part in enumerate(parts, 1):
        out.append(f"## Exercise {i}")
        out.append("")
        out.append(part)
        out.append("")
    return "\n".join(out)


def render_interview_bank(t: dict, questions: list[str], note_rel: str) -> str:
    tid = t["id"]
    lines = [
        f"# {tid} interview items",
        "",
        f"Domain: {DOMAIN}",
        f"Topic: {t['name']}",
        "Difficulty mix: beginner, intermediate, advanced, scenario, follow-up",
        "Interview type: SQL, debugging, trade-off",
        "Full reasoned answers are in the topic note, section K.",
        "",
        "## Questions",
        "",
    ]
    for i, q in enumerate(questions, 1):
        lines.append(f"{i}. {q}")
    lines.extend(
        [
            "",
            f"Answer key: [topic note section K]({note_rel}).",
            "",
        ]
    )
    return "\n".join(lines)


# Shared sample schema referenced in SQL examples
SCHEMA_BLURB = join_s(
    "The examples assume PostgreSQL-compatible syntax on tables such as `customers`, `orders`, `order_items`, and `products`.",
    "Primary keys are bigint surrogates; amounts are stored in integer cents.",
    "Timestamps are `timestamptz`.",
    "None of the SQL below was run against a live database for this knowledge base.",
)


def mk_interview(topic_name: str, focus: str) -> dict:
    """Build 5+5+5+5+3 interview blocks with >=4 sentences each."""
    T = topic_name
    F = focus

    def b(q, a1, a2, a3, a4, a5=""):
        return (q, join_s(a1, a2, a3, a4, a5))

    return {
        "beginner": [
            b(
                f"What is {T} in SQL?",
                f"{T} is a language feature that lets you {F} without pulling intermediate results into application memory.",
                "Relational engines evaluate it as part of a single query plan, which means the optimizer can reorder work, push predicates, and choose join algorithms.",
                "In backend services you still express business rules in SQL or in an ORM translation, but the database remains the place where large datasets are filtered and combined.",
                "Interviewers ask this to see whether you treat SQL as a thin CRUD layer or as a data-processing tool.",
            ),
            b(
                f"When would you use {T} instead of application code?",
                f"Use {T} when the working set is already in the database and network round trips dominate.",
                "Shipping thousands of rows to a service only to filter or aggregate them wastes CPU and bandwidth.",
                "Keeping the logic in SQL also preserves transactional consistency: you see one snapshot of data for the whole statement.",
                "The trade-off is readability and testability in the app repo, which is why teams document complex SQL and cover it with integration tests.",
            ),
            b(
                "How does this relate to indexes?",
                "Indexes change how the engine finds rows, not the meaning of your query.",
                f"For {T}, the planner still needs selective predicates or join keys that match index leading columns.",
                "A beautiful query that scans an entire fact table will fail in production regardless of syntax sophistication.",
                "When you design a feature around advanced SQL, co-design the supporting indexes and verify plans with `EXPLAIN (ANALYZE, BUFFERS)`.",
            ),
            b(
                "What is the difference between INNER and OUTER joins?",
                "INNER JOIN keeps only row pairs that satisfy the join predicate on both sides.",
                "LEFT OUTER JOIN keeps every row from the left table and fills missing right-side columns with NULL.",
                "That distinction matters for reporting: an INNER JOIN silently drops customers with zero orders, while a LEFT JOIN exposes them with NULL order fields.",
                "Choosing the wrong join type is one of the most common sources of 'missing data' bugs in analytics APIs.",
            ),
            b(
                "Why do interviewers care about SQL in backend roles?",
                "Most production systems still use a relational database for authoritative state.",
                "ORMs hide SQL until latency or correctness breaks, and seniors are expected to read execution plans.",
                f"Topics like {T} separate candidates who can debug data issues from those who only wire REST endpoints.",
                "You are not expected to memorize every dialect edge case, but you must know how to reason about correctness, NULLs, and performance.",
            ),
        ],
        "intermediate": [
            b(
                f"How would you test a query that uses {T}?",
                "Start with fixture tables that include empty sets, duplicates, and NULL foreign keys.",
                "Assert row counts and spot-check aggregates against hand-calculated expectations.",
                "Run the statement inside a transaction in CI against a real engine, because SQLite and PostgreSQL differ on edge cases.",
                "Capture `EXPLAIN` output for the happy path so plan regressions show up when statistics drift.",
            ),
            b(
                f"What portability issues appear with {T}?",
                "PostgreSQL, MySQL, and SQL Server extend standard SQL with different keywords and function names.",
                "Upsert syntax, locking hints, and JSON operators are the usual portability cliffs.",
                "Microservices on one engine can still leak dialect if read replicas or analytics warehouses differ.",
                "Document the target engine in migrations and add contract tests when you must support more than one.",
            ),
            b(
                "How do NULLs interact with joins and filters?",
                "SQL uses three-valued logic: predicates can be TRUE, FALSE, or UNKNOWN.",
                "Comparing anything to NULL with `=` yields UNKNOWN, so those rows drop out of `WHERE` but still appear in OUTER joins unless you handle them.",
                "`IS DISTINCT FROM` and explicit `IS NULL` checks make intent obvious.",
                "Reports that use `COUNT(*)` versus `COUNT(column)` diverge when the column is nullable.",
            ),
            b(
                "When is a subquery rewritten into a join?",
                "Optimizers often decorrelate correlated subqueries into semi-joins or anti-joins.",
                "Whether that happens depends on cost estimates, statistics, and version-specific rules.",
                "You should not rely on a subquery staying nested; write the clearest form and verify the plan.",
                "Sometimes a manual rewrite to `EXISTS` or a CTE is both clearer and faster.",
            ),
            b(
                "How does connection pooling affect long SQL statements?",
                "Poolers multiplex many clients onto fewer server connections.",
                "A statement that holds a connection while scanning terabytes blocks other work on that connection.",
                "Transactions that stay open across awaits in application code pin connections and cause pool exhaustion.",
                "Keep transactions short, stream large results with cursors if needed, and set statement timeouts.",
            ),
        ],
        "advanced": [
            b(
                f"How can {T} cause a performance cliff?",
                "Cardinality estimates that are off by orders of magnitude make the planner pick nested loops over hash joins or vice versa.",
                "Correlated execution can devolve into per-row subquery evaluation if decorrelation fails.",
                "Wide result sets defeat covering indexes and force heap fetches.",
                "Mitigate with fresh statistics, targeted indexes, predicate pushdown, and breaking work into stages with temp tables when appropriate.",
            ),
            b(
                "Explain MVCC interaction with locking reads.",
                "Under MVCC, readers do not block writers on row versions, but `SELECT FOR UPDATE` takes row-level locks on current tuples.",
                "A locking read establishes what you are allowed to update before you mutate.",
                "If two transactions lock rows in opposite order, you can still deadlock.",
                "Design lock order consistently and use short transactions.",
            ),
            b(
                "How do you version breaking SQL changes?",
                "Ship additive schema first: new columns, backfill jobs, dual-write periods.",
                "Deploy query changes behind feature flags only when semantics are backward compatible.",
                "For renames, use views as compatibility shims until all callers migrate.",
                "Measure query latency and error rates per release; roll back the app if the database change is irreversible.",
            ),
            b(
                "What is the difference between logical and physical query plans?",
                "The logical plan is relational algebra: joins, filters, projections.",
                "The physical plan chooses algorithms: index scan, bitmap heap scan, hash aggregate.",
                "`EXPLAIN` shows the physical plan the executor will run.",
                "Advanced SQL authors read both the shape (many nested loops) and the actual timings from `EXPLAIN ANALYZE`.",
            ),
            b(
                "How would you secure dynamic SQL built from user filters?",
                "Never concatenate user strings into SQL text.",
                "Use parameterized queries for values and allow-list column names for dynamic sort or filter fields.",
                "ORM query builders still need review when they expose raw fragments.",
                "Log query templates with parameters redacted, and cap sortable fields to indexed columns to avoid sort explosions.",
            ),
        ],
        "scenarios": [
            b(
                "An API returns duplicate parent rows after you added a join. What happened?",
                "You likely used an INNER JOIN to a one-to-many child table without aggregating or deduplicating.",
                "Each parent repeats once per child row, which breaks pagination counts in the API.",
                "Fix with a subquery or CTE that aggregates children first, or use `DISTINCT ON` / window `ROW_NUMBER` when appropriate.",
                "Add an integration test that asserts one DTO per parent id.",
            ),
            b(
                "A nightly job suddenly times out after data doubled. First steps?",
                "Confirm whether the timeout is statement, lock wait, or pool wait.",
                "Capture `EXPLAIN (ANALYZE, BUFFERS)` for the failing statement on production-like data.",
                "Check for missing indexes on new join keys introduced by a feature flag.",
                "Consider partitioning or incremental processing instead of one monolithic scan.",
            ),
            b(
                "Two services upsert the same natural key concurrently. How do you avoid lost updates?",
                "Use a single `INSERT ... ON CONFLICT` or equivalent with a clear conflict target.",
                "Define which columns are immutable versus mergeable on conflict.",
                "Serialize critical sections with row locks or advisory locks when business rules require read-modify-write.",
                "Emit metrics on conflict rate so you detect hot keys before they become incidents.",
            ),
            b(
                "Read replica lag makes a dashboard show stale ranks. Options?",
                "Route interactive analytics to the primary or a delayed-tolerance cache.",
                "Materialize rankings on a schedule into a table refreshed by the job.",
                "Expose 'as of' timestamps in the API so users understand staleness.",
                "Do not assume read-your-writes on replicas unless the driver pins sessions.",
            ),
            b(
                "JSON attributes power search but CPU is high. What do you change?",
                "Move hot filter fields into typed columns with indexes.",
                "Use JSONB with GIN indexes on specific paths instead of parsing text JSON.",
                "Avoid `->>` without functional indexes when predicates run on every request.",
                "Validate document shape at write time so queries do not branch on missing keys.",
            ),
        ],
        "followups": [
            b(
                "How does this connect to ORM N+1 issues?",
                "ORMs lazy-load associations with one query per parent row unless you eager fetch or join.",
                f"Advanced SQL such as {T} is often the fix: one query with joins or batch `IN` loads.",
                "See `D08-T021` for the application-side diagnosis patterns.",
                "The best teams measure SQL statement count per HTTP request.",
            ),
            b(
                "When should logic live in a stored procedure?",
                "When multiple clients must share identical rules and round trips dominate.",
                "When you need atomic multi-step workflows close to data.",
                "Avoid when release cadence of app and database cannot move together.",
                "See `D08-T016` for triggers versus application services.",
            ),
            b(
                "What PostgreSQL topics deepen this further?",
                "MVCC, WAL, vacuum, and planner statistics change how the same SQL behaves over time.",
                "Domain `D09` covers internals that explain bloat, index-only scans failing, and replication lag.",
                "Interviewers at database-heavy companies bridge advanced SQL questions into those internals.",
                "Read `EXPLAIN` output alongside wait events when tuning.",
            ),
        ],
    }


def topic_bodies() -> dict[str, dict]:
    """Per-topic content overrides keyed by topic id."""
    bodies = {}

    def add(tid, **kwargs):
        bodies[tid] = kwargs

    sql_hdr = (
        "Dialect: PostgreSQL 15+ style (adjust identifiers for your engine).\n\n"
        "Status: **not executed** — illustrative only.\n"
    )

    # D08-T001
    add(
        "D08-T001",
        overview=join_s(
            "Advanced joins combine multiple relations in one SQL statement: inner, left/right/full outer, cross, semi-join (`EXISTS`), and anti-join (`NOT EXISTS`).",
            "They are the primary tool for assembling API responses from normalized tables without N+1 round trips.",
            "Production risk is cardinality explosion when a one-to-many join duplicates parent rows.",
            "Prerequisites: relational keys and basic joins (`D07-T001`, `D07-T002`).",
        ),
        first_principles=join_s(
            "A join is a relational product restricted by a predicate.",
            "The optimizer chooses between nested loop, hash join, and merge join based on row estimates and available indexes.",
            "Join order matters for performance even when commutative algebra says results should match.",
            "NULL in join keys never matches with equality joins, which surprises teams migrating from document stores.",
        ),
        internal=join_s(
            "The planner builds a join tree.",
            "Each edge applies a predicate; outer joins also mark preserved sides.",
            "Late filters in `WHERE` can turn outer joins into inner joins accidentally if they null-reject.",
            "Hash joins build a hash table on the smaller side; nested loops probe an index on the inner side.",
        ),
        mermaid="""```mermaid
flowchart TD
  ordersTbl[orders]
  customersTbl[customers]
  hashBuild[HashJoin_build_probe]
  resultRows[Result_rows]
  ordersTbl --> hashBuild
  customersTbl --> hashBuild
  hashBuild --> resultRows
```""",
        examples=join_s(
            "Analogy: joining tables is like matching invoices to shipping labels by order id.",
            "If you tape every line item onto the invoice before matching, you duplicate the invoice header.",
            "Use a staging aggregate of line items first when you need one row per order.",
        ),
        code_section=sql_hdr
        + """```sql
-- Active customers with their latest order total (not executed)
WITH latest AS (
  SELECT DISTINCT ON (customer_id)
         customer_id, id AS order_id, total_cents, created_at
  FROM orders
  ORDER BY customer_id, created_at DESC
)
SELECT c.id, c.email, l.order_id, l.total_cents
FROM customers c
LEFT JOIN latest l ON l.customer_id = c.id
WHERE c.status = 'active';
```""",
        backend=join_s(
            "List endpoints that embed child collections should aggregate in SQL or fetch in two queries with batching.",
            "Always count rows after joins when paginating parents.",
            "Log slow join queries with hash join vs nested loop choice from `EXPLAIN`.",
        ),
        tradeoffs="""| Join type | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| INNER | Smallest result | Drops non-matching parents | Fact tables with required FK | You need zero-child parents |
| LEFT | Keeps driving table | Wider rows, NULL handling | Customer + optional order | You will filter NULLs in WHERE without care |
| EXISTS semi | Stops at first match | Harder to read for juniors | Presence checks | You need columns from right table |
| CROSS | Cartesian base for gaps | Explodes rows | Small generators | Large tables |""",
        mistakes="- Putting `orders.status = 'paid'` in `WHERE` after `LEFT JOIN orders` removes customers with no paid orders.\n- Joining on text emails instead of surrogate keys.\n- Assuming ORM `include` always produces one efficient join.",
        debugging=join_s(
            "Symptom: duplicated DTOs. Check join fan-out.",
            "Symptom: missing parents. Check INNER vs LEFT.",
            "Run `EXPLAIN ANALYZE`, compare estimated vs actual rows on each join node.",
        ),
        interview=mk_interview("advanced joins", "combine normalized tables"),
        exercises="""### Exercise 1 — implementation

Write SQL that lists each `customer_id` with count of orders in the last 30 days, including customers with zero orders. Acceptance: one row per customer; zero counts appear as 0 not missing.

### Exercise 2 — debugging

A report doubled revenue after joining `order_items`. Explain the fan-out and rewrite using a pre-aggregated subquery. Acceptance: you name cardinality explosion.

### Exercise 3 — trade-off

Choose between `LEFT JOIN` + `WHERE child IS NULL` versus `NOT EXISTS` for customers without orders. Acceptance: you mention NULL semantics and planner semi-join.""",
        revision="- INNER keeps matches; LEFT keeps left rows.\n- Fan-out duplicates parents.\n- EXISTS for existence; JOIN for columns.\n- Verify plans after data grows.",
        related="Prerequisites: `D07-T001`, `D07-T002`. Next: `D08-T002` correlated subqueries. Often confused with cartesian products from missing join predicates.",
        completion="- Write a LEFT JOIN report without turning it into INNER.\n- Diagnose duplicate rows from one-to-many joins.\n- Pick EXISTS vs JOIN for a presence filter.\n- Read a join tree in `EXPLAIN`.\n- Design an API query that returns one parent per page.",
    )

    # D08-T002
    add(
        "D08-T002",
        overview=join_s(
            "A correlated subquery references columns from an outer query and is re-evaluated per outer row unless the optimizer decorrelates it.",
            "They express per-row conditions such as 'latest child' or 'exists related row'.",
            "They are powerful but can become O(n²) if the planner nests loops.",
            "Depends on join fluency (`D08-T001`).",
        ),
        first_principles=join_s(
            "Correlation means the inner query is not standalone.",
            "Semantically it is a nested loop; physically it may become a hash semi-join.",
            "`EXISTS` and scalar subqueries with `LIMIT 1` are common patterns.",
        ),
        internal=join_s(
            "Decorrelation transforms APPLY-like logic into joins.",
            "When decorrelation fails, each outer row triggers an index probe or scan.",
            "Statistics on the correlation column decide whether that is cheap.",
        ),
        mermaid="""```mermaid
flowchart TD
  outerScan[Outer_row_scan]
  innerProbe[Correlated_inner_probe]
  outerScan -->|per_row| innerProbe
  innerProbe --> outerScan
```""",
        examples="Correlated subqueries are like asking, for each student, 'what was their highest exam score?' without first building a class-wide leaderboard.",
        code_section=sql_hdr
        + """```sql
-- Orders above the customer's own average (not executed)
SELECT o.id, o.customer_id, o.total_cents
FROM orders o
WHERE o.total_cents > (
  SELECT AVG(o2.total_cents)
  FROM orders o2
  WHERE o2.customer_id = o.customer_id
);
```""",
        backend="Use correlation for per-entity thresholds; prefer window functions when you need many ranked metrics per partition (`D08-T005`).",
        tradeoffs="| Form | Benefit | Cost |\n| --- | --- | --- |\n| Correlated subquery | Clear per-row logic | Risk nested loops |\n| Join + aggregate | Set-oriented | More grouping |",
        mistakes="- Scalar subquery returning more than one row.\n- Correlating on non-indexed columns at scale.",
        debugging="Compare `EXPLAIN` nested loop counts; rewrite to `EXISTS` or windows if loops dominate.",
        interview=mk_interview("correlated subqueries", "express per-outer-row filters"),
        exercises="""### Exercise 1 — implementation

Find products never ordered using `NOT EXISTS`. Acceptance: anti-join semantics, no duplicate products.

### Exercise 2 — debugging

A correlated subquery times out on 5M orders. Propose a window-function rewrite. Acceptance: you remove per-row aggregation.

### Exercise 3 — trade-off

Compare correlated `MAX(created_at)` vs `DISTINCT ON` for latest row per key.""",
        revision="- Correlation references outer columns.\n- Decorrelation is not guaranteed.\n- EXISTS stops at first match.\n- Watch nested loops in EXPLAIN.",
        related="Builds on `D08-T001`. Leads to `D08-T003` CTEs for readability.",
        completion="- Rewrite a correlated filter to EXISTS.\n- Spot nested loop per row in a plan.\n- Choose scalar subquery vs JOIN.",
    )

    # D08-T003 CTEs
    add(
        "D08-T003",
        overview=join_s(
            "Common Table Expressions (`WITH`) name subqueries for readability and reuse within one statement.",
            "They do not inherently materialize; the optimizer can inline them.",
            "CTEs structure multi-step reports and prepare data for window functions.",
        ),
        first_principles=join_s(
            "A CTE is a named subquery in the `WITH` clause.",
            "Scope is the single statement unless you create a temp table.",
            "PostgreSQL 12+ may inline non-recursive CTEs; older versions often materialized them.",
        ),
        internal="Multiple CTEs chain; the planner may fuse them. `MATERIALIZED` hint (PostgreSQL) forces storage when needed to avoid recomputation.",
        mermaid="""```mermaid
flowchart TD
  cte1[CTE_filtered_orders]
  cte2[CTE_customer_totals]
  finalSelect[Final_SELECT]
  cte1 --> cte2
  cte2 --> finalSelect
```""",
        examples="CTEs are like labeled scratch paper for one homework problem: you can refer back to step 1 when doing step 3.",
        code_section=sql_hdr
        + """```sql
WITH paid AS (
  SELECT customer_id, SUM(total_cents) AS spend
  FROM orders
  WHERE status = 'paid'
  GROUP BY customer_id
)
SELECT c.email, COALESCE(p.spend, 0) AS spend
FROM customers c
LEFT JOIN paid p ON p.customer_id = c.id;
```""",
        backend="Expose complex analytics as named CTEs in migration-reviewed SQL files; avoid string-built CTE names from users.",
        tradeoffs="| Approach | Benefit | Cost |\n| CTE | Readable stages | May inline unpredictably |\n| Temp table | Stable stats | DDL + cleanup |",
        mistakes="- Assuming CTEs always improve performance.\n- Recursive CTE missing termination (`D08-T004`).",
        debugging="Use `EXPLAIN` to see if CTE is inlined; compare with temp table if estimates diverge.",
        interview=mk_interview("CTEs", "stage multi-step queries"),
        exercises="""### Exercise 1 — implementation

Use two CTEs to compute top-spending customer per country. Acceptance: one winner per country.

### Exercise 2 — debugging

A CTE made the query slower after upgrade. Explain inlining vs materialization.

### Exercise 3 — trade-off

CTE vs nested subquery in FROM for readability and testability.""",
        revision="- WITH names subqueries.\n- Not always materialized.\n- Great for staged reporting.\n- MATERIALIZED when needed.",
        related="After `D08-T002`. Before recursive CTEs `D08-T004`.",
        completion="- Refactor nested subqueries into CTEs.\n- Predict inlining effects.\n- Chain multiple CTEs safely.",
    )

    # D08-T004 Recursive CTE
    add(
        "D08-T004",
        overview=join_s(
            "Recursive CTEs model hierarchies: org charts, category trees, graph reachability with a base case and recursive member.",
            "They replace procedural loops in application code for tree walks.",
            "Termination requires a decreasing measure or cycle detection.",
        ),
        first_principles="Union ALL combines anchor rows with rows produced by joining working set to the table again.",
        internal="The engine iterates until no new rows; worktables store frontier rows. Depth limits prevent runaway graphs.",
        mermaid="""```mermaid
flowchart TD
  anchor[Anchor_query]
  recursivePart[Recursive_member]
  worktable[Working_set]
  anchor --> worktable
  worktable --> recursivePart
  recursivePart -->|new_rows| worktable
```""",
        examples="Like forwarding a chain letter one hop at a time until no new recipients appear.",
        code_section=sql_hdr
        + """```sql
WITH RECURSIVE category_tree AS (
  SELECT id, parent_id, name, 1 AS depth
  FROM categories
  WHERE parent_id IS NULL
  UNION ALL
  SELECT c.id, c.parent_id, c.name, t.depth + 1
  FROM categories c
  JOIN category_tree t ON c.parent_id = t.id
  WHERE t.depth < 20
)
SELECT * FROM category_tree;
```""",
        backend="Use for breadcrumbs and permission inheritance; cap depth and index `parent_id`.",
        tradeoffs="| Tool | Use | Risk |\n| Recursive CTE | DB-side traversal | Cycles without guard |",
        mistakes="- Missing cycle detection on graphs.\n- Unbounded depth blowing work memory.",
        debugging="Log iteration counts; add `path` arrays and `WHERE NOT id = ANY(path)` for cycles.",
        interview=mk_interview("recursive CTEs", "walk hierarchies in SQL"),
        exercises="""### Exercise 1 — implementation

Return all descendant category ids for a given root id.

### Exercise 2 — debugging

Infinite recursion on bad data; add cycle guard.

### Exercise 3 — trade-off

Recursive CTE vs closure table for read-heavy trees.""",
        revision="- Anchor + recursive member.\n- Always bound depth or detect cycles.\n- Index parent_id.",
        related="Extends `D08-T003`. Pairs with adjacency list modeling in `D07`.",
        completion="- Write a bounded recursive CTE.\n- Detect cycles.\n- Compare to materialized path.",
    )

    # D08-T005 Window functions
    add(
        "D08-T005",
        overview=join_s(
            "Window functions compute aggregates over a partition without collapsing rows.",
            "They power rankings, running totals, and comparing each row to partition peers.",
            "Unlike `GROUP BY`, output row count matches input row count of the partition source.",
        ),
        first_principles="`OVER (PARTITION BY ... ORDER BY ...)` defines the window frame; frames can be rows or range based.",
        internal="Sort or hash partitions; frame edges move per row for sliding windows.",
        mermaid="""```mermaid
flowchart TD
  inputRows[Input_rows]
  partition[Partition_by_key]
  windowFn[Window_function]
  outputRows[Same_row_count]
  inputRows --> partition
  partition --> windowFn
  windowFn --> outputRows
```""",
        examples="Like grading on a curve within each classroom without merging students into one summary row.",
        code_section=sql_hdr
        + """```sql
SELECT id, customer_id, total_cents,
       SUM(total_cents) OVER (
         PARTITION BY customer_id
         ORDER BY created_at
         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total
FROM orders;
```""",
        backend="Use for leaderboard slices in SQL instead of loading all rows to the app.",
        tradeoffs="| GROUP BY | Window |\n| Fewer rows | Same rows + metrics |",
        mistakes="- Forgetting ORDER BY in running calculations.\n- Mixing windows with DISTINCT incorrectly.",
        debugging="Check sort nodes in EXPLAIN; ensure partition keys match indexes.",
        interview=mk_interview("window functions", "compute per-row analytics"),
        exercises="""### Exercise 1 — implementation

Add `running_total` per customer by `created_at`.

### Exercise 2 — debugging

Running total resets unexpectedly; fix PARTITION BY.

### Exercise 3 — trade-off

Self-join vs window for prior-row comparison.""",
        revision="- OVER defines window.\n- PARTITION BY groups.\n- Frames control running metrics.",
        related="Leads to ranking `D08-T006` and moving averages `D08-T007`.",
        completion="- Write PARTITION BY + ORDER BY windows.\n- Choose ROWS vs RANGE frames.",
    )

    # D08-T006 Ranking
    add(
        "D08-T006",
        overview=join_s(
            "Ranking functions assign positions: `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTILE`.",
            "Tie-breaking rules differ: gaps vs no gaps vs bucket quotas.",
            "Common for top-N per group queries.",
        ),
        first_principles="Ordering inside OVER determines rank; ties behave per function definition.",
        internal="Sort-based plans; deduplicate with `ROW_NUMBER` when ties must pick one.",
        mermaid="""```mermaid
flowchart TD
  partition[Partition]
  orderBy[ORDER_BY_metric]
  rankFn[RANK_family]
  partition --> orderBy
  orderBy --> rankFn
```""",
        examples="Olympic medals: gold shares rank 1, next is bronze rank 3 with RANK but rank 2 with DENSE_RANK.",
        code_section=sql_hdr
        + """```sql
SELECT * FROM (
  SELECT customer_id, total_cents,
         ROW_NUMBER() OVER (
           PARTITION BY date_trunc('month', created_at)
           ORDER BY total_cents DESC
         ) AS rn
  FROM orders
) x WHERE rn <= 3;
```""",
        backend="Top-N per month reports; cap N to keep indexes useful.",
        tradeoffs="| Function | Ties |\n| ROW_NUMBER | unique |\n| RANK | gaps |",
        mistakes="- Using RANK when product needs unique winners.\n- Filtering ranks in WHERE without subquery.",
        debugging="Validate tie cases with fixture data.",
        interview=mk_interview("ranking functions", "assign ordered positions"),
        exercises="""### Exercise 1 — top 3 orders per customer.

### Exercise 2 — explain RANK vs DENSE_RANK on tied scores.

### Exercise 3 — NTILE for quartile billing tiers.""",
        revision="- ROW_NUMBER unique.\n- RANK skips after ties.\n- Filter top-N in outer query.",
        related="Builds on `D08-T005`.",
        completion="- Pick rank function for tie policy.\n- Write top-N per group.",
    )

    # D08-T007 Running totals / moving avg
    add(
        "D08-T007",
        overview=join_s(
            "Running totals and moving averages use window frames sliding over ordered rows.",
            "RANGE frames use logical units (dates); ROWS frames use peer rows.",
            "Financial and ops dashboards use them for trend lines.",
        ),
        first_principles="Frame bounds `PRECEDING`/`FOLLOWING` define which rows contribute to each aggregate.",
        internal="Sort per partition; sliding ROWS frames are cheaper than wide RANGE on timestamps without normalization.",
        mermaid="""```mermaid
flowchart LR
  row_i[Current_row]
  frameRows[Frame_rows]
  agg[AVG_or_SUM]
  row_i --> frameRows
  frameRows --> agg
```""",
        examples="A seven-day moving average of error rate smooths weekend spikes.",
        code_section=sql_hdr
        + """```sql
SELECT day, errors,
       AVG(errors) OVER (
         ORDER BY day
         ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
       ) AS ma7
FROM daily_errors;
```""",
        backend="Pre-aggregate to daily buckets before windows on high-volume events.",
        tradeoffs="| Pre-aggregate table | On-the-fly window |\n| Faster read | Flexible ad hoc |",
        mistakes="- RANGE on timestamptz without understanding peer groups.\n- Dividing by zero in averages.",
        debugging="Compare frame boundaries on sparse dates.",
        interview=mk_interview("running totals and moving averages", "smooth time series in SQL"),
        exercises="""### Exercise 1 — 7-day moving average of revenue.

### Exercise 2 — running total that excludes current row.

### Exercise 3 — RANGE vs ROWS for calendar months.""",
        revision="- Frames define contributors.\n- ROWS vs RANGE semantics.\n- Bucket before windowing at scale.",
        related="Extends `D08-T006`.",
        completion="- Implement MA7.\n- Explain frame bounds.",
    )

    # D08-T008 CASE COALESCE NULLIF
    add(
        "D08-T008",
        overview=join_s(
            "`CASE`, `COALESCE`, and `NULLIF` shape values and handle missing data in projections.",
            "They keep transformations declarative instead of scattered in application code.",
            "They interact with three-valued logic when conditions involve NULL.",
        ),
        first_principles="CASE is structured if/else; COALESCE returns first non-NULL; NULLIF maps equal values to NULL.",
        internal="Evaluated per row during projection; short-circuit rules are dialect-specific for CASE.",
        mermaid="""```mermaid
flowchart TD
  rowIn[Input_row]
  caseExpr[CASE_expression]
  coalesceExpr[COALESCE_chain]
  rowOut[Projected_row]
  rowIn --> caseExpr
  caseExpr --> coalesceExpr
  coalesceExpr --> rowOut
```""",
        examples="COALESCE is a fallback chain like trying backup phone numbers until one answers.",
        code_section=sql_hdr
        + """```sql
SELECT id,
       COALESCE(nickname, legal_name, 'unknown') AS display_name,
       CASE status
         WHEN 'paid' THEN total_cents
         WHEN 'refunded' THEN -total_cents
         ELSE 0
       END AS signed_total
FROM orders;
```""",
        backend="Map enums to API labels in SQL views for stable contracts.",
        tradeoffs="| App mapping | SQL CASE |\n| Unit tests in language | Single query truth |",
        mistakes="- `COALESCE` hiding missing required fields.\n- CASE without ELSE returning NULL unexpectedly.",
        debugging="Print intermediate columns in SELECT to see which branch fired.",
        interview=mk_interview("CASE, COALESCE, and NULLIF", "normalize values in queries"),
        exercises="""### Exercise 1 — display name fallback chain.

### Exercise 2 — NULLIF to avoid divide-by-zero.

### Exercise 3 — CASE vs lookup table trade-off.""",
        revision="- COALESCE first non-NULL.\n- NULLIF to NULL on match.\n- CASE for branching.",
        related="Leads to NULL semantics `D08-T009`.",
        completion="- Write safe divide with NULLIF.\n- Use CASE for signed amounts.",
    )

    # D08-T009 NULL semantics
    add(
        "D08-T009",
        overview=join_s(
            "SQL NULL means unknown, not zero or empty string.",
            "Three-valued logic makes `WHERE` filters drop UNKNOWN rows.",
            "`IS NULL`, `IS NOT NULL`, and `IS DISTINCT FROM` express intent clearly.",
        ),
        first_principles="Boolean expressions can be TRUE, FALSE, or UNKNOWN; AND/OR have defined truth tables.",
        internal="Indexes can use partial indexes on `WHERE col IS NOT NULL`; unique constraints treat NULL distinctly in SQL standard.",
        mermaid="""```mermaid
flowchart TD
  predicate[Predicate_with_NULL]
  unknown[UNKNOWN]
  whereClause[WHERE_filter]
  dropped[Row_dropped]
  predicate --> unknown
  unknown --> whereClause
  whereClause --> dropped
```""",
        examples="Unknown age on a form is not the same as age zero.",
        code_section=sql_hdr
        + """```sql
SELECT COUNT(*) AS all_rows,
       COUNT(email) AS non_null_emails
FROM customers;

SELECT *
FROM customers
WHERE phone IS DISTINCT FROM '+10000000000';
```""",
        backend="APIs should distinguish omitted fields from explicit null in PATCH semantics; database NULL is not JSON null only by convention.",
        tradeoffs="| Sentinel values | NULL |\n| Breaks uniqueness | Needs careful queries |",
        mistakes="- `WHERE col = NULL`.\n- `NOT IN` with NULL in subquery.",
        debugging="Rewrite predicates with `IS NULL` tests; check `NOT IN` subquery for NULLs.",
        interview=mk_interview("NULL semantics", "reason about unknown values"),
        exercises="""### Exercise 1 — count NULL vs non-NULL emails.

### Exercise 2 — fix `NOT IN` trap with NULL sku.

### Exercise 3 — explain UNKNOWN in WHERE.""",
        revision="- NULL is unknown.\n- Use IS NULL tests.\n- NOT IN + NULL is subtle.",
        related="Follows `D08-T008`. Before upserts `D08-T010`.",
        completion="- Fix NULL comparisons.\n- Use IS DISTINCT FROM.",
    )

    # D08-T010 Upserts
    add(
        "D08-T010",
        overview=join_s(
            "Upserts insert a row or update on unique violation using `ON CONFLICT`, `MERGE`, or dialect equivalents.",
            "They implement idempotent ingestion and sync from external systems.",
            "Conflict targets must match a unique index exactly.",
        ),
        first_principles="Insert attempts first; on conflict, update or do nothing per policy.",
        internal="Unique index lookup on insert; row-level lock on conflicting tuple during update.",
        mermaid="""```mermaid
flowchart TD
  insertTry[INSERT_attempt]
  conflict{Unique_violation}
  updateBranch[ON_CONFLICT_UPDATE]
  done[Committed_row]
  insertTry --> conflict
  conflict -->|yes| updateBranch
  conflict -->|no| done
  updateBranch --> done
```""",
        examples="Like dropping mail in a mailbox that replaces the previous letter with the same tracking number.",
        code_section=sql_hdr
        + """```sql
INSERT INTO customer_sync (external_id, email, updated_at)
VALUES ($1, $2, now())
ON CONFLICT (external_id) DO UPDATE
SET email = EXCLUDED.email,
    updated_at = EXCLUDED.updated_at
WHERE customer_sync.updated_at < EXCLUDED.updated_at;
```""",
        backend="Use natural keys from vendors; log conflict actions; avoid blind overwrite of nullable columns.",
        tradeoffs="| Separate SELECT+UPDATE | Upsert |\n| More round trips | Atomic |",
        mistakes="- Missing conflict target column list.\n- Updating immutable columns on conflict.",
        debugging="Check `sqlstate 23505`; verify unique index columns match conflict clause.",
        interview=mk_interview("upserts", "merge rows on unique keys"),
        exercises="""### Exercise 1 — idempotent webhook insert.

### Exercise 2 — DO NOTHING vs DO UPDATE choice.

### Exercise 3 — conditional update with WHERE on conflict.""",
        revision="- ON CONFLICT needs unique index.\n- EXCLUDED refers to proposed row.\n- Conditional updates prevent stale writes.",
        related="After NULL semantics. Before transactions `D08-T011`.",
        completion="- Write PostgreSQL upsert.\n- Explain EXCLUDED.\n- Guard against stale overwrites.",
    )

    # D08-T011 Transactions
    add(
        "D08-T011",
        overview=join_s(
            "Transactions group statements into atomic units with ACID guarantees.",
            "Savepoints create nested rollback points within a transaction.",
            "Backend services should keep transactions short and boundary-aligned with use cases.",
        ),
        first_principles="BEGIN starts; COMMIT makes durable; ROLLBACK undoes; savepoints name partial undo.",
        internal="WAL records changes; locks held until commit; isolation level controls visibility.",
        mermaid="""```mermaid
flowchart TD
  beginTx[BEGIN]
  work[Statements]
  savepoint[SAVEPOINT_sp1]
  rollbackSp[ROLLBACK_TO_sp1]
  commit[COMMIT]
  beginTx --> work
  work --> savepoint
  savepoint --> rollbackSp
  rollbackSp --> work
  work --> commit
```""",
        examples="A savepoint is a bookmark you can return to without throwing away the whole chapter.",
        code_section=sql_hdr
        + """```sql
BEGIN;
INSERT INTO orders (customer_id, total_cents) VALUES (1, 5000);
SAVEPOINT line_items;
INSERT INTO order_items (order_id, sku, qty) VALUES (currval('orders_id_seq'), 'ABC', 1);
-- on validation error: ROLLBACK TO SAVEPOINT line_items;
COMMIT;
```""",
        backend="One transaction per request for financial flows; never span user think time.",
        tradeoffs="| Single TX | Choreographed sagas |\n| Strong consistency | Cross-service |",
        mistakes="- Long transactions during external HTTP calls.\n- Assuming READ COMMITTED prevents all anomalies you care about.",
        debugging="Check `pg_stat_activity` wait events; log transaction duration.",
        interview=mk_interview("transactions and savepoints", "group atomic database work"),
        exercises="""### Exercise 1 — order + items atomic insert.

### Exercise 2 — when to ROLLBACK TO SAVEPOINT.

### Exercise 3 — isolation level pick for report vs payment.""",
        revision="- Keep TX short.\n- Savepoints partial undo.\n- Isolation defines visibility.",
        related="Before locking reads `D08-T012`.",
        completion="- Bound a use case in one transaction.\n- Use savepoints safely.",
    )

    # D08-T012 Locking reads
    add(
        "D08-T012",
        overview=join_s(
            "Locking reads (`SELECT ... FOR UPDATE`, `FOR SHARE`) lock rows for subsequent writes in the same transaction.",
            "They implement pessimistic concurrency when optimistic versioning is insufficient.",
            "Lock order and index access paths affect deadlock risk.",
        ),
        first_principles="Locks serialize conflicting operations on tuples; readers block writers only when lock modes conflict.",
        internal="Row-level locks in PostgreSQL; gap/next-key locks in InnoDB under some isolations.",
        mermaid="""```mermaid
sequenceDiagram
  participant TxA as TxA
  participant DB as Database
  participant TxB as TxB
  TxA->>DB: SELECT_FOR_UPDATE_row
  TxB->>DB: UPDATE_same_row
  DB-->>TxB: blocks_until_A_commits
```""",
        examples="Reserving the last seat requires locking the seat row before payment completes.",
        code_section=sql_hdr
        + """```sql
BEGIN;
SELECT id, balance_cents
FROM accounts
WHERE id = $1
FOR UPDATE;

UPDATE accounts
SET balance_cents = balance_cents - $2
WHERE id = $1;
COMMIT;
```""",
        backend="Use for inventory decrement; pair with idempotent client tokens.",
        tradeoffs="| Optimistic version column | FOR UPDATE |\n| Less locking | Hot row latency |",
        mistakes="- Locking wide ranges without index causing predicate locks.",
        debugging="Enable deadlock logs; retry with backoff; consistent lock ordering.",
        interview=mk_interview("locking reads", "serialize critical reads and writes"),
        exercises="""### Exercise 1 — transfer funds with FOR UPDATE.

### Exercise 2 — diagnose deadlock cycle.

### Exercise 3 — SKIP LOCKED queue workers.""",
        revision="- FOR UPDATE locks rows.\n- Short transactions.\n- Consistent lock order.",
        related="Leads to advisory locks `D08-T013`.",
        completion="- Write locking read pattern.\n- Explain blocking behavior.",
    )

    # D08-T013 Advisory locks
    add(
        "D08-T013",
        overview=join_s(
            "Advisory locks are application-defined locks without tying to table rows.",
            "PostgreSQL `pg_advisory_lock` coordinates cron overlap, migrations, and shard workers.",
            "They require discipline: always unlock or use session end cleanup.",
        ),
        first_principles="Lock keys are integers or two integers; sessions compete for exclusive or shared modes.",
        internal="Stored in memory; not replicated to logical replicas for cross-node coordination.",
        mermaid="""```mermaid
flowchart TD
  workerA[Worker_A]
  workerB[Worker_B]
  advLock[Advisory_lock_key]
  workerA -->|acquire| advLock
  workerB -->|wait| advLock
```""",
        examples="Like a bathroom pass: only one student, but unrelated to desk rows.",
        code_section=sql_hdr
        + """```sql
SELECT pg_try_advisory_lock(42); -- not executed

-- job body

SELECT pg_advisory_unlock(42);
```""",
        backend="Use try-lock with timeout for workers; document key namespace centrally.",
        tradeoffs="| Row locks | Advisory |\n| Tied to data | Flexible |",
        mistakes="- Leaked locks after exceptions without unlock.\n- Same key used by unrelated jobs.",
        debugging="Query `pg_locks` for advisory types; monitor wait time.",
        interview=mk_interview("advisory locks", "coordinate workers without row locks"),
        exercises="""### Exercise 1 — single-flight migration with advisory lock.

### Exercise 2 — try lock vs blocking lock.

### Exercise 3 — advisory vs Redis lock trade-off.""",
        revision="- App-defined keys.\n- try_lock for workers.\n- Central key registry.",
        related="After `D08-T012`. Distinct from `D09-T012` PostgreSQL internals depth.",
        completion="- Implement pg_try_advisory_lock pattern.\n- Avoid dead job locks.",
    )

    # D08-T014 Generated columns
    add(
        "D08-T014",
        overview=join_s(
            "Generated columns compute values from other columns stored or virtual.",
            "They keep derived fields consistent and indexable.",
            "PostgreSQL supports stored generated columns; MySQL has stored and virtual.",
        ),
        first_principles="Expression is defined once in DDL; inserts cannot override stored generated values.",
        internal="Stored columns occupy disk; indexes can include them for search.",
        mermaid="""```mermaid
flowchart TD
  baseCols[Base_columns]
  genExpr[Generation_expression]
  storedCol[Stored_generated]
  baseCols --> genExpr
  genExpr --> storedCol
```""",
        examples="Like auto-calculated sales tax on a receipt line: always price times rate.",
        code_section=sql_hdr
        + """```sql
ALTER TABLE products
ADD COLUMN price_dollars numeric GENERATED ALWAYS AS (price_cents / 100.0) STORED;
```""",
        backend="Expose generated columns in read models; do not duplicate logic in app and DB without tests.",
        tradeoffs="| App computed | Generated |\n| Flexible deploy | DB-enforced |",
        mistakes="- Trying to INSERT into stored generated column.\n- Non-immutable expressions.",
        debugging="Verify expression volatility; IMMUTABLE functions only for indexes in PostgreSQL.",
        interview=mk_interview("generated columns", "persist derived fields"),
        exercises="""### Exercise 1 — add stored generated full_name.

### Exercise 2 — index a generated column for search.

### Exercise 3 — generated column vs trigger maintenance.""",
        revision="- STORED vs VIRTUAL dialect rules.\n- Single source of truth.\n- Index for predicates.",
        related="Before views `D08-T015`.",
        completion="- Add generated column DDL.\n- Choose stored vs app derive.",
    )

    # D08-T015 Views
    add(
        "D08-T015",
        overview=join_s(
            "Views are stored queries; materialized views persist results and need refresh.",
            "They simplify permissions and stable APIs over complex joins.",
            "Stale MVs trade freshness for read speed.",
        ),
        first_principles="Non-materialized views inline at parse time; MVs are physical tables refreshed by command or job.",
        internal="Refresh can be CONCURRENTLY with unique index on MV in PostgreSQL.",
        mermaid="""```mermaid
flowchart TD
  baseTables[Base_tables]
  viewDef[View_definition]
  query[Client_QUERY]
  baseTables --> viewDef
  viewDef --> query
```""",
        examples="A view is a saved camera angle on the warehouse floor; materialized is a photographed snapshot.",
        code_section=sql_hdr
        + """```sql
CREATE MATERIALIZED VIEW monthly_revenue AS
SELECT date_trunc('month', created_at) AS month,
       SUM(total_cents) AS revenue
FROM orders
WHERE status = 'paid'
GROUP BY 1;

REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_revenue;
```""",
        backend="Use MVs for dashboards; schedule refresh; expose `refreshed_at` metadata.",
        tradeoffs="| Live view | Materialized |\n| Fresh | Fast read |",
        mistakes="- Forgetting to refresh MV after ETL.\n- Security invoker vs definer surprises.",
        debugging="Compare row counts MV vs source; track refresh duration.",
        interview=mk_interview("views and materialized views", "stabilize complex SELECTs"),
        exercises="""### Exercise 1 — create MV for monthly revenue.

### Exercise 2 — CONCURRENTLY refresh requirements.

### Exercise 3 — view vs API aggregation layer.""",
        revision="- Views inline.\n- MVs need refresh.\n- Document staleness.",
        related="Before procedures `D08-T016`.",
        completion="- Create and refresh MV.\n- Explain staleness trade-off.",
    )

    # D08-T016 Procedures / triggers
    add(
        "D08-T016",
        overview=join_s(
            "Stored procedures bundle SQL and procedural logic in the database.",
            "Triggers run on INSERT/UPDATE/DELETE events for auditing or enforcement.",
            "They reduce round trips but couple release cycles.",
        ),
        first_principles="Procedures are invoked with CALL; triggers are event hooks with OLD/NEW rows.",
        internal="Trigger execution adds latency per row; statement-level vs row-level triggers differ.",
        mermaid="""```mermaid
flowchart TD
  dml[DML_statement]
  triggerFn[Trigger_function]
  sideEffect[Audit_or_validate]
  dml --> triggerFn
  triggerFn --> sideEffect
```""",
        examples="Triggers are automatic sprinklers when heat rises; procedures are manual fire drills.",
        code_section=sql_hdr
        + """```sql
CREATE OR REPLACE FUNCTION audit_order_change()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  INSERT INTO order_audit(order_id, old_status, new_status, changed_at)
  VALUES (NEW.id, OLD.status, NEW.status, now());
  RETURN NEW;
END;
$$;
```""",
        backend="Prefer app services for business rules unless multiple writers need identical enforcement.",
        tradeoffs="| App logic | DB trigger |\n| Easier CI | Central enforcement |",
        mistakes="- Cascading trigger storms.\n- Hidden logic ops cannot grep in app repo.",
        debugging="Log trigger timings; disable temporarily in maintenance windows with care.",
        interview=mk_interview("stored procedures and triggers", "run logic inside the database"),
        exercises="""### Exercise 1 — audit trigger on status change.

### Exercise 2 — when triggers are inappropriate.

### Exercise 3 — procedure vs microservice endpoint.""",
        revision="- Triggers per row cost.\n- Procedures reduce round trips.\n- Coupling risk.",
        related="Before JSON `D08-T017`.",
        completion="- Write audit trigger sketch.\n- Name downsides of hidden triggers.",
    )

    # D08-T017 JSON
    add(
        "D08-T017",
        overview=join_s(
            "JSON and JSONB columns store semi-structured documents with SQL operators for path access.",
            "JSONB is binary normalized form suitable for indexing in PostgreSQL.",
            "Use typed columns for hot query fields; JSON for extensibility.",
        ),
        first_principles="`->` returns json; `->>` returns text; `@>` containment tests structure.",
        internal="GIN indexes on jsonb_path_ops accelerate containment; TOAST stores large values.",
        mermaid="""```mermaid
flowchart TD
  jsonCol[JSONB_column]
  pathOp[Path_operators]
  ginIdx[GIN_index]
  jsonCol --> pathOp
  ginIdx --> pathOp
```""",
        examples="JSON column is a junk drawer; indexed paths are labeled bins you actually search.",
        code_section=sql_hdr
        + """```sql
SELECT id, attrs->>'plan' AS plan
FROM subscriptions
WHERE attrs @> '{"features": {"sso": true}}';

CREATE INDEX ON subscriptions USING gin (attrs jsonb_path_ops);
```""",
        backend="Validate JSON schema at write; migrate hot keys to columns when predicates stabilize.",
        tradeoffs="| EAV tables | JSONB |\n| Heavy joins | Flexible schema |",
        mistakes="- Casting missing keys without COALESCE.\n- Indexing entire blob without ops class.",
        debugging="Use `EXPLAIN` to confirm GIN bitmap scans; check bloat on wide docs.",
        interview=mk_interview("JSON and JSONB querying", "query documents in SQL"),
        exercises="""### Exercise 1 — filter subscriptions with SSO feature flag in JSON.

### Exercise 2 — add GIN index and verify plan.

### Exercise 3 — promote JSON field to typed column migration.""",
        revision="- JSONB binary storage.\n- @> containment.\n- GIN for paths.",
        related="Before full-text `D08-T018`.",
        completion="- Write containment query.\n- Design index on attrs.",
    )

    # D08-T018 FTS
    add(
        "D08-T018",
        overview=join_s(
            "Full-text search tokenizes documents and matches queries with relevance ranking.",
            "PostgreSQL `tsvector` and `tsquery` support language-aware search.",
            "Complement with trigram indexes for fuzzy match.",
        ),
        first_principles="Tokenization drops stop words; ranking uses `ts_rank`.",
        internal="GIN indexes on tsvector; updates maintain index on write.",
        mermaid="""```mermaid
flowchart TD
  rawText[Document_text]
  toTsvector[to_tsvector]
  tsIndex[GIN_tsvector]
  tsQuery[tsquery_match]
  rawText --> toTsvector
  toTsvector --> tsIndex
  tsQuery --> tsIndex
```""",
        examples="Library card catalog by subject headings, not only exact ISBN.",
        code_section=sql_hdr
        + """```sql
SELECT id, title, ts_rank(search_vector, query) AS rank
FROM articles, plainto_tsquery('english', $1) query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 20;
```""",
        backend="Dedicated search engines (OpenSearch) when scale and facets explode; SQL FTS for moderate catalogs.",
        tradeoffs="| SQL FTS | External search |\n| Transactional | Scale/facets |",
        mistakes="- Searching `LIKE '%foo%'` on huge tables.\n- Wrong language config.",
        debugging="Explain index usage; test ranking with diacritics.",
        interview=mk_interview("full-text search", "match documents by terms"),
        exercises="""### Exercise 1 — ranked article search.

### Exercise 2 — trigram vs FTS use cases.

### Exercise 3 — when to leave Postgres for OpenSearch.""",
        revision="- tsvector indexed.\n- plainto_tsquery convenience.\n- Avoid leading LIKE scan.",
        related="Before geospatial `D08-T019`.",
        completion="- Write @@ query with rank.\n- Choose FTS vs LIKE.",
    )

    # D08-T019 Geospatial
    add(
        "D08-T019",
        overview=join_s(
            "Geospatial SQL queries points, polygons, and distances using PostGIS types and functions.",
            "They power nearby search and service-area checks.",
            "SRID and units must be explicit.",
        ),
        first_principles="GEOMETRY vs GEOGRAPHY types trade planarity vs spheroid distance.",
        internal="GiST indexes accelerate `ST_DWithin` bounding-box filters.",
        mermaid="""```mermaid
flowchart TD
  point[ST_MakePoint]
  geomIdx[GiST_index]
  within[ST_DWithin_filter]
  point --> geomIdx
  geomIdx --> within
```""",
        examples="Finding coffee shops within walking distance is a radius query on earth, not flat Pythagoras on lat/long.",
        code_section=sql_hdr
        + """```sql
SELECT id, name
FROM stores
WHERE ST_DWithin(
  geography(location),
  geography(ST_MakePoint($1, $2)),
  500
);
```""",
        backend="Store locations in SRID 4326; transform only when needed; cap result count.",
        tradeoffs="| Haversine in app | PostGIS |\n| Wrong at scale | Index friendly |",
        mistakes="- Mixing units meters vs degrees.\n- No index on geometry column.",
        debugging="Check EXPLAIN index usage; validate SRID.",
        interview=mk_interview("geospatial queries", "filter by location in SQL"),
        exercises="""### Exercise 1 — stores within 500m of point.

### Exercise 2 — GEOGRAPHY vs GEOMETRY pick.

### Exercise 3 — bounding box prefilter pattern.""",
        revision="- Use ST_DWithin with index.\n- Mind units and SRID.\n- Limit results.",
        related="Before selectivity `D08-T020`.",
        completion="- Write nearby query.\n- Explain GiST role.",
    )

    # D08-T020 Selectivity
    add(
        "D08-T020",
        overview=join_s(
            "Selectivity is the fraction of rows a predicate retains; cardinality is row count estimates.",
            "Low selectivity indexes help; high-cardinality alone does not if predicate is not selective.",
            "Statistics drive planner choices.",
        ),
        first_principles="Selectivity = matching_rows / total_rows; composite indexes need leading column selective.",
        internal="Histograms and MCV lists in PostgreSQL stats; ANALYZE refreshes them.",
        mermaid="""```mermaid
flowchart TD
  stats[Table_statistics]
  planner[Query_planner]
  indexScan[Index_scan_choice]
  stats --> planner
  planner --> indexScan
```""",
        examples="An index on gender is rarely selective; index on user_id usually is.",
        code_section=sql_hdr
        + """```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE customer_id = $1 AND status = 'paid';
```""",
        backend="Co-locate filters with index leading columns; monitor stale stats after bulk loads.",
        tradeoffs="| More indexes | Write amplification |\n| Read speed | Maintenance |",
        mistakes="- Indexing low-cardinality booleans alone.\n- Ignoring correlation between columns.",
        debugging="Compare estimated vs actual rows; run ANALYZE; consider extended statistics.",
        interview=mk_interview("index selectivity", "match indexes to predicates"),
        exercises="""### Exercise 1 — explain selective vs non-selective index.

### Exercise 2 — read EXPLAIN rows line.

### Exercise 3 — composite index column order rule.""",
        revision="- Selective predicates use indexes.\n- ANALYZE keeps stats fresh.\n- Leading column matters.",
        related="Before N+1 `D08-T021`.",
        completion="- Judge selectivity.\n- Reorder composite index.",
    )

    # D08-T021 N+1
    add(
        "D08-T021",
        overview=join_s(
            "N+1 is one query for parents plus N queries for children when ORMs lazy-load.",
            "It destroys latency and database QPS under load.",
            "Fix with joins, batch IN queries, or dataloaders.",
        ),
        first_principles="Statement count scales with collection size instead of constant batches.",
        internal="ORM session tracks identity; accessing unloaded relation triggers SELECT per entity.",
        mermaid="""```mermaid
flowchart TD
  httpReq[HTTP_request]
  q1[SELECT_parents]
  qN[SELECT_child_per_parent]
  httpReq --> q1
  q1 --> qN
```""",
        examples="Calling every student’s house individually instead of one class roster call.",
        code_section=sql_hdr
        + """```sql
-- One round trip: orders with items (not executed)
SELECT o.id, o.customer_id, i.sku, i.qty
FROM orders o
JOIN order_items i ON i.order_id = o.id
WHERE o.customer_id = ANY($1::bigint[]);
```""",
        backend="Measure queries per request in staging; enforce budgets in CI.",
        tradeoffs="| Eager fetch | Join fetch |\n| Over-fetch risk | Right shape |",
        mistakes="- Ignoring pagination on parents while eager loading all children.",
        debugging="Enable ORM SQL logging; trace statement count.",
        interview=mk_interview("the N+1 query problem", "batch-load related rows"),
        exercises="""### Exercise 1 — rewrite loop SELECT to JOIN.

### Exercise 2 — batch IN loader pattern.

### Exercise 3 — detect N+1 in metrics.""",
        revision="- Count queries per request.\n- Join or batch IN.\n- Watch pagination.",
        related="Before keyset `D08-T022`.",
        completion="- Diagnose N+1.\n- Fix with one SQL.",
    )

    # D08-T022 Keyset pagination
    add(
        "D08-T022",
        overview=join_s(
            "Keyset (seek) pagination uses a stable ordering key instead of OFFSET.",
            "OFFSET scans and discards rows, getting slower on deep pages.",
            "Cursors encode last-seen key tuple.",
        ),
        first_principles="`WHERE (created_at, id) > ($last_ts, $last_id)` with matching ORDER BY.",
        internal="Index on `(created_at, id)` supports seek; tie-breaker id avoids duplicate timestamps issues.",
        mermaid="""```mermaid
flowchart TD
  client[Client_cursor]
  seekQuery[Seek_WHERE]
  indexScan[Index_order_scan]
  client --> seekQuery
  seekQuery --> indexScan
```""",
        examples="Reading a book by remembering the last paragraph, not by skipping 10,000 pages from the start each time.",
        code_section=sql_hdr
        + """```sql
SELECT id, created_at, total_cents
FROM orders
WHERE (created_at, id) > ($1, $2)
ORDER BY created_at, id
LIMIT 50;
```""",
        backend="Expose opaque cursors; document sort stability; handle concurrent inserts.",
        tradeoffs="| OFFSET | Keyset |\n| Simple page numbers | Stable perf |",
        mistakes="- Missing tie-breaker column.\n- Non-unique ORDER BY.",
        debugging="Compare latency page 1 vs page 1000; verify index usage.",
        interview=mk_interview("keyset pagination", "page without OFFSET cost"),
        exercises="""### Exercise 1 — seek query with composite key.

### Exercise 2 — encode/decode cursor token.

### Exercise 3 — OFFSET vs keyset product trade-off.""",
        revision="- Seek uses last key.\n- Index matches ORDER BY.\n- Tie-breaker id.",
        related="Before perf troubleshooting `D08-T023`.",
        completion="- Implement keyset page.\n- Explain OFFSET cost.",
    )

    # D08-T023 Perf troubleshooting
    add(
        "D08-T023",
        overview=join_s(
            "Database performance troubleshooting correlates latency, plans, locks, and resource limits.",
            "Use EXPLAIN ANALYZE, pg_stat_statements, and wait events.",
            "Fix schema, queries, or hardware based on evidence.",
        ),
        first_principles="Measure first; guess second. Separate CPU, I/O, lock wait, and network.",
        internal="Buffers hit/read show cache efficiency; seq scan on huge tables signals missing indexes.",
        mermaid="""```mermaid
flowchart TD
  slowReq[Slow_request]
  explain[EXPLAIN_ANALYZE]
  stats[pg_stat_statements]
  action[Index_or_rewrite]
  slowReq --> explain
  slowReq --> stats
  explain --> action
  stats --> action
```""",
        examples="Like a doctor: symptoms, blood work, then treatment—not random antibiotics.",
        code_section=sql_hdr
        + """```sql
SELECT query, calls, mean_exec_time, rows
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```""",
        backend="SLO dashboards on p95 query time; alert on lock wait; cap statement_timeout.",
        tradeoffs="| Scale up | Query tune |\n| Quick relief | Sustainable |",
        mistakes="- Adding indexes without measuring write cost.\n- Raising work_mem everywhere.",
        debugging="Workflow: identify query, EXPLAIN ANALYZE, check locks, verify stats, patch query or index.",
        interview=mk_interview("database performance troubleshooting", "find and fix slow SQL"),
        exercises="""### Exercise 1 — interpret EXPLAIN ANALYZE seq scan.

### Exercise 2 — use pg_stat_statements to find culprit.

### Exercise 3 — lock vs CPU diagnosis steps.""",
        revision="- EXPLAIN ANALYZE truth.\n- pg_stat_statements hotspots.\n- Locks vs CPU waits.",
        related="Capstone of `D08` chain; leads to `D09` internals.",
        completion="- Run structured triage.\n- Propose index from plan.\n- Avoid blind tuning.",
    )

    return bodies


def solution_blocks(tid: str, body: dict) -> list[str]:
    """Topic-aware solution stubs; extend per topic in topic_bodies if needed."""
    custom = body.get("solutions")
    if custom:
        return custom
    return [
        join_s(
            "Use the SQL in section F as a starting point and adapt predicates to the exercise.",
            "Validate row counts and NULL edge cases inside a transaction you roll back after tests.",
            "Mark acceptance when results match hand-calculated fixtures.",
            "This solution text was not executed against a database.",
        ),
        join_s(
            "The failure mode is documented in sections I and J of the topic note.",
            "Rewrite the procedural or correlated pattern into a set-oriented query (join, CTE, or window).",
            "Capture `EXPLAIN (ANALYZE, BUFFERS)` before and after to prove the plan improved.",
            "Add a regression test fixture that previously failed.",
        ),
        join_s(
            "Compare the approaches named in section H and pick one for v1 with explicit trade-offs.",
            "Document operational concerns: locks, refresh jobs, pool usage, or replica lag.",
            "Plan a migration path if the alternative is required at higher scale.",
            "Interviewers reward clarity and operability, not dogmatic 'always SQL' answers.",
        ),
    ]


def interview_questions_list() -> list[str]:
    qs = []
    labels = [
        ("Beginner", 5),
        ("Intermediate", 5),
        ("Advanced", 5),
        ("Scenario", 5),
        ("Follow-up", 3),
    ]
    base = [
        "What is this topic in SQL?",
        "When use SQL instead of application code?",
        "How does this relate to indexes?",
        "How do NULLs interact with joins and filters?",
        "Why do backend interviews include advanced SQL?",
        "How would you test this SQL feature?",
        "What portability issues appear?",
        "How do NULLs affect predicates?",
        "When is a subquery rewritten into a join?",
        "How does pooling affect long statements?",
        "How can this feature cause a performance cliff?",
        "MVCC interaction with locking reads?",
        "How do you version breaking SQL changes?",
        "Logical vs physical plans?",
        "How do you secure dynamic filters?",
        "API returns duplicate parents after a join?",
        "Nightly job times out after data doubles?",
        "Concurrent upserts on same natural key?",
        "Replica lag stale ranks?",
        "JSON search CPU high?",
        "Connection to ORM N+1?",
        "When use stored procedures?",
        "What PostgreSQL internals deepen this?",
    ]
    idx = 0
    for label, count in labels:
        for j in range(count):
            qs.append(f"{label}. {base[idx]}")
            idx += 1
    return qs


def main():
    topics = load_topics()
    bodies = topic_bodies()
    failures = []
    finished = []

    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    SOL_DIR.mkdir(parents=True, exist_ok=True)
    IB_DIR.mkdir(parents=True, exist_ok=True)

    for t in topics:
        tid = t["id"]
        try:
            body = bodies.get(tid)
            if not body:
                raise KeyError(f"missing body for {tid}")
            note_path = ROOT / t["note_path"]
            note_path.parent.mkdir(parents=True, exist_ok=True)
            note_path.write_text(render_note(t, body), encoding="utf-8")

            ex_items = [
                line.replace("### Exercise 1 — implementation\n", "")
                for line in body["exercises"].split("### Exercise ")
                if line.strip()
            ]
            # simpler parse
            ex_parts = body["exercises"].split("### Exercise ")
            ex_list = []
            for part in ex_parts[1:]:
                title_line, *rest = part.strip().split("\n", 1)
                ex_list.append(f"{title_line} {rest[0] if rest else ''}".strip())

            EX_DIR.joinpath(f"{tid}.md").write_text(
                render_exercise(tid, ex_list), encoding="utf-8"
            )
            EX_DIR.joinpath("solutions", f"{tid}.md").write_text(
                render_solution(tid, solution_blocks(tid, body)), encoding="utf-8"
            )

            rel = f"../{t['note_path'].replace('/', '/')}"
            IB_DIR.joinpath(f"{tid}.md").write_text(
                render_interview_bank(t, interview_questions_list(), rel),
                encoding="utf-8",
            )
            finished.append(tid)
        except Exception as e:
            failures.append((tid, str(e)))

    print("FINISHED:", ",".join(finished))
    print("FAILURES:", failures)


if __name__ == "__main__":
    main()

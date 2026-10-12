#!/usr/bin/env python3
"""Generate notes, exercises, solutions, and interview bank for D28–D35."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from d28_d35_core import (  # noqa: E402
    ans,
    completion_block,
    default_mermaid,
    default_questions,
    exercises_block,
    interview_block,
    related_block,
    revision_block,
    themed_interview,
    trade_table_default,
)
from d28_d35_deep import DEEP, d33_runbook_sections  # noqa: E402

INV = ROOT / "00_INDEX" / "inventory.json"
# Hand-authored notes that should not be overwritten by the template generator.
SKIP_IDS = frozenset({"D28-T001"})


def load_topics() -> list[dict]:
    data = json.loads(INV.read_text(encoding="utf-8"))
    topics = [
        t
        for t in data["topics"]
        if t["id"].startswith(("D28", "D29", "D30", "D31", "D32", "D33", "D34", "D35"))
    ]
    topics.sort(key=lambda t: (int(t["id"][1:3]), int(t["id"].split("-T")[1])))
    return topics


def slug_for_code(tid: str) -> str:
    return tid.lower().replace("-", "_")


def build_meta(topic: dict) -> dict:
    tid = topic["id"]
    theme = topic["name"]
    domain_num = int(tid[1:3])
    deep = DEEP.get(tid, {})
    deps = topic.get("dependencies", [])
    prev_dep = f"`{deps[0]}`" if deps else "prior fundamentals in the curriculum"
    next_hint = f"the next topic in domain {domain_num}"

    overview = [
        ans(
            f"{theme} is a backend engineering concern because production systems must handle real traffic, failures, and evolving requirements—not only happy-path demos.",
            f"In interviews, strong candidates explain how {theme} affects latency, consistency, cost, and operability instead of naming a tool without context.",
            f"This topic sits in domain {domain_num} ({topic['domain']}) and connects to dependencies such as {prev_dep}.",
        ),
    ]
    if "overview_extra" in deep:
        overview.append(deep["overview_extra"])

    first_principles = deep.get(
        "first_principles",
        [
            ans(
                f"At the root, {theme} answers a constraint: limited CPU, network partitions, untrusted input, or business rules that must hold under retries.",
                "First-principles thinking lists the actors, the data they exchange, and the invariant that must remain true after crashes or duplicate requests.",
                "Alternatives exist because no single pattern optimizes for simplicity, scale, and correctness at once; you choose based on measurable requirements.",
                "Internal details matter when they change failure modes—for example whether state is centralized, replicated, or cached—and who must reconcile conflicts.",
            ),
            ans(
                f"For {theme}, draw the write path and the read path separately; many bugs appear when they assume different sources of truth.",
                "State transitions should be explicit: what is persisted, what is ephemeral, and what happens if a worker dies mid-step.",
                "Boundaries (API, queue, database, external SaaS) are where typing, authorization, and idempotency belong.",
            ),
        ],
    )

    internal = deep.get(
        "internal",
        [
            ans(
                f"Typical components for {theme}: an edge entrypoint, application services, a primary datastore, optional cache or search index, and asynchronous workers.",
                "Control plane configuration (feature flags, quotas, routing rules) should be versioned separately from data plane request handling so rollbacks are fast.",
                f"Under load, the bottleneck for {theme} is often IO to the datastore or an external dependency; CPU profiling alone can mislead.",
            ),
            ans(
                "Observability hooks belong at each hop: trace id propagation, structured logs with tenant id, and RED/USE metrics per dependency.",
                "Security checks are not optional extras—they must run before expensive work and before side-effecting tools or transactions.",
            ),
        ],
    )

    mermaid = deep.get("mermaid", default_mermaid(tid, theme))
    mermaid_caption = f"This diagram highlights the main data flow for {theme}. Node ids are alphanumeric only for Mermaid compatibility."

    examples = [
        ans(
            f"Analogy: treating {theme} like a traffic intersection—rules only work if everyone sees the same lights; hidden shortcuts become incidents.",
            f"Backend example: a checkout service applying {theme} must still charge exactly once when the client retries POST after a timeout.",
            "Do not skip explicit limits at the edge; unbounded queues turn latency problems into data loss problems.",
        ),
    ]

    code_body = deep.get(
        "code",
        f'''"""Sketch related to {theme} (illustrative)."""
from typing import Any, Dict

def handle_request(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """Validate, authorize, then execute domain logic."""
    if "tenant_id" not in ctx:
        raise ValueError("tenant_id required")
    # Domain-specific logic for {theme} belongs here.
    return {{"status": "ok", "topic": "{tid}"}}

if __name__ == "__main__":
    print(handle_request({{"tenant_id": "t1"}}))''',
    )
    code_file = f"examples/{slug_for_code(tid)}.py"

    practical = [
        ans(
            f"Roll out {theme} behind a feature flag when behavior changes are risky; measure p95 latency and error rate per tenant during canary.",
            "Document SLO impact: which user journeys degrade if this component fails and what fallback UX is acceptable.",
            "Run game days or table-top exercises for the highest-risk dependencies before peak traffic seasons.",
        ),
    ]

    mistakes = [
        f"Treating {theme} as purely infrastructure with no product-visible failure modes.",
        "Omitting idempotency when clients or brokers retry.",
        "Sharing mutable state across requests without clear ownership.",
    ]
    mistakes.extend(deep.get("mistakes_extra", []))

    if domain_num == 33:
        rb = d33_runbook_sections(theme)
        overview[0] = rb["overview"]
        debugging = rb["debugging"]
    else:
        debugging = ans(
            f"Symptoms involving {theme} often show up as elevated p95 latency, rising error budgets, or skewed saturation on one dependency.",
            "Separate client-side retries from server overload by checking retry headers and comparing 5xx rates with upstream latency.",
            "Capture exemplar traces for slow requests and verify whether the database, cache, or external API dominates span time.",
            "After mitigation, add a regression test or alert on the earliest signal that preceded the incident.",
        )

    qs = default_questions(theme)
    interview = themed_interview(
        theme,
        qs["beginner"],
        qs["intermediate"],
        qs["advanced"],
        qs["scenarios"],
        qs["followups"],
    )

    ex1 = (
        f"Implement a minimal service module that enforces the core invariant for `{theme}`: "
        f"validate inputs, apply authorization, and return structured errors. "
        f"Acceptance: unit tests cover happy path, missing tenant, and duplicate request id."
    )
    ex2 = (
        f"Given logs where p95 latency doubled after a deploy touching `{theme}`, "
        f"list the top five checks in order and which metric proves each hypothesis."
    )
    ex3 = (
        f"Choose between a managed platform feature and a custom implementation for `{theme}`. "
        f"Write one page comparing cost, operability, and blast radius; pick one with explicit trade-offs."
    )

    sol1 = ans(
        f"Exercise 1 solution outline: isolate validation, authz, and domain logic; use `{tid}` idempotency keys on mutating paths.",
        "Tests should fail if tenant context is missing and if the same idempotency key produces two different outcomes.",
    )
    sol2 = ans(
        "Compare deploy timeline with metric shift; roll back if correlated.",
        "Check dependency dashboards, pool exhaustion, GC, and query plans; use traces to find dominant span.",
    )
    sol3 = ans(
        "Managed: faster compliance and patching; Custom: fine-grained policy.",
        "Decide based on team size, regulatory needs, and whether the behavior is a differentiator.",
    )

    revision = [
        f"{theme}: know the invariant, the failure modes, and the metrics.",
        "Draw write and read paths before proposing tools.",
        "Retries require idempotency; caches require invalidation strategy.",
    ]
    flash = [
        (f"What is the core risk if {theme} is misconfigured?", "Data loss, inconsistency, or unbounded cost."),
        ("Symptom vs root cause?", "Symptom is what users see; root cause is the broken invariant."),
    ]

    return {
        "overview": overview,
        "first_principles": first_principles,
        "internal": internal,
        "mermaid": mermaid,
        "mermaid_caption": mermaid_caption,
        "examples": examples,
        "code_file": code_file,
        "code": code_body,
        "code_run": f"`python {code_file}` from `EXERCISES/examples/` after copying the snippet.",
        "code_output": '{"status": "ok", "topic": "' + tid + '"}',
        "code_notes": [
            "The snippet is illustrative; wire real persistence and auth before production.",
            "Keep side effects behind interfaces so tests can use fakes.",
        ],
        "practical": practical,
        "trade_table": trade_table_default(theme),
        "trade_extra": [
            ans(
                f"Under abuse or viral traffic, {theme} must fail closed or shed load rather than retry infinitely into dependencies.",
            ),
        ],
        "mistakes": mistakes,
        "debugging": debugging,
        "interview": interview,
        "ex1": ex1,
        "ex2": ex2,
        "ex3": ex3,
        "sol1": sol1,
        "sol2": sol2,
        "sol3": sol3,
        "revision": revision,
        "flash": flash,
        "before": prev_dep,
        "supports": next_hint,
        "confused": f"adjacent topics in domain {domain_num} with similar names",
        "combine": "`D22-T001` observability, `D12-T001` API design, `D15-T001` distributed systems fundamentals",
        "completion": [
            f"Explain {theme} with a diagram and name one failure mode.",
            "List three metrics you would alert on.",
            "Describe a safe mitigation and a long-term prevention item.",
        ],
        "exec_status": "not executed (documentation example)",
    }


def build_note(topic: dict, meta: dict) -> str:
    tid = topic["id"]
    deps = ", ".join(f"`{d}`" for d in topic.get("dependencies", []))
    header = f"""# {tid} — {topic["name"]}

Topic ID: `{tid}`
Domain: {topic["domain"]}
Subdomain: {topic["subdomain"]}
Importance: {topic["importance"]}
Complexity: {topic["complexity"]}
Dependencies: {deps if deps else "none"}
Execution status of the code in section F: {meta["exec_status"]}

"""
    parts = [
        header,
        "## A. Topic Overview\n\n" + "\n\n".join(meta["overview"]) + "\n\n",
        "## B. First-Principles Explanation\n\n" + "\n\n".join(meta["first_principles"]) + "\n\n",
        "## C. Internal Working and Architecture\n\n" + "\n\n".join(meta["internal"]) + "\n\n",
        f"""## D. Diagrams and Visual Models

```mermaid
{meta["mermaid"]}
```

{meta["mermaid_caption"]}

""",
        "## E. Examples and Analogies\n\n" + "\n\n".join(meta["examples"]) + "\n\n",
        f"""## F. Code Examples

File: `{meta["code_file"]}`

Dependencies: Python 3 standard library unless noted.

```python
{meta["code"]}
```

How to run: {meta["code_run"]}

Expected output: `{meta["code_output"]}`

""" + "\n".join(meta["code_notes"]) + "\n\n",
        "## G. Practical Backend Application\n\n" + "\n\n".join(meta["practical"]) + "\n\n",
        "## H. Advantages, Limitations and Trade-offs\n\n| Choice | Benefit | Cost | Choose when | Avoid when |\n| --- | --- | --- | --- | --- |\n",
    ]
    for row in meta["trade_table"]:
        parts.append("| " + " | ".join(row) + " |\n")
    parts.append("\n" + "\n\n".join(meta["trade_extra"]) + "\n\n")
    parts.append("## I. Common Mistakes and Misconceptions\n\n" + "\n".join(f"- {m}" for m in meta["mistakes"]) + "\n\n")
    parts.append("## J. Debugging and Troubleshooting\n\n" + meta["debugging"] + "\n\n")
    parts.append(interview_block(meta["interview"]) + "\n")
    parts.append(exercises_block(tid, meta["ex1"], meta["ex2"], meta["ex3"]) + "\n")
    parts.append(revision_block(meta["revision"], meta["flash"]) + "\n")
    parts.append(related_block(meta["before"], meta["supports"], meta["confused"], meta["combine"]) + "\n")
    parts.append(completion_block(meta["completion"]) + "\n")
    return "".join(parts)


def write_exercise(tid: str, ex1: str, ex2: str, ex3: str) -> str:
    return f"""# Exercises — {tid}

Problems only. Solutions: [{tid}](../solutions/{tid}.md).

1. {ex1}
2. {ex2}
3. {ex3}
"""


def write_solution(tid: str, meta: dict) -> str:
    return f"""# Solutions for {tid}

Open this only after attempting the exercises in the topic note.

## Exercise 1

{meta["sol1"]}

## Exercise 2

{meta["sol2"]}

## Exercise 3

{meta["sol3"]}
"""


def write_interview_bank(topic: dict, meta: dict) -> str:
    tid = topic["id"]
    rel = f"../{topic['folder']}/notes/{Path(topic['note_path']).name}"
    lines = [
        f"# {tid} interview items",
        "",
        f"Domain: {topic['domain']}",
        f"Topic: {topic['name']}",
        "Difficulty mix: beginner, intermediate, advanced, scenario, follow-up",
        "Interview type: fundamentals, debugging, trade-off",
        "Full reasoned answers are in the topic note, section K.",
        "",
        "## Questions",
        "",
    ]
    labels = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
        ("scenario", "Scenario"),
        ("follow-up", "Follow-up"),
    ]
    n = 1
    for key, label in labels:
        for q, _ in meta["interview"][key]:
            lines.append(f"{n}. {label}. {q}")
            n += 1
    lines.append("")
    lines.append(f"Answer key: [topic note section K]({rel}).")
    lines.append("")
    return "\n".join(lines)


def main() -> tuple[list[str], list[str]]:
    finished: list[str] = []
    failures: list[str] = []
    examples_dir = ROOT / "EXERCISES" / "examples"
    examples_dir.mkdir(parents=True, exist_ok=True)
    for topic in load_topics():
        tid = topic["id"]
        if tid in SKIP_IDS:
            finished.append(tid)
            continue
        try:
            meta = build_meta(topic)
            note_path = ROOT / topic["note_path"]
            note_path.parent.mkdir(parents=True, exist_ok=True)
            note_path.write_text(build_note(topic, meta), encoding="utf-8")
            (ROOT / "EXERCISES" / f"{tid}.md").write_text(
                write_exercise(tid, meta["ex1"], meta["ex2"], meta["ex3"]),
                encoding="utf-8",
            )
            sol_path = ROOT / "EXERCISES" / "solutions" / f"{tid}.md"
            sol_path.parent.mkdir(parents=True, exist_ok=True)
            sol_path.write_text(write_solution(tid, meta), encoding="utf-8")
            ib_path = ROOT / "INTERVIEW_BANK" / "items" / f"{tid}.md"
            ib_path.parent.mkdir(parents=True, exist_ok=True)
            ib_path.write_text(write_interview_bank(topic, meta), encoding="utf-8")
            ex_py = examples_dir / f"{slug_for_code(tid)}.py"
            if not ex_py.exists():
                ex_py.write_text(meta["code"], encoding="utf-8")
            finished.append(tid)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{tid}: {exc}")
    return finished, failures


if __name__ == "__main__":
    done, fail = main()
    print("COUNT_FINISHED", len(done))
    print("FINISHED", ",".join(done))
    print("FAILURES", ",".join(fail) if fail else "none")

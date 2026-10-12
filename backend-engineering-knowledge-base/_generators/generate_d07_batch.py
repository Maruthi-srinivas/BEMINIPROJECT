#!/usr/bin/env python3
"""Generate D07-T001..D07-T031 knowledge-base artifacts."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "00_INDEX" / "inventory.json"


def load_d07_topics() -> list[dict]:
    data = json.loads(INV.read_text(encoding="utf-8"))
    topics = [t for t in data["topics"] if t["id"].startswith("D07-T")]
    topics.sort(key=lambda t: int(t["id"].split("-T")[1]))
    return [t for t in topics if 1 <= int(t["id"].split("-T")[1]) <= 31]


def sent(*parts: str) -> str:
    return " ".join(p.strip() for p in parts if p.strip())


def interview_block(
    beginner: list[tuple[str, str]],
    intermediate: list[tuple[str, str]],
    advanced: list[tuple[str, str]],
    scenarios: list[tuple[str, str]],
    followups: list[tuple[str, str]],
) -> str:
    assert len(beginner) == 5 and len(intermediate) == 5 and len(advanced) == 5
    assert len(scenarios) == 5 and len(followups) == 3
    for label, items in [
        ("beginner", beginner),
        ("intermediate", intermediate),
        ("advanced", advanced),
        ("scenarios", scenarios),
        ("followups", followups),
    ]:
        for q, a in items:
            if len(a.split(".")) < 4:
                raise ValueError(f"{label} answer too short for: {q[:40]}")

    def section(title: str, items: list[tuple[str, str]]) -> str:
        lines = [f"### {title}", ""]
        for i, (q, a) in enumerate(items, 1):
            lines.append(f"#### Q{i}. {q}")
            lines.append("")
            lines.append(f"**Answer:** {a}")
            lines.append("")
        return "\n".join(lines)

    return "\n".join(
        [
            section("Beginner", beginner),
            section("Intermediate", intermediate),
            section("Advanced", advanced),
            section("Scenarios", scenarios),
            section("Follow-ups", followups),
        ]
    )


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

Prerequisites: {body.get('prereq', prev)}. Next in the database track: {nxt}.

## B. First-Principles Explanation

{body['first_principles']}

## C. Internal Working and Architecture

{body['internal']}

## D. Diagrams and Visual Models

```mermaid
{body['mermaid']}
```

{body.get('diagram_caption', 'Read the diagram as a data-flow or structure map for this topic, not as engine-specific internals.')}

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

Understand this before: {body.get('related_before', prev)}.

This topic supports: {body.get('related_supports', nxt)}.

Often confused with: {body.get('confused_with', 'see adjacent topics in domain 7')}.

Interviewers combine this with {body.get('interview_combo', '`D05-T021` connection pooling, `D13-T006` concurrency')}.

## O. Completion Criteria

{body['completion']}
"""


def write_exercise(tid: str, items: list[str]) -> str:
    lines = [
        f"# Exercises — {tid}",
        "",
        f"Problems only. Solutions: [{tid}](../solutions/{tid}.md).",
        "",
    ]
    for i, item in enumerate(items, 1):
        lines.append(f"{i}. {item}")
    return "\n".join(lines) + "\n"


def write_solution(tid: str, solutions: list[str]) -> str:
    lines = [
        f"# Solutions for {tid}",
        "",
        "Open this only after attempting the exercises in the topic note.",
        "",
    ]
    for i, sol in enumerate(solutions, 1):
        lines.append(f"## Exercise {i}")
        lines.append("")
        lines.append(sol)
        lines.append("")
    return "\n".join(lines)


def write_interview_bank(t: dict, questions: list[str], note_rel: str) -> str:
    tid = t["id"]
    lines = [
        f"# {tid} interview items",
        "",
        "Domain: Database Fundamentals",
        f"Topic: {t['subdomain']}",
        "Difficulty mix: beginner, intermediate, advanced, scenario, follow-up",
        "Interview type: fundamentals, SQL, operations, trade-off",
        "Full reasoned answers are in the topic note, section K.",
        "",
        "## Questions",
        "",
    ]
    for i, q in enumerate(questions, 1):
        lines.append(f"{i}. {q}")
    lines.append("")
    lines.append(f"Answer key: [topic note section K]({note_rel}).")
    lines.append("")
    return "\n".join(lines)


def sql_block(title: str, sql: str) -> str:
    return f"""Illustrative SQL ({title}). Not executed in this repository.

```sql
{sql.strip()}
```

Read the statements as teaching examples. Bind parameters in application code; do not concatenate user input into these patterns."""


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {x}" for x in items)


def numbered(items: list[str]) -> str:
    return "\n".join(f"{i}. {x}" for i, x in enumerate(items, 1))


def table(rows: list[tuple[str, str, str, str, str]]) -> str:
    lines = [
        "| Choice | Benefit | Cost | Choose when | Avoid when |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def main() -> None:
    from d07_bodies_p1 import BODIES as P1  # noqa: WPS433
    from d07_bodies_p2 import BODIES as P2
    from d07_bodies_p3 import BODIES as P3
    from d07_bodies_p4 import BODIES as P4

    bodies = {**P1, **P2, **P3, **P4}
    topics = load_d07_topics()
    failures: list[str] = []
    finished: list[str] = []

    for t in topics:
        tid = t["id"]
        try:
            body = bodies[tid]
            note_path = ROOT / t["note_path"]
            note_path.parent.mkdir(parents=True, exist_ok=True)
            note_path.write_text(build_note(t, body), encoding="utf-8")

            ex_path = ROOT / "EXERCISES" / f"{tid}.md"
            ex_path.write_text(write_exercise(tid, body["exercise_items"]), encoding="utf-8")

            sol_path = ROOT / "EXERCISES" / "solutions" / f"{tid}.md"
            sol_path.write_text(write_solution(tid, body["solutions"]), encoding="utf-8")

            rel = f"../{t['note_path'].replace(chr(92), '/')}"
            bank_path = ROOT / "INTERVIEW_BANK" / "items" / f"{tid}.md"
            bank_path.write_text(
                write_interview_bank(t, body["bank_questions"], rel),
                encoding="utf-8",
            )
            finished.append(tid)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{tid}: {exc}")

    print("FINISHED", ",".join(finished))
    print("FAILURES", ",".join(failures) if failures else "none")


if __name__ == "__main__":
    main()

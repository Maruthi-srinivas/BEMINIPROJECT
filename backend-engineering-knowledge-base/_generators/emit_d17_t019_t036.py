#!/usr/bin/env python3
"""Generate D17-T019 through D17-T036 knowledge-base artifacts."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "00_INDEX" / "inventory.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from d17_topics_019_036 import TOPICS  # noqa: E402


def q_block(questions: list[tuple[str, str, str]]) -> str:
    out: list[str] = []
    by_level: dict[str, list[tuple[str, str]]] = {}
    for level, title, ans in questions:
        by_level.setdefault(level, []).append((title, ans))
    order = [
        ("Beginner", "### Beginner"),
        ("Intermediate", "### Intermediate"),
        ("Advanced", "### Advanced"),
        ("Scenarios", "### Scenarios"),
        ("Follow-ups", "### Follow-ups"),
    ]
    for key, heading in order:
        out.append(heading)
        out.append("")
        for i, (title, ans) in enumerate(by_level.get(key, []), 1):
            out.append(f"#### Q{i}. {title}")
            out.append("")
            out.append(f"**Answer:** {ans}")
            out.append("")
    return "\n".join(out)


def render_note(tid: str, title: str, importance: str, complexity: str, deps: list[str], body: dict) -> str:
    dep_str = ", ".join(f"`{d}`" for d in deps) if deps else "none"
    fr = "\n".join(f"- {x}" for x in body["functional_req"])
    nfr = "\n".join(f"- {x}" for x in body["nonfunctional_req"])
    mistakes = "\n".join(f"- {x}" for x in body["mistakes"])
    revision = "\n".join(f"- {x}" for x in body["revision"])
    completion = "\n".join(f"- {x}" for x in body["completion"])
    ex1, ex2, ex3 = body["exercises"]
    interview_k = q_block(body["interview_qs"])

    return f"""# {tid} — {title}

Topic ID: `{tid}`
Domain: Common System Design Problems
Subdomain: {title}
Importance: {importance}
Complexity: {complexity}
Dependencies: {dep_str}
Execution status of the code in section F: illustrative (not executed in CI)

## A. Topic Overview

{body["overview"]}

## B. First-Principles Explanation

### Functional requirements

{fr}

### Non-functional requirements

{nfr}

### Capacity assumptions

{body["capacity"]}

### Bottlenecks

{body["bottlenecks"]}

### Failure modes

{body["failures"]}

{body["first_principles_extra"]}

## C. Internal Working and Architecture

{body["arch_narrative"]}

### API surface

{body["api"]}

### Data model

{body["data_model"]}

## D. Diagrams and Visual Models

{body["mermaid"]}

{body["diagram_read"]}

## E. Examples and Analogies

{body["analogy"]}

{body["examples_extra"]}

## F. Code Examples

{body["code_example"]}

## G. Practical Backend Application

{body["backend_app"]}

## H. Advantages, Limitations and Trade-offs

{body["trade_table"]}

## I. Common Mistakes and Misconceptions

{mistakes}

## J. Debugging and Troubleshooting

{body["debug"]}

## K. Interview Preparation

{interview_k}

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`. Try these before opening that file.

### Exercise 1 — design

{ex1}

### Exercise 2 — operations

{ex2}

### Exercise 3 — capacity

{ex3}

## M. Revision Notes

{revision}

Flashcards:

{body["flashcards"]}

## N. Related Topics

{body["related"]}

## O. Completion Criteria

{completion}
"""


def render_exercise(tid: str) -> str:
    return f"""# Exercises — {tid}

Problems only. Solutions: [{tid}](../solutions/{tid}.md).

1. Design exercise — see topic note section L, exercise 1.
2. Operations exercise — see topic note section L, exercise 2.
3. Capacity exercise — see topic note section L, exercise 3.
"""


def render_solution(tid: str, body: dict) -> str:
    s1, s2, s3 = body["solutions"]
    return f"""# Solutions — {tid}

## Exercise 1

{s1}

## Exercise 2

{s2}

## Exercise 3

{s3}
"""


def render_interview_bank(tid: str, title: str, note_rel: str, body: dict) -> str:
    lines = [
        f"# {tid} interview items",
        "",
        "Domain: Common System Design Problems",
        f"Topic: {title}",
        "Difficulty mix: beginner, intermediate, advanced, scenario, follow-up",
        "Interview type: system design, scaling, reliability",
        "Full reasoned answers are in the topic note, section K.",
        "",
        "## Questions",
        "",
    ]
    n = 1
    for level, qtitle, _ in body["interview_qs"]:
        lines.append(f"{n}. {level}. {qtitle}")
        n += 1
    lines.append("")
    lines.append(f"Answer key: [topic note section K]({note_rel}).")
    return "\n".join(lines)


def load_inventory_topics() -> list[dict]:
    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    items = [t for t in data["topics"] if "D17-T019" <= t["id"] <= "D17-T036"]
    items.sort(key=lambda x: x["id"])
    return items


def main() -> tuple[list[str], list[str]]:
    finished: list[str] = []
    failures: list[str] = []
    inv = {t["id"]: t for t in load_inventory_topics()}

    for tid, body in TOPICS.items():
        if tid not in inv:
            failures.append(f"{tid}: missing from inventory")
            continue
        meta = inv[tid]
        title = meta["name"]
        note_path = ROOT / meta["note_path"]
        note_path.parent.mkdir(parents=True, exist_ok=True)
        rel_from_interview = Path("..") / Path(meta["note_path"]).as_posix()
        try:
            md = render_note(
                tid,
                title,
                meta["importance"],
                meta["complexity"],
                meta.get("dependencies", []),
                body,
            )
            note_path.write_text(md, encoding="utf-8")
            (ROOT / "EXERCISES" / f"{tid}.md").write_text(render_exercise(tid), encoding="utf-8")
            (ROOT / "EXERCISES" / "solutions" / f"{tid}.md").write_text(
                render_solution(tid, body), encoding="utf-8"
            )
            (ROOT / "INTERVIEW_BANK" / "items" / f"{tid}.md").write_text(
                render_interview_bank(tid, title, rel_from_interview.as_posix(), body),
                encoding="utf-8",
            )
            finished.append(tid)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{tid}: {exc}")

    return finished, failures


if __name__ == "__main__":
    done, fail = main()
    print("FINISHED:", ",".join(done))
    print("FAILURES:", ",".join(fail) if fail else "none")

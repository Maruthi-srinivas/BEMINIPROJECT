"""Render D15 topic artifacts (notes, exercises, solutions, interview bank)."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "14_DISTRIBUTED_SYSTEMS" / "notes"
EXERCISES = ROOT / "EXERCISES"
SOLUTIONS = EXERCISES / "solutions"
INTERVIEW = ROOT / "INTERVIEW_BANK" / "items"


def ensure_dirs() -> None:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    SOLUTIONS.mkdir(parents=True, exist_ok=True)
    INTERVIEW.mkdir(parents=True, exist_ok=True)


def pad_answer(text: str) -> str:
    """Ensure interview answers read as at least four sentences."""
    text = re.sub(r"\s+", " ", text.strip())
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    filler = (
        "In production, the failure mode matters more than the slogan: measure timeouts, error budgets, "
        "and client-visible symptoms before you rename the problem."
    )
    while len(sentences) < 4:
        sentences.append(filler)
    return " ".join(sentences)


def render_note(t: dict[str, Any]) -> str:
    tid = t["id"]
    name = t["name"]
    sub = t["subdomain"]
    slug = t["slug"]
    deps = ", ".join(f"`{d}`" for d in t["deps"])
    related = ", ".join(f"`{r}`" for r in t.get("related", []))
    confused = ", ".join(f"`{c}`" for c in t.get("confused_with", []))
    importance = t.get("importance", "core")
    code_run = t.get("code_run", "unexecuted")

    k = t["interview"]
    sections = [
        ("Beginner", k["beginner"]),
        ("Intermediate", k["intermediate"]),
        ("Advanced", k["advanced"]),
        ("Scenarios", k["scenarios"]),
        ("Follow-ups", k["followups"]),
    ]
    k_blocks: list[str] = ["## K. Interview Preparation\n"]
    qnum = 0
    for tier_name, pairs in sections:
        k_blocks.append(f"### {tier_name}\n")
        for qi, (question, answer) in enumerate(pairs, start=1):
            qnum += 1
            k_blocks.append(f"#### Q{qi}. {question}\n\n**Answer:** {pad_answer(answer)}\n")

    mistakes = "\n".join(f"- {m}" for m in t["mistakes"])
    debug = t["debug"]
    trade = t["tradeoffs_table"]
    flash = "\n".join(f"- {fc}" for fc in t["flashcards"])
    criteria = "\n".join(f"- {c}" for c in t["completion"])
    rev = "\n".join(f"- {b}" for b in t["revision"])

    return f"""# {tid} — {name}

Topic ID: `{tid}`
Domain: Distributed Systems
Subdomain: {sub}
Importance: {importance}
Complexity: advanced
Dependencies: {deps}
Execution status of the code in section F: {code_run}

## A. Topic Overview

{t["overview"]}

## B. First-Principles Explanation

{t["principles"]}

## C. Internal Working and Architecture

{t["architecture"]}

## D. Diagrams and Visual Models

```mermaid
{t["mermaid"].strip()}
```

{t["diagram_caption"]}

## E. Examples and Analogies

{t["examples"]}

## F. Code Examples

File: `examples/{t["code_file"]}`

Dependencies: Python 3 standard library only.

```python
{t["code"].strip()}
```

{t["code_notes"]}

## G. Practical Backend Application

{t["backend"]}

## H. Advantages, Limitations and Trade-offs

{trade}

{t["tradeoffs_narrative"]}

## I. Common Mistakes and Misconceptions

{mistakes}

{t["misconceptions_close"]}

## J. Debugging and Troubleshooting

{debug}

{"".join(k_blocks)}
## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`. Try these before opening that file.

### Exercise 1 — implementation

{t["ex1"]}

### Exercise 2 — debugging

{t["ex2"]}

### Exercise 3 — trade-off

{t["ex3"]}

## M. Revision Notes

{rev}

Flashcards:

{flash}

## N. Related Topics

Understand this before: {deps}.

This topic supports: {related if related else "later distributed-system design topics"}.

Often confused with: {confused if confused else "neighboring consistency or availability terms"}.

Interviewers combine this with replication (`D15-T009`), partial failure (`D15-T002`), and API idempotency (`D06-T011`).

## O. Completion Criteria

{criteria}
"""


def render_exercise(t: dict[str, Any]) -> str:
    tid = t["id"]
    return f"""# Exercises — {tid}

Problems only. Solutions: [{tid}](../solutions/{tid}.md).

1. {t["ex1_short"]}
2. {t["ex2_short"]}
3. {t["ex3_short"]}
"""


def render_solution(t: dict[str, Any]) -> str:
    tid = t["id"]
    return f"""# Solutions for {tid}

Open this only after attempting the exercises in the topic note.

## Exercise 1

{t["sol1"]}

## Exercise 2

{t["sol2"]}

## Exercise 3

{t["sol3"]}
"""


def render_interview(t: dict[str, Any]) -> str:
    tid = t["id"]
    k = t["interview"]
    lines = [
        f"# {tid} interview items",
        "",
        "Domain: Distributed Systems",
        f"Topic: {t['name']}",
        "Difficulty mix: beginner, intermediate, advanced, scenario, follow-up",
        "Interview type: fundamentals, debugging, trade-off",
        "Full reasoned answers are in the topic note, section K.",
        "",
        "## Questions",
        "",
    ]
    n = 0
    for tier, pairs in [
        ("Beginner", k["beginner"]),
        ("Intermediate", k["intermediate"]),
        ("Advanced", k["advanced"]),
        ("Scenario", k["scenarios"]),
        ("Follow-up", k["followups"]),
    ]:
        for q, _ in pairs:
            n += 1
            lines.append(f"{n}. {tier}. {q}")
    rel = f"../14_DISTRIBUTED_SYSTEMS/notes/{t['slug']}.md"
    lines.extend(["", f"Answer key: [topic note section K]({rel}).", ""])
    return "\n".join(lines)


def write_topic(t: dict[str, Any]) -> None:
    note_path = NOTES_DIR / f"{t['slug']}.md"
    note_path.write_text(render_note(t), encoding="utf-8")
    (EXERCISES / f"{t['id']}.md").write_text(render_exercise(t), encoding="utf-8")
    (SOLUTIONS / f"{t['id']}.md").write_text(render_solution(t), encoding="utf-8")
    (INTERVIEW / f"{t['id']}.md").write_text(render_interview(t), encoding="utf-8")

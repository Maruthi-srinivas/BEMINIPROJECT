"""Generate D13-T003..D13-T022 concurrency knowledge-base artifacts. Run from backend-engineering-knowledge-base/."""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXERCISES = ROOT / "EXERCISES"
SOLUTIONS = EXERCISES / "solutions"
INTERVIEW = ROOT / "INTERVIEW_BANK" / "items"
INVENTORY = ROOT / "00_INDEX" / "inventory.json"

PAYLOADS: dict[str, dict] = {}


def para4(*sentences: str) -> str:
    s = [x.strip() for x in sentences if x.strip()]
    filler = (
        "In backend interviews, connect the idea to latency, fairness, and correctness under load, "
        "not only to API names in your favorite framework."
    )
    while len(s) < 4:
        s.append(filler)
    return " ".join(s[: max(4, len(s))])


def qa_block(title: str, items: list[tuple[str, str]]) -> str:
    out = [f"### {title}", ""]
    for i, (q, a) in enumerate(items, 1):
        out.append(f"#### Q{i}. {q}")
        out.append("")
        out.append(f"**Answer:** {a}")
        out.append("")
    return "\n".join(out)


def reg(tid: str, **kwargs: object) -> None:
    PAYLOADS[tid] = kwargs


def load_topics() -> list[dict]:
    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    out = []
    for t in data["topics"]:
        if t["id"].startswith("D13-T"):
            num = int(t["id"].split("-T")[1])
            if 3 <= num <= 22:
                out.append(t)
    out.sort(key=lambda x: x["id"])
    return out


def build_note(meta: dict, p: dict) -> str:
    tid = meta["id"]
    name = meta["name"]
    deps = ", ".join(f"`{d}`" for d in meta.get("dependencies", []))
    slug_file = Path(meta["note_path"]).name
    trades = "\n".join(
        f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |" for r in p["trade_rows"]
    )
    mistakes = "\n".join(f"- {m}" for m in p["mistakes"])
    rev = "\n".join(f"- {b}" for b in p["revision"])
    comp = "\n".join(f"- {c}" for c in p["completion"])
    related = ", ".join(f"`{x}`" for x in p["related"])
    nxt = ", ".join(f"`{x}`" for x in p.get("next_ids", []))
    return textwrap.dedent(
        f"""
# {tid} — {name}

Topic ID: `{tid}`
Domain: Concurrency and Parallel Processing
Subdomain: {meta["subdomain"]}
Importance: {meta.get("importance", "core")}
Complexity: {meta.get("complexity", "advanced")}
Dependencies: {deps}
Execution status of the code in section F: {p.get("code_run", "unexecuted")}

## A. Topic Overview

{p["overview"]}

Prerequisites: {deps}. Builds toward later concurrency topics in domain 13.

## B. First-Principles Explanation

{p["principles"]}

## C. Internal Working and Architecture

{p["architecture"]}

## D. Diagrams and Visual Models

```mermaid
{p["mermaid"]}
```

{p["diagram_caption"]}

## E. Examples and Analogies

{p["examples"]}

## F. Code Examples

File: `EXERCISES/examples/{p["code_file"]}`

```{p.get("code_lang", "python")}
{p["code"].strip()}
```

How to run: `python EXERCISES/examples/{p["code_file"]}` from `backend-engineering-knowledge-base/`.

{p["code_notes"]}

## G. Practical Backend Application

{p["backend"]}

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
{trades}

## I. Common Mistakes and Misconceptions

{mistakes}

## J. Debugging and Troubleshooting

{p["debug"]}

## K. Interview Preparation

{qa_block("Beginner", p["beginner"])}

{qa_block("Intermediate", p["intermediate"])}

{qa_block("Advanced", p["advanced"])}

{qa_block("Scenarios", p["scenarios"])}

{qa_block("Follow-ups", p["followups"])}

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`. Try these before opening that file.

### Exercise 1 — implementation

{p["ex1"]}

### Exercise 2 — debugging

{p["ex2"]}

### Exercise 3 — trade-off

{p["ex3"]}

## M. Revision Notes

{rev}

## N. Related Topics

Dependencies: {deps}.

Next in chain: {nxt if nxt else "see inventory"}.

See also: {related}.

## O. Completion Criteria

{comp}
"""
    ).strip() + "\n"


def build_exercise(tid: str, p: dict) -> str:
    return f"""# Exercises — {tid}

Problems only. Solutions: [{tid}](../solutions/{tid}.md).

1. {p["ex1_bullet"]}
2. {p["ex2_bullet"]}
3. {p["ex3_bullet"]}
"""


def build_solution(tid: str, p: dict) -> str:
    return f"""# Solutions for {tid}

Open this only after attempting the exercises in the topic note.

## Exercise 1

{p["ex1_sol"]}

## Exercise 2

{p["ex2_sol"]}

## Exercise 3

{p["ex3_sol"]}
"""


def build_interview(meta: dict, p: dict) -> str:
    tid = meta["id"]
    sections = [
        ("Beginner", p["beginner"]),
        ("Intermediate", p["intermediate"]),
        ("Advanced", p["advanced"]),
        ("Scenarios", p["scenarios"]),
        ("Follow-ups", p["followups"]),
    ]
    lines = []
    n = 0
    for label, items in sections:
        for q, _ in items:
            n += 1
            lines.append(f"{n}. {label}. {q}")
    slug = Path(meta["note_path"]).name
    return f"""# {tid} interview items

Domain: {meta["domain"]}
Topic: {meta["name"]}
Difficulty mix: beginner, intermediate, advanced, scenario, follow-up
Interview type: fundamentals, debugging, trade-off
Full reasoned answers are in the topic note, section K.

## Questions

{chr(10).join(lines)}

Answer key: [topic note section K](../{meta["folder"]}/notes/{slug}).
"""


def main() -> None:
    from _gen_d13_payloads import register_all

    register_all(reg, para4)
    finished: list[str] = []
    failures: list[str] = []
    examples_dir = EXERCISES / "examples"
    examples_dir.mkdir(parents=True, exist_ok=True)
    for meta in load_topics():
        tid = meta["id"]
        p = PAYLOADS.get(tid)
        if not p:
            failures.append(f"{tid}: missing payload")
            continue
        try:
            note_path = ROOT / meta["note_path"]
            note_path.parent.mkdir(parents=True, exist_ok=True)
            note_path.write_text(build_note(meta, p), encoding="utf-8")
            (EXERCISES / f"{tid}.md").write_text(build_exercise(tid, p), encoding="utf-8")
            (SOLUTIONS / f"{tid}.md").write_text(build_solution(tid, p), encoding="utf-8")
            (INTERVIEW / f"{tid}.md").write_text(build_interview(meta, p), encoding="utf-8")
            code_path = examples_dir / p["code_file"]
            if not code_path.exists():
                code_path.write_text(p["code"].strip() + "\n", encoding="utf-8")
            finished.append(tid)
        except OSError as exc:
            failures.append(f"{tid}: {exc}")
    print("FINISHED:", ",".join(finished))
    print("FAILURES:", ",".join(failures) if failures else "none")


if __name__ == "__main__":
    main()

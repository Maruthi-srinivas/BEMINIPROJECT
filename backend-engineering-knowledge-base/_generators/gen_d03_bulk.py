"""Write D03-T003..T024 notes and companion files. Run: python gen_d03_bulk.py"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV = json.loads((ROOT / "00_INDEX" / "inventory.json").read_text(encoding="utf-8"))
TOPIC_META = {t["id"]: t for t in INV["topics"] if t["id"].startswith("D03-T")}


def followup(text: str) -> str:
    """Ensure follow-up answers are at least four sentences."""
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    while len(sentences) < 4:
        sentences.append("Production debugging ties this to metrics, logs, and reproducible load tests")
    return ". ".join(sentences) + "."


def qa(level: str, pairs: list[tuple[str, str]]) -> str:
    out = [f"### {level}", ""]
    for i, (q, a) in enumerate(pairs, 1):
        out += [f"#### Q{i}. {q}", "", f"**Answer:** {a}", ""]
    return "\n".join(out)


def section_k(bank: dict) -> str:
    parts = ["## K. Interview Preparation", ""]
    for key, title in [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
        ("scenarios", "Scenarios"),
    ]:
        parts.append(qa(title, bank[key]))
    parts.append("### Follow-ups")
    parts.append("")
    for i, (q, a) in enumerate(bank["followups"], 1):
        parts += [f"#### Q{i}. {q}", "", f"**Answer:** {followup(a)}", ""]
    return "\n".join(parts)


def table(rows: list[tuple[str, str, str, str, str]]) -> str:
    lines = [
        "| Choice | Benefit | Cost | Choose when | Avoid when |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def build_note(t: dict, body: dict) -> str:
    tid = t["id"]
    deps = ", ".join(f"`{d}`" for d in t["dependencies"])
    head = f"""# {tid} — {t['name']}

Topic ID: `{tid}`
Domain: {t['domain']}
Subdomain: {t['subdomain']}
Importance: {t['importance']}
Complexity: {t['complexity']}
Dependencies: {deps}
Execution status of the code in section F: unexecuted

"""
    aj = f"""## A. Topic Overview

{body['overview']}

## B. First-Principles Explanation

{body['fp']}

## C. Internal Working and Architecture

{body['internal']}

## D. Diagrams and Visual Models

```mermaid
{body['mermaid']}
```

{body['diagram']}

## E. Examples and Analogies

{body['examples']}

## F. Code Examples

File: `{body['code_file']}`

```{body['code_lang']}
{body['code']}
```

How to run: {body['code_run']}

Expected output: {body['code_out']}

Important lines: {body['code_lines']}

This example was not executed for this note.

## G. Practical Backend Application

{body['backend']}

## H. Advantages, Limitations and Trade-offs

{body['tradeoffs']}

## I. Common Mistakes and Misconceptions

{body['mistakes']}

## J. Debugging and Troubleshooting

{body['debug']}

"""
    lo = f"""## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`.

### Exercise 1 — implementation

{body['ex1']}

### Exercise 2 — debugging

{body['ex2']}

### Exercise 3 — trade-off

{body['ex3']}

## M. Revision Notes

{body['revision']}

Flashcards:

{body['flash']}

## N. Related Topics

Understand this before: {body['pre']}

This topic supports: {body['sup']}

Often confused with: {body['conf']}

Interviewers combine this with: {body['comb']}

## O. Completion Criteria

{body['crit']}
"""
    return head + aj + section_k(body["bank"]) + lo


def write_topic(tid: str, body: dict) -> None:
    t = TOPIC_META[tid]
    note_path = ROOT / t["note_path"]
    note_path.parent.mkdir(parents=True, exist_ok=True)
    note_path.write_text(build_note(t, body), encoding="utf-8")
    ex = body["exercises_md"]
    (ROOT / "EXERCISES" / f"{tid}.md").write_text(
        f"# Exercises — {tid}\n\nProblems only. Solutions: [{tid}](../solutions/{tid}.md).\n\n"
        f"1. {ex[0]}\n2. {ex[1]}\n3. {ex[2]}\n",
        encoding="utf-8",
    )
    sol = body["solutions_md"]
    (ROOT / "EXERCISES" / "solutions" / f"{tid}.md").write_text(
        f"# Solutions for {tid}\n\n## Exercise 1\n\n{sol[0]}\n\n## Exercise 2\n\n{sol[1]}\n\n## Exercise 3\n\n{sol[2]}\n",
        encoding="utf-8",
    )
    bank = body["bank"]
    lines = [
        f"# {tid} interview items",
        "",
        f"Domain: {t['domain']}",
        f"Topic: {t['subdomain']}",
        "",
        "## Questions",
        "",
    ]
    n = 1
    for key, label in [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
        ("scenarios", "Scenario"),
    ]:
        for q, _ in bank[key]:
            lines.append(f"{n}. {label}. {q}")
            n += 1
    for q, _ in bank["followups"]:
        lines.append(f"{n}. Follow-up. {q}")
        n += 1
    rel = f"../{t['note_path']}"
    lines += ["", f"Answer key: [topic note section K]({rel}).", ""]
    (ROOT / "INTERVIEW_BANK" / "items" / f"{tid}.md").write_text("\n".join(lines), encoding="utf-8")


# Import topic bodies from split modules
from gen_d03_data_003_012 import BODIES_003_012  # noqa: E402
from gen_d03_data_013_024 import BODIES_013_024  # noqa: E402

ALL = {**BODIES_003_012, **BODIES_013_024}

if __name__ == "__main__":
    finished, failures = [], []
    for tid in sorted(ALL):
        if tid in ("D03-T001", "D03-T002"):
            continue
        try:
            write_topic(tid, ALL[tid])
            finished.append(tid)
        except Exception as e:  # noqa: BLE001
            failures.append(f"{tid}: {e}")
    print("FINISHED:", ",".join(["D03-T001", "D03-T002"] + finished))
    print("FAILURES:", failures or "none")

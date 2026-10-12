"""One-shot generator for D10-T001..D10-T019 knowledge-base artifacts."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOSQL = ROOT / "09_NOSQL_DATABASES"
NOTES = NOSQL / "notes"
EXERCISES = ROOT / "EXERCISES"
SOLUTIONS = EXERCISES / "solutions"
INTERVIEW = ROOT / "INTERVIEW_BANK" / "items"


def four(sentences: list[str]) -> str:
    assert len(sentences) == 4
    return " ".join(sentences)


def interview_block(items: dict) -> str:
    lines = ["## K. Interview Preparation", ""]
    for level, qs in [
        ("Beginner", items["beginner"]),
        ("Intermediate", items["intermediate"]),
        ("Advanced", items["advanced"]),
        ("Scenarios", items["scenarios"]),
        ("Follow-ups", items["followups"]),
    ]:
        lines.append(f"### {level}")
        lines.append("")
        for i, (q, a) in enumerate(qs, 1):
            lines.append(f"#### Q{i}. {q}")
            lines.append("")
            lines.append(f"**Answer:** {a}")
            lines.append("")
    return "\n".join(lines)


def build_note(meta: dict) -> str:
    tid = meta["id"]
    slug = meta["slug"]
    title = meta["title"]
    subdomain = meta["subdomain"]
    deps = meta["dependencies"]
    imp = meta["importance"]
    cx = meta["complexity"]
    dep_str = ", ".join(f"`{d}`" for d in deps) if deps else "none listed in inventory"

    body = meta["sections"]
    iv = meta["interview"]

    return f"""# {tid} — {title}

Topic ID: `{tid}`
Domain: NoSQL Databases
Subdomain: {subdomain}
Importance: {imp}
Complexity: {cx}
Dependencies: {dep_str}
Execution status of the code in section F: illustrative (not executed in CI for this topic)

## A. Topic Overview

{body["A"]}

## B. First-Principles Explanation

{body["B"]}

## C. Internal Working and Architecture

{body["C"]}

## D. Diagrams and Visual Models

```mermaid
{body["mermaid"]}
```

{body["D_caption"]}

## E. Examples and Analogies

{body["E"]}

## F. Code Examples

{body["F"]}

## G. Practical Backend Application

{body["G"]}

## H. Advantages, Limitations and Trade-offs

{body["H"]}

## I. Common Mistakes and Misconceptions

{body["I"]}

## J. Debugging and Troubleshooting

{body["J"]}

{interview_block(iv)}

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`. Try these before opening that file.

{body["L"]}

## M. Revision Notes

{body["M"]}

## N. Related Topics

{body["N"]}

## O. Completion Criteria

{body["O"]}
"""


def write_artifacts(meta: dict) -> None:
    tid = meta["id"]
    NOTES.mkdir(parents=True, exist_ok=True)
    note_file = NOTES / f"{meta['slug']}.md"
    note_file.write_text(build_note(meta), encoding="utf-8")

    ex = meta["exercises"]
    EXERCISES.mkdir(parents=True, exist_ok=True)
    (EXERCISES / f"{tid}.md").write_text(
        f"""# Exercises — {tid}

Problems only. Solutions: [{tid}](solutions/{tid}.md).

1. {ex[0]}
2. {ex[1]}
3. {ex[2]}
""",
        encoding="utf-8",
    )

    SOLUTIONS.mkdir(parents=True, exist_ok=True)
    (SOLUTIONS / f"{tid}.md").write_text(
        f"""# Solutions for {tid}

Open this only after attempting the exercises in the topic note.

## Exercise 1

{meta["sol"][0]}

## Exercise 2

{meta["sol"][1]}

## Exercise 3

{meta["sol"][2]}
""",
        encoding="utf-8",
    )

    INTERVIEW.mkdir(parents=True, exist_ok=True)
    qs = []
    n = 1
    for level, pairs in [
        ("Beginner", meta["interview"]["beginner"]),
        ("Intermediate", meta["interview"]["intermediate"]),
        ("Advanced", meta["interview"]["advanced"]),
        ("Scenario", meta["interview"]["scenarios"]),
        ("Follow-up", meta["interview"]["followups"]),
    ]:
        for q, _ in pairs:
            qs.append(f"{n}. {level}. {q}")
            n += 1

    (INTERVIEW / f"{tid}.md").write_text(
        f"""# {tid} interview items

Domain: NoSQL Databases
Topic: {meta["title"]}
Difficulty mix: beginner, intermediate, advanced, scenario, follow-up
Interview type: fundamentals, debugging, trade-off, system design
Full reasoned answers are in the topic note, section K.

## Questions

{chr(10).join(qs)}

Answer key: [topic note section K](../../09_NOSQL_DATABASES/notes/{meta["slug"]}.md).
""",
        encoding="utf-8",
    )


# Load inventory ids/paths for sanity
inv_path = ROOT / "00_INDEX" / "inventory.json"
inventory = json.loads(inv_path.read_text(encoding="utf-8"))
by_id = {t["id"]: t for t in inventory["topics"]}

def load_topics() -> list[dict]:
    from d10_topic_defs import TOPICS  # noqa: WPS433

    return TOPICS


def main() -> None:
    expected = [f"D10-T{i:03d}" for i in range(1, 20)]
    topics = load_topics()
    ids = [t["id"] for t in topics]
    missing = [x for x in expected if x not in ids]
    extra = [x for x in ids if x not in expected]
    if missing or extra:
        raise SystemExit(f"topic id mismatch missing={missing} extra={extra}")

    failures: list[str] = []
    finished: list[str] = []
    for meta in topics:
        tid = meta["id"]
        try:
            inv = by_id[tid]
            if inv["note_path"] != f"09_NOSQL_DATABASES/notes/{meta['slug']}.md":
                raise ValueError(f"note_path mismatch for {tid}")
            write_artifacts(meta)
            finished.append(tid)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{tid}: {exc}")

    print("FINISHED", ",".join(finished))
    print("FAILURES", ",".join(failures) if failures else "none")


if __name__ == "__main__":
    main()

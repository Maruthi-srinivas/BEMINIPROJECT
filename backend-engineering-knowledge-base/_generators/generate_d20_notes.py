#!/usr/bin/env python3
"""Generate D20-T001..D20-T026 Software Testing knowledge-base artifacts."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from d20_topic_meta import TOPIC_META, TAXONOMY_BLOCK

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "00_INDEX" / "inventory.json"
TESTING = ROOT / "19_TESTING"
NOTES = TESTING / "notes"
EXERCISES = ROOT / "EXERCISES"
SOLUTIONS = EXERCISES / "solutions"
INTERVIEW = ROOT / "INTERVIEW_BANK" / "items"


def load_topics() -> list[dict]:
    data = json.loads(INV.read_text(encoding="utf-8"))
    out = []
    for t in data["topics"]:
        if not t["id"].startswith("D20-T"):
            continue
        n = int(t["id"].split("-T")[1])
        if 1 <= n <= 26:
            out.append(t)
    out.sort(key=lambda x: int(x["id"].split("-T")[1]))
    return out


def slug_from_path(note_path: str) -> str:
    return Path(note_path).stem


def sentence_count(text: str) -> int:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return len([p for p in parts if p])


def ensure_answer_length(answer: str, context: str) -> None:
    if sentence_count(answer) < 4:
        raise ValueError(f"Answer needs 4+ sentences ({context}): {answer[:80]}...")


def interview_block(pairs: dict[str, list[tuple[str, str]]]) -> str:
    for level, items in pairs.items():
        assert len(items) == (3 if level == "followups" else 5), level
        for q, a in items:
            ensure_answer_length(a, f"{level}: {q[:50]}")

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
            section("Beginner", pairs["beginner"]),
            section("Intermediate", pairs["intermediate"]),
            section("Advanced", pairs["advanced"]),
            section("Scenarios", pairs["scenarios"]),
            section("Follow-ups", pairs["followups"]),
        ]
    )


def build_note(t: dict, meta: dict) -> str:
    tid = t["id"]
    num = int(tid.split("-T")[1])
    deps = ", ".join(f"`{d}`" for d in t.get("dependencies", []))
    prev = f"`D20-T{num-1:03d}`" if num > 1 else "`D05-T002`"
    nxt = f"`D20-T{num+1:03d}`" if num < 26 else "`D21-T001`"
    taxonomy = TAXONOMY_BLOCK if meta.get("include_taxonomy") else meta.get("taxonomy_note", "")

    return f"""# {tid} — {t['name']}

Topic ID: `{tid}`
Domain: Software Testing
Subdomain: {t['subdomain']}
Importance: {t['importance']}
Complexity: {t['complexity']}
Dependencies: {deps}
Execution status of the code in section F: unexecuted (illustrative pytest only)

## A. Topic Overview

{meta['overview']}

{taxonomy}

Prerequisites: {meta.get('prereq', prev)}. Next in the testing track: {nxt}.

## B. First-Principles Explanation

{meta['first_principles']}

## C. Internal Working and Architecture

{meta['internal']}

## D. Diagrams and Visual Models

```mermaid
{meta['mermaid']}
```

{meta['diagram_caption']}

## E. Examples and Analogies

{meta['examples']}

## F. Code Examples

{meta['code_section']}

## G. Practical Backend Application

{meta['practical']}

## H. Advantages, Limitations and Trade-offs

{meta['tradeoffs']}

## I. Common Mistakes and Misconceptions

{meta['mistakes']}

## J. Debugging and Troubleshooting

{meta['debugging']}

## K. Interview Preparation

{interview_block(meta['interview'])}

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`. Try these before opening that file.

{meta['exercises']}

## M. Revision Notes

{meta['revision']}

## N. Related Topics

Understand this before: {meta.get('related_before', prev)}.

This topic supports: {meta.get('related_supports', nxt)}.

Often confused with: {meta.get('confused_with', 'adjacent layers in the test pyramid')}.

Interviewers combine this with {meta.get('interview_combo', '`D20-T001` unit tests, `D20-T025` CI pipelines')}.

## O. Completion Criteria

{meta['completion']}
"""


def write_exercise(tid: str, items: list[str]) -> None:
    text = (
        f"# Exercises — {tid}\n\n"
        f"Problems only. Solutions: [{tid}](../solutions/{tid}.md).\n\n"
        + "\n".join(f"{i}. {item}" for i, item in enumerate(items, 1))
        + "\n"
    )
    (EXERCISES / f"{tid}.md").write_text(text, encoding="utf-8")


def write_solution(tid: str, solutions: list[str]) -> None:
    lines = [
        f"# Solutions for {tid}",
        "",
        "Open this only after attempting the exercises in the topic note.",
        "",
    ]
    for i, sol in enumerate(solutions, 1):
        lines.extend([f"## Exercise {i}", "", sol, ""])
    (SOLUTIONS / f"{tid}.md").write_text("\n".join(lines), encoding="utf-8")


def write_interview_bank(t: dict, meta: dict, slug: str) -> None:
    tid = t["id"]
    qs: list[str] = []
    n = 1
    for level, key in [
        ("Beginner", "beginner"),
        ("Intermediate", "intermediate"),
        ("Advanced", "advanced"),
        ("Scenario", "scenarios"),
        ("Follow-up", "followups"),
    ]:
        for q, _ in meta["interview"][key]:
            qs.append(f"{n}. {level}. {q}")
            n += 1
    rel = f"../../19_TESTING/notes/{slug}.md"
    text = f"""# {tid} interview items

Domain: Software Testing
Topic: {t['subdomain']}
Difficulty mix: beginner, intermediate, advanced, scenario, follow-up
Interview type: fundamentals, debugging, trade-off, operations
Full reasoned answers are in the topic note, section K.

## Questions

{chr(10).join(qs)}

Answer key: [topic note section K]({rel}).
"""
    (INTERVIEW / f"{tid}.md").write_text(text, encoding="utf-8")


def main() -> int:
    finished, failures = materialize_to_disk()
    if failures:
        return 1
    return 0


def materialize_to_disk() -> tuple[list[str], list[str]]:
    """Write all D20 artifacts; returns (finished_ids, failures)."""
    topics = load_topics()
    failures: list[str] = []
    finished: list[str] = []

    NOTES.mkdir(parents=True, exist_ok=True)
    EXERCISES.mkdir(parents=True, exist_ok=True)
    SOLUTIONS.mkdir(parents=True, exist_ok=True)
    INTERVIEW.mkdir(parents=True, exist_ok=True)

    for t in topics:
        tid = t["id"]
        try:
            if tid not in TOPIC_META:
                raise KeyError(f"missing TOPIC_META for {tid}")
            meta = TOPIC_META[tid]
            slug = slug_from_path(t["note_path"])
            note_file = NOTES / f"{slug}.md"
            note_file.write_text(build_note(t, meta), encoding="utf-8")
            write_exercise(tid, meta["exercise_list"])
            write_solution(tid, meta["solution_list"])
            write_interview_bank(t, meta, slug)
            finished.append(tid)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{tid}: {exc}")
    return finished, failures


if __name__ == "__main__":
    finished, failures = materialize_to_disk()
    print("FINISHED:", ", ".join(finished))
    if failures:
        for f in failures:
            print(f"FAILURE: {f}")
        raise SystemExit(1)
    print(f"Wrote {len(finished)} topics ({len(finished) * 4} files).")
    raise SystemExit(0)

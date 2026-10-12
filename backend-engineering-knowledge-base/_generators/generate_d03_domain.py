#!/usr/bin/env python3
"""Generate D03 Operating Systems notes, exercises, solutions, and interview bank items."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV_PATH = ROOT / "00_INDEX" / "inventory.json"


def load_d03_topics() -> list[dict]:
    data = json.loads(INV_PATH.read_text(encoding="utf-8"))
    topics = [t for t in data["topics"] if t["id"].startswith("D03-T")]
    topics.sort(key=lambda t: t["id"])
    return topics


def interview_block(topic: dict) -> str:
    """Section K: 5+5+5+5 questions and 3 follow-ups (4+ sentences each)."""
    tid = topic["id"]
    name = topic["name"]
    subdomain = topic["subdomain"]
    # Topic-specific interview content keyed by id
    banks: dict[str, dict] = INTERVIEW_BANKS
    bank = banks.get(tid)
    if not bank:
        raise KeyError(f"Missing interview bank for {tid}")
    lines = ["## K. Interview Preparation", ""]
    for level in ("Beginner", "Intermediate", "Advanced", "Scenarios"):
        lines.append(f"### {level}")
        lines.append("")
        qs = bank[level.lower()]
        for i, (q, a) in enumerate(qs, 1):
            lines.append(f"#### Q{i}. {q}")
            lines.append("")
            lines.append(f"**Answer:** {a}")
            lines.append("")
    lines.append("### Follow-ups")
    lines.append("")
    for i, (q, a) in enumerate(bank["followups"], 1):
        lines.append(f"#### Q{i}. {q}")
        lines.append("")
        lines.append(f"**Answer:** {a}")
        lines.append("")
    return "\n".join(lines)


def build_note(topic: dict) -> str:
    body = NOTE_BODIES[topic["id"]]
    header = f"""# {topic['id']} — {topic['name']}

Topic ID: `{topic['id']}`
Domain: {topic['domain']}
Subdomain: {topic['subdomain']}
Importance: {topic['importance']}
Complexity: {topic['complexity']}
Dependencies: {', '.join(f'`{d}`' for d in topic['dependencies'])}
Execution status of the code in section F: unexecuted

"""
    return header + body + "\n" + interview_block(topic) + NOTE_TAIL[topic["id"]]


def write_exercise(topic: dict) -> str:
    ex = EXERCISES[topic["id"]]
    return f"""# Exercises — {topic['id']}

Problems only. Solutions: [{topic['id']}](../solutions/{topic['id']}.md).

1. {ex[0]}
2. {ex[1]}
3. {ex[2]}
"""


def write_solution(topic: dict) -> str:
    sol = SOLUTIONS[topic["id"]]
    return f"""# Solutions for {topic['id']}

Open this only after attempting the exercises in the topic note.

## Exercise 1

{sol[0]}

## Exercise 2

{sol[1]}

## Exercise 3

{sol[2]}
"""


def write_interview_item(topic: dict) -> str:
    bank = INTERVIEW_BANKS[topic["id"]]
    note_rel = f"../{topic['note_path']}"
    lines = [
        f"# {topic['id']} interview items",
        "",
        f"Domain: {topic['domain']}",
        f"Topic: {topic['subdomain']}",
        "Difficulty mix: beginner, intermediate, advanced, scenario, follow-up",
        "Interview type: fundamentals, debugging, trade-off, systems",
        "Full reasoned answers are in the topic note, section K.",
        "",
        "## Questions",
        "",
    ]
    n = 1
    for level, key in [
        ("Beginner", "beginner"),
        ("Intermediate", "intermediate"),
        ("Advanced", "advanced"),
        ("Scenario", "scenarios"),
    ]:
        for q, _ in bank[key]:
            lines.append(f"{n}. {level}. {q}")
            n += 1
    for q, _ in bank["followups"]:
        lines.append(f"{n}. Follow-up. {q}")
        n += 1
    lines.append("")
    lines.append(f"Answer key: [topic note section K]({note_rel}).")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    topics = load_d03_topics()
    failures: list[str] = []
    finished: list[str] = []
    for topic in topics:
        tid = topic["id"]
        try:
            note_path = ROOT / topic["note_path"]
            note_path.parent.mkdir(parents=True, exist_ok=True)
            note_path.write_text(build_note(topic), encoding="utf-8")
            (ROOT / "EXERCISES" / f"{tid}.md").write_text(write_exercise(topic), encoding="utf-8")
            (ROOT / "EXERCISES" / "solutions" / f"{tid}.md").write_text(
                write_solution(topic), encoding="utf-8"
            )
            (ROOT / "INTERVIEW_BANK" / "items" / f"{tid}.md").write_text(
                write_interview_item(topic), encoding="utf-8"
            )
            finished.append(tid)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{tid}: {exc}")
    print("FINISHED:", ",".join(finished))
    print("FAILURES:", ",".join(failures) if failures else "none")


# --- Content loaded from companion module ---
from d03_content_data import (  # noqa: E402
    EXERCISES,
    INTERVIEW_BANKS,
    NOTE_BODIES,
    NOTE_TAIL,
    SOLUTIONS,
)

if __name__ == "__main__":
    main()

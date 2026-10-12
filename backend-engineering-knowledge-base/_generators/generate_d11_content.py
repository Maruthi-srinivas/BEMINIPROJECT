#!/usr/bin/env python3
"""Generate D11-T001..D11-T025 notes, exercises, solutions, interview bank items."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "00_INDEX" / "inventory.json"


def load_topics() -> list[dict]:
    data = json.loads(INV.read_text(encoding="utf-8"))
    topics = [t for t in data["topics"] if t["id"].startswith("D11-T")]
    topics.sort(key=lambda t: int(t["id"].split("-T")[1]))
    return topics


def para(*sentences: str) -> str:
    return " ".join(sentences)


def interview_block(sections: dict[str, list[tuple[str, str]]]) -> str:
    lines = ["## K. Interview Preparation", ""]
    order = [
        ("Beginner", "beginner"),
        ("Intermediate", "intermediate"),
        ("Advanced", "advanced"),
        ("Scenarios", "scenario"),
        ("Follow-ups", "follow-up"),
    ]
    for title, key in order:
        lines.append(f"### {title}")
        lines.append("")
        for i, (q, a) in enumerate(sections[key], 1):
            lines.append(f"#### Q{i}. {q}")
            lines.append("")
            lines.append(f"**Answer:** {a}")
            lines.append("")
    return "\n".join(lines)


def exercises_block(ex1: str, ex2: str, ex3: str, tid: str) -> str:
    return f"""## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`. Try these before opening that file.

### Exercise 1 — implementation

{ex1}

### Exercise 2 — debugging

{ex2}

### Exercise 3 — trade-off

{ex3}
"""


def revision_block(bullets: list[str], flash: list[tuple[str, str]]) -> str:
    lines = ["## M. Revision Notes", ""]
    for b in bullets:
        lines.append(f"- {b}")
    lines.append("")
    lines.append("Flashcards:")
    lines.append("")
    for q, a in flash:
        lines.append(f"- {q} {a}")
    return "\n".join(lines)


def related_block(before: str, supports: str, confused: str, combine: str) -> str:
    return f"""## N. Related Topics

Understand this before: {before}

This topic supports: {supports}

Often confused with: {confused}

Interviewers combine this with: {combine}
"""


def completion_block(items: list[str]) -> str:
    lines = ["## O. Completion Criteria", ""]
    for it in items:
        lines.append(f"- {it}")
    return "\n".join(lines)


# Topic-specific content registry (abbreviated keys; full prose in build_note)
TOPIC_META: dict[str, dict] = {}


def register(
    tid: str,
    *,
    overview: list[str],
    first_principles: list[str],
    internal: list[str],
    mermaid: str,
    mermaid_caption: str,
    examples: list[str],
    code_file: str,
    code: str,
    code_run: str,
    code_output: str,
    code_notes: list[str],
    practical: list[str],
    trade_table: list[tuple[str, str, str, str, str]],
    trade_extra: list[str],
    mistakes: list[str],
    debug: list[str],
    interview: dict[str, list[tuple[str, str]]],
    ex1: str,
    ex2: str,
    ex3: str,
    revision: list[str],
    flash: list[tuple[str, str]],
    before: str,
    supports: str,
    confused: str,
    combine: str,
    completion: list[str],
    exec_status: str = "not executed (documentation example)",
    sol1: str = "See topic note section L and F.",
    sol2: str = "See topic note section J.",
    sol3: str = "See topic note section H.",
) -> None:
    TOPIC_META[tid] = {
        "overview": overview,
        "first_principles": first_principles,
        "internal": internal,
        "mermaid": mermaid,
        "mermaid_caption": mermaid_caption,
        "examples": examples,
        "code_file": code_file,
        "code": code,
        "code_run": code_run,
        "code_output": code_output,
        "code_notes": code_notes,
        "practical": practical,
        "trade_table": trade_table,
        "trade_extra": trade_extra,
        "mistakes": mistakes,
        "debug": debug,
        "interview": interview,
        "ex1": ex1,
        "ex2": ex2,
        "ex3": ex3,
        "revision": revision,
        "flash": flash,
        "before": before,
        "supports": supports,
        "confused": confused,
        "combine": combine,
        "completion": completion,
        "exec_status": exec_status,
        "sol1": sol1,
        "sol2": sol2,
        "sol3": sol3,
    }


def build_note(topic: dict) -> str:
    tid = topic["id"]
    meta = TOPIC_META[tid]
    slug = Path(topic["note_path"]).stem
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
    sec_a = "## A. Topic Overview\n\n" + "\n\n".join(meta["overview"]) + "\n\n"
    sec_b = "## B. First-Principles Explanation\n\n" + "\n\n".join(meta["first_principles"]) + "\n\n"
    sec_c = "## C. Internal Working and Architecture\n\n" + "\n\n".join(meta["internal"]) + "\n\n"
    sec_d = f"""## D. Diagrams and Visual Models

```mermaid
{meta["mermaid"]}
```

{meta["mermaid_caption"]}

"""
    sec_e = "## E. Examples and Analogies\n\n" + "\n\n".join(meta["examples"]) + "\n\n"
    sec_f = f"""## F. Code Examples

File: `{meta["code_file"]}`

Dependencies: Redis client library or standard library as noted in the snippet.

```python
{meta["code"]}
```

How to run: {meta["code_run"]}

Expected output: {meta["code_output"]}

""" + "\n".join(meta["code_notes"]) + "\n\n"
    sec_g = "## G. Practical Backend Application\n\n" + "\n\n".join(meta["practical"]) + "\n\n"
    rows = meta["trade_table"]
    sec_h = "## H. Advantages, Limitations and Trade-offs\n\n| Choice | Benefit | Cost | Choose when | Avoid when |\n| --- | --- | --- | --- | --- |\n"
    for r in rows:
        sec_h += "| " + " | ".join(r) + " |\n"
    sec_h += "\n" + "\n\n".join(meta["trade_extra"]) + "\n\n"
    sec_i = "## I. Common Mistakes and Misconceptions\n\n" + "\n".join(f"- {m}" for m in meta["mistakes"]) + "\n\n"
    sec_j = "## J. Debugging and Troubleshooting\n\n" + "\n\n".join(meta["debug"]) + "\n\n"
    body = (
        header
        + sec_a
        + sec_b
        + sec_c
        + sec_d
        + sec_e
        + sec_f
        + sec_g
        + sec_h
        + sec_i
        + sec_j
        + interview_block(meta["interview"])
        + exercises_block(meta["ex1"], meta["ex2"], meta["ex3"], tid)
        + revision_block(meta["revision"], meta["flash"])
        + related_block(meta["before"], meta["supports"], meta["confused"], meta["combine"])
        + completion_block(meta["completion"])
    )
    return body


def write_exercise(tid: str, name: str, ex1: str, ex2: str, ex3: str) -> str:
    return f"""# Exercises — {tid}

Problems only. Solutions: [{tid}](../solutions/{tid}.md).

1. {ex1}
2. {ex2}
3. {ex3}
"""


def write_solution(tid: str, s1: str, s2: str, s3: str) -> str:
    return f"""# Solutions for {tid}

Open this only after attempting the exercises in the topic note.

## Exercise 1

{s1}

## Exercise 2

{s2}

## Exercise 3

{s3}
"""


def write_interview_bank(topic: dict, questions: list[str]) -> str:
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
    for i, q in enumerate(questions, 1):
        lines.append(f"{i}. {q}")
    lines.append("")
    lines.append(f"Answer key: [topic note section K]({rel}).")
    return "\n".join(lines)


def bank_questions(interview: dict[str, list[tuple[str, str]]]) -> list[str]:
    out: list[str] = []
    labels = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
        ("scenario", "Scenario"),
        ("follow-up", "Follow-up"),
    ]
    for key, label in labels:
        for q, _ in interview[key]:
            out.append(f"{label}. {q}")
    return out


# --- Populate TOPIC_META (content defined in populate_d11 module) ---
import sys

sys.path.insert(0, str(Path(__file__).parent))
from populate_d11 import populate  # noqa: E402

populate(register)


def all_artifacts() -> dict[str, str]:
    """Return relative path -> content for every D11 artifact (for tooling without shell)."""
    artifacts: dict[str, str] = {}
    topics = load_topics()
    for topic in topics:
        tid = topic["id"]
        if tid not in TOPIC_META:
            continue
        meta = TOPIC_META[tid]
        artifacts[topic["note_path"]] = build_note(topic)
        artifacts[f"EXERCISES/{tid}.md"] = write_exercise(tid, topic["name"], meta["ex1"], meta["ex2"], meta["ex3"])
        artifacts[f"EXERCISES/solutions/{tid}.md"] = write_solution(
            tid, meta["sol1"], meta["sol2"], meta["sol3"]
        )
        artifacts[f"INTERVIEW_BANK/items/{tid}.md"] = write_interview_bank(
            topic, bank_questions(meta["interview"])
        )
    return artifacts


def main() -> tuple[list[str], list[str]]:
    finished: list[str] = []
    failures: list[str] = []
    topics = load_topics()
    for topic in topics:
        tid = topic["id"]
        try:
            if tid not in TOPIC_META:
                failures.append(f"{tid}: missing content registry")
                continue
            note_path = ROOT / topic["note_path"]
            note_path.parent.mkdir(parents=True, exist_ok=True)
            note_path.write_text(build_note(topic), encoding="utf-8")
            meta = TOPIC_META[tid]
            ex_path = ROOT / "EXERCISES" / f"{tid}.md"
            ex_path.write_text(
                write_exercise(tid, topic["name"], meta["ex1"], meta["ex2"], meta["ex3"]),
                encoding="utf-8",
            )
            sol_path = ROOT / "EXERCISES" / "solutions" / f"{tid}.md"
            sol_path.parent.mkdir(parents=True, exist_ok=True)
            sol_path.write_text(
                write_solution(tid, meta.get("sol1", "See topic note."), meta.get("sol2", "See topic note."), meta.get("sol3", "See topic note.")),
                encoding="utf-8",
            )
            ib_path = ROOT / "INTERVIEW_BANK" / "items" / f"{tid}.md"
            ib_path.parent.mkdir(parents=True, exist_ok=True)
            ib_path.write_text(
                write_interview_bank(topic, bank_questions(meta["interview"])),
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

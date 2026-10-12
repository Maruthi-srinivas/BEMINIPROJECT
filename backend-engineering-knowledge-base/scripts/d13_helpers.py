"""Helpers for D13 artifact generation."""
from __future__ import annotations


def interview_block(questions: dict[str, list[tuple[str, str]]]) -> str:
    parts = ["## K. Interview Preparation\n"]
    for level, items in questions.items():
        parts.append(f"### {level}\n")
        for i, (q, a) in enumerate(items, 1):
            parts.append(f"#### Q{i}. {q}\n\n**Answer:** {a.strip()}\n\n")
    return "".join(parts)


def make_exercises(tid: str, e1: str, e2: str, e3: str) -> str:
    return f"""# Exercises — {tid}

Problems only. Solutions: [{tid}](../solutions/{tid}.md).

1. {e1}
2. {e2}
3. {e3}
"""


def make_interview_bank(
    tid: str, title: str, questions: dict[str, list[str]], note_rel: str
) -> str:
    lines = [
        f"# {tid} interview items",
        "",
        "Domain: Concurrency and Parallel Processing",
        f"Topic: {title}",
        "Difficulty mix: beginner, intermediate, advanced, scenario, follow-up",
        "Interview type: fundamentals, debugging, trade-off",
        "Full reasoned answers are in the topic note, section K.",
        "",
        "## Questions",
        "",
    ]
    n = 1
    for level, qs in questions.items():
        for q in qs:
            lines.append(f"{n}. {level}. {q}")
            n += 1
    lines.append("")
    lines.append(f"Answer key: [topic note section K]({note_rel}).")
    lines.append("")
    return "\n".join(lines)


def note_header(tid: str, title: str, importance: str, deps: list[str]) -> str:
    dep_txt = ", ".join(f"`{d}`" for d in deps) if deps else "none listed"
    return f"""# {tid} — {title}

Topic ID: `{tid}`
Domain: Concurrency and Parallel Processing
Subdomain: {title}
Importance: {importance}
Complexity: advanced
Dependencies: {dep_txt}
Execution status of the code in section F: executed (local interpreter where applicable)

"""

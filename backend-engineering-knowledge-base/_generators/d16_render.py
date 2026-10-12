"""Render D16 System Design Fundamentals topic packages."""

from __future__ import annotations

from pathlib import Path

KB = Path(__file__).resolve().parents[1]


def _join_paragraphs(paragraphs: list[str]) -> str:
    return "\n\n".join(p.strip() for p in paragraphs if p.strip())


def render_interview_section(k: dict) -> str:
    parts = ["## K. Interview Preparation\n"]
    for level, count in [
        ("Beginner", 5),
        ("Intermediate", 5),
        ("Advanced", 5),
        ("Scenarios", 5),
        ("Follow-ups", 3),
    ]:
        key = level.lower().replace("-", "_")
        parts.append(f"### {level}\n")
        for i, item in enumerate(k[key][:count], 1):
            q, a = item["q"], item["a"]
            parts.append(f"#### Q{i}. {q}\n\n**Answer:** {a}\n")
    return "\n".join(parts)


def render_note(topic: dict) -> str:
    meta = topic["meta"]
    lines = [
        f"# {meta['id']} — {meta['name']}",
        "",
        f"Topic ID: `{meta['id']}`",
        "Domain: System Design Fundamentals",
        f"Subdomain: {meta['subdomain']}",
        f"Importance: {meta['importance']}",
        f"Complexity: {meta['complexity']}",
        f"Dependencies: {meta['deps_display']}",
        "Execution status of the code in section F: unexecuted (illustrative sizing script)",
        "",
        "## A. Topic Overview",
        "",
        _join_paragraphs(topic["overview"]),
        "",
        "## B. First-Principles Explanation",
        "",
        _join_paragraphs(topic["first_principles"]),
        "",
        topic["capacity_section"],
        "",
        "## C. Internal Working and Architecture",
        "",
        _join_paragraphs(topic["internal"]),
        "",
        "## D. Diagrams and Visual Models",
        "",
        "```mermaid",
        topic["mermaid"].strip(),
        "```",
        "",
        topic.get("diagram_caption", "Read the diagram as a design-time flow, not a vendor-specific deployment."),
        "",
        "## E. Examples and Analogies",
        "",
        _join_paragraphs(topic["examples"]),
        "",
        "## F. Code Examples",
        "",
        topic["code_intro"],
        "",
        "```python",
        topic["code"].strip(),
        "```",
        "",
        topic["code_footer"],
        "",
        "## G. Practical Backend Application",
        "",
        _join_paragraphs(topic["practical"]),
        "",
        "## H. Advantages, Limitations and Trade-offs",
        "",
        topic["tradeoffs_table"],
        "",
        "## I. Common Mistakes and Misconceptions",
        "",
        topic["mistakes"],
        "",
        "## J. Debugging and Troubleshooting",
        "",
        _join_paragraphs(topic["debugging"]),
        "",
        render_interview_section(topic["interview"]),
        "",
        "## L. Practical Exercises",
        "",
        f"Solutions are in `EXERCISES/solutions/{meta['id']}.md`. Try these before opening that file.",
        "",
        topic["exercises_section"],
        "",
        "## M. Revision Notes",
        "",
        topic["revision"],
        "",
        "## N. Related Topics",
        "",
        topic["related"],
        "",
        "## O. Completion Criteria",
        "",
        topic["completion"],
        "",
    ]
    return "\n".join(lines)


def render_exercise_file(meta: dict, exercises: list[dict]) -> str:
    body = [
        f"# Exercises — {meta['id']}",
        "",
        f"Problems only. Solutions: [{meta['id']}](../solutions/{meta['id']}.md).",
        "",
    ]
    for i, ex in enumerate(exercises, 1):
        body.append(f"{i}. {ex['prompt']}")
    return "\n".join(body) + "\n"


def render_solution_file(meta: dict, solutions: list[str]) -> str:
    body = [
        f"# Solutions for {meta['id']}",
        "",
        "Open this only after attempting the exercises in the topic note.",
        "",
    ]
    for i, sol in enumerate(solutions, 1):
        body.append(f"## Exercise {i}")
        body.append("")
        body.append(sol.strip())
        body.append("")
    return "\n".join(body)


def render_interview_bank(meta: dict, interview: dict) -> str:
    questions: list[str] = []
    n = 0
    for level, count in [
        ("Beginner", 5),
        ("Intermediate", 5),
        ("Advanced", 5),
        ("Scenarios", 5),
        ("Follow-ups", 3),
    ]:
        key = level.lower().replace("-", "_")
        for item in interview[key][:count]:
            n += 1
            questions.append(f"{n}. {level}. {item['bank']}")
    rel = f"../{meta['note_path']}"
    return "\n".join(
        [
            f"# {meta['id']} interview items",
            "",
            "Domain: System Design Fundamentals",
            f"Topic: {meta['name']}",
            "Difficulty mix: beginner, intermediate, advanced, scenario, follow-up",
            "Interview type: requirements, estimation, architecture, trade-off",
            "Full reasoned answers are in the topic note, section K.",
            "",
            "## Questions",
            "",
            *questions,
            "",
            f"Answer key: [topic note section K]({rel}).",
            "",
        ]
    )


def write_topic_package(topic: dict) -> None:
    meta = topic["meta"]
    note_path = KB / meta["note_path"]
    note_path.parent.mkdir(parents=True, exist_ok=True)
    note_path.write_text(render_note(topic), encoding="utf-8", newline="\n")

    ex_path = KB / "EXERCISES" / f"{meta['id']}.md"
    ex_path.write_text(render_exercise_file(meta, topic["exercises"]), encoding="utf-8", newline="\n")

    sol_path = KB / "EXERCISES" / "solutions" / f"{meta['id']}.md"
    sol_path.write_text(render_solution_file(meta, topic["solutions"]), encoding="utf-8", newline="\n")

    bank_path = KB / "INTERVIEW_BANK" / "items" / f"{meta['id']}.md"
    bank_path.write_text(render_interview_bank(meta, topic["interview"]), encoding="utf-8", newline="\n")

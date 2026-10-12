"""Helpers to assemble D04 topic dicts with consistent section shape."""

from __future__ import annotations


def A(*parts: str) -> str:
    if len(parts) < 4:
        raise ValueError("interview answers need at least four sentences")
    return " ".join(p.strip() for p in parts if p.strip())


def iv(level_items: list[tuple[str, str, str]]) -> dict:
    """Build interview dict from (question, answer, bank_short) tuples grouped by caller."""
    return level_items


def ex_block(items: list[tuple[str, str]]) -> tuple[str, list[dict], list[dict]]:
    """Return exercises_section markdown, exercises list, solutions list."""
    section_lines = []
    exercises: list[dict] = []
    solutions: list[dict] = []
    for i, (title_body, acceptance) in enumerate(items, 1):
        kind = "implementation" if i == 1 else ("debugging" if i == 2 else "trade-off")
        section_lines.append(f"### Exercise {i} — {kind}")
        section_lines.append("")
        section_lines.append(title_body)
        section_lines.append("")
        section_lines.append(f"Acceptance: {acceptance}")
        section_lines.append("")
        exercises.append({"prompt": f"{title_body} Acceptance: {acceptance}"})
        solutions.append(f"See topic note exercise {i}. {acceptance}")
    return "\n".join(section_lines), exercises, solutions


def make_topic(
    *,
    id: str,
    name: str,
    subdomain: str,
    note_path: str,
    importance: str,
    complexity: str,
    deps: list[str],
    overview: list[str],
    first_principles: list[str],
    internal: list[str],
    mermaid: str,
    diagram_caption: str,
    examples: list[str],
    code_intro: str,
    code: str,
    code_footer: str,
    practical: list[str],
    tradeoffs_table: str,
    mistakes: str,
    debugging: list[str],
    interview_levels: dict[str, list[dict]],
    exercise_triplet: list[tuple[str, str]],
    solution_bodies: list[str],
    revision: str,
    related: str,
    completion: str,
) -> dict:
    ex_section, exercises, _ = ex_block(exercise_triplet)
    return {
        "meta": {
            "id": id,
            "name": name,
            "subdomain": subdomain,
            "note_path": note_path,
            "importance": importance,
            "complexity": complexity,
            "deps_display": ", ".join(f"`{d}`" for d in deps) if deps else "none",
        },
        "overview": overview,
        "first_principles": first_principles,
        "internal": internal,
        "mermaid": mermaid,
        "diagram_caption": diagram_caption,
        "examples": examples,
        "code_intro": code_intro,
        "code": code,
        "code_footer": code_footer,
        "practical": practical,
        "tradeoffs_table": tradeoffs_table,
        "mistakes": mistakes,
        "debugging": debugging,
        "interview": interview_levels,
        "exercises_section": ex_section,
        "exercises": exercises,
        "solutions": solution_bodies,
        "revision": revision,
        "related": related,
        "completion": completion,
    }


def q(level: str, question: str, answer: str, bank: str) -> dict:
    return {"q": question, "a": answer, "bank": bank, "_level": level}

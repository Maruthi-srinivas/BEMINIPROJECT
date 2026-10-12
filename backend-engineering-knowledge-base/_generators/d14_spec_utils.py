"""Utilities to define D14 topic specs with consistent shape."""

from __future__ import annotations

from d14_helpers import DEFAULT_CODE, completion, mistakes, paragraphs, qa, tradeoffs


def interview_from_levels(
    beginner: list,
    intermediate: list,
    advanced: list,
    scenarios: list,
    follow_ups: list,
) -> dict:
    def conv(items):
        out = []
        for item in items:
            if len(item) == 2:
                q, sents = item
                bank = None
            else:
                q, sents, bank = item
            if isinstance(sents, str):
                out.append({"q": q, "a": sents, "bank": bank or q})
            else:
                out.append(qa(q, sents, bank))
        return out

    return {
        "beginner": conv(beginner),
        "intermediate": conv(intermediate),
        "advanced": conv(advanced),
        "scenarios": conv(scenarios),
        "follow_ups": conv(follow_ups),
    }


def spec(
    *,
    overview: list[str],
    first_principles: list[str],
    internal: list[str],
    mermaid: str,
    examples: list[str],
    practical: list[str],
    trade_rows: list[tuple[str, str, str, str, str]],
    mistake_list: list[str],
    debugging: list[str],
    interview: dict,
    ex1_section: str,
    ex2_section: str,
    ex3_section: str,
    ex1_prompt: str,
    ex2_prompt: str,
    ex3_prompt: str,
    ex1_solution: str,
    ex2_solution: str,
    ex3_solution: str,
    revision: str,
    related: str,
    completion: str,
    code: str | None = None,
    code_intro: str | None = None,
    code_footer: str | None = None,
    diagram_caption: str | None = None,
) -> dict:
    return {
        "overview": overview,
        "first_principles": first_principles,
        "internal": internal,
        "mermaid": mermaid,
        "diagram_caption": diagram_caption or "",
        "examples": examples,
        "practical": practical,
        "tradeoffs_table": tradeoffs(*trade_rows),
        "mistakes": mistakes(*mistake_list),
        "debugging": debugging,
        "interview": interview,
        "ex1_section": ex1_section,
        "ex2_section": ex2_section,
        "ex3_section": ex3_section,
        "ex1_prompt": ex1_prompt,
        "ex2_prompt": ex2_prompt,
        "ex3_prompt": ex3_prompt,
        "ex1_solution": ex1_solution,
        "ex2_solution": ex2_solution,
        "ex3_solution": ex3_solution,
        "revision": revision,
        "related": related,
        "completion": completion,
        "code": code or DEFAULT_CODE,
        "code_intro": code_intro,
        "code_footer": code_footer,
    }


def sent(*parts: str) -> tuple[str, ...]:
    return tuple(p.strip() for p in parts if p.strip())

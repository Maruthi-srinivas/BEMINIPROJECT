"""Shared builders for D07 topic bodies."""
from __future__ import annotations

from typing import Any


def interview_block(
    beginner: list[tuple[str, str]],
    intermediate: list[tuple[str, str]],
    advanced: list[tuple[str, str]],
    scenarios: list[tuple[str, str]],
    followups: list[tuple[str, str]],
) -> str:
    assert len(beginner) == 5 and len(intermediate) == 5 and len(advanced) == 5
    assert len(scenarios) == 5 and len(followups) == 3

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
            section("Beginner", beginner),
            section("Intermediate", intermediate),
            section("Advanced", advanced),
            section("Scenarios", scenarios),
            section("Follow-ups", followups),
        ]
    )


def sql_block(title: str, sql: str) -> str:
    return f"""Illustrative SQL ({title}). Not executed in this repository.

```sql
{sql.strip()}
```

Read the statements as teaching examples. Bind parameters in application code; do not concatenate user input into these patterns."""


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {x}" for x in items)


def mk_body(**kwargs: Any) -> dict[str, Any]:
    required = {
        "overview",
        "first_principles",
        "internal",
        "mermaid",
        "examples",
        "sql_title",
        "sql",
        "practical",
        "tradeoffs",
        "mistakes",
        "debugging",
        "beginner",
        "intermediate",
        "advanced",
        "scenarios",
        "followups",
        "exercises",
        "exercise_items",
        "solutions",
        "bank_questions",
        "revision",
        "completion",
    }
    missing = required - set(kwargs)
    if missing:
        raise KeyError(f"missing fields: {missing}")

    body = dict(kwargs)
    body["code_section"] = sql_block(kwargs["sql_title"], kwargs["sql"])
    body["interview"] = interview_block(
        kwargs["beginner"],
        kwargs["intermediate"],
        kwargs["advanced"],
        kwargs["scenarios"],
        kwargs["followups"],
    )
    return body


def fact_block(*lines: str) -> list[str]:
    return list(lines)


def bank_from_sections(
    beginner: list[tuple[str, str]],
    intermediate: list[tuple[str, str]],
    advanced: list[tuple[str, str]],
    scenarios: list[tuple[str, str]],
    followups: list[tuple[str, str]],
) -> list[str]:
    out: list[str] = []
    for label, items in [
        ("Beginner", beginner),
        ("Intermediate", intermediate),
        ("Advanced", advanced),
        ("Scenario", scenarios),
        ("Follow-up", followups),
    ]:
        for q, _ in items:
            out.append(f"{label}. {q}")
    return out

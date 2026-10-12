"""Shared builders for D14 topic packages."""

from __future__ import annotations

from textwrap import dedent


def paragraphs(*parts: str) -> list[str]:
    return [p.strip() for p in parts if p and p.strip()]


def answer(*sentences: str) -> str:
    s = [x.strip() for x in sentences if x.strip()]
    pad = (
        "In backend interviews, connect the mechanism to consumer lag, duplicate side effects, "
        "or broker failure modes instead of treating messaging as fire-and-forget."
    )
    while len(s) < 4:
        s.append(pad)
    return " ".join(s)


def qa(q: str, sentences: tuple[str, ...], bank: str | None = None) -> dict:
    return {"q": q, "a": answer(*sentences), "bank": bank or q}


def interview_pack(
    beginner: list[dict],
    intermediate: list[dict],
    advanced: list[dict],
    scenarios: list[dict],
    followups: list[dict],
) -> dict:
    return {
        "beginner": beginner,
        "intermediate": intermediate,
        "advanced": advanced,
        "scenarios": scenarios,
        "follow_ups": followups,
    }


TRADE_TABLE = dedent(
    """
| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| {row1} |
| {row2} |
| {row3} |
| {row4} |
"""
).strip()


def tradeoffs(*rows: tuple[str, str, str, str, str]) -> str:
    lines = [
        "| Choice | Benefit | Cost | Choose when | Avoid when |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def mistakes(*items: str) -> str:
    return "\n".join(f"- {i.strip()}" for i in items)


def ex_section(e1: str, e2: str, e3: str) -> str:
    return dedent(
        f"""
### Exercise 1 — implementation

{e1}

### Exercise 2 — debugging

{e2}

### Exercise 3 — trade-off

{e3}
"""
    ).strip()


def completion(*bullets: str) -> str:
    return "\n".join(f"- {b.strip()}" for b in bullets)


DEFAULT_CODE = dedent(
    """
def dedupe_processed(event_id: str, seen: set[str]) -> bool:
    \"\"\"Return True if this event_id was already applied (idempotent consumer sketch).\"\"\"
    if event_id in seen:
        return False
    seen.add(event_id)
    return True


if __name__ == "__main__":
    processed: set[str] = set()
    assert dedupe_processed("evt-1", processed) is True
    assert dedupe_processed("evt-1", processed) is False
    print("ok")
"""
).strip()

"""Reusable markdown blocks for D04 topics."""

TRADEOFF_HEADER = """| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |"""


def tradeoffs(*rows: tuple[str, str, str, str, str]) -> str:
    lines = [TRADEOFF_HEADER]
    for r in rows:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def bullets(*items: str) -> str:
    return "\n".join(f"- {i}" for i in items)


def revision(*items: str) -> str:
    return "\n".join(f"- {i}" for i in items)

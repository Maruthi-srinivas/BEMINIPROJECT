def bank(beginner, intermediate, advanced, scenarios, followups):
    return {
        "beginner": beginner,
        "intermediate": intermediate,
        "advanced": advanced,
        "scenarios": scenarios,
        "followups": followups,
    }


def std_tradeoffs(rows):
    from gen_d03_bulk import table  # circular if imported at runtime only inside build

    lines = [
        "| Choice | Benefit | Cost | Choose when | Avoid when |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def bullets(items):
    return "\n".join(f"- {x}" for x in items)

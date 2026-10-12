"""Shared helpers for D18 topic generators (no imports from generate_d18_domain)."""
from __future__ import annotations


def ans(*sentences: str) -> str:
    s = [x.strip() for x in sentences if x.strip()]
    pad = (
        "In production services, the trade-off shows up in testability, deploy risk, and how often "
        "teams touch the same class during incidents."
    )
    while len(s) < 4:
        s.append(pad)
    return " ".join(s)


def mk_interview(questions: list[tuple[str, str, str]]) -> dict:
    """(level, short_bank_q, long_answer) -> grouped dict."""
    groups = {
        "beginner": [],
        "intermediate": [],
        "advanced": [],
        "scenarios": [],
        "follow_ups": [],
    }
    limits = [("beginner", 5), ("intermediate", 5), ("advanced", 5), ("scenarios", 5), ("follow_ups", 3)]
    idx = 0
    for key, count in limits:
        for _ in range(count):
            level, bank, answer = questions[idx]
            groups[key].append({"q": bank, "a": answer, "bank": bank})
            idx += 1
    return groups

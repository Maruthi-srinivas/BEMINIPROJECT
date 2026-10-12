# Part 1: D15-T001 .. D15-T008 topic payloads (imported by d15_topics.py)
from __future__ import annotations

from typing import Any

def iq(*pairs: tuple[str, str]) -> list[tuple[str, str]]:
    return list(pairs)


def base_interview(
    b: list[tuple[str, str]],
    i: list[tuple[str, str]],
    a: list[tuple[str, str]],
    s: list[tuple[str, str]],
    f: list[tuple[str, str]],
) -> dict[str, list[tuple[str, str]]]:
    assert len(b) == 5 and len(i) == 5 and len(a) == 5 and len(s) == 5 and len(f) == 3
    return {"beginner": b, "intermediate": i, "advanced": a, "scenarios": s, "followups": f}


PART1: list[dict[str, Any]] = []

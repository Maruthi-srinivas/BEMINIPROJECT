"""Shared helpers to build D15 topic dicts."""
from __future__ import annotations

from typing import Any


def iq(*pairs: tuple[str, str]) -> list[tuple[str, str]]:
    return list(pairs)


def interview_pack(
    b: list[tuple[str, str]],
    i: list[tuple[str, str]],
    a: list[tuple[str, str]],
    s: list[tuple[str, str]],
    f: list[tuple[str, str]],
) -> dict[str, list[tuple[str, str]]]:
    assert len(b) == 5 and len(i) == 5 and len(a) == 5 and len(s) == 5 and len(f) == 3
    return {"beginner": b, "intermediate": i, "advanced": a, "scenarios": s, "followups": f}


def T(**kwargs: Any) -> dict[str, Any]:
    defaults: dict[str, Any] = {
        "importance": "core",
        "code_run": "unexecuted",
        "related": [],
        "confused_with": [],
        "diagram_caption": "Read the diagram as a causal flow from client action to stored or observed outcome, including failure branches.",
        "tradeoffs_narrative": "Under load, the cheap choice on paper becomes the choice that amplifies retries, stale reads, or operator toil. Measure p99 latency and error budgets, not only happy-path throughput.",
        "misconceptions_close": "A weak interview answer names a buzzword without a failure story. A strong answer names what breaks, what users see, and what invariant you still enforce.",
        "code_notes": "The snippet models control flow you would embed in a service or test harness. It is not a production client library.",
    }
    defaults.update(kwargs)
    required = [
        "id",
        "slug",
        "name",
        "subdomain",
        "deps",
        "overview",
        "principles",
        "architecture",
        "mermaid",
        "examples",
        "code_file",
        "code",
        "backend",
        "tradeoffs_table",
        "mistakes",
        "debug",
        "revision",
        "flashcards",
        "completion",
        "interview",
        "ex1",
        "ex2",
        "ex3",
        "ex1_short",
        "ex2_short",
        "ex3_short",
        "sol1",
        "sol2",
        "sol3",
    ]
    for key in required:
        if key not in defaults:
            raise KeyError(f"missing {key} in {defaults.get('id')}")
    return defaults

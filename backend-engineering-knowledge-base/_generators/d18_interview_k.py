"""Render section K markdown for D18 topics (mirrors d18_topic_data._iq + d18_helpers)."""
from __future__ import annotations

from d18_helpers import ans, mk_interview
from d18_topic_data import _iq  # noqa: PLC2701


def render_section_k(name: str, seed: str) -> str:
    interview = mk_interview(_iq(name, seed))
    parts = ["## K. Interview Preparation\n"]
    for level, count, label in [
        ("beginner", 5, "Beginner"),
        ("intermediate", 5, "Intermediate"),
        ("advanced", 5, "Advanced"),
        ("scenarios", 5, "Scenarios"),
        ("follow_ups", 3, "Follow-ups"),
    ]:
        parts.append(f"### {label}\n")
        for i, item in enumerate(interview[level][:count], 1):
            parts.append(f"#### Q{i}. {item['q']}\n\n**Answer:** {item['a']}\n")
    return "\n".join(parts)

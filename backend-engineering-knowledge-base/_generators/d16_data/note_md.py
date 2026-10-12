# ruff: noqa: E501
"""Render markdown for a D16 topic without importing assembled TOPICS (for offline file writes)."""

from __future__ import annotations

from d16_data.assembler import assemble
from d16_render import (
    render_exercise_file,
    render_interview_bank,
    render_note,
    render_solution_file,
)


def package_for_row(inv_row: dict) -> dict:
    from d16_data.assembler import assemble

    return assemble(inv_row)


def render_all(inv_row: dict) -> dict[str, str]:
    topic = package_for_row(inv_row)
    meta = topic["meta"]
    return {
        "note": render_note(topic),
        "exercise": render_exercise_file(meta, topic["exercises"]),
        "solution": render_solution_file(meta, topic["solutions"]),
        "interview": render_interview_bank(meta, topic["interview"]),
        "id": meta["id"],
        "note_path": meta["note_path"],
    }

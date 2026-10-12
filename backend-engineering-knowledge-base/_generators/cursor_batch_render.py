"""Render helpers for manual/cursor batch writes (mirrors generate_d24_d27_batch)."""
from __future__ import annotations

# Re-export everything needed to render one topic
from generate_d24_d27_batch import (  # noqa: F401
    build_body,
    build_note,
    classify,
    interview_question_lists,
    load_topics,
    slug_from_path,
)
from d24_d27_write_helper import render_satellites  # noqa: F401

SKIP_NOTE_PATH = "23_KUBERNETES_AND_CLOUD/notes/d24-t001-kubernetes-architecture.md"


def files_for_topic(t: dict) -> dict[str, str]:
    body = build_body(t)
    out = render_satellites(t, body)
    if t["note_path"] != SKIP_NOTE_PATH:
        out[t["note_path"]] = build_note(t, body)
    return out

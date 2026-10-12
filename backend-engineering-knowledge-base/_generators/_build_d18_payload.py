#!/usr/bin/env python3
"""Build JSON payload for D18-T002..T028 (path relative to KB root)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "_generators"
sys.path.insert(0, str(GEN))

from generate_d18_domain import (  # noqa: E402
    load_inventory_topics,
    render_bank,
    render_exercise,
    render_note,
    render_solutions,
)
from d18_topic_data import TOPICS  # noqa: E402

OUT = GEN / "d18_payload_t002_t028.json"
SKIP = {"D18-T001"}


def main() -> None:
    inv = load_inventory_topics()
    payload: list[dict[str, str]] = []
    for topic in TOPICS:
        tid = topic["meta"]["id"]
        if tid in SKIP:
            continue
        if tid not in inv:
            continue
        inv_row = inv[tid]
        topic["meta"]["note_path"] = inv_row["note_path"]
        topic["meta"]["subdomain"] = inv_row["subdomain"]
        topic["meta"]["name"] = inv_row["name"]
        topic["meta"]["dependencies"] = inv_row.get("dependencies", [])
        m = topic["meta"]
        payload.append({"path": m["note_path"], "content": render_note(topic)})
        payload.append(
            {"path": f"EXERCISES/{tid}.md", "content": render_exercise(m, topic["exercise_prompts"])}
        )
        payload.append(
            {
                "path": f"EXERCISES/solutions/{tid}.md",
                "content": render_solutions(m, topic["exercise_solutions"]),
            }
        )
        payload.append(
            {"path": f"INTERVIEW_BANK/items/{tid}.md", "content": render_bank(m, topic["interview"])}
        )
    OUT.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    print(len(payload), "entries ->", OUT)


if __name__ == "__main__":
    main()

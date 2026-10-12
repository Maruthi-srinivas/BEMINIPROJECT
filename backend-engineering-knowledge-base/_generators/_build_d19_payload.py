#!/usr/bin/env python3
"""Build JSON payload of all D19 writes (path relative to KB root)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_generators"))

from d19_build_topics import build_topic  # noqa: E402
from d19_render import (  # noqa: E402
    render_exercise_file,
    render_interview_bank,
    render_note,
    render_solution_file,
)
from d19_topic_specs import TOPIC_SPECS  # noqa: E402

INV_PATH = ROOT / "00_INDEX" / "inventory.json"
OUT = Path(__file__).resolve().parent / "d19_payload.json"


def main() -> None:
    data = json.loads(INV_PATH.read_text(encoding="utf-8"))
    topics = sorted(
        [t for t in data["topics"] if t["id"].startswith("D19-T")],
        key=lambda t: t["id"],
    )
    payload: list[dict[str, str]] = []
    for inv in topics:
        tid = inv["id"]
        if tid not in TOPIC_SPECS:
            continue
        package = build_topic(inv)
        meta = package["meta"]
        payload.append({"path": meta["note_path"], "content": render_note(package)})
        payload.append(
            {
                "path": f"EXERCISES/{tid}.md",
                "content": render_exercise_file(meta, package["exercises"]),
            }
        )
        payload.append(
            {
                "path": f"EXERCISES/solutions/{tid}.md",
                "content": render_solution_file(meta, package["solutions"]),
            }
        )
        payload.append(
            {
                "path": f"INTERVIEW_BANK/items/{tid}.md",
                "content": render_interview_bank(meta, package["interview"]),
            }
        )
    OUT.write_text(json.dumps(payload), encoding="utf-8")
    print(len(payload), "entries ->", OUT)


if __name__ == "__main__":
    main()

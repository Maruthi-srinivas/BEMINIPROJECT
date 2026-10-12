#!/usr/bin/env python3
"""Write all D19 packages to disk (same as emit script). Safe to run locally."""
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


def main() -> int:
    data = json.loads(INV_PATH.read_text(encoding="utf-8"))
    topics = sorted(
        [t for t in data["topics"] if t["id"].startswith("D19-T")],
        key=lambda t: t["id"],
    )
    finished: list[str] = []
    failures: list[str] = []
    for inv in topics:
        tid = inv["id"]
        try:
            if tid not in TOPIC_SPECS:
                raise KeyError(f"no spec for {tid}")
            package = build_topic(inv)
            meta = package["meta"]
            note_path = ROOT / meta["note_path"]
            note_path.parent.mkdir(parents=True, exist_ok=True)
            note_path.write_text(render_note(package), encoding="utf-8")
            (ROOT / "EXERCISES" / f"{tid}.md").write_text(
                render_exercise_file(meta, package["exercises"]), encoding="utf-8"
            )
            (ROOT / "EXERCISES" / "solutions" / f"{tid}.md").write_text(
                render_solution_file(meta, package["solutions"]), encoding="utf-8"
            )
            (ROOT / "INTERVIEW_BANK" / "items" / f"{tid}.md").write_text(
                render_interview_bank(meta, package["interview"]), encoding="utf-8"
            )
            finished.append(tid)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{tid}: {exc}")
    print("FINISHED:", ", ".join(finished))
    if failures:
        print("FAILURES:", "; ".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

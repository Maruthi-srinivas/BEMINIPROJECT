#!/usr/bin/env python3
"""Write D19, D21, and D22 topic packages (notes, exercises, solutions, interview bank).

Run from this directory:
  python materialize_d19_d21_d22.py

Does not modify inventory.json. Skips notes that already contain '## O. Completion Criteria'.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "_generators"))

from d19_build_topics import build_topic  # noqa: E402
from d19_render import (  # noqa: E402
    render_exercise_file,
    render_interview_bank,
    render_note,
    render_solution_file,
)
from d19_topic_specs import TOPIC_SPECS  # noqa: E402
from generate_d21_d22_d23 import (  # noqa: E402
    build_note,
    expand_seed,
    load_topics,
    write_exercise,
    write_interview_item,
    write_solution,
)
from d21_d22_d23_seeds import SEEDS  # noqa: E402

INV = ROOT / "00_INDEX" / "inventory.json"
MARKER = "## O. Completion Criteria"


def note_complete(note_path: Path) -> bool:
    if not note_path.is_file():
        return False
    return MARKER in note_path.read_text(encoding="utf-8")


def emit_d19() -> tuple[list[str], list[str]]:
    data = json.loads(INV.read_text(encoding="utf-8"))
    topics = sorted([t for t in data["topics"] if t["id"].startswith("D19-T")], key=lambda t: t["id"])
    finished: list[str] = []
    skipped: list[str] = []
    for inv in topics:
        tid = inv["id"]
        note_path = ROOT / inv["note_path"]
        if note_complete(note_path):
            skipped.append(tid)
            continue
        if tid not in TOPIC_SPECS:
            raise KeyError(f"no D19 spec for {tid}")
        package = build_topic(inv)
        meta = package["meta"]
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
    return finished, skipped


def emit_d21_d22() -> tuple[list[str], list[str]]:
    topics = load_topics(("D21-T", "D22-T"))
    finished: list[str] = []
    skipped: list[str] = []
    for topic in topics:
        tid = topic["id"]
        note_path = ROOT / topic["note_path"]
        if note_complete(note_path):
            skipped.append(tid)
            continue
        if tid not in SEEDS:
            raise KeyError(f"no seed for {tid}")
        body = expand_seed(SEEDS[tid], topic)
        note_path.parent.mkdir(parents=True, exist_ok=True)
        note_path.write_text(build_note(topic, body), encoding="utf-8")
        (ROOT / "EXERCISES" / f"{tid}.md").write_text(
            write_exercise(tid, body["exercises"]), encoding="utf-8"
        )
        (ROOT / "EXERCISES" / "solutions" / f"{tid}.md").write_text(
            write_solution(tid, body["solutions"]), encoding="utf-8"
        )
        (ROOT / "INTERVIEW_BANK" / "items" / f"{tid}.md").write_text(
            write_interview_item(topic, body["interview"]), encoding="utf-8"
        )
        finished.append(tid)
    return finished, skipped


def main() -> int:
    d19_done, d19_skip = emit_d19()
    d21_done, d21_skip = emit_d21_d22()
    finished = d19_done + d21_done
    skipped = d19_skip + d21_skip
    print("FINISHED:", ",".join(finished))
    print("SKIPPED:", ",".join(skipped))
    print("COUNT_FINISHED:", len(finished))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

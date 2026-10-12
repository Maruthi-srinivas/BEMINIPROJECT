"""Write D13-T003..T022 artifacts to disk. Run: python scripts/d13_write_topics_003_022.py"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.d13_materialize_writes import (  # noqa: E402
    build_exercise,
    build_interview,
    build_note,
    build_solution,
    collect_gen_payloads,
    load_inventory_meta,
)


def main() -> None:
    meta = load_inventory_meta()
    payloads = collect_gen_payloads()
    finished: list[str] = []
    for tid in sorted(payloads.keys()):
        if tid not in meta:
            continue
        m = meta[tid]
        p = payloads[tid]
        note_path = ROOT / m["note_path"]
        note_path.parent.mkdir(parents=True, exist_ok=True)
        note_path.write_text(build_note(m, p), encoding="utf-8")
        (ROOT / "EXERCISES" / f"{tid}.md").write_text(build_exercise(tid, p), encoding="utf-8")
        (ROOT / "EXERCISES" / "solutions" / f"{tid}.md").write_text(
            build_solution(tid, p), encoding="utf-8"
        )
        (ROOT / "INTERVIEW_BANK" / "items" / f"{tid}.md").write_text(
            build_interview(m, p), encoding="utf-8"
        )
        ex = ROOT / "EXERCISES" / "examples" / p["code_file"]
        ex.parent.mkdir(parents=True, exist_ok=True)
        ex.write_text(p["code"].strip() + "\n", encoding="utf-8")
        finished.append(tid)
    print(json.dumps({"finished": finished}))


if __name__ == "__main__":
    main()

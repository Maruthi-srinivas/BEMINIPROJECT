"""Write D16-T001..T033 artifacts using existing assembler/render (run locally if needed)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

GEN = Path(__file__).resolve().parent
KB = GEN.parent
sys.path.insert(0, str(GEN))

from d16_data.note_md import render_all  # noqa: E402


def main() -> int:
    inv = json.loads((KB / "00_INDEX" / "inventory.json").read_text(encoding="utf-8"))
    rows = sorted(
        (t for t in inv["topics"] if t["id"].startswith("D16-T")),
        key=lambda r: r["id"],
    )
    finished: list[str] = []
    failures: list[str] = []
    for row in rows:
        tid = row["id"]
        try:
            out = render_all(row)
            note_path = KB / out["note_path"]
            note_path.parent.mkdir(parents=True, exist_ok=True)
            note_path.write_text(out["note"], encoding="utf-8", newline="\n")
            (KB / "EXERCISES" / f"{tid}.md").write_text(
                out["exercise"], encoding="utf-8", newline="\n"
            )
            (KB / "EXERCISES" / "solutions" / f"{tid}.md").write_text(
                out["solution"], encoding="utf-8", newline="\n"
            )
            (KB / "INTERVIEW_BANK" / "items" / f"{tid}.md").write_text(
                out["interview"], encoding="utf-8", newline="\n"
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

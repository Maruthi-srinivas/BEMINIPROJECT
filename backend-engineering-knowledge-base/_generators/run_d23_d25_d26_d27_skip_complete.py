#!/usr/bin/env python3
"""Generate D23, D25, D26, D27 artifacts; skip notes that already have section O."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "00_INDEX" / "inventory.json"
GEN = Path(__file__).resolve().parent
sys.path.insert(0, str(GEN))


def is_complete(topic: dict) -> bool:
    path = ROOT / topic["note_path"]
    if not path.is_file():
        return False
    return "## O. Completion Criteria" in path.read_text(encoding="utf-8")


def load_topics(domain_numbers: tuple[int, ...]) -> list[dict]:
    data = json.loads(INV.read_text(encoding="utf-8"))
    out = [t for t in data["topics"] if t["domain_number"] in domain_numbers]
    out.sort(key=lambda t: (t["domain_number"], int(t["id"].split("-T")[1])))
    return out


def main() -> int:
    from d21_d22_d23_seeds import SEEDS
    from generate_d21_d22_d23 import (
        build_note,
        expand_seed,
        write_exercise,
        write_interview_item,
        write_solution,
    )
    from generate_d24_d27_batch import write_topic

    finished: list[str] = []
    skipped: list[str] = []
    failures: list[str] = []

    for t in load_topics((23,)):
        tid = t["id"]
        if is_complete(t):
            skipped.append(tid)
            continue
        try:
            if tid not in SEEDS:
                raise KeyError(f"no seed for {tid}")
            body = expand_seed(SEEDS[tid], t)
            note_path = ROOT / t["note_path"]
            note_path.parent.mkdir(parents=True, exist_ok=True)
            note_path.write_text(build_note(t, body), encoding="utf-8")
            (ROOT / "EXERCISES" / f"{tid}.md").write_text(
                write_exercise(tid, body["exercises"]), encoding="utf-8"
            )
            (ROOT / "EXERCISES" / "solutions" / f"{tid}.md").write_text(
                write_solution(tid, body["solutions"]), encoding="utf-8"
            )
            (ROOT / "INTERVIEW_BANK" / "items" / f"{tid}.md").write_text(
                write_interview_item(t, body["interview"]), encoding="utf-8"
            )
            finished.append(tid)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{tid}: {exc}")

    for t in load_topics((25, 26, 27)):
        tid = t["id"]
        if is_complete(t):
            skipped.append(tid)
            continue
        try:
            write_topic(t)
            finished.append(tid)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{tid}: {exc}")

    print("FINISHED:", ",".join(finished))
    print("COUNT:", len(finished))
    if skipped:
        print("SKIPPED:", ",".join(skipped))
    if failures:
        print("FAILURES:", "; ".join(failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

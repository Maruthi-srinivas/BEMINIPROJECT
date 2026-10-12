#!/usr/bin/env python3
"""Generate D14-T001..D14-T032 knowledge-base artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV_PATH = ROOT / "00_INDEX" / "inventory.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))

from d14_factory import build_topic_packages  # noqa: E402
from d14_render import write_topic_package  # noqa: E402


def load_d14_inventory() -> list[dict]:
    data = json.loads(INV_PATH.read_text(encoding="utf-8"))
    topics = [t for t in data["topics"] if t["id"].startswith("D14-T")]
    topics.sort(key=lambda t: t["id"])
    return topics


def main() -> None:
    inv = load_d14_inventory()
    packages = build_topic_packages(inv)
    finished: list[str] = []
    failures: list[str] = []
    for pkg in packages:
        tid = pkg["meta"]["id"]
        try:
            write_topic_package(pkg)
            finished.append(tid)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{tid}: {exc}")
    print("FINISHED:", ",".join(finished))
    print("FAILURES:", ",".join(failures) if failures else "none")


def export_all(base: Path | None = None) -> tuple[list[str], list[str]]:
    """Write all D14 packages; returns (finished, failures)."""
    root = base or ROOT
    inv = load_d14_inventory()
    packages = build_topic_packages(inv)
    finished: list[str] = []
    failures: list[str] = []
    for pkg in packages:
        tid = pkg["meta"]["id"]
        try:
            meta = pkg["meta"]
            from d14_render import (  # noqa: WPS433
                render_exercise_file,
                render_interview_bank,
                render_note,
                render_solution_file,
            )

            note_path = root / meta["note_path"]
            note_path.parent.mkdir(parents=True, exist_ok=True)
            note_path.write_text(render_note(pkg), encoding="utf-8")
            (root / "EXERCISES" / f"{tid}.md").write_text(
                render_exercise_file(meta, pkg["exercises"]), encoding="utf-8"
            )
            (root / "EXERCISES" / "solutions" / f"{tid}.md").write_text(
                render_solution_file(meta, pkg["solutions"]), encoding="utf-8"
            )
            (root / "INTERVIEW_BANK" / "items" / f"{tid}.md").write_text(
                render_interview_bank(meta, pkg["interview"]), encoding="utf-8"
            )
            finished.append(tid)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{tid}: {exc}")
    return finished, failures


if __name__ == "__main__":
    main()

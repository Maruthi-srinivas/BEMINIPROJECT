"""Materialize D14-T004..D14-T032 topic packages. Run from this directory: python d14_materialize_t004_t032.py"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from d14_factory import build_topic_packages
from d14_render import write_topic_package

KB = Path(__file__).resolve().parents[1]
TARGET = {f"D14-T{i:03d}" for i in range(4, 33)}


def main() -> None:
    inv = json.loads((KB / "00_INDEX" / "inventory.json").read_text(encoding="utf-8"))
    rows = [t for t in inv["topics"] if t["id"] in TARGET]
    rows.sort(key=lambda r: r["id"])
    finished: list[str] = []
    failures: list[str] = []
    for pkg in build_topic_packages(rows):
        try:
            write_topic_package(pkg)
            finished.append(pkg["meta"]["id"])
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{pkg['meta']['id']}: {exc}")
    print("FINISHED:", ",".join(finished))
    print("FAILURES:", ";".join(failures) if failures else "none")


if __name__ == "__main__":
    main()

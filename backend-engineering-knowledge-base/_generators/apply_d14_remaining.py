#!/usr/bin/env python3
"""Write D14-T003..D14-T032 artifacts (skip T001-T002 if present). Run from repo when shell works."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from d14_factory import build_topic_packages  # noqa: E402
from d14_render import write_topic_package  # noqa: E402
from generate_d14_domain import load_d14_inventory  # noqa: E402

SKIP = {"D14-T001", "D14-T002"}


def main() -> None:
    finished: list[str] = []
    failures: list[str] = []
    for pkg in build_topic_packages(load_d14_inventory()):
        tid = pkg["meta"]["id"]
        if tid in SKIP:
            finished.append(tid)
            continue
        try:
            write_topic_package(pkg)
            finished.append(tid)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{tid}: {exc}")
    print("FINISHED:", ",".join(finished))
    print("FAILURES:", ",".join(failures) if failures else "none")


if __name__ == "__main__":
    main()

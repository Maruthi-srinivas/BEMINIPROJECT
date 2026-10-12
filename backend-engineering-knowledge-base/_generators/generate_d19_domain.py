#!/usr/bin/env python3
"""Generate D19 Microservices notes, exercises, solutions, and interview bank items."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from d19_build_topics import build_topic  # noqa: E402
from d19_render import write_topic_package  # noqa: E402
from d19_topic_specs import TOPIC_SPECS  # noqa: E402

INV_PATH = ROOT / "00_INDEX" / "inventory.json"


def load_d19_topics() -> list[dict]:
    data = json.loads(INV_PATH.read_text(encoding="utf-8"))
    topics = [t for t in data["topics"] if t["id"].startswith("D19-T")]
    topics.sort(key=lambda t: t["id"])
    return topics


def main() -> int:
    inv_topics = load_d19_topics()
    finished: list[str] = []
    failures: list[str] = []

    for inv in inv_topics:
        tid = inv["id"]
        try:
            if tid not in TOPIC_SPECS:
                raise KeyError(f"no spec for {tid}")
            package = build_topic(inv)
            write_topic_package(package)
            finished.append(tid)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{tid}: {exc}")

    print("FINISHED:", ", ".join(finished))
    if failures:
        print("FAILURES:", "; ".join(failures))
        return 1
    print(f"Wrote {len(finished)} topic packages ({len(finished) * 4} files).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

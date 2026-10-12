"""Generate D16-T001..D16-T033 knowledge-base artifacts.

Run from repository root:

    python backend-engineering-knowledge-base/_generators/build_d16_notes.py
"""

from __future__ import annotations

import sys
from pathlib import Path

GEN = Path(__file__).resolve().parent
sys.path.insert(0, str(GEN))

from d16_data import TOPICS  # noqa: E402
from d16_render import write_topic_package  # noqa: E402


def main() -> int:
    finished: list[str] = []
    failures: list[str] = []
    for topic in TOPICS:
        tid = topic["meta"]["id"]
        try:
            write_topic_package(topic)
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

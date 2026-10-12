"""Emit all D04 packages (notes, exercises, solutions, interview bank).

Run from repository root:

    python backend-engineering-knowledge-base/_generators/emit_all_d04.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from d04_data.batch1 import topic_001  # noqa: E402
from d04_data.all_topics import TOPICS  # noqa: E402
from d04_render import write_topic_package  # noqa: E402


def main() -> int:
    finished: list[str] = []
    failures: list[str] = []
    for topic in [topic_001(), *TOPICS]:
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

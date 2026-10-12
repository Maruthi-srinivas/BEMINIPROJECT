#!/usr/bin/env python3
"""Emit D15-T001..T034 knowledge-base artifacts. Run from repo root."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_generators"))

from d15_emit_core import ensure_dirs, write_topic  # noqa: E402
from d15_all_topics import TOPICS  # noqa: E402


def main() -> None:
    ensure_dirs()
    ok: list[str] = []
    fail: list[str] = []
    for t in TOPICS:
        try:
            write_topic(t)
            ok.append(t["id"])
            print("wrote", t["id"])
        except Exception as exc:  # noqa: BLE001
            fail.append(f"{t['id']}: {exc}")
            print("FAIL", t["id"], exc)
    print("FINISHED", len(ok), "failures", len(fail))
    for f in fail:
        print(f)


if __name__ == "__main__":
    main()

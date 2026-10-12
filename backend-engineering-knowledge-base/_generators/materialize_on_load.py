"""Write all D15-T001..T034 artifacts from generator data.

Usage (from backend-engineering-knowledge-base):
    python _generators/materialize_on_load.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_generators"))

from d15_all_topics import TOPICS
from d15_emit_core import ensure_dirs, write_topic


def materialize() -> tuple[list[str], list[str]]:
    ensure_dirs()
    ok: list[str] = []
    fail: list[str] = []
    for t in TOPICS:
        try:
            write_topic(t)
            ok.append(t["id"])
        except Exception as exc:  # noqa: BLE001
            fail.append(f"{t['id']}: {exc}")
    return ok, fail


if __name__ == "__main__":
    finished, failures = materialize()
    print("FINISHED", finished)
    print("FAILURES", failures)

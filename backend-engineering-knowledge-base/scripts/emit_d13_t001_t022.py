#!/usr/bin/env python3
"""Emit D13-T001..T022 knowledge-base artifacts. Run from backend-engineering-knowledge-base/."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def write(rel: str, text: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


import sys

sys.path.insert(0, str(ROOT))
from scripts.d13_topic_bundles import BUNDLES  # noqa: E402

def main() -> None:
    ok: list[str] = []
    fail: list[str] = []
    for tid, b in BUNDLES.items():
        try:
            write(b["note_path"], b["note"])
            write(f"EXERCISES/{tid}.md", b["exercises"])
            write(f"EXERCISES/solutions/{tid}.md", b["solutions"])
            write(f"INTERVIEW_BANK/items/{tid}.md", b["interview"])
            ok.append(tid)
        except Exception as exc:  # noqa: BLE001
            fail.append(f"{tid}: {exc}")
    print("OK:", ", ".join(ok))
    if fail:
        print("FAIL:", "; ".join(fail))


if __name__ == "__main__":
    main()

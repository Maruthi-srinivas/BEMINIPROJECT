#!/usr/bin/env python3
"""Emit D02-T016..T027 knowledge-base artifacts."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def write(rel: str, text: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


from scripts.d02_bundles_t016_t027 import TOPICS  # noqa: E402


def main() -> None:
    ok: list[str] = []
    fail: list[str] = []
    for tid, b in TOPICS.items():
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

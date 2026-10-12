#!/usr/bin/env python3
"""Write all D24–D27 artifacts from render_all() (skips D24-T001 note)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from d24_d27_write_helper import render_all  # noqa: E402


def main() -> int:
    files = render_all()
    for rel, text in files.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    print(f"Wrote {len(files)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

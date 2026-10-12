#!/usr/bin/env python3
"""Emit D19-T001..T030 artifacts. Run: python scripts/emit_d19_t001_t030.py from knowledge-base root."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_generators"))

from generate_d19_domain import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())

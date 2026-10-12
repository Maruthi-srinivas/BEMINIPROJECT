#!/usr/bin/env python3
"""Generate D24–D27 notes, exercises, solutions, and interview bank items."""
from __future__ import annotations

import sys
from pathlib import Path

GEN = Path(__file__).resolve().parent / "_generators"
sys.path.insert(0, str(GEN))

from generate_d24_d27_batch import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())

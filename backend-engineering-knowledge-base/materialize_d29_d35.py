#!/usr/bin/env python3
"""Materialize D29–D35 notes (skips topics that already have section O)."""
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "_generators"))

if __name__ == "__main__":
    script = ROOT / "_generators" / "generate_d29_d35_batch.py"
    runpy.run_path(str(script), run_name="__main__")

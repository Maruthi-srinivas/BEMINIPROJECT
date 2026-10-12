#!/usr/bin/env python3
"""Emit D20-T001..T026 artifacts. Run from repo: python scripts/emit_d20_t001_t026.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_generators"))
from generate_d20_notes import main

if __name__ == "__main__":
    raise SystemExit(main())

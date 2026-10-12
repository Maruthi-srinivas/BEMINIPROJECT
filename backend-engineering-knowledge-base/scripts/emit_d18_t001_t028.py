"""Emit D18-T001..D18-T028 packages. Run from repo root: python backend-engineering-knowledge-base/scripts/emit_d18_t001_t028.py"""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

GEN = Path(__file__).resolve().parents[1] / "_generators" / "generate_d18_domain.py"
sys.path.insert(0, str(GEN.parent))
raise SystemExit(runpy.run_path(str(GEN), run_name="__main__") or 0)

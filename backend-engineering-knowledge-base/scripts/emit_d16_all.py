#!/usr/bin/env python3
"""Standalone emitter for D16 artifacts (no package path setup). Run from repo root."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GEN = REPO / "backend-engineering-knowledge-base" / "_generators"
sys.path.insert(0, str(GEN))

spec = importlib.util.spec_from_file_location("build_d16", GEN / "build_d16_notes.py")
mod = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(mod)
raise SystemExit(mod.main())

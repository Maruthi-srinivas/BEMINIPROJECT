#!/usr/bin/env python3
"""Write D12 notes, solutions, and interview items only (no exercise stubs)."""
from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("g", HERE / "generate_d12_security.py")
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

finished: list[str] = []
failures: list[str] = []

for t in g.TOPICS:
    tid = t[0]
    slug = t[1]
    try:
        g.NOTES_DIR.mkdir(parents=True, exist_ok=True)
        g.SOL_DIR.mkdir(parents=True, exist_ok=True)
        g.IB_DIR.mkdir(parents=True, exist_ok=True)
        (g.NOTES_DIR / f"d12-{slug}.md").write_text(g.build_note(t), encoding="utf-8")
        (g.SOL_DIR / f"{tid}.md").write_text(g.build_solution(tid), encoding="utf-8")
        (g.IB_DIR / f"{tid}.md").write_text(g.build_interview(t), encoding="utf-8")
        finished.append(tid)
    except Exception as exc:
        failures.append(f"{tid}: {exc}")

print("FINISHED:", ",".join(finished))
print("FAILURES:", ",".join(failures) if failures else "none")
print("COUNT:", len(finished))

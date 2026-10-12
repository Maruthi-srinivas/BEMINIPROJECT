#!/usr/bin/env python3
"""Write every D11 artifact from in-memory registry (no inventory edits)."""
from __future__ import annotations

from pathlib import Path

from generate_d11_content import ROOT, all_artifacts


def materialize() -> int:
    count = 0
    for rel, content in all_artifacts().items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        count += 1
    return count


if __name__ == "__main__":
    n = materialize()
    print(f"Wrote {n} files under {ROOT}")

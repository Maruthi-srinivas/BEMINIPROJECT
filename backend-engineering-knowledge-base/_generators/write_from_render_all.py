#!/usr/bin/env python3
"""Write render_all() output to repo paths. Run locally: py -3 _generators/write_from_render_all.py"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from d24_d27_write_helper import render_all  # noqa: E402

SKIP_NOTE = "23_KUBERNETES_AND_CLOUD/notes/d24-t001-kubernetes-architecture.md"


def main() -> int:
    files = render_all()
    for rel, text in files.items():
        if rel == SKIP_NOTE:
            continue
        p = ROOT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    print(json.dumps(sorted({k.split("/")[-1].replace(".md", "") for k in files if "/notes/" in k or k.startswith("EXERCISES/D")})))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

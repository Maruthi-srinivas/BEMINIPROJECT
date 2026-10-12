#!/usr/bin/env python3
"""Write files from d18_payload_t002_t028.json."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "_generators" / "d18_payload_t002_t028.json"


def main() -> None:
    items = json.loads(PAYLOAD.read_text(encoding="utf-8"))
    for item in items:
        path = ROOT / item["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(item["content"], encoding="utf-8", newline="\n")
    print("Wrote", len(items), "files")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path

from d16_data.assembler import assemble

ROOT = Path(__file__).resolve().parents[2]
INV = ROOT / "00_INDEX" / "inventory.json"


def load_d16_inventory() -> list[dict]:
    data = json.loads(INV.read_text(encoding="utf-8"))
    rows = [t for t in data["topics"] if t["id"].startswith("D16-T")]
    rows.sort(key=lambda r: int(r["id"].split("-T")[1]))
    return [r for r in rows if 1 <= int(r["id"].split("-T")[1]) <= 33]


TOPICS = [assemble(r) for r in load_d16_inventory()]

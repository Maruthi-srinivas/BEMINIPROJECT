"""Emit D18-T002..T028 packages only. Run from repo root or _generators."""
from __future__ import annotations

import json
import sys
from pathlib import Path

GEN = Path(__file__).resolve().parent
KB = GEN.parent
sys.path.insert(0, str(GEN))

from generate_d18_domain import (  # noqa: E402
    load_inventory_topics,
    render_bank,
    render_exercise,
    render_note,
    render_solutions,
    write_pkg,
)
from d18_topic_data import TOPICS  # noqa: E402

SKIP = {"D18-T001"}
INV = KB / "00_INDEX" / "inventory.json"


def main() -> int:
    inv = load_inventory_topics()
    ok: list[str] = []
    fail: list[str] = []
    for topic in TOPICS:
        tid = topic["meta"]["id"]
        if tid in SKIP:
            continue
        if tid not in inv:
            fail.append(f"{tid}: missing from inventory")
            continue
        inv_row = inv[tid]
        topic["meta"]["note_path"] = inv_row["note_path"]
        topic["meta"]["subdomain"] = inv_row["subdomain"]
        topic["meta"]["name"] = inv_row["name"]
        topic["meta"]["dependencies"] = inv_row.get("dependencies", [])
        try:
            write_pkg(topic)
            ok.append(tid)
        except Exception as exc:  # noqa: BLE001
            fail.append(f"{tid}: {exc}")
    out = KB / "_generators" / "emit_d18_result.txt"
    out.write_text("OK: " + ", ".join(ok) + "\nFAIL: " + "; ".join(fail) + "\n", encoding="utf-8")
    print("OK:", ", ".join(ok))
    if fail:
        print("FAIL:", "; ".join(fail))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

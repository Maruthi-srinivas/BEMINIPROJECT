"""Structural check for generated topic notes.

    python backend-engineering-knowledge-base/_generators/audit_notes.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KB = ROOT / "backend-engineering-knowledge-base"
INVENTORY = KB / "00_INDEX" / "inventory.json"

REQUIRED = [f"## {letter}." for letter in "ABCDEFGHIJKLMNO"]


def main() -> None:
    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    missing_file = []
    missing_sections = []
    ok = []
    for topic in data["topics"]:
        path = KB / topic["note_path"]
        if not path.exists():
            missing_file.append(topic["id"])
            continue
        text = path.read_text(encoding="utf-8")
        absent = [heading for heading in REQUIRED if heading not in text]
        if absent or "TODO" in text or "TBD" in text:
            missing_sections.append((topic["id"], absent))
        else:
            ok.append(topic["id"])
    print(f"structurally_complete={len(ok)}")
    print(f"missing_file={len(missing_file)}")
    print(f"incomplete={len(missing_sections)}")
    if missing_file[:20]:
        print("first_missing", ", ".join(missing_file[:20]))
    if missing_sections[:10]:
        for tid, absent in missing_sections[:10]:
            print(tid, absent)


if __name__ == "__main__":
    main()

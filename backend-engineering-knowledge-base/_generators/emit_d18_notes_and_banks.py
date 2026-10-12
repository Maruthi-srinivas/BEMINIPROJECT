#!/usr/bin/env python3
"""Write D18-T002..T028 notes and interview banks (run when shell works)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "_generators"
sys.path.insert(0, str(GEN))

from d18_bank_md import bank_md  # noqa: E402
from d18_compose_note import compose_note  # noqa: E402
from d18_topic_data import TOPICS  # noqa: E402
from d18_topic_data_rest import REST_TOPICS  # noqa: E402
from generate_d18_domain import load_inventory_topics  # noqa: E402

# Map topic id -> _iq seed from REST builder (last arg before exercises in pattern(), or explicit in _topic)
SEEDS: dict[str, str] = {
    "D18-T002": "three simplicity rules that prevent speculative abstraction",
    "D18-T003": "hide state enforce invariants compose behaviors",
    "D18-T004": "stable contracts hiding infrastructure details",
    "D18-T005": "depend on abstractions inject implementations at the edge",
    "D18-T006": "visual contracts for structure and message order",
    "D18-T007": "assign responsibilities before writing classes",
    "D18-T008": "clear creation use disposal and who mutates",
    "D18-T009": "centralize object creation behind an interface",
    "D18-T010": "stepwise assembly with validation at build()",
    "D18-T011": "one controlled instance vs hidden global state",
    "D18-T012": "copy configured template instead of rebuilding",
    "D18-T013": "pluggable algorithms selected at runtime",
    "D18-T014": "publish state changes to interested listeners",
    "D18-T015": "translate interfaces without changing legacy vendor code",
    "D18-T016": "stack behaviors around same interface",
    "D18-T017": "simplify subsystem access for callers",
    "D18-T018": "control access lazy load caching remote calls",
    "D18-T019": "requests as objects for queue undo audit",
    "D18-T020": "behavior changes with internal state object",
    "D18-T021": "fixed algorithm skeleton with overridable steps",
    "D18-T022": "linked handlers each optionally processing",
    "D18-T023": "collection-like persistence with transactional unit of work",
    "D18-T024": "framework-managed object graph and scopes",
    "D18-T025": "seams and tests that enable safe change",
    "D18-T026": "immutability confinement or synchronized shared state",
    "D18-T027": "entities values and rules that must always hold",
    "D18-T028": "safe structural change without behavior change",
}


def main() -> None:
    inv = load_inventory_topics()
    skip = {"D18-T001"}
    for topic in TOPICS:
        tid = topic["meta"]["id"]
        if tid in skip or tid not in inv:
            continue
        row = inv[tid]
        topic["meta"]["note_path"] = row["note_path"]
        topic["meta"]["subdomain"] = row["subdomain"]
        topic["meta"]["name"] = row["name"]
        topic["meta"]["dependencies"] = row.get("dependencies", [])
        topic["_iq_seed"] = SEEDS[tid]
        note_path = ROOT / row["note_path"]
        note_path.parent.mkdir(parents=True, exist_ok=True)
        note_path.write_text(compose_note(topic), encoding="utf-8", newline="\n")
        bank_path = ROOT / "INTERVIEW_BANK" / "items" / f"{tid}.md"
        bank_path.write_text(bank_md(tid, row["name"], row["note_path"]), encoding="utf-8", newline="\n")
        print("wrote", tid)


if __name__ == "__main__":
    main()

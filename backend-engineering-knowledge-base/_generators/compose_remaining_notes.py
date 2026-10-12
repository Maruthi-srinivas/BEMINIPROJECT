"""Compose D17-T021..T035 notes (T019,T020,T036 may exist). Run: python compose_remaining_notes.py"""
from pathlib import Path

from d17_k_md import section_k_for
from d17_topics_019_036 import TOPICS
from emit_d17_t019_t036 import load_inventory_topics, render_note

SKIP = {"D17-T019", "D17-T020", "D17-T036"}

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    for meta in load_inventory_topics():
        tid = meta["id"]
        if tid in SKIP:
            continue
        body = TOPICS[tid]
        md = render_note(
            tid,
            meta["name"],
            meta["importance"],
            meta["complexity"],
            meta.get("dependencies", []),
            body,
        )
        path = ROOT / meta["note_path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(md, encoding="utf-8")
        print("wrote", tid)


if __name__ == "__main__":
    main()

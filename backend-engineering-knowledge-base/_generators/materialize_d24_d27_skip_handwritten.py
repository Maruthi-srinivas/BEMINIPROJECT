#!/usr/bin/env python3
"""Materialize D24–D27 artifacts; skip overwriting hand-written D24-T001 note."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from d24_d27_write_helper import (  # noqa: E402
    build_body,
    build_note,
    load_topics,
    render_satellites,
)

SKIP_NOTE_IDS = {"D24-T001"}


def note_has_topic_id(path: Path, tid: str) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    return f"Topic ID: `{tid}`" in text or text.startswith(f"# {tid} —")


def write_satellites(t: dict, body: dict) -> None:
    tid = t["id"]
    for rel, text in render_satellites(t, body).items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def materialize_topic(t: dict) -> None:
    body = build_body(t)
    tid = t["id"]
    note_path = ROOT / t["note_path"]
    note_path.parent.mkdir(parents=True, exist_ok=True)

    if tid in SKIP_NOTE_IDS:
        pass  # never overwrite hand-written note
    elif note_has_topic_id(note_path, tid):
        pass  # already materialized
    else:
        note_path.write_text(build_note(t, body), encoding="utf-8")

    write_satellites(t, body)


def main() -> int:
    topics = load_topics((24, 25, 26, 27))
    ok: list[str] = []
    fail: list[str] = []
    for t in topics:
        try:
            materialize_topic(t)
            ok.append(t["id"])
        except Exception as exc:  # noqa: BLE001
            fail.append(f"{t['id']}: {exc}")
    print(f"OK {len(ok)}")
    for i in ok:
        print(i)
    if fail:
        print(f"FAIL {len(fail)}", file=sys.stderr)
        for f in fail:
            print(f, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

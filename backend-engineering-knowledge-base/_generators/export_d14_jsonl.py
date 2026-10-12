#!/usr/bin/env python3
"""Export rendered D14 artifacts as JSONL lines: {"path": "...", "content": "..."}."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from d14_factory import build_topic_packages  # noqa: E402
from d14_render import (  # noqa: E402
    render_exercise_file,
    render_interview_bank,
    render_note,
    render_solution_file,
)
from generate_d14_domain import load_d14_inventory  # noqa: E402

OUT = Path(__file__).with_name("d14_export.jsonl")


def main() -> None:
    packages = build_topic_packages(load_d14_inventory())
    finished: list[str] = []
    failures: list[str] = []
    with OUT.open("w", encoding="utf-8") as fh:
        for topic in packages:
            meta = topic["meta"]
            tid = meta["id"]
            try:
                rows = [
                    (meta["note_path"], render_note(topic)),
                    (f"EXERCISES/{meta['id']}.md", render_exercise_file(meta, topic["exercises"])),
                    (
                        f"EXERCISES/solutions/{meta['id']}.md",
                        render_solution_file(meta, topic["solutions"]),
                    ),
                    (
                        f"INTERVIEW_BANK/items/{meta['id']}.md",
                        render_interview_bank(meta, topic["interview"]),
                    ),
                ]
                for rel_path, content in rows:
                    fh.write(
                        json.dumps({"path": rel_path, "content": content}, ensure_ascii=False) + "\n"
                    )
                finished.append(tid)
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{tid}: {exc}")
    print("FINISHED:", ",".join(finished))
    print("FAILURES:", ",".join(failures) if failures else "none")
    print("WROTE:", OUT, "lines", len(finished) * 4)


if __name__ == "__main__":
    main()

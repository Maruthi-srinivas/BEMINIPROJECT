"""Write domain README and topic index pages from the inventory.

A domain page lists every topic and whether its note is on disk.
It does not claim the domain is validated.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KB = ROOT / "backend-engineering-knowledge-base"
DATA = json.loads((KB / "00_INDEX" / "inventory.json").read_text(encoding="utf-8"))

REQUIRED_END = "## O."


def main() -> None:
    by_folder: dict[str, list[dict]] = {}
    for topic in DATA["topics"]:
        by_folder.setdefault(topic["folder"], []).append(topic)
    for folder, topics in by_folder.items():
        directory = KB / folder
        directory.mkdir(parents=True, exist_ok=True)
        present = 0
        lines = [
            f"# {folder}",
            "",
            "Topic notes for this folder. A link appears when the note file contains the full A–O structure.",
            "Missing notes are not done.",
            "",
            "| ID | Topic | Status |",
            "| --- | --- | --- |",
        ]
        for topic in topics:
            path = KB / topic["note_path"]
            ready = path.exists() and REQUIRED_END in path.read_text(encoding="utf-8")
            if ready:
                present += 1
                status = f"[note](./{Path(topic['note_path']).relative_to(folder).as_posix()})"
            elif path.exists():
                status = "partial"
            else:
                status = "not started"
            name = topic["name"].replace("|", "\\|")
            lines.append(f"| {topic['id']} | {name} | {status} |")
        lines.extend(["", f"Notes with a full structure: {present} / {len(topics)}.", ""])
        (directory / "TOPIC_INDEX.md").write_text("\n".join(lines), encoding="utf-8")
        readme = [
            f"# {topics[0]['domain'] if len({t['domain'] for t in topics}) == 1 else folder}",
            "",
            f"This folder holds notes for {len(topics)} checklist topics.",
            f"{present} currently have the full note structure. The rest are still being written.",
            "",
            "Start at [TOPIC_INDEX.md](./TOPIC_INDEX.md).",
            "Interview answers live in each note, section K, and under `INTERVIEW_BANK/items/`.",
            "Exercises are under `EXERCISES/`. Solutions are separate, in `EXERCISES/solutions/`.",
            "",
        ]
        # Fix the domain title: if two domains share a folder, name both.
        domains = []
        for topic in topics:
            if topic["domain"] not in domains:
                domains.append(topic["domain"])
        readme[0] = "# " + " and ".join(domains)
        (directory / "README.md").write_text("\n".join(readme), encoding="utf-8")
        print(folder, present, "/", len(topics))


if __name__ == "__main__":
    main()

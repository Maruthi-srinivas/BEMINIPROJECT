"""Mark notes GENERATED when sections A-O exist, and refresh the progress tracker.

Does not mark VALIDATED. That is reserved for the audit.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KB = ROOT / "backend-engineering-knowledge-base"
INDEX = KB / "00_INDEX"
INVENTORY = INDEX / "inventory.json"

REQUIRED = [f"## {letter}." for letter in "ABCDEFGHIJKLMNO"]


def note_status(path: Path) -> str:
    if not path.exists():
        return "NOT_STARTED"
    text = path.read_text(encoding="utf-8")
    if all(heading in text for heading in REQUIRED) and "TODO" not in text and "TBD" not in text:
        return "GENERATED"
    if text.strip():
        return "IN_PROGRESS"
    return "NOT_STARTED"


def main() -> None:
    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    counts: Counter[str] = Counter()
    by_domain: dict[int, list[dict]] = {}
    for topic in data["topics"]:
        status = note_status(KB / topic["note_path"])
        # Never downgrade a validated row.
        if topic.get("validation_status") != "VALIDATED":
            topic["doc_status"] = status
            topic["validation_status"] = status if status == "GENERATED" else (
                "IN_PROGRESS" if status == "IN_PROGRESS" else "NOT_STARTED"
            )
        counts[topic["validation_status"]] += 1
        by_domain.setdefault(topic["domain_number"], []).append(topic)
    INVENTORY.write_text(json.dumps(data, indent=2), encoding="utf-8")

    lines = [
        "# Progress tracker",
        "",
        "A topic is `GENERATED` when its note contains sections A through O and no TODO placeholder.",
        "Only `VALIDATED` counts as finished. Validation has not been run to completion.",
        "",
        f"Inventoried topics: {len(data['topics'])}",
        "",
        "| Domain | Topics | NOT_STARTED | IN_PROGRESS | GENERATED | VALIDATION_FAILED | VALIDATED | BLOCKED |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    order = {row["number"]: row["name"] for row in data["domains"]}
    for number in range(1, 36):
        rows = by_domain.get(number, [])
        c = Counter(row["validation_status"] for row in rows)
        lines.append(
            f"| D{number:02d} {order[number]} | {len(rows)} | {c['NOT_STARTED']} | {c['IN_PROGRESS']} | {c['GENERATED']} | {c['VALIDATION_FAILED']} | {c['VALIDATED']} | {c['BLOCKED']} |"
        )
    total = len(data["topics"])
    lines.extend(
        [
            "",
            f"| Total | {total} | {counts['NOT_STARTED']} | {counts['IN_PROGRESS']} | {counts['GENERATED']} | {counts['VALIDATION_FAILED']} | {counts['VALIDATED']} | {counts['BLOCKED']} |",
            "",
            f"Generated: {counts['GENERATED']} / {total}. Validated: {counts['VALIDATED']} / {total}.",
            "",
        ]
    )
    (INDEX / "PROGRESS_TRACKER.md").write_text("\n".join(lines), encoding="utf-8")
    print(dict(counts))


if __name__ == "__main__":
    main()

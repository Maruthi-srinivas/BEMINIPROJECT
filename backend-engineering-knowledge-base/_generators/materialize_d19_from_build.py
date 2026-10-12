"""Write all D19 artifacts by calling build_topic + write_topic_package. Run once locally."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from d19_build_topics import build_topic  # noqa: E402
from d19_render import write_topic_package  # noqa: E402

inv = json.loads((ROOT / "00_INDEX" / "inventory.json").read_text(encoding="utf-8"))
topics = [t for t in inv["topics"] if t["id"].startswith("D19-T")]
topics.sort(key=lambda t: t["id"])

finished = []
failures = []
for row in topics:
    try:
        write_topic_package(build_topic(row))
        finished.append(row["id"])
    except Exception as exc:  # noqa: BLE001
        failures.append(f"{row['id']}: {exc}")

print("FINISHED:", ", ".join(finished))
if failures:
    print("FAILURES:", "; ".join(failures))
    raise SystemExit(1)

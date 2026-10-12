import json
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "00_INDEX" / "inventory.json"
data = json.loads(p.read_text(encoding="utf-8"))
topics = [t for t in data["topics"] if t["id"].startswith(("D28", "D29", "D30", "D31", "D32", "D33", "D34", "D35"))]
topics.sort(key=lambda t: (t["id"][:3], int(t["id"].split("-T")[1])))
print(len(topics))
for t in topics:
    print(t["id"] + "|" + t["name"][:80])

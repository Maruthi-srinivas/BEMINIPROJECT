"""Write only topic notes for D17-T019..T036. Run: python emit_notes_only.py"""
from pathlib import Path

from emit_d17_t019_t036 import load_inventory_topics, render_note
from d17_topics_019_036 import TOPICS

ROOT = Path(__file__).resolve().parents[1]


def main() -> tuple[list[str], list[str]]:
    done: list[str] = []
    fail: list[str] = []
    for meta in load_inventory_topics():
        tid = meta["id"]
        try:
            body = TOPICS[tid]
            path = ROOT / meta["note_path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                render_note(
                    tid,
                    meta["name"],
                    meta["importance"],
                    meta["complexity"],
                    meta.get("dependencies", []),
                    body,
                ),
                encoding="utf-8",
            )
            done.append(tid)
        except Exception as exc:  # noqa: BLE001
            fail.append(f"{tid}: {exc}")
    return done, fail


if __name__ == "__main__":
    d, f = main()
    print("FINISHED:", ",".join(d))
    print("FAILURES:", f or "none")

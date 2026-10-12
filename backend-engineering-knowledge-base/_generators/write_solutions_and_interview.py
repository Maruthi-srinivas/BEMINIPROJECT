"""One-shot: write solutions + interview bank for D17-T019..T036. Run: python write_solutions_and_interview.py"""
from emit_d17_t019_t036 import load_inventory_topics, render_interview_bank, render_solution
from d17_topics_019_036 import TOPICS
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    for meta in load_inventory_topics():
        tid = meta["id"]
        body = TOPICS[tid]
        (ROOT / "EXERCISES" / "solutions" / f"{tid}.md").write_text(
            render_solution(tid, body), encoding="utf-8"
        )
        rel = Path("..") / Path(meta["note_path"]).as_posix()
        (ROOT / "INTERVIEW_BANK" / "items" / f"{tid}.md").write_text(
            render_interview_bank(tid, meta["name"], rel.as_posix(), body),
            encoding="utf-8",
        )
        print(tid)

if __name__ == "__main__":
    main()

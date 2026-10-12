"""Run from repo root: python _generators/d12_emit_all.py — writes notes, solutions, interviews."""
from generate_d12_security import TOPICS, build_note, build_solution, build_interview, NOTES_DIR, SOL_DIR, IB_DIR

if __name__ == "__main__":
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    SOL_DIR.mkdir(parents=True, exist_ok=True)
    IB_DIR.mkdir(parents=True, exist_ok=True)
    for t in TOPICS:
        tid, slug = t[0], t[1]
        (NOTES_DIR / f"d12-{slug}.md").write_text(build_note(t), encoding="utf-8")
        (SOL_DIR / f"{tid}.md").write_text(build_solution(tid), encoding="utf-8")
        (IB_DIR / f"{tid}.md").write_text(build_interview(t), encoding="utf-8")
    print("done", len(TOPICS))

"""Write INTERVIEW_BANK/items for D17-T019..T036."""
from pathlib import Path
from d17_k_md import TOPIC_K_ARGS
from emit_d17_t019_t036 import load_inventory_topics

ROOT = Path(__file__).resolve().parents[1]

TITLES = {m["id"]: m["name"] for m in load_inventory_topics()}


def slug_for(tid: str) -> str:
    for m in load_inventory_topics():
        if m["id"] == tid:
            return Path(m["note_path"]).name.replace(".md", "")
    raise KeyError(tid)


def main() -> None:
    for tid in sorted(TOPIC_K_ARGS):
        name = TITLES[tid]
        slug = slug_for(tid)
        lines = [
            f"# {tid} interview items",
            "",
            "Domain: Common System Design Problems",
            f"Topic: {name}",
            "Difficulty mix: beginner, intermediate, advanced, scenario, follow-up",
            "Interview type: system design, scaling, reliability",
            "Full reasoned answers are in the topic note, section K.",
            "",
            "## Questions",
            "",
        ]
        from d17_interview_factory import build_interview

        args = TOPIC_K_ARGS[tid]
        n = 1
        for level, title, _ in build_interview(*args):
            lines.append(f"{n}. {level}. {title}")
            n += 1
        lines.append("")
        lines.append(
            f"Answer key: [topic note section K](../../16_SYSTEM_DESIGN_PROBLEMS/notes/{slug}.md)."
        )
        out = ROOT / "INTERVIEW_BANK" / "items" / f"{tid}.md"
        out.write_text("\n".join(lines), encoding="utf-8")
        print(tid)


if __name__ == "__main__":
    main()

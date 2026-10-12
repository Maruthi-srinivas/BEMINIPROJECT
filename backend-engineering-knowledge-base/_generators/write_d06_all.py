# -*- coding: utf-8 -*-
"""Write D06-T005..D06-T021 notes + exercises + solutions + interview items."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "05_API_DESIGN" / "notes"
EX = ROOT / "EXERCISES"
SOL = EX / "solutions"
INT = ROOT / "INTERVIEW_BANK" / "items"

# Each entry: filename slug, title, subdomain, deps, exercises list, interview qs, body markdown (A-J + tail L-O embedded)


def write_bundle(tid: str, slug: str, title: str, subdomain: str, deps, body: str, exercises, iqs):
    header = f"""# {tid} — {title}

Topic ID: `{tid}`
Domain: API Design and REST
Subdomain: {subdomain}
Importance: core
Complexity: intermediate
Dependencies: {", ".join(f"`{d}`" for d in deps)}
Execution status of the code in section F: illustrative (not executed in CI for this topic)

"""
    path = NOTES / f"d06-{slug}.md"
    path.write_text(header + body, encoding="utf-8")
    EX.write_text = None
    (EX / f"{tid}.md").write_text(
        f"# Exercises — {tid}\n\nProblems only. Solutions: [{tid}](../solutions/{tid}.md).\n\n"
        + "\n".join(f"{i}. {e}" for i, e in enumerate(exercises, 1))
        + "\n",
        encoding="utf-8",
    )
    sol = f"# Solutions for {tid}\n\nOpen after attempting exercises.\n\n"
    for i, e in enumerate(exercises, 1):
        sol += f"## Exercise {i}\n\n{e}\n\nSee topic note section L for acceptance criteria.\n\n"
    (SOL / f"{tid}.md").write_text(sol, encoding="utf-8")
    rel = f"../05_API_DESIGN/notes/d06-{slug}.md"
    iq_lines = "\n".join(f"{n}. {q}" for n, q in enumerate(iqs, 1))
    (INT / f"{tid}.md").write_text(
        f"# {tid} interview items\n\nTopic: {title}\nAnswers: [section K]({rel}).\n\n## Questions\n\n{iq_lines}\n",
        encoding="utf-8",
    )
    return tid


def main():
    written = []
    # Import topic bodies from companion module
    from d06_topic_bodies import TOPICS  # noqa: WPS433

    for t in TOPICS:
        written.append(
            write_bundle(
                t["id"],
                t["slug"],
                t["name"],
                t["subdomain"],
                t["deps"],
                t["body"],
                t["exercises"],
                t["interview_questions"],
            )
        )
    print("OK", len(written), written)


if __name__ == "__main__":
    main()

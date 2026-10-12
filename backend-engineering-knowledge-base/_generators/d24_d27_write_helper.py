"""Import-safe helpers to render D24–D27 artifacts (no side effects on import)."""
from __future__ import annotations

from generate_d24_d27_batch import (  # noqa: F401
    build_body,
    build_note,
    classify,
    interview_question_lists,
    load_topics,
    slug_from_path,
    write_topic,
)

SKIP_NOTE_IDS = frozenset({"D24-T001"})


def render_satellites(t: dict, body: dict) -> dict[str, str]:
    tid = t["id"]
    sol = body["ex_solutions"]
    slug = slug_from_path(t["note_path"])
    rel = f"../../{t['folder']}/notes/{slug}.md"
    kind = classify(t)
    qs: list[str] = []
    n = 1
    for level, questions in interview_question_lists(t, kind):
        for q in questions:
            qs.append(f"{n}. {level}. {q}")
            n += 1
    return {
        f"EXERCISES/{tid}.md": f"""# Exercises — {tid}

Problems only. Solutions: [{tid}](solutions/{tid}.md).

1. Apply or draft the staging change described in section L exercise 1 for {t['name']}.
2. List read-only diagnostic commands for the fictional incident in exercise 2.
3. Write the trade-off paragraph for exercise 3.
""",
        f"EXERCISES/solutions/{tid}.md": f"""# Solutions for {tid}

Open this only after attempting the exercises in the topic note.

## Exercise 1

{sol[0]}

## Exercise 2

{sol[1]}

## Exercise 3

{sol[2]}
""",
        f"INTERVIEW_BANK/items/{tid}.md": f"""# {tid} interview items

Domain: {t['domain']}
Topic: {t['name']}
Difficulty mix: beginner, intermediate, advanced, scenario, follow-up
Interview type: operations, debugging, trade-off, system design
Full reasoned answers are in the topic note, section K.

## Questions

{chr(10).join(qs)}

Answer key: [topic note section K]({rel}).
""",
    }


def render_all() -> dict[str, str]:
    """Return relative path -> UTF-8 text for all D24–D27 artifacts."""
    out: dict[str, str] = {}
    for t in load_topics((24, 25, 26, 27)):
        body = build_body(t)
        tid = t["id"]
        if tid not in SKIP_NOTE_IDS:
            out[t["note_path"]] = build_note(t, body)
        out.update(render_satellites(t, body))
    return out

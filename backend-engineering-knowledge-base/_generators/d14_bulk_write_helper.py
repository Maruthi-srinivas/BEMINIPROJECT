"""Helper to render D14 bulk topic ancillary files (exercise, solution, interview bank)."""

from __future__ import annotations

from d14_bulk_specs import TOPIC_DEFS, build_spec_entry


def ancillary_files(tid: str) -> dict[str, str]:
    row = next(t for t in TOPIC_DEFS if t[0] == tid)
    spec = build_spec_entry(*row)
    meta = {"id": tid, "name": row[1], "note_path": f"13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t{int(tid.split('-T')[1]):03d}-"}
    # note_path filled by caller from inventory
    ex = f"# Exercises — {tid}\n\nProblems only. Solutions: [{tid}](../solutions/{tid}.md).\n\n"
    ex += f"1. {spec['ex1_prompt']}\n2. {spec['ex2_prompt']}\n3. {spec['ex3_prompt']}\n"
    sol = f"# Solutions for {tid}\n\nOpen this only after attempting the exercises in the topic note.\n\n"
    for i, key in enumerate(["ex1_solution", "ex2_solution", "ex3_solution"], 1):
        sol += f"## Exercise {i}\n\n{spec[key]}\n\n"
    return {"exercise": ex, "solution": sol, "spec": spec}


if __name__ == "__main__":
    for tid, title, focus, *_ in TOPIC_DEFS:
        print(tid, title, focus)

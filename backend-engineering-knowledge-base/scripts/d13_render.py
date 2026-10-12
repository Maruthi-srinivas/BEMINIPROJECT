"""Render D13 topic bundles from compact specs."""
from __future__ import annotations

from scripts.d13_helpers import interview_block, make_exercises, make_interview_bank, note_header


def render(spec: dict) -> dict:
    tid = spec["id"]
    title = spec["title"]
    slug = spec["slug"]
    importance = spec.get("importance", "core")
    deps = spec["deps"]
    note_path = f"12_CONCURRENCY/notes/{slug}.md"
    header = note_header(tid, title, importance, deps)
    note = (
        header
        + "## A. Topic Overview\n\n"
        + spec["a"]
        + "\n\n## B. First-Principles Explanation\n\n"
        + spec["b"]
        + "\n\n## C. Internal Working and Architecture\n\n"
        + spec["c"]
        + "\n\n## D. Diagrams and Visual Models\n\n```mermaid\n"
        + spec["mermaid"].strip()
        + "\n```\n\n"
        + spec.get("d_cap", "Use the diagram as the mental model for ordering and ownership.")
        + "\n\n## E. Examples and Analogies\n\n"
        + spec["e"]
        + "\n\n## F. Code Examples\n\n"
        + spec["f"]
        + "\n\n## G. Practical Backend Application\n\n"
        + spec["g"]
        + "\n\n## H. Advantages, Limitations and Trade-offs\n\n"
        + spec["h"]
        + "\n\n## I. Common Mistakes and Misconceptions\n\n"
        + spec["i"]
        + "\n\n## J. Debugging and Troubleshooting\n\n"
        + spec["j"]
        + "\n\n"
        + interview_block(spec["iq"])
        + "## L. Practical Exercises\n\n"
        + f"Solutions are in `EXERCISES/solutions/{tid}.md`. Try these before opening that file.\n\n"
        + f"### Exercise 1 — implementation\n\n{spec['l1']}\n\n"
        + f"### Exercise 2 — debugging\n\n{spec['l2']}\n\n"
        + f"### Exercise 3 — trade-off\n\n{spec['l3']}\n\n"
        + "## M. Revision Notes\n\n"
        + spec["m"]
        + "\n\n## N. Related Topics\n\n"
        + spec["n"]
        + "\n\n## O. Completion Criteria\n\n"
        + spec["o"]
        + "\n"
    )
    bank_qs = {k: [q for q, _ in v] for k, v in spec["iq"].items()}
    rel = f"../12_CONCURRENCY/notes/{slug}.md"
    return {
        "note_path": note_path,
        "note": note,
        "exercises": make_exercises(tid, spec["ex1"], spec["ex2"], spec["ex3"]),
        "solutions": (
            f"# Solutions for {tid}\n\n"
            f"Open this only after attempting the exercises in the topic note.\n\n"
            f"## Exercise 1\n\n{spec['sol1']}\n\n"
            f"## Exercise 2\n\n{spec['sol2']}\n\n"
            f"## Exercise 3\n\n{spec['sol3']}\n"
        ),
        "interview": make_interview_bank(tid, title, bank_qs, rel),
    }

"""Shared helpers for D02 note emission."""
from __future__ import annotations


def four(s1: str, s2: str, s3: str, s4: str) -> str:
    return f"{s1} {s2} {s3} {s4}"


def k_block(qa: dict[str, list[tuple[str, str]]]) -> str:
    parts = ["## K. Interview Preparation\n"]
    for level, items in qa.items():
        parts.append(f"### {level}\n")
        for i, (q, a) in enumerate(items, 1):
            parts.append(f"#### Q{i}. {q}\n\n**Answer:** {a}\n\n")
    return "".join(parts)


def header(tid: str, title: str, slug: str, deps: list[str]) -> str:
    dep_txt = ", ".join(f"`{d}`" for d in deps)
    return f"""# {tid} — {title}

Topic ID: `{tid}`
Domain: Data Structures and Algorithms
Subdomain: {title}
Importance: core
Complexity: intermediate
Dependencies: {dep_txt}
Execution status of the code in section F: unexecuted

"""


def exercises_md(tid: str, items: list[str]) -> str:
    body = "\n".join(f"{i}. {t}" for i, t in enumerate(items, 1))
    return f"""# Exercises — {tid}

Problems only. Solutions: [{tid}](../solutions/{tid}.md).

{body}
"""


def interview_md(tid: str, title: str, note_rel: str, qs: list[str]) -> str:
    lines = [
        f"# {tid} interview items",
        "",
        "Domain: Data Structures and Algorithms",
        f"Topic: {title}",
        "Difficulty mix: beginner, intermediate, advanced, scenario, follow-up",
        "Interview type: fundamentals, debugging, trade-off",
        "Full reasoned answers are in the topic note, section K.",
        "",
        "## Questions",
        "",
    ]
    for i, q in enumerate(qs, 1):
        lines.append(f"{i}. {q}")
    lines += ["", f"Answer key: [topic note section K]({note_rel}).", ""]
    return "\n".join(lines)


def completion_criteria(items: list[str]) -> str:
    bullets = "\n".join(f"- {x}" for x in items)
    return f"""## O. Completion Criteria

{bullets}
"""


def std_sections(
    tid: str,
    title: str,
    slug: str,
    chain_dep: str,
    overview: str,
    first_principles: str,
    internal: str,
    mermaid: str,
    diagram_caption: str,
    examples: str,
    code_file: str,
    code: str,
    code_blurb: str,
    backend: str,
    trade_table: str,
    mistakes: str,
    debug: str,
    qa: dict,
    ex: tuple[str, str, str],
    sol: str,
    revision: str,
    related: str,
    criteria: list[str],
    interview_qs: list[str],
) -> dict:
    note_rel = f"../01_PROGRAMMING_AND_ALGORITHMS/notes/{slug}.md"
    note = (
        header(tid, title, slug, [chain_dep] + DOMAIN_DEPS)
        + f"## A. Topic Overview\n\n{overview}\n\n"
        + f"## B. First-Principles Explanation\n\n{first_principles}\n\n"
        + f"## C. Internal Working and Architecture\n\n{internal}\n\n"
        + "## D. Diagrams and Visual Models\n\n"
        + f"```mermaid\n{mermaid}\n```\n\n"
        + f"{diagram_caption}\n\n"
        + f"## E. Examples and Analogies\n\n{examples}\n\n"
        + f"## F. Code Examples\n\nFile: `{code_file}`\n\nDependencies: Python 3 standard library only.\n\n"
        + f"```python\n{code.strip()}\n```\n\n{code_blurb}\n\n"
        + f"## G. Practical Backend Application\n\n{backend}\n\n"
        + f"## H. Advantages, Limitations and Trade-offs\n\n{trade_table}\n\n"
        + f"## I. Common Mistakes and Misconceptions\n\n{mistakes}\n\n"
        + f"## J. Debugging and Troubleshooting\n\n{debug}\n\n"
        + k_block(qa)
        + "## L. Practical Exercises\n\n"
        + f"Solutions are in `EXERCISES/solutions/{tid}.md`. Try these before opening that file.\n\n"
        + f"### Exercise 1 — implementation\n\n{ex[0]}\n\n"
        + f"### Exercise 2 — debugging\n\n{ex[1]}\n\n"
        + f"### Exercise 3 — trade-off\n\n{ex[2]}\n\n"
        + f"## M. Revision Notes\n\n{revision}\n\n"
        + f"## N. Related Topics\n\n{related}\n\n"
        + completion_criteria(criteria)
    )
    return {
        "note_path": f"01_PROGRAMMING_AND_ALGORITHMS/notes/{slug}.md",
        "note": note,
        "exercises": exercises_md(
            tid,
            [
                ex[0].split("\n")[0],
                ex[1].split("\n")[0],
                ex[2].split("\n")[0],
            ],
        ),
        "solutions": f"# Solutions for {tid}\n\nOpen this only after attempting the exercises in the topic note.\n\n{sol}",
        "interview": interview_md(tid, title, note_rel, interview_qs),
    }


DOMAIN_DEPS = ["D02-T001", "D01-T001", "D01-T002"]


def qa_set(beg, inter, adv, scen, fol):  # noqa: ANN001
    return {
        "Beginner": beg,
        "Intermediate": inter,
        "Advanced": adv,
        "Scenarios": scen,
        "Follow-ups": fol,
    }

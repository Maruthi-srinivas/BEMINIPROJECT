"""Shared builders for D13 topic artifacts."""
from __future__ import annotations

from scripts.d13_helpers import (
    interview_block,
    make_exercises,
    make_interview_bank,
    note_header,
)


def four(s: str) -> str:
    return s.strip()


def section_k(iq: dict[str, list[tuple[str, str]]]) -> str:
    return interview_block(iq)


def exercises_section(e1: str, e2: str, e3: str) -> str:
    return f"""## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{{tid}}.md`. Try these before opening that file.

### Exercise 1 — implementation

{e1}

### Exercise 2 — debugging

{e2}

### Exercise 3 — trade-off

{e3}
"""


def solutions_md(tid: str, s1: str, s2: str, s3: str) -> str:
    return f"""# Solutions for {tid}

Open this only after attempting the exercises in the topic note.

## Exercise 1

{s1}

## Exercise 2

{s2}

## Exercise 3

{s3}
"""


def build_note(
    tid: str,
    title: str,
    slug: str,
    importance: str,
    deps: list[str],
    a: str,
    b: str,
    c: str,
    mermaid: str,
    e: str,
    f_code: str,
    f_run: str,
    f_out: str,
    g: str,
    h_table: str,
    i: str,
    j: str,
    iq: dict[str, list[tuple[str, str]]],
    l1: str,
    l2: str,
    l3: str,
    m: str,
    n: str,
    o: str,
) -> str:
    header = note_header(tid, title, title, importance, deps)
    d = f"""## D. Diagrams and Visual Models

```mermaid
{mermaid.strip()}
```

Read this as the control flow for the topic. Arrows show ordering or ownership, not every syscall.

"""
    fsec = f"""## F. Code Examples

{f_code}

How to run: {f_run}

Expected output: {f_out}

"""
    lsec = exercises_section(l1, l2, l3).replace("{tid}", tid)
    body = (
        header
        + "## A. Topic Overview\n\n"
        + a
        + "\n\n## B. First-Principles Explanation\n\n"
        + b
        + "\n\n## C. Internal Working and Architecture\n\n"
        + c
        + "\n\n"
        + d
        + "## E. Examples and Analogies\n\n"
        + e
        + "\n\n"
        + fsec
        + "## G. Practical Backend Application\n\n"
        + g
        + "\n\n## H. Advantages, Limitations and Trade-offs\n\n"
        + h_table
        + "\n\n## I. Common Mistakes and Misconceptions\n\n"
        + i
        + "\n\n## J. Debugging and Troubleshooting\n\n"
        + j
        + "\n\n"
        + section_k(iq)
        + lsec
        + "\n\n## M. Revision Notes\n\n"
        + m
        + "\n\n## N. Related Topics\n\n"
        + n
        + "\n\n## O. Completion Criteria\n\n"
        + o
        + "\n"
    )
    return body


def bundle(
    tid: str,
    title: str,
    slug: str,
    importance: str,
    deps: list[str],
    **kwargs,
) -> dict:
    note_path = f"12_CONCURRENCY/notes/{slug}.md"
    note = build_note(tid, title, slug, importance, deps, **kwargs)
    bank_qs = {
        "Beginner": [q for q, _ in kwargs["iq"]["Beginner"]],
        "Intermediate": [q for q, _ in kwargs["iq"]["Intermediate"]],
        "Advanced": [q for q, _ in kwargs["iq"]["Advanced"]],
        "Scenarios": [q for q, _ in kwargs["iq"]["Scenarios"]],
        "Follow-ups": [q for q, _ in kwargs["iq"]["Follow-ups"]],
    }
    rel = f"../12_CONCURRENCY/notes/{slug}.md"
    return {
        "note_path": note_path,
        "note": note,
        "exercises": make_exercises(tid, kwargs["ex1"], kwargs["ex2"], kwargs["ex3"]),
        "solutions": solutions_md(tid, kwargs["sol1"], kwargs["sol2"], kwargs["sol3"]),
        "interview": make_interview_bank(tid, title, bank_qs, rel),
    }

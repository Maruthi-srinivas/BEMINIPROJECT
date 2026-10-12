"""Topic metadata and bodies for D10-T001..D10-T019."""
from __future__ import annotations

from generate_d10_notes import four


def iv_pack(
    b: list[tuple[str, list[str]]],
    i: list[tuple[str, list[str]]],
    a: list[tuple[str, list[str]]],
    s: list[tuple[str, list[str]]],
    f: list[tuple[str, list[str]]],
) -> dict:
    return {
        "beginner": [(q, four(ans)) for q, ans in b],
        "intermediate": [(q, four(ans)) for q, ans in i],
        "advanced": [(q, four(ans)) for q, ans in a],
        "scenarios": [(q, four(ans)) for q, ans in s],
        "followups": [(q, four(ans)) for q, ans in f],
    }


def std_table(rows: str) -> str:
    return (
        "| Choice | Benefit | Cost | Choose when | Avoid when |\n"
        "| --- | --- | --- | --- | --- |\n" + rows
    )


def std_mistakes(bullets: list[str]) -> str:
    return "\n".join(f"- {x}" for x in bullets)


def std_debug(steps: list[str]) -> str:
    body = "\n".join(f"{n}. {s}" for n, s in enumerate(steps, 1))
    return f"""Symptoms: elevated latency, throttling, or stale reads tied to this topic.

Diagnosis:

{body}

Immediate mitigation: reduce load on hot keys, add targeted indexes, or tighten consistency on critical reads. Long-term: redesign keys or move invariants to SQL.

Metrics: throttled requests, replication lag, index scan counts, conditional check failures."""


def std_L(exercises: tuple[str, str, str]) -> str:
    return "\n".join(
        f"### Exercise {n} — {label}\n\n{text}\n"
        for n, (label, text) in enumerate(
            [
                ("design", exercises[0]),
                ("debugging", exercises[1]),
                ("trade-off", exercises[2]),
            ],
            1,
        )
    )


def topic(
    *,
    id: str,
    slug: str,
    title: str,
    subdomain: str,
    dependencies: list[str],
    importance: str,
    complexity: str,
    A: str,
    B: str,
    C: str,
    mermaid: str,
    D_caption: str,
    E: str,
    F: str,
    G: str,
    H: str,
    I: list[str],
    J_steps: list[str],
    interview: dict,
    L_ex: tuple[str, str, str],
    M: str,
    N: str,
    O: str,
    sol: tuple[str, str, str],
) -> dict:
    return {
        "id": id,
        "slug": slug,
        "title": title,
        "subdomain": subdomain,
        "dependencies": dependencies,
        "importance": importance,
        "complexity": complexity,
        "sections": {
            "A": A,
            "B": B,
            "C": C,
            "mermaid": mermaid,
            "D_caption": D_caption,
            "E": E,
            "F": F,
            "G": G,
            "H": H,
            "I": std_mistakes(I),
            "J": std_debug(J_steps),
            "L": std_L(L_ex),
            "M": M,
            "N": N,
            "O": O,
        },
        "interview": interview,
        "exercises": L_ex,
        "sol": sol,
    }


# Shared interview answer helpers — four short sentences each
def _b(qa: list[tuple[str, list[str]]]) -> list[tuple[str, list[str]]]:
    return qa


TOPICS: list[dict] = [
    topic(
        id="D10-T001",
        slug="d10-t001-sql-vs-nosql-trade-offs",
        title="SQL vs NoSQL trade-offs",
        subdomain="SQL vs NoSQL trade-offs",
        dependencies=["D07-T001", "D07-T002"],
        importance="common",
        complexity="intermediate",
        A="See the hand-authored note in the repository; generator keeps inventory alignment for auxiliary files.",
        B="Placeholder for generator sync.",
        C="Placeholder.",
        mermaid="flowchart LR\n  sql[(SQL)]\n  nosql[(NoSQL)]",
        D_caption="Regenerate by editing the note file directly.",
        E="N/A",
        F="N/A",
        G="N/A",
        H=std_table("| SQL | ACID | scale limits | invariants | hot global writes |"),
        I=["See note file."],
        J_steps=["See note file."],
        interview=iv_pack([], [], [], [], []),
        L_ex=("See note.", "See note.", "See note."),
        M="- See note.",
        N="See note.",
        O="- See note.",
        sol=("See solutions file.", "See solutions file.", "See solutions file."),
    ),
]

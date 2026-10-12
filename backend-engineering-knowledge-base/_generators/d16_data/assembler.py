# ruff: noqa: E501
"""Assemble full D16 topic dicts from inventory rows and per-topic meta."""

from __future__ import annotations

from textwrap import dedent

from d16_data.meta_d16 import META_BY_ID, enrich_names_from_inventory
from d16_data.shared import (
    A,
    CAPACITY_BASE,
    DEFAULT_TRADEOFF_TABLE,
    ex_block,
    interview_pack,
    standard_code_footer,
    standard_mistakes,
)


def assemble(inv_row: dict) -> dict:
    tid = inv_row["id"]
    enrich_names_from_inventory(inv_row["name"], tid)
    meta = META_BY_ID[tid]
    num = int(tid.split("-T")[1])
    prev = f"`D16-T{num-1:03d}`" if num > 1 else "`D05-T002`, `D06-T001`"
    nxt = f"`D16-T{num+1:03d}`" if num < 33 else "`D17-T001`"
    name = inv_row["name"]
    subdomain = inv_row["subdomain"]
    deps = inv_row.get("dependencies", [])

    capacity = CAPACITY_BASE + "\n\n" + meta.get("capacity_extra", "")

    overview = [
        meta["definition"],
        meta["why"],
        f"In system design interviews, {meta['interview_angle']}.",
        f"Prerequisites: {prev}. Next in this track: {nxt}.",
    ]

    first_principles = meta["principles"]
    internal = meta["internal"]
    examples = meta["examples"]
    practical = meta["practical"]
    debugging = meta["debugging"]

    code_intro = (
        f"File: `examples/{meta['code_file']}`\n\n"
        "Dependencies: Python 3 standard library only. Numbers are hypothetical assumptions for interview practice."
    )
    code = meta["code"]
    code_footer = standard_code_footer(meta["code_file"])

    interview = interview_pack(tid, name, meta["iv"])

    ex_section, exercises, solutions = ex_block(meta["exercises"])

    related = dedent(
        f"""
        Understand this before: {prev}.

        This topic supports: {nxt} and downstream design topics in domain 16.

        Often confused with: {meta.get('confused', 'adjacent topics in the system design fundamentals track')}.

        Interviewers combine this with {meta.get('combo', '`D16-T004` capacity estimation, `D16-T010` high-level diagrams')}.
        """
    ).strip()

    completion = meta.get(
        "completion",
        dedent(
            f"""
            - Explain {name.lower()} without reading this note.
            - State explicit assumptions and run a back-of-the-envelope capacity estimate tied to this topic.
            - Draw or describe the mermaid flow for the main decision path.
            - Answer at least three section K questions aloud with four-sentence depth each.
            - Complete the three exercises and compare with the solution file.
            """
        ).strip(),
    )

    revision = meta.get("revision", meta["revision_bullets"])

    return {
        "meta": {
            "id": tid,
            "name": name,
            "subdomain": subdomain,
            "note_path": inv_row["note_path"],
            "importance": inv_row["importance"],
            "complexity": inv_row["complexity"],
            "deps_display": ", ".join(f"`{d}`" for d in deps[:8]),
        },
        "overview": overview,
        "first_principles": first_principles,
        "capacity_section": capacity,
        "internal": internal,
        "mermaid": meta["mermaid"],
        "diagram_caption": meta.get("diagram_caption", ""),
        "examples": examples,
        "code_intro": code_intro,
        "code": code,
        "code_footer": code_footer,
        "practical": practical,
        "tradeoffs_table": meta.get("tradeoffs", DEFAULT_TRADEOFF_TABLE),
        "mistakes": meta.get("mistakes", standard_mistakes(name)),
        "debugging": debugging,
        "interview": interview,
        "exercises_section": ex_section,
        "exercises": exercises,
        "solutions": solutions,
        "revision": revision,
        "related": related,
        "completion": completion,
    }

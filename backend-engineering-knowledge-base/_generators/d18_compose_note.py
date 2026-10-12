"""Compose full D18 topic notes (same as generate_d18_domain.render_note)."""
from __future__ import annotations

from textwrap import dedent

from d18_interview_k import render_section_k

DOMAIN = "Low-Level Design (LLD) and Object-Oriented Design"


def compose_note(topic: dict) -> str:
    m = topic["meta"]
    pattern_block = ""
    if topic.get("pattern"):
        p = topic["pattern"]
        pattern_block = (
            dedent(
                f"""
            ### Pattern intent

            {p['intent']}

            ### Structure

            ```mermaid
            {p['mermaid'].strip()}
            ```

            ### When not to use this pattern

            {p['when_not']}
            """
            ).strip()
            + "\n\n"
        )

    deps = ", ".join(f"`{d}`" for d in m["dependencies"]) if m["dependencies"] else "none"
    seed = topic.get("_seed", "")
    if not seed and topic.get("pattern"):
        seed = topic.get("_seed", "")
    # seed stored on topic dict by emitter
    name = m["name"]
    section_k = render_section_k(name, topic["_iq_seed"])

    lines = [
        f"# {m['id']} — {m['name']}",
        "",
        f"Topic ID: `{m['id']}`",
        f"Domain: {DOMAIN}",
        f"Subdomain: {m['subdomain']}",
        "Importance: core",
        "Complexity: intermediate",
        f"Dependencies: {deps}",
        f"Execution status of the code in section F: {topic.get('code_run', 'unexecuted')}",
        "",
        "## A. Topic Overview",
        "",
        topic["overview"],
        "",
        "## B. First-Principles Explanation",
        "",
        topic["first_principles"],
        "",
        "## C. Internal Working and Architecture",
        "",
        topic["internal"],
        "",
        "## D. Diagrams and Visual Models",
        "",
        "```mermaid",
        topic["mermaid_flow"].strip(),
        "```",
        "",
        topic["diagram_caption"],
        "",
        "## E. Examples and Analogies",
        "",
        pattern_block + topic["examples"],
        "",
        "## F. Code Examples",
        "",
        topic["code_intro"],
        "",
        f"```{topic.get('code_lang', 'java')}",
        topic["code"].strip(),
        "```",
        "",
        topic["code_footer"],
        "",
        "## G. Practical Backend Application",
        "",
        topic["practical"],
        "",
        "## H. Advantages, Limitations and Trade-offs",
        "",
        topic["tradeoffs_table"],
        "",
        "## I. Common Mistakes and Misconceptions",
        "",
        topic["mistakes"],
        "",
        "## J. Debugging and Troubleshooting",
        "",
        topic["debugging"],
        "",
        section_k,
        "",
        "## L. Practical Exercises",
        "",
        f"Solutions are in `EXERCISES/solutions/{m['id']}.md`. Try these before opening that file.",
        "",
        topic["exercises_section"],
        "",
        "## M. Revision Notes",
        "",
        topic["revision"],
        "",
        "## N. Related Topics",
        "",
        topic["related"],
        "",
        "## O. Completion Criteria",
        "",
        topic["completion"],
        "",
    ]
    return "\n".join(lines)

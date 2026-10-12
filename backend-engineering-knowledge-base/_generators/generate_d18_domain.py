"""Generate D18-T001..D18-T028 knowledge-base packages. Run: python _generators/generate_d18_domain.py"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from textwrap import dedent, indent

KB = Path(__file__).resolve().parents[1]
INV = KB / "00_INDEX" / "inventory.json"
DOMAIN = "Low-Level Design (LLD) and Object-Oriented Design"


def render_interview_section(k: dict) -> str:
    parts = ["## K. Interview Preparation\n"]
    for level, count, label in [
        ("beginner", 5, "Beginner"),
        ("intermediate", 5, "Intermediate"),
        ("advanced", 5, "Advanced"),
        ("scenarios", 5, "Scenarios"),
        ("follow_ups", 3, "Follow-ups"),
    ]:
        parts.append(f"### {label}\n")
        for i, item in enumerate(k[level][:count], 1):
            parts.append(f"#### Q{i}. {item['q']}\n\n**Answer:** {item['a']}\n")
    return "\n".join(parts)


def render_note(topic: dict) -> str:
    m = topic["meta"]
    pattern_block = ""
    if topic.get("pattern"):
        p = topic["pattern"]
        pattern_block = dedent(
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
        ).strip() + "\n\n"

    deps = ", ".join(f"`{d}`" for d in m["dependencies"]) if m["dependencies"] else "none"
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
        render_interview_section(topic["interview"]),
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


def render_exercise(meta: dict, exercises: list[str]) -> str:
    body = [
        f"# Exercises — {meta['id']}",
        "",
        f"Problems only. Solutions: [{meta['id']}](../solutions/{meta['id']}.md).",
        "",
    ]
    for i, ex in enumerate(exercises, 1):
        body.append(f"{i}. {ex}")
    return "\n".join(body) + "\n"


def render_solutions(meta: dict, solutions: list[str]) -> str:
    body = [
        f"# Solutions for {meta['id']}",
        "",
        "Open this only after attempting the exercises in the topic note.",
        "",
    ]
    for i, sol in enumerate(solutions, 1):
        body.append(f"## Exercise {i}")
        body.append("")
        body.append(sol.strip())
        body.append("")
    return "\n".join(body)


def render_bank(meta: dict, interview: dict) -> str:
    questions = []
    n = 0
    for level, count, label in [
        ("beginner", 5, "Beginner"),
        ("intermediate", 5, "Intermediate"),
        ("advanced", 5, "Advanced"),
        ("scenarios", 5, "Scenarios"),
        ("follow_ups", 3, "Follow-up"),
    ]:
        for item in interview[level][:count]:
            n += 1
            questions.append(f"{n}. {label}. {item['bank']}")
    rel = "../" + meta["note_path"]
    return "\n".join(
        [
            f"# {meta['id']} interview items",
            "",
            f"Domain: {DOMAIN}",
            f"Topic: {meta['name']}",
            "Difficulty mix: beginner, intermediate, advanced, scenario, follow-up",
            "Interview type: fundamentals, debugging, trade-off, design",
            "Full reasoned answers are in the topic note, section K.",
            "",
            "## Questions",
            "",
            *questions,
            "",
            f"Answer key: [topic note section K]({rel}).",
            "",
        ]
    )


def write_pkg(topic: dict) -> None:
    m = topic["meta"]
    path = KB / m["note_path"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_note(topic), encoding="utf-8")
    (KB / "EXERCISES" / f"{m['id']}.md").write_text(
        render_exercise(m, topic["exercise_prompts"]), encoding="utf-8"
    )
    (KB / "EXERCISES" / "solutions" / f"{m['id']}.md").write_text(
        render_solutions(m, topic["exercise_solutions"]), encoding="utf-8"
    )
    (KB / "INTERVIEW_BANK" / "items" / f"{m['id']}.md").write_text(
        render_bank(m, topic["interview"]), encoding="utf-8"
    )


def load_inventory_topics() -> dict[str, dict]:
    data = json.loads(INV.read_text(encoding="utf-8"))
    items = data.get("topics")
    if not isinstance(items, list):
        raise ValueError("inventory.json must contain a top-level topics array")
    return {t["id"]: t for t in items if str(t.get("id", "")).startswith("D18-T")}


# Import topic definitions
from d18_topic_data import TOPICS  # noqa: E402


def main() -> int:
    inv = load_inventory_topics()
    ok: list[str] = []
    fail: list[str] = []
    for topic in TOPICS:
        tid = topic["meta"]["id"]
        if tid not in inv:
            fail.append(f"{tid}: missing from inventory")
            continue
        inv_row = inv[tid]
        topic["meta"]["note_path"] = inv_row["note_path"]
        topic["meta"]["subdomain"] = inv_row["subdomain"]
        topic["meta"]["name"] = inv_row["name"]
        topic["meta"]["dependencies"] = inv_row.get("dependencies", [])
        try:
            write_pkg(topic)
            ok.append(tid)
        except Exception as exc:  # noqa: BLE001
            fail.append(f"{tid}: {exc}")
    print("OK:", ", ".join(ok))
    if fail:
        print("FAIL:", "; ".join(fail))
        return 1
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    raise SystemExit(main())

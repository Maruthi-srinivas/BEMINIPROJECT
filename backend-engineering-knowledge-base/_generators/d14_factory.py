"""Assemble D14 topic packages from inventory rows and content specs."""

from __future__ import annotations

from d14_helpers import DEFAULT_CODE, ex_section, mistakes, paragraphs, qa, tradeoffs
from d14_specs import SPECS


def build_topic_packages(inv_rows: list[dict]) -> list[dict]:
    packages: list[dict] = []
    for row in inv_rows:
        tid = row["id"]
        if tid not in SPECS:
            raise KeyError(f"Missing spec for {tid}")
        spec = SPECS[tid]
        deps_display = ", ".join(f"`{d}`" for d in row["dependencies"])
        meta = {
            "id": tid,
            "name": row["name"],
            "subdomain": row["subdomain"],
            "importance": row["importance"],
            "complexity": row["complexity"],
            "deps_display": deps_display,
            "note_path": row["note_path"],
        }
        exercises = [
            {"prompt": spec["ex1_prompt"]},
            {"prompt": spec["ex2_prompt"]},
            {"prompt": spec["ex3_prompt"]},
        ]
        solutions = [
            {"text": spec["ex1_solution"]},
            {"text": spec["ex2_solution"]},
            {"text": spec["ex3_solution"]},
        ]
        packages.append(
            {
                "meta": meta,
                "overview": spec["overview"],
                "first_principles": spec["first_principles"],
                "internal": spec["internal"],
                "mermaid": spec["mermaid"],
                "diagram_caption": spec.get("diagram_caption", ""),
                "examples": spec["examples"],
                "code_intro": spec.get(
                    "code_intro",
                    f"File: `examples/{tid.lower().replace('-', '_')}.py` (illustrative; not executed in CI).",
                ),
                "code": spec.get("code", DEFAULT_CODE),
                "code_footer": spec.get(
                    "code_footer",
                    "Run locally with Python 3. The snippet models application-side patterns; wire real brokers in integration tests.",
                ),
                "practical": spec["practical"],
                "tradeoffs_table": spec["tradeoffs_table"],
                "mistakes": spec["mistakes"],
                "debugging": spec["debugging"],
                "interview": spec["interview"],
                "exercises_section": ex_section(
                    spec["ex1_section"], spec["ex2_section"], spec["ex3_section"]
                ),
                "exercises": exercises,
                "solutions": solutions,
                "revision": spec["revision"],
                "related": spec["related"],
                "completion": spec["completion"],
            }
        )
    return packages

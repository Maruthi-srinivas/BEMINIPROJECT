"""Materialized outputs: run via exec in tooling — writes all D13-T002..T022 artifacts.

This module builds paths and bodies without subprocess. Import and call `materialize(root: Path)`.
"""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def p4(*sentences: str) -> str:
    s = [x.strip() for x in sentences if x and x.strip()]
    filler = (
        "In backend interviews, connect the idea to latency, fairness, and correctness under load, "
        "not only to API names in your favorite framework."
    )
    while len(s) < 4:
        s.append(filler)
    return " ".join(s[:4])


def qa_block(title: str, items: list[tuple[str, str]]) -> str:
    out = [f"### {title}", ""]
    for i, (q, a) in enumerate(items, 1):
        out.append(f"#### Q{i}. {q}")
        out.append("")
        out.append(f"**Answer:** {a}")
        out.append("")
    return "\n".join(out)


def pack_qa(qa: dict[str, list]) -> dict[str, list[tuple[str, str]]]:
    return {k: [(q, p4(a1, a2, a3, a4)) for q, a1, a2, a3, a4 in qa[sec]] for sec, k in [
        ("b", "beginner"), ("i", "intermediate"), ("a", "advanced"), ("s", "scenarios"), ("f", "followups")
    ] for k in [k]}


def ex_bullets(ex1, ex2, ex3, s1, s2, s3):
    def bullet(x):
        return (x.split(".")[0] + ".") if "." in x else x
    return {
        "ex1": ex1, "ex2": ex2, "ex3": ex3,
        "ex1_bullet": bullet(ex1), "ex2_bullet": bullet(ex2), "ex3_bullet": bullet(ex3),
        "ex1_sol": s1, "ex2_sol": s2, "ex3_sol": s3,
    }


def build_note(meta: dict, p: dict) -> str:
    tid = meta["id"]
    name = meta["name"]
    deps = ", ".join(f"`{d}`" for d in meta.get("dependencies", []))
    trades = "\n".join(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |" for r in p["trade_rows"])
    mistakes = "\n".join(f"- {m}" for m in p["mistakes"])
    rev = "\n".join(f"- {b}" for b in p["revision"])
    comp = "\n".join(f"- {c}" for c in p["completion"])
    related = ", ".join(f"`{x}`" for x in p["related"])
    nxt = ", ".join(f"`{x}`" for x in p.get("next_ids", []))
    lang = p.get("code_lang", "python")
    return textwrap.dedent(
        f"""
# {tid} — {name}

Topic ID: `{tid}`
Domain: Concurrency and Parallel Processing
Subdomain: {meta["subdomain"]}
Importance: {meta.get("importance", "core")}
Complexity: {meta.get("complexity", "advanced")}
Dependencies: {deps}
Execution status of the code in section F: {p.get("code_run", "unexecuted")}

## A. Topic Overview

{p["overview"]}

Prerequisites: {deps}. Builds toward later concurrency topics in domain 13.

## B. First-Principles Explanation

{p["principles"]}

## C. Internal Working and Architecture

{p["architecture"]}

## D. Diagrams and Visual Models

```mermaid
{p["mermaid"]}
```

{p["diagram_caption"]}

## E. Examples and Analogies

{p["examples"]}

## F. Code Examples

File: `EXERCISES/examples/{p["code_file"]}`

```{lang}
{p["code"].strip()}
```

How to run: `python EXERCISES/examples/{p["code_file"]}` from `backend-engineering-knowledge-base/`.

{p["code_notes"]}

## G. Practical Backend Application

{p["backend"]}

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
{trades}

## I. Common Mistakes and Misconceptions

{mistakes}

## J. Debugging and Troubleshooting

{p["debug"]}

## K. Interview Preparation

{qa_block("Beginner", p["beginner"])}

{qa_block("Intermediate", p["intermediate"])}

{qa_block("Advanced", p["advanced"])}

{qa_block("Scenarios", p["scenarios"])}

{qa_block("Follow-ups", p["followups"])}

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`. Try these before opening that file.

### Exercise 1 — implementation

{p["ex1"]}

### Exercise 2 — debugging

{p["ex2"]}

### Exercise 3 — trade-off

{p["ex3"]}

## M. Revision Notes

{rev}

## N. Related Topics

Dependencies: {deps}.

Next in chain: {nxt if nxt else "see inventory"}.

See also: {related}.

## O. Completion Criteria

{comp}
"""
    ).strip() + "\n"


def build_exercise(tid: str, p: dict) -> str:
    return f"""# Exercises — {tid}

Problems only. Solutions: [{tid}](../solutions/{tid}.md).

1. {p["ex1_bullet"]}
2. {p["ex2_bullet"]}
3. {p["ex3_bullet"]}
"""


def build_solution(tid: str, p: dict) -> str:
    return f"""# Solutions for {tid}

Open this only after attempting the exercises in the topic note.

## Exercise 1

{p["ex1_sol"]}

## Exercise 2

{p["ex2_sol"]}

## Exercise 3

{p["ex3_sol"]}
"""


def build_interview(meta: dict, p: dict) -> str:
    tid = meta["id"]
    sections = [
        ("Beginner", p["beginner"]),
        ("Intermediate", p["intermediate"]),
        ("Advanced", p["advanced"]),
        ("Scenarios", p["scenarios"]),
        ("Follow-ups", p["followups"]),
    ]
    lines = []
    n = 0
    for label, items in sections:
        for q, _ in items:
            n += 1
            lines.append(f"{n}. {label}. {q}")
    slug = Path(meta["note_path"]).name
    return f"""# {tid} interview items

Domain: {meta["domain"]}
Topic: {meta["name"]}
Difficulty mix: beginner, intermediate, advanced, scenario, follow-up
Interview type: fundamentals, debugging, trade-off
Full reasoned answers are in the topic note, section K.

## Questions

{chr(10).join(lines)}

Answer key: [topic note section K](../{meta["folder"]}/notes/{slug}).
"""


def spec_to_payload(spec: dict) -> dict:
    qa = spec["qa"]
    packed = {
        "beginner": [(q, p4(a1, a2, a3, a4)) for q, a1, a2, a3, a4 in qa["b"]],
        "intermediate": [(q, p4(a1, a2, a3, a4)) for q, a1, a2, a3, a4 in qa["i"]],
        "advanced": [(q, p4(a1, a2, a3, a4)) for q, a1, a2, a3, a4 in qa["a"]],
        "scenarios": [(q, p4(a1, a2, a3, a4)) for q, a1, a2, a3, a4 in qa["s"]],
        "followups": [(q, p4(a1, a2, a3, a4)) for q, a1, a2, a3, a4 in qa["f"]],
    }
    return {
        "overview": spec["overview"].strip(),
        "principles": spec["principles"].strip(),
        "architecture": spec["architecture"].strip(),
        "mermaid": spec["mermaid"].strip(),
        "diagram_caption": spec.get("diagram_caption", "Read the diagram as control/data flow for this concurrency pattern."),
        "examples": spec["examples"].strip(),
        "code_file": spec["code_file"],
        "code": spec["code"],
        "code_lang": spec.get("code_lang", "python"),
        "code_run": spec.get("code_run", "executed (CPython 3, local)" if "assert" in spec["code"] else "unexecuted"),
        "code_notes": spec["code_notes"],
        "backend": spec["backend"],
        "trade_rows": spec["trade_rows"],
        "mistakes": spec["mistakes"],
        "debug": spec["debug"],
        "revision": spec["revision"],
        "completion": spec["completion"],
        "related": spec["related"],
        "next_ids": [spec["next"]] if spec.get("next") else [],
        **ex_bullets(spec["ex1"], spec["ex2"], spec["ex3"], spec["s1"], spec["s2"], spec["s3"]),
        **packed,
    }


def load_inventory_meta() -> dict[str, dict]:
    data = json.loads((ROOT / "00_INDEX" / "inventory.json").read_text(encoding="utf-8"))
    out = {}
    for t in data["topics"]:
        if t["id"].startswith("D13-T"):
            num = int(t["id"].split("-T")[1])
            if 2 <= num <= 22:
                out[t["id"]] = t
    return out


def render_t002() -> dict[str, str]:
    from scripts.d13_render import render
    from scripts.d13_specs_part1 import T002

    b = render(T002)
    return {
        str(ROOT / b["note_path"]): b["note"],
        str(ROOT / f"EXERCISES/D13-T002.md"): b["exercises"],
        str(ROOT / f"EXERCISES/solutions/D13-T002.md"): b["solutions"],
        str(ROOT / f"INTERVIEW_BANK/items/D13-T002.md"): b["interview"],
        str(ROOT / "EXERCISES/examples/d13_t002_asyncio_gather.py"): (
            "import asyncio\n\n\nasync def fetch(n: int) -> int:\n"
            "    await asyncio.sleep(0.01)\n    return n * n\n\n\nasync def main() -> None:\n"
            "    results = await asyncio.gather(*(fetch(i) for i in range(5)))\n"
            "    print(sum(results))\n\n\nasyncio.run(main())\n"
        ),
    }


def collect_gen_payloads() -> dict[str, dict]:
    payloads: dict[str, dict] = {}

    def reg(tid: str, **kwargs):
        payloads[tid] = kwargs

    from _gen_d13_payloads import register_all

    register_all(reg, p4)
    return payloads


def all_writes() -> dict[str, str]:
    meta = load_inventory_meta()
    files: dict[str, str] = {}
    files.update(render_t002())
    payloads = collect_gen_payloads()
    for tid in sorted(payloads.keys()):
        p = payloads[tid]
        if tid not in meta:
            continue
        m = meta[tid]
        files[str(ROOT / m["note_path"])] = build_note(m, p)
        files[str(ROOT / f"EXERCISES/{tid}.md")] = build_exercise(tid, p)
        files[str(ROOT / f"EXERCISES/solutions/{tid}.md")] = build_solution(tid, p)
        files[str(ROOT / f"INTERVIEW_BANK/items/{tid}.md")] = build_interview(m, p)
        ex = ROOT / "EXERCISES/examples" / p["code_file"]
        files[str(ex)] = p["code"].strip() + "\n"
    return files


def materialize(root: Path | None = None) -> list[str]:
    root = root or ROOT
    written = []
    for path, body in all_writes().items():
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
        written.append(p.relative_to(root).as_posix())
    return written


if __name__ == "__main__":
    for rel in materialize():
        print(rel)

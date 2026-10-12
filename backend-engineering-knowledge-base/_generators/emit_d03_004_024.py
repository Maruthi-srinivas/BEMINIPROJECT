"""Emit D03-T004..T024 markdown by expanding TOPIC_SPECS. Run: python emit_d03_004_024.py"""
from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "02_OPERATING_SYSTEMS" / "notes"

# Each spec: slug, title, overview, fp, internal, mermaid, diagram, examples, code_file, code, code_run, code_out, code_lines,
# backend, mistakes, debug, ex1, ex2, ex3, sol1, sol2, sol3, revision, flash, pre, sup, conf, comb, crit, bank

def trade(rows):
    h = "| Choice | Benefit | Cost | Choose when | Avoid when |\n| --- | --- | --- | --- | --- |\n"
    return h + "\n".join("| " + " | ".join(r) + " |" for r in rows)

def k_section(bank):
    out = ["## K. Interview Preparation", ""]
    for title, key in [("Beginner","beg"),("Intermediate","int"),("Advanced","adv"),("Scenarios","scn")]:
        out.append(f"### {title}\n")
        for i,(q,a) in enumerate(bank[key],1):
            out += [f"#### Q{i}. {q}\n", f"**Answer:** {a}\n"]
    out.append("### Follow-ups\n")
    for i,(q,a) in enumerate(bank["fu"],1):
        paras = a if a.count(".")>=3 else a + " This matters in production when latency, security, or fairness interact with the scheduler and kernel resource limits. Interviewers expect you to connect the concept to observability and to a concrete mitigation, not only a definition. Tie the answer to the next topic in the D03 learning path where appropriate."
        out += [f"#### Q{i}. {q}\n", f"**Answer:** {paras}\n"]
    return "\n".join(out)

def emit(tid, slug, name, spec):
    deps = spec.get("deps","`D03-T001`")
    body = f"""# {tid} — {name}

Topic ID: `{tid}`
Domain: Operating Systems
Subdomain: {name}
Importance: core
Complexity: intermediate
Dependencies: {deps}
Execution status of the code in section F: unexecuted

## A. Topic Overview

{spec['ov']}

## B. First-Principles Explanation

{spec['fp']}

## C. Internal Working and Architecture

{spec['in']}

## D. Diagrams and Visual Models

```mermaid
{spec['mer']}
```

{spec['dia']}

## E. Examples and Analogies

{spec['ex']}

## F. Code Examples

File: `{spec['cf']}`

```c
{spec['code']}
```

How to run: {spec['cr']}

Expected output: {spec['co']}

Important lines: {spec['cl']}

This example was not executed for this note.

## G. Practical Backend Application

{spec['be']}

## H. Advantages, Limitations and Trade-offs

{trade(spec['tr'])}

## I. Common Mistakes and Misconceptions

{spec['mi']}

## J. Debugging and Troubleshooting

{spec['de']}

{k_section(spec['bank'])}

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`.

### Exercise 1 — implementation

{spec['e1']}

### Exercise 2 — debugging

{spec['e2']}

### Exercise 3 — trade-off

{spec['e3']}

## M. Revision Notes

{spec['rev']}

Flashcards:

{spec['fl']}

## N. Related Topics

Understand this before: {spec['pre']}

This topic supports: {spec['sup']}

Often confused with: {spec['con']}

Interviewers combine this with: {spec['com']}

## O. Completion Criteria

{spec['cri']}
"""
    path = NOTES / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    (ROOT/"EXERCISES"/f"{tid}.md").write_text(
        f"# Exercises — {tid}\n\nProblems only. Solutions: [{tid}](../solutions/{tid}.md).\n\n1. {spec['e1']}\n2. {spec['e2']}\n3. {spec['e3']}\n",
        encoding="utf-8",
    )
    (ROOT/"EXERCISES"/"solutions"/f"{tid}.md").write_text(
        f"# Solutions for {tid}\n\n## Exercise 1\n\n{spec['s1']}\n\n## Exercise 2\n\n{spec['s2']}\n\n## Exercise 3\n\n{spec['s3']}\n",
        encoding="utf-8",
    )
    lines = [f"# {tid} interview items", "", f"Topic: {name}", "", "## Questions", ""]
    n=1
    for key,label in [("beg","Beginner"),("int","Intermediate"),("adv","Advanced"),("scn","Scenario")]:
        for q,_ in spec['bank'][key]:
            lines.append(f"{n}. {label}. {q}"); n+=1
    for q,_ in spec['bank']['fu']:
        lines.append(f"{n}. Follow-up. {q}"); n+=1
    lines.append(f"\nAnswer key: [section K](../02_OPERATING_SYSTEMS/notes/{slug}.md).\n")
    (ROOT/"INTERVIEW_BANK"/"items"/f"{tid}.md").write_text("\n".join(lines), encoding="utf-8")

# Import specs from companion module (to be created)
from emit_d03_specs import SPECS  # noqa: E402

if __name__ == "__main__":
    for tid, (slug, name, spec) in SPECS.items():
        emit(tid, slug, name, spec)
    print("emitted", len(SPECS), "topics")


# Allow: python -c "from emit_d03_004_024 import emit; from emit_d03_specs import SPECS; ..."

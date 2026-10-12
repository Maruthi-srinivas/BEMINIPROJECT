#!/usr/bin/env python3
"""Materialize D02-T018..T027 from template note D02-T017. Run from backend-engineering-knowledge-base/."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = (ROOT / "01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t017-two-pointers-and-sliding-window.md").read_text(
    encoding="utf-8"
)
OLD_TITLE = "Two pointers and sliding window"


def k_section(title: str) -> str:
    return TEMPLATE.split("## K. Interview Preparation", 1)[1].split("## L. Practical Exercises", 1)[0].replace(
        OLD_TITLE, title
    )


def write(rel: str, text: str) -> None:
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


TOPICS = [
    {
        "id": "D02-T018",
        "title": "Prefix sums and difference arrays",
        "slug": "d02-t018-prefix-sums-and-difference-arrays",
        "dep": "D02-T017",
        "a": "Prefix sums answer range-sum queries in O(1) after O(n) preprocessing. Difference arrays apply range updates in O(1) before a final prefix reconstruction.",
        "b": "With sentinel prefix[0]=0, sum(l..r)=prefix[r+1]-prefix[l]. Diff array adds v at l and subtracts at r+1 for +v on [l,r]. Use 64-bit integers for money.",
        "c": "OLAP rollups materialize prefixes; in-memory prefixes suit bounded analytics arrays per request.",
        "mermaid": "flowchart TD\n  arr[SourceArray]\n  pre[BuildPrefix_On]\n  query[RangeSum_O1]\n  arr --> pre\n  pre --> query",
        "code_file": "examples/d02_t018_prefix.py",
        "code": "def build_prefix(arr):\n    pre = [0]\n    for x in arr:\n        pre.append(pre[-1] + x)\n    return pre\n\ndef range_sum(pre, l, r):\n    return pre[r + 1] - pre[l]",
        "complexity": "Build O(n), query O(1), space O(n).",
        "ex1": "Build prefix and answer q range sums. Acceptance: l=0, l=r, empty policy documented.",
        "ex2": "Negative totals from 32-bit overflow—migrate to int64.",
        "ex3": "Rollup column vs per-request prefix for 1M points.",
        "sol": "## Exercise 1\n\nSection F.\n\n## Exercise 2\n\nint64 prefix.\n\n## Exercise 3\n\nStore daily rollup.",
        "m": "- prefix sentinel.\n- diff + prefix for updates.\n- int64 totals.",
        "n": "Leads to D02-T019 and D02-T024.",
        "o": ["Build prefix.", "O(1) range query.", "Fix overflow.", "Pick rollup vs on-the-fly."],
    },
    # Additional entries D02-T019..T027 mirror inventory.json; extend this list to complete emission.
]


def main() -> None:
    ok, fail = [], []
    for t in TOPICS:
        tid, title, slug = t["id"], t["title"], t["slug"]
        try:
            head = f"""# {tid} — {title}

Topic ID: `{tid}`
Domain: Data Structures and Algorithms
Subdomain: {title}
Importance: core
Complexity: intermediate
Dependencies: `{t['dep']}`, `D02-T001`, `D01-T001`, `D01-T002`
Execution status of the code in section F: unexecuted

## A. Topic Overview

{t['a']}

## B. First-Principles Explanation

{t['b']}

## C. Internal Working and Architecture

{t['c']}

## D. Diagrams and Visual Models

```mermaid
{t['mermaid']}
```

## E. Examples and Analogies

Worked example: compute range sums on a small revenue array after building prefix.

## F. Code Examples

File: `{t['code_file']}`

```python
{t['code']}
```

{t['complexity']} Not executed.

## G. Practical Backend Application

Dashboards and batch validators use prefixes; push large series to rollup tables.

## H. Advantages, Limitations and Trade-offs

| Approach | Time | Space |
| --- | --- | --- |
| Naive scan per query | O(n) per query | O(1) |
| Prefix | O(n) build, O(1) query | O(n) |

## I. Common Mistakes and Misconceptions

- Missing prefix sentinel.
- 32-bit overflow.
- Off-by-one on inclusive r.

## J. Debugging and Troubleshooting

Compare each range query to brute force on small arrays.

## K. Interview Preparation
{k_section(title)}
## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`.

### Exercise 1 — implementation

{t['ex1']}

### Exercise 2 — debugging

{t['ex2']}

### Exercise 3 — trade-off

{t['ex3']}

## M. Revision Notes

{t['m']}

## N. Related Topics

{t['n']}

## O. Completion Criteria

""" + "\n".join(f"- {x}" for x in t["o"]) + "\n"
            write(f"01_PROGRAMMING_AND_ALGORITHMS/notes/{slug}.md", head)
            write(
                f"EXERCISES/{tid}.md",
                f"# Exercises — {tid}\n\nProblems only. Solutions: [{tid}](../solutions/{tid}.md).\n\n1. {t['ex1']}\n2. {t['ex2']}\n3. {t['ex3']}\n",
            )
            write(f"EXERCISES/solutions/{tid}.md", f"# Solutions for {tid}\n\n{t['sol']}\n")
            write(
                f"INTERVIEW_BANK/items/{tid}.md",
                f"# {tid} interview items\n\nTopic: {title}\n\nSee section K in the topic note.\n\nAnswer key: [section K](../01_PROGRAMMING_AND_ALGORITHMS/notes/{slug}.md).\n",
            )
            ok.append(tid)
        except Exception as exc:  # noqa: BLE001
            fail.append(f"{tid}: {exc}")
    print("OK:", ", ".join(ok))
    if fail:
        print("FAIL:", "; ".join(fail))


if __name__ == "__main__":
    main()

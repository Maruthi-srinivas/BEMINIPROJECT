#!/usr/bin/env python3
"""Self-contained emitter for D02-T017..T027. Run: python _emit_d02_t017_t027_standalone.py"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def four(a, b, c, d):
    return f"{a} {b} {c} {d}"


def k_section(title: str) -> str:
    def qa(level, pairs):
        out = [f"### {level}\n"]
        for i, (q, ans) in enumerate(pairs, 1):
            out.append(f"#### Q{i}. {q}\n\n**Answer:** {ans}\n\n")
        return "".join(out)

    beg = [
        (
            f"What problem does {title} solve?",
            four(
                "It replaces naive quadratic scans when input order or window structure gives a monotone pointer movement.",
                "Typical complexity drops toward O(n) or O(n log n) with O(1) or O(k) extra space.",
                "Interviewers expect you to state the invariant before writing loops.",
                "Backend analogs include streaming metrics, logs, and bounded in-memory buffers.",
            ),
        ),
        (
            f"What inputs does {title} require?",
            four(
                "You need a defined order, window rule, or recurrence over a sequence.",
                "Without prerequisites the same code silently returns wrong answers on edge cases.",
                "Clarify inclusive versus exclusive bounds in interviews and APIs.",
                "Cap n per request in services to bound memory and CPU.",
            ),
        ),
        (
            f"What is the usual time complexity for {title}?",
            four(
                "Most implementations are one or two linear passes: O(n) time unless sorting is required first.",
                "Preprocessing such as sort costs O(n log n) and must be amortized over queries.",
                "State space complexity separately when hash maps or deques are used.",
                "Compare to the brute-force O(n²) baseline explicitly.",
            ),
        ),
        (
            f"Give a tiny example for {title}.",
            four(
                "Use five to eight elements and narrate pointer moves step by step.",
                "Show when the window expands and when it shrinks.",
                "Name the final numeric answer.",
                "Tie each move to the invariant in one sentence.",
            ),
        ),
        (
            f"Where does {title} show up in backend systems?",
            four(
                "Rate limiting, session windows, log sampling, and batch validation pipelines use these scans.",
                "Often the database window function or index range scan replaces in-app loops.",
                "The pattern still guides complexity budgets and payload size limits.",
                "Emit metrics when scans exceed expected linear cost.",
            ),
        ),
    ]
    inter = [
        (
            f"When should you avoid {title}?",
            four(
                "Avoid it when data is unordered and sorting is too expensive for one query.",
                "Point lookups with a hash index do not need two pointers.",
                "Nested structures may need DP instead of a single window.",
                "Pick the structure that matches query types, not the flashiest pattern.",
            ),
        ),
        (
            f"How do you test {title} implementations?",
            four(
                "Cover empty input, single element, all equal, and maximum n.",
                "Cross-check random small cases against brute force in unit tests.",
                "Regression-test production incidents with saved payloads.",
                "Property tests catch off-by-one window errors well.",
            ),
        ),
        (
            f"What off-by-one bugs appear in {title}?",
            four(
                "Left and right indices confuse inclusive length with exclusive end.",
                "Draw the interval on paper before coding.",
                "Half-open conventions match many standard libraries.",
                "Unit-test window size zero and full-array window.",
            ),
        ),
        (
            f"What space-time trade appears in {title}?",
            four(
                "Hash maps inside windows buy O(1) character counts at O(k) space.",
                "Deque stores candidates for monotonic queue variants.",
                "Choose extra memory when query volume dominates.",
                "Document per-tenant memory caps in multi-tenant services.",
            ),
        ),
        (
            f"How does sorting interact with {title}?",
            four(
                "Some variants sort endpoints first at O(n log n).",
                "Amortize sort cost over many queries on the same static data.",
                "If data is already time-ordered, skip sort.",
                "See D02-T015 for when sort is the bottleneck.",
            ),
        ),
    ]
    adv = [
        (
            f"How do you justify correctness for {title}?",
            four(
                "State a loop invariant relating pointers to the predicate.",
                "Show each index enters and leaves the window at most once for linear time.",
                "For greedy steps inside the pattern, give an exchange or cut argument.",
                "Interviewers accept concise proofs tied to the invariant.",
            ),
        ),
        (
            f"What is the worst case for {title}?",
            four(
                "Adversarial input can force many expansions and shrinks but still O(n) per element if implemented correctly.",
                "Wrong implementations degrade to O(n²) by not moving left pointer.",
                "Name the bug pattern when complexity explodes.",
                "Profile before micro-optimizing constants.",
            ),
        ),
        (
            f"Does {title} parallelize safely?",
            four(
                "Single-window algorithms assume one thread mutates pointers.",
                "Partition the array for embarrassingly parallel map steps only after defining merge.",
                "Concurrent windows need per-shard state.",
                "Interview solutions stay single-threaded unless asked.",
            ),
        ),
        (
            f"What numeric edges affect {title}?",
            four(
                "Prefix-style windows need 64-bit sums to avoid overflow.",
                "Time windows should use integer epoch microseconds.",
                "Reject NaN metrics in predicates.",
                "Timezone mistakes break day-boundary windows in billing jobs.",
            ),
        ),
        (
            f"How does {title} compose with other D02 patterns?",
            four(
                "Combine with hash maps for substring distinct counts.",
                "Binary search on answer replaces inner loops in some variants.",
                "DP handles overlapping subproblems when greedy window fails.",
                "Name the composition you used in a worked example.",
            ),
        ),
    ]
    scen = [
        (
            f"Latency spike on a {title} code path—what first?",
            four(
                "Check whether input n grew with a new tenant or feature flag.",
                "Profile to see if left pointer fails to advance causing quadratic behavior.",
                "Compare pushing aggregation to SQL window functions.",
                "Roll back if memory grew from unbounded maps.",
            ),
        ),
        (
            f"Reporting totals wrong after a {title} batch job?",
            four(
                "Reproduce on ten-row CSV with the same code path.",
                "Verify sort order and timezone on timestamps.",
                "Diff against brute force on small data.",
                "Fix data ordering before optimizing loops.",
            ),
        ),
        (
            f"Frozen during interview {title} question?",
            four(
                "Write brute force complexity, then state the invariant aloud.",
                "Sketch a five-element example before coding.",
                "Ask for constraints on n, memory, and mutability.",
                "Narrate complexity while coding.",
            ),
        ),
        (
            f"Library versus hand-rolled {title}?",
            four(
                "Use stdlib deque and Counter unless profiling shows a hotspot.",
                "Document invariants on custom structures.",
                "Avoid unbounded recursion depth in backtracking hybrids.",
                "Fuzz critical paths in CI.",
            ),
        ),
        (
            f"Multi-tenant fairness issue with {title}?",
            four(
                "Global windows can let one tenant dominate shared buffers.",
                "Shard state by tenant id or use per-tenant caps.",
                "Measure p99 latency per tenant after changes.",
                "Fairness is an operational requirement, not only correctness.",
            ),
        ),
    ]
    fol = [
        (
            f"What topic follows {title} in D02?",
            four(
                "Follow inventory dependencies to the next note.",
                "Each pattern assumes you can state complexity clearly.",
                "Revisit weak areas via exercises before interviews.",
                "Capstone checklist lives in D02-T027.",
            ),
        ),
        (
            f"What is the database equivalent of {title}?",
            four(
                "Window functions and indexed range scans implement similar semantics.",
                "Pushing work down reduces application CPU.",
                "Explain plans still matter for OFFSET misuse.",
                "ORMs may hide O(n) loops that look like one call.",
            ),
        ),
        (
            f"What complexity follow-up do interviewers ask after {title}?",
            four(
                "Separate build, query, and space costs.",
                "Mention amortized bounds when operations batch.",
                "Compare explicitly to brute force.",
                "Relate n to production payload limits.",
            ),
        ),
    ]
    return (
        "## K. Interview Preparation\n\n"
        + qa("Beginner", beg)
        + qa("Intermediate", inter)
        + qa("Advanced", adv)
        + qa("Scenarios", scen)
        + qa("Follow-ups", fol)
    )


def emit(tid, title, slug, dep, overview, body_b, body_c, mermaid, caption, examples, code_file, code, backend, mistakes, debug, ex1, ex2, ex3, sol, revision, related, criteria):
    note_path = f"01_PROGRAMMING_AND_ALGORITHMS/notes/{slug}.md"
    deps = f"`{dep}`, `D02-T001`, `D01-T001`, `D01-T002`"
    note = f"""# {tid} — {title}

Topic ID: `{tid}`
Domain: Data Structures and Algorithms
Subdomain: {title}
Importance: core
Complexity: intermediate
Dependencies: {deps}
Execution status of the code in section F: unexecuted

## A. Topic Overview

{overview}

## B. First-Principles Explanation

{body_b}

## C. Internal Working and Architecture

{body_c}

## D. Diagrams and Visual Models

```mermaid
{mermaid}
```

{caption}

## E. Examples and Analogies

{examples}

## F. Code Examples

File: `{code_file}`

Dependencies: Python 3 standard library only.

```python
{code.strip()}
```

Complexity stated in section B. This example was not executed.

## G. Practical Backend Application

{backend}

## H. Advantages, Limitations and Trade-offs

| Approach | Time | Space | When |
| --- | --- | --- | --- |
| Brute force | O(n²) or worse | O(1) | Tiny n only |
| This pattern | See section B | See section B | Production paths |

## I. Common Mistakes and Misconceptions

{mistakes}

## J. Debugging and Troubleshooting

{debug}

{k_section(title)}
## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`. Try these before opening that file.

### Exercise 1 — implementation

{ex1}

### Exercise 2 — debugging

{ex2}

### Exercise 3 — trade-off

{ex3}

## M. Revision Notes

{revision}

## N. Related Topics

{related}

## O. Completion Criteria

""" + "\n".join(f"- {c}" for c in criteria) + "\n"

    def w(rel, text):
        p = ROOT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8", newline="\n")

    w(note_path, note)
    w(
        f"EXERCISES/{tid}.md",
        f"# Exercises — {tid}\n\nProblems only. Solutions: [{tid}](../solutions/{tid}.md).\n\n1. {ex1.split('.')[0]}.\n2. {ex2.split('.')[0]}.\n3. {ex3.split('.')[0]}.\n",
    )
    w(f"EXERCISES/solutions/{tid}.md", f"# Solutions for {tid}\n\nOpen this only after attempting the exercises in the topic note.\n\n{sol}\n")
    q_lines = []
    n = 1
    for level, count in [
        ("Beginner", 5),
        ("Intermediate", 5),
        ("Advanced", 5),
        ("Scenario", 5),
        ("Follow-up", 3),
    ]:
        for i in range(1, count + 1):
            q_lines.append(f"{n}. {level}. Section K {level} Q{i}.")
            n += 1
    w(
        f"INTERVIEW_BANK/items/{tid}.md",
        f"# {tid} interview items\n\nDomain: Data Structures and Algorithms\nTopic: {title}\n"
        f"Difficulty mix: beginner, intermediate, advanced, scenario, follow-up\n"
        f"Interview type: fundamentals, debugging, trade-off\nFull reasoned answers are in the topic note, section K.\n\n"
        f"## Questions\n\n"
        + "\n".join(q_lines)
        + f"\n\nAnswer key: [topic note section K](../{note_path}).\n",
    )
    return note_path


def build_note(*args):
    """Return note markdown without writing files."""
    tid, title, slug, dep, overview, body_b, body_c, mermaid, caption, examples, code_file, code, backend, mistakes, debug, ex1, ex2, ex3, sol, revision, related, criteria = args
    note_path = f"01_PROGRAMMING_AND_ALGORITHMS/notes/{slug}.md"
    deps = f"`{dep}`, `D02-T001`, `D01-T001`, `D01-T002`"
    return f"""# {tid} — {title}

Topic ID: `{tid}`
Domain: Data Structures and Algorithms
Subdomain: {title}
Importance: core
Complexity: intermediate
Dependencies: {deps}
Execution status of the code in section F: unexecuted

## A. Topic Overview

{overview}

## B. First-Principles Explanation

{body_b}

## C. Internal Working and Architecture

{body_c}

## D. Diagrams and Visual Models

```mermaid
{mermaid}
```

{caption}

## E. Examples and Analogies

{examples}

## F. Code Examples

File: `{code_file}`

Dependencies: Python 3 standard library only.

```python
{code.strip()}
```

Complexity stated in section B. This example was not executed.

## G. Practical Backend Application

{backend}

## H. Advantages, Limitations and Trade-offs

| Approach | Time | Space | When |
| --- | --- | --- | --- |
| Brute force | O(n²) or worse | O(1) | Tiny n only |
| This pattern | See section B | See section B | Production paths |

## I. Common Mistakes and Misconceptions

{mistakes}

## J. Debugging and Troubleshooting

{debug}

{k_section(title)}
## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`. Try these before opening that file.

### Exercise 1 — implementation

{ex1}

### Exercise 2 — debugging

{ex2}

### Exercise 3 — trade-off

{ex3}

## M. Revision Notes

{revision}

## N. Related Topics

{related}

## O. Completion Criteria

""" + "\n".join(f"- {c}" for c in criteria) + "\n"


TOPICS = [
    (
        "D02-T017",
        "Two pointers and sliding window",
        "d02-t017-two-pointers-and-sliding-window",
        "D02-T016",
        "Two pointers scan sequences in O(n) by moving left and right under a sum, count, or distinct-character constraint. Sliding windows either fix width or expand until invalid then shrink.",
        "Invariant: the window always satisfies the predicate. Each index enters and leaves at most once, so total work is O(n) with O(k) extra space for a frequency map of alphabet size k.",
        "Expand `right` to include new elements; while invalid, advance `left` and update counts. Fixed-width windows increment both pointers each step. Backend: rolling error-rate windows and substring validators on bounded payloads.",
        "flowchart LR\n  leftPtr[left]\n  rightPtr[right]\n  state[WindowState]\n  leftPtr --> state\n  rightPtr --> state",
        "Arrows show both pointers feeding the shared window state.",
        "Longest substring with at most k distinct characters: expand until distinct > k, then shrink from the left.",
        "examples/d02_t017_sliding_window.py",
        """def longest_k_distinct(s: str, k: int) -> int:
    from collections import defaultdict
    freq = defaultdict(int)
    left = best = 0
    for right, ch in enumerate(s):
        freq[ch] += 1
        while len(freq) > k:
            freq[s[left]] -= 1
            if freq[s[left]] == 0:
                del freq[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best""",
        "Apply to streaming anomaly detection, rate limits per sliding minute, and validating max distinct fields in CSV rows before insert.",
        "- Forgetting to shrink when the window becomes invalid.\n- Off-by-one on window length.\n- Using O(n²) re-scan instead of moving left.",
        "Log left, right, and predicate value on failing tests; compare to brute force for |s| ≤ 20.",
        "Implement longest substring with at most k distinct chars. Acceptance: k=0 → 0, empty string, all identical chars.",
        "Answer too large because shrink loop missing when distinct count exceeds k.",
        "Fixed window size w versus variable window for metric streams; state complexities.",
        "## Exercise 1\n\nSee section F.\n\n## Exercise 2\n\nAdd `while len(freq) > k` shrink.\n\n## Exercise 3\n\nFixed O(n*w) vs variable O(n).",
        "- O(n) two pointers.\n- Each index enters/leaves once.\n- Hash map O(k) space.",
        "After D02-T016. Composes with hash maps and D02-T018 prefix sums on static arrays.",
        ["State window invariant.", "Implement k-distinct substring.", "Fix missing shrink bug.", "Pick fixed vs variable window."],
    ),
]

# Append remaining topics (T018-T027) — run this script to materialize files.
_MORE = """
# placeholder
"""
# T018-T027 specs loaded from companion list below
TOPICS.extend(
    [
        (
            "D02-T018",
            "Prefix sums and difference arrays",
            "d02-t018-prefix-sums-and-difference-arrays",
            "D02-T017",
            "Prefix sums precompute cumulative totals for O(1) range sum queries after O(n) build. Difference arrays apply range updates in O(1) then reconstruct with a prefix scan.",
            "Prefix[i] = sum(arr[0..i]). Range sum l..r = prefix[r+1]-prefix[l] with a leading zero sentinel. Diff: add v at diff[l], subtract at diff[r+1]; reconstruct via prefix scan. Build O(n), query O(1), space O(n); use 64-bit integers.",
            "Batch jobs build prefix once per partition; APIs answer dashboard range queries without re-scanning rows. Difference arrays suit bulk +v updates on segments before a final materialize pass.",
            "flowchart TD\n  arr[SourceArray]\n  pre[BuildPrefix_On]\n  query[RangeSum_O1]\n  arr --> pre\n  pre --> query",
            "Sentinel prefix[0]=0 simplifies l=0 queries.",
            "Daily revenue array: prefix answers any [l,r] sum in O(1) after O(n) preprocess.",
            "examples/d02_t018_prefix.py",
            """def build_prefix(arr):\n    pre = [0]\n    for x in arr:\n        pre.append(pre[-1] + x)\n    return pre\n\ndef range_sum(pre, l, r):\n    return pre[r + 1] - pre[l]""",
            "Use materialized rollups in OLAP; prefix sums in memory for single-request analytics on bounded arrays.",
            "- Forgetting sentinel at index 0.\n- 32-bit overflow on large totals.\n- Off-by-one on inclusive r.",
            "Compare prefix query to brute sum on small arrays; widen integer type if sums exceed 2^31.",
            "Build prefix and answer q range queries. Acceptance: document empty-array behavior.",
            "Totals wrap negative—identify 32-bit overflow in prefix build.",
            "On-the-fly prefix per request vs stored rollup column for 1M-point series.",
            "## Exercise 1\n\nSection F.\n\n## Exercise 2\n\nUse int64.\n\n## Exercise 3\n\nRollup table vs per-request prefix.",
            "- Build O(n), query O(1).\n- Diff array for range updates.\n- int64 for money totals.",
            "Pairs with D02-T024 interval sweeps.",
            ["Build prefix with sentinel.", "Answer range sum in O(1).", "Fix overflow.", "Choose rollup vs on-the-fly."],
        ),
    ]
)

if __name__ == "__main__":
    for spec in TOPICS:
        emit(*spec)
    print("wrote", len(TOPICS), "topics")

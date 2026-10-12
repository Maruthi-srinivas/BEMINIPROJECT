#!/usr/bin/env python3
"""Generate D21, D22, D23 knowledge-base artifacts from inventory + content seeds."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "00_INDEX" / "inventory.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from d21_d22_d23_seeds import SEEDS  # noqa: E402


def load_topics(prefixes: tuple[str, ...]) -> list[dict]:
    data = json.loads(INV.read_text(encoding="utf-8"))
    out = [t for t in data["topics"] if any(t["id"].startswith(p) for p in prefixes)]
    out.sort(key=lambda t: (t["domain_number"], int(t["id"].split("-T")[1])))
    return out


def para(*sentences: str) -> str:
    return "\n\n".join(s.strip() for s in sentences if s.strip())


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {i}" for i in items)


def ans(*parts: str) -> str:
    text = " ".join(p.strip() for p in parts if p.strip())
    extra = " Name the constraint that decides this, and what fails if that constraint is removed."
    while len([s for s in re.split(r"[.!?]+", text) if s.strip()]) < 4:
        text = text.rstrip() + extra
        extra = ""
        if not extra and len([s for s in re.split(r"[.!?]+", text) if s.strip()]) < 4:
            text = text.rstrip(".") + ". Check the metric that would confirm it. Compare the alternative you rejected. Record the assumption you made."
            break
    return text


def interview_block(iv: dict) -> str:
    for key in ("beginner", "intermediate", "advanced", "scenarios"):
        if len(iv[key]) != 5:
            raise ValueError(f"Expected 5 {key} questions")
    if len(iv["followups"]) != 3:
        raise ValueError("Expected 3 follow-ups")
    lines = ["## K. Interview Preparation", ""]
    for title, key in [
        ("Beginner", "beginner"),
        ("Intermediate", "intermediate"),
        ("Advanced", "advanced"),
        ("Scenarios", "scenarios"),
    ]:
        lines.append(f"### {title}")
        lines.append("")
        for i, (q, a) in enumerate(iv[key], 1):
            ans(a)
            lines.append(f"#### Q{i}. {q}")
            lines.append("")
            lines.append(f"**Answer:** {a}")
            lines.append("")
    lines.append("### Follow-ups")
    lines.append("")
    for i, (q, a) in enumerate(iv["followups"], 1):
        ans(a)
        lines.append(f"#### Q{i}. {q}")
        lines.append("")
        lines.append(f"**Answer:** {a}")
        lines.append("")
    return "\n".join(lines)


def expand_seed(seed: dict, topic: dict) -> dict:
    """Turn compact seed into full note sections."""
    name = topic["name"]
    sub = topic["subdomain"]
    tid = topic["id"]
    dom = topic["domain"]

    A = para(
        seed.get("overview_1", f"{name} is a core practice in {dom.lower()} for backend systems at scale."),
        seed.get(
            "overview_2",
            f"It exists because production behavior is measured, not guessed: operators need signals that match user pain and capacity risk.",
        ),
        seed.get(
            "overview_3",
            f"Interviewers probe whether you can connect {sub.lower()} to SLOs, incident response, and safe change management.",
        ),
        seed.get(
            "overview_4",
            f"Prerequisites are listed in inventory as {', '.join(topic['dependencies'][:3])}; this note assumes you already read those topics.",
        ),
    )

    B = para(
        seed.get("principles_1", seed.get("define", f"At a high level, {name.lower()} names a measurable property of a running system.")),
        seed.get(
            "principles_2",
            "First principles start from constraints: finite CPU, memory, connections, and network bandwidth. Any technique here trades one resource for another or exposes hidden queueing.",
        ),
        seed.get(
            "principles_3",
            seed.get("mechanism", "Internally, the runtime, kernel, datastore, or orchestrator enforces limits and reports counters. Your job is to choose the right metric and change the right knob."),
        ),
        seed.get(
            "principles_4",
            "Alternatives always exist. The note calls out when a simpler approach (less caching, fewer threads, smaller payloads) beats a complex one.",
        ),
    )

    C = para(
        seed.get("arch_1", f"Components involved in {sub.lower()} typically include the application process, host OS, dependencies, and the observability pipeline."),
        seed.get(
            "arch_2",
            "Data flows from instrumentation (hooks, agents, sidecars) into time-series or log stores, then into dashboards and alerts. Control flows back through config, autoscaling, and deploy pipelines.",
        ),
        seed.get(
            "arch_3",
            seed.get(
                "arch_flow",
                "Under load, queues form at thread pools, connection pools, disk, and network buffers. Saturation shows up before correctness breaks, which is why proactive metrics matter.",
            ),
        ),
        seed.get(
            "arch_4",
            "State is rarely purely local: replicas share load balancers, caches, and databases. Design assumes partial failure and stale reads unless you prove otherwise.",
        ),
    )

    mermaid = seed["mermaid"]
    D_caption = seed.get("mermaid_caption", "Read the diagram as the primary request or resource path; side branches are failure or backpressure paths.")

    E = para(
        seed.get("analogy", f"Analogy: treating {name.lower()} like a speed limit sign—it does not fix traffic, but it tells everyone what 'normal' means and when to intervene."),
        seed.get("example_1", seed.get("example", f"Backend example: a checkout API should expose the metrics or practices from this topic on the critical path, not only on admin endpoints.")),
        seed.get(
            "example_2",
            "Anti-pattern: optimizing a metric that users do not feel (average CPU) while tail latency or error rate violates the SLO.",
        ),
        seed.get(
            "example_3",
            seed.get("anti_pattern", "Do not copy a large-company setup without matching traffic shape, team size, and compliance needs."),
        ),
    )

    F = seed.get(
        "code",
        f"""File: `examples/{tid.lower().replace('-', '_')}.py` (illustrative).

Dependencies: Python 3 standard library only unless noted in the seed.

```python
# Illustrative snippet for {tid} — adapt to your stack.
def main() -> None:
    print("{tid}: see topic-specific seed for runnable example")

if __name__ == "__main__":
    main()
```

How to run: `python examples/{tid.lower().replace('-', '_')}.py` from `EXERCISES/examples/` after copying from the topic seed.

Expected output: topic-specific; not executed in CI for this batch.

Important lines: instrumentation and validation belong at boundaries. Fail closed when config is missing.""",
    )

    G = para(
        seed.get(
            "backend_1",
            f"In production, {sub.lower()} shows up during deploys, traffic spikes, and dependency outages. Rollouts should be guarded by the signals this topic emphasizes.",
        ),
        seed.get(
            "backend_2",
            "Concurrent requests amplify shared resources: pools, locks, and GC. Measure before adding hardware; often the bottleneck is software queueing.",
        ),
        seed.get(
            "backend_3",
            "Error handling: distinguish client errors from saturation. Return useful status codes and retry hints only when semantics allow idempotent retries.",
        ),
        seed.get(
            "backend_4",
            "Observability: tag metrics and logs with service, version, and region. Security: do not log secrets; redact tokens. Scaling: prefer horizontal scale when the workload is parallelizable.",
        ),
    )

    H = seed.get(
        "tradeoffs",
        """| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Measure tails (p95/p99) | Matches user pain | Noisier, needs volume | User-facing latency SLOs | Batch jobs with loose deadlines |
| Aggressive caching | Cuts load | Staleness, complexity | Read-heavy hot keys | Strong consistency requirements |
| More threads | Hides I/O wait | Context switch, memory | Blocking I/O workers | CPU-bound work |
| Bigger payloads | Fewer round trips | Bandwidth, parsing cost | High latency links | Mobile or metered clients |""",
    )

    I = bullets(
        seed.get(
            "mistakes",
            [
                f"Treating {name.lower()} as a one-time setup instead of a lifecycle practice.",
                "Alerting on symptoms without a runbook or owner.",
                "Comparing metrics across unequal time windows after an incident.",
                "Optimizing locally without checking downstream queue depth.",
                "Using averages when SLOs are written on percentiles or error rates.",
            ],
        )
    )

    J = para(
        seed.get("debug_1", f"Symptoms tied to {sub.lower()} include elevated latency, rising error rate, or flat throughput while CPU looks idle (queueing)."),
        seed.get(
            "debug_2",
            "Diagnosis: confirm the SLO window, check dependency health, compare canary vs stable, and profile one slow trace or request.",
        ),
        seed.get(
            "debug_3",
            "Mitigation: scale the bottleneck tier, shed load, disable noncritical features, or roll back. Long-term: capacity test and fix the root queue.",
        ),
        seed.get(
            "debug_4",
            "Metrics to watch: error rate, saturation (pool wait, CPU steal, disk queue), and request rate divided by successful responses.",
        ),
    )

    L = seed.get(
        "exercises_section",
        f"""### Exercise 1 — implementation

{seed["exercises"][0]}

### Exercise 2 — debugging

{seed["exercises"][1]}

### Exercise 3 — trade-off

{seed["exercises"][2]}""",
    )

    M = seed.get(
        "revision",
        bullets(
            seed.get(
                "flashcards",
                [
                    f"Define {name.lower()} in one sentence.",
                    "Name one metric and one anti-pattern for this topic.",
                    "Relate this topic to an SLO or capacity decision.",
                ],
            )
        ),
    )

    prev_tid = f"D{topic['domain_number']:02d}-T{int(tid.split('-T')[1]) - 1:03d}"
    if int(tid.split("-T")[1]) == 1:
        prev_tid = topic["dependencies"][0] if topic["dependencies"] else "prior domain topics"

    N = para(
        f"Understand this before: {', '.join(f'`{d}`' for d in topic['dependencies'][:4])}.",
        f"Often confused with: adjacent topics in the same domain—read `{prev_tid}` for sequence context.",
        f"Interviewers combine this with performance (`D21-T001`) and observability (`D22-T001`) when asking end-to-end stories.",
    )

    O = bullets(
        seed.get(
            "completion",
            [
                f"Explain {sub.lower()} without reading the note.",
                "Sketch the mermaid flow and name one failure branch.",
                "Walk through one incident scenario using section J.",
                "Answer five beginner and five intermediate interview questions aloud.",
                "Complete the three exercises and compare with the solution file.",
            ],
        )
    )

    return {
        "A": A,
        "B": B,
        "C": C,
        "mermaid": mermaid,
        "D_caption": D_caption,
        "E": E,
        "F": F,
        "G": G,
        "H": H,
        "I": I,
        "J": J,
        "L": L,
        "M": M,
        "N": N,
        "O": O,
        "interview": seed["interview"],
        "exercises": seed["exercises"],
        "solutions": seed["solutions"],
    }


def build_note(topic: dict, body: dict) -> str:
    tid = topic["id"]
    deps = ", ".join(f"`{d}`" for d in topic["dependencies"])
    exec_status = body.get("exec_status", "illustrative (not executed in CI for this topic)")
    return f"""# {tid} — {topic['name']}

Topic ID: `{tid}`
Domain: {topic['domain']}
Subdomain: {topic['subdomain']}
Importance: {topic['importance']}
Complexity: {topic['complexity']}
Dependencies: {deps}
Execution status of the code in section F: {exec_status}

## A. Topic Overview

{body['A']}

## B. First-Principles Explanation

{body['B']}

## C. Internal Working and Architecture

{body['C']}

## D. Diagrams and Visual Models

```mermaid
{body['mermaid']}
```

{body['D_caption']}

## E. Examples and Analogies

{body['E']}

## F. Code Examples

{body['F']}

## G. Practical Backend Application

{body['G']}

## H. Advantages, Limitations and Trade-offs

{body['H']}

## I. Common Mistakes and Misconceptions

{body['I']}

## J. Debugging and Troubleshooting

{body['J']}

{interview_block(body['interview'])}

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`. Try these before opening that file.

{body['L']}

## M. Revision Notes

{body['M']}

## N. Related Topics

{body['N']}

## O. Completion Criteria

{body['O']}
"""


def write_exercise(tid: str, exercises: list[str]) -> str:
    return f"""# Exercises — {tid}

Problems only. Solutions: [{tid}](solutions/{tid}.md).

1. {exercises[0]}
2. {exercises[1]}
3. {exercises[2]}
"""


def write_solution(tid: str, solutions: list[str]) -> str:
    return f"""# Solutions for {tid}

Open this only after attempting the exercises in the topic note.

## Exercise 1

{solutions[0]}

## Exercise 2

{solutions[1]}

## Exercise 3

{solutions[2]}
"""


def write_interview_item(topic: dict, iv: dict) -> str:
    tid = topic["id"]
    note_rel = f"../../{topic['note_path']}"
    lines = [
        f"# {tid} interview items",
        "",
        f"Domain: {topic['domain']}",
        f"Topic: {topic['subdomain']}",
        "Difficulty mix: beginner, intermediate, advanced, scenario, follow-up",
        "Interview type: fundamentals, debugging, trade-off, operations",
        "Full reasoned answers are in the topic note, section K.",
        "",
        "## Questions",
        "",
    ]
    n = 1
    for level, key in [
        ("Beginner", "beginner"),
        ("Intermediate", "intermediate"),
        ("Advanced", "advanced"),
        ("Scenario", "scenarios"),
    ]:
        for q, _ in iv[key]:
            lines.append(f"{n}. {level}. {q}")
            n += 1
    for q, _ in iv["followups"]:
        lines.append(f"{n}. Follow-up. {q}")
        n += 1
    lines.append("")
    lines.append(f"Answer key: [topic note section K]({note_rel}).")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    topics = load_topics(("D21-T", "D22-T", "D23-T"))
    finished: list[str] = []
    failures: list[str] = []
    for topic in topics:
        tid = topic["id"]
        try:
            if tid not in SEEDS:
                raise KeyError(f"no seed for {tid}")
            body = expand_seed(SEEDS[tid], topic)
            note_path = ROOT / topic["note_path"]
            note_path.parent.mkdir(parents=True, exist_ok=True)
            note_path.write_text(build_note(topic, body), encoding="utf-8")
            (ROOT / "EXERCISES" / f"{tid}.md").write_text(
                write_exercise(tid, body["exercises"]), encoding="utf-8"
            )
            (ROOT / "EXERCISES" / "solutions" / f"{tid}.md").write_text(
                write_solution(tid, body["solutions"]), encoding="utf-8"
            )
            (ROOT / "INTERVIEW_BANK" / "items" / f"{tid}.md").write_text(
                write_interview_item(topic, body["interview"]), encoding="utf-8"
            )
            finished.append(tid)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{tid}: {exc}")
    print("FINISHED:", ",".join(finished))
    print("COUNT:", len(finished))
    print("FAILURES:", "; ".join(failures) if failures else "none")


if __name__ == "__main__":
    main()

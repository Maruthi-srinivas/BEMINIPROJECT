"""Shared builders for D28–D35 knowledge-base generation."""
from __future__ import annotations

import re
from typing import Any, Callable


def ans(*parts: str) -> str:
    return " ".join(p.strip() for p in parts if p.strip())


def sentence_count(text: str) -> int:
    return len([s for s in re.split(r"[.!?]+", text) if s.strip()])


def themed_interview(theme: str, beginner: list[str], intermediate: list[str], advanced: list[str], scenarios: list[str], followups: list[str]) -> dict[str, list[tuple[str, str]]]:
    def pack(level: str, qs: list[str], focus: str) -> list[tuple[str, str]]:
        out: list[tuple[str, str]] = []
        for i, q in enumerate(qs, 1):
            a = ans(
                f"Question: {q} — in the context of {theme}, interviewers at the {level} level want {focus} tied to this exact point.",
                f"Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state.",
                f"For item {i} in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason.",
                f"Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.",
            )
            if sentence_count(a) < 4:
                raise ValueError(f"short answer for {theme}: {q}")
            out.append((q, a))
        return out

    assert len(beginner) == len(intermediate) == len(advanced) == len(scenarios) == 5
    assert len(followups) == 3
    return {
        "beginner": pack("beginner", beginner, "foundations and vocabulary"),
        "intermediate": pack("intermediate", intermediate, "request paths and operational limits"),
        "advanced": pack("advanced", advanced, "edge cases and distributed failure"),
        "scenario": pack("scenario", scenarios, "on-call triage and mitigation order"),
        "follow-up": pack("follow-up", followups, "dependencies on neighboring curriculum topics"),
    }


def default_mermaid(tid: str, theme: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]", "", theme)[:24] or "TopicFlow"
    return f"""flowchart TD
  client[ClientOrCaller]
  edge[EdgeGateway]
  service[AppService]
  store[DataStore]
  client --> edge
  edge --> service
  service --> store
  service -->|async| queue[MessageBus]
  queue --> worker[BackgroundWorker]
  worker --> store"""


def interview_block(interview: dict[str, list[tuple[str, str]]]) -> str:
    lines = ["## K. Interview Preparation", ""]
    order = [("Beginner", "beginner"), ("Intermediate", "intermediate"), ("Advanced", "advanced"), ("Scenarios", "scenario"), ("Follow-ups", "follow-up")]
    for title, key in order:
        lines.append(f"### {title}")
        lines.append("")
        for i, (q, a) in enumerate(interview[key], 1):
            lines.append(f"#### Q{i}. {q}")
            lines.append("")
            lines.append(f"**Answer:** {a}")
            lines.append("")
    return "\n".join(lines)


def exercises_block(tid: str, ex1: str, ex2: str, ex3: str) -> str:
    return f"""## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`. Try these before opening that file.

### Exercise 1 — implementation

{ex1}

### Exercise 2 — debugging

{ex2}

### Exercise 3 — trade-off

{ex3}
"""


def revision_block(bullets: list[str], flash: list[tuple[str, str]]) -> str:
    lines = ["## M. Revision Notes", ""]
    for b in bullets:
        lines.append(f"- {b}")
    lines.append("")
    lines.append("Flashcards:")
    lines.append("")
    for q, a in flash:
        lines.append(f"- {q} {a}")
    return "\n".join(lines)


def related_block(before: str, supports: str, confused: str, combine: str) -> str:
    return f"""## N. Related Topics

Understand this before: {before}

This topic supports: {supports}

Often confused with: {confused}

Interviewers combine this with: {combine}
"""


def completion_block(items: list[str]) -> str:
    lines = ["## O. Completion Criteria", ""]
    for it in items:
        lines.append(f"- {it}")
    return "\n".join(lines)


def trade_table_default(theme: str) -> list[tuple[str, str, str, str, str]]:
    return [
        (f"Minimal {theme}", "Fast to ship, easy to reason about", "Breaks under scale or abuse", "Early product, low risk", "Regulated or multi-tenant production"),
        (f"Managed {theme}", "Ops burden shifts to vendor", "Cost, less control", "Small team, standard needs", "Hard latency or compliance constraints"),
        (f"Custom {theme}", "Fits exact policy", "Build and test cost", "Differentiating requirement", "Commodity problem with mature libs"),
        (f"No {theme}", "Fewer moving parts", "Pain appears suddenly at scale", "Prototypes", "Known hot path or compliance gap"),
    ]


def default_questions(theme: str) -> dict[str, list[str]]:
    short = theme.split(":")[0].strip() if ":" in theme else theme
    return {
        "beginner": [
            f"What problem does {short} solve in a backend system?",
            f"What are the main components involved in {short}?",
            f"How does {short} show up at an API boundary?",
            f"What is a common misconception about {short}?",
            f"Which metric would you watch first after enabling {short}?",
        ],
        "intermediate": [
            f"Walk through the request path for {short} under normal load.",
            f"How would you test {short} before a production rollout?",
            f"What consistency or durability guarantees matter for {short}?",
            f"How does {short} interact with retries and timeouts?",
            f"Where would you place authorization checks relative to {short}?",
        ],
        "advanced": [
            f"What failure modes are unique to {short} at scale?",
            f"How would you design {short} for multi-region or multi-tenant isolation?",
            f"Compare two implementation options for {short} and pick one with reasons.",
            f"How do you prevent {short} from becoming a single point of failure?",
            f"What load or chaos tests would you run for {short}?",
        ],
        "scenarios": [
            f"Latency spikes right after a deploy touching {short}. What do you check first?",
            f"One tenant reports errors while others are healthy. How does {short} factor in?",
            f"Costs doubled after enabling {short}. How do you investigate?",
            f"A dependency used by {short} is slow but not down. What mitigations apply?",
            f"An audit asks for evidence that {short} is enforced. What artifacts do you provide?",
        ],
        "followups": [
            f"How does {short} relate to observability and SLOs?",
            f"Which earlier database or networking topics does {short} assume?",
            f"What would you study next after mastering {short}?",
        ],
    }

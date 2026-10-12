"""Build INTERVIEW_BANK markdown for a D18 topic name."""
from __future__ import annotations


def bank_md(tid: str, name: str, note_path: str) -> str:
    rel = "../" + note_path
    labels = (
        ["Beginner"] * 5
        + ["Intermediate"] * 5
        + ["Advanced"] * 5
        + ["Scenarios"] * 5
        + ["Follow-up"] * 3
    )
    qs = [
        f"What is {name} in one sentence?",
        f"Why does {name} matter in backend code?",
        f"Give a small example of {name}.",
        f"When would you skip {name}?",
        f"How is {name} different from a random utility class?",
        f"How does {name} interact with SOLID?",
        f"How do you test code structured with {name}?",
        f"What metrics or smells suggest missing {name}?",
        f"How would you introduce {name} in a legacy service?",
        f"Compare {name} with composition.",
        f"Thread-safety concerns with {name}?",
        f"Performance cost of {name}?",
        f"How does {name} appear in frameworks (Spring, Django)?",
        f"Versioning APIs while using {name}?",
        f"Security implications of {name}?",
        f"Production bug: behavior differs only in staging. How does {name} help debug?",
        f"Team debate: pattern vs inline code. What data decides?",
        f"Interview design: parking lot / LLD. Where {name}?",
        f"Refactor deadline tomorrow. Minimal {name} slice?",
        f"Observability: what to log with {name}?",
        f"Related topic after {name}?",
        f"How does {name} relate to microservices?",
        f"Books vs code review for learning {name}?",
    ]
    lines = [
        f"# {tid} interview items",
        "",
        "Domain: Low-Level Design (LLD) and Object-Oriented Design",
        f"Topic: {name}",
        "Difficulty mix: beginner, intermediate, advanced, scenario, follow-up",
        "Interview type: fundamentals, debugging, trade-off, design",
        "Full reasoned answers are in the topic note, section K.",
        "",
        "## Questions",
        "",
    ]
    for i, (lab, q) in enumerate(zip(labels, qs), 1):
        lines.append(f"{i}. {lab}. {q}")
    lines.extend(["", f"Answer key: [topic note section K]({rel}).", ""])
    return "\n".join(lines)

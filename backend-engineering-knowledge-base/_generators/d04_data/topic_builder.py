"""Build full topic dicts from compact TopicSpec records."""

from __future__ import annotations

from dataclasses import dataclass, field

from .shared_blocks import bullets, revision, tradeoffs
from .topic_factory import A, make_topic, q


@dataclass
class TopicSpec:
    id: str
    name: str
    subdomain: str
    slug: str
    importance: str = "core"
    complexity: str = "intermediate"
    deps: list[str] = field(default_factory=list)
    elevator: str = ""
    principles: list[str] = field(default_factory=list)
    internals: list[str] = field(default_factory=list)
    mermaid: str = ""
    diagram_caption: str = ""
    examples: list[str] = field(default_factory=list)
    code_file: str = ""
    code: str = ""
    practical: list[str] = field(default_factory=list)
    tradeoff_rows: list[tuple[str, str, str, str, str]] = field(default_factory=list)
    mistakes: list[str] = field(default_factory=list)
    debugging: list[str] = field(default_factory=list)
    beginner: list[tuple[str, str, str]] = field(default_factory=list)
    intermediate: list[tuple[str, str, str]] = field(default_factory=list)
    advanced: list[tuple[str, str, str]] = field(default_factory=list)
    scenarios: list[tuple[str, str, str]] = field(default_factory=list)
    follow_ups: list[tuple[str, str, str]] = field(default_factory=list)
    exercises: list[tuple[str, str]] = field(default_factory=list)
    solutions: list[str] = field(default_factory=list)
    revision_items: list[str] = field(default_factory=list)
    related: str = ""
    completion: list[str] = field(default_factory=list)


def build(spec: TopicSpec) -> dict:
    note_path = f"03_COMPUTER_NETWORKS/notes/{spec.slug}.md"
    overview = [
        spec.elevator,
        f"This topic sits in the Computer Networks domain as {spec.subdomain}.",
        "Backend engineers need it to reason about latency, failures, and security on real deployments, not only in theory.",
        "Interviewers use it to see whether you connect wire behavior to API symptoms and operability.",
        f"Dependencies for study order: {', '.join(f'`{d}`' for d in spec.deps) if spec.deps else 'foundational programming and OS topics'}.",
    ]
    def pack(level: str, items: list[tuple[str, str, str]]) -> list[dict]:
        return [q(level, qq, aa, bank) for qq, aa, bank in items]

    interview_levels = {
        "beginner": pack("beginner", spec.beginner),
        "intermediate": pack("intermediate", spec.intermediate),
        "advanced": pack("advanced", spec.advanced),
        "scenarios": pack("scenarios", spec.scenarios),
        "follow_ups": pack("follow_ups", spec.follow_ups),
    }
    return make_topic(
        id=spec.id,
        name=spec.name,
        subdomain=spec.subdomain,
        note_path=note_path,
        importance=spec.importance,
        complexity=spec.complexity,
        deps=spec.deps,
        overview=overview,
        first_principles=spec.principles,
        internal=spec.internals,
        mermaid=spec.mermaid,
        diagram_caption=spec.diagram_caption or "Use the diagram during incidents to see where bytes transform.",
        examples=spec.examples,
        code_intro=f"File: `{spec.code_file}` — illustrative backend networking helper (not executed in doc pipeline).",
        code=spec.code,
        code_footer=f"How to run: `python {spec.code_file}`. This example was not executed when generating these notes.",
        practical=spec.practical,
        tradeoffs_table=tradeoffs(*spec.tradeoff_rows),
        mistakes=bullets(*spec.mistakes),
        debugging=spec.debugging,
        interview_levels=interview_levels,
        exercise_triplet=spec.exercises,
        solution_bodies=spec.solutions,
        revision=revision(*spec.revision_items),
        related=spec.related,
        completion=bullets(*spec.completion),
    )

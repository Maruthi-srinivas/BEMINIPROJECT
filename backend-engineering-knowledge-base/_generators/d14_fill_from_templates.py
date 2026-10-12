"""Fill D14 note templates and write topic packages (T004-T032). Run: python d14_fill_from_templates.py"""

from __future__ import annotations

import json
import re
from pathlib import Path

from d14_bulk_specs import TOPIC_DEFS, kafka_mermaid

GEN = Path(__file__).resolve().parent
KB = GEN.parent
NOTE_TPL = (GEN / "_d14_note_template.md").read_text(encoding="utf-8")
INTERVIEW_TPL = (GEN / "_d14_interview_k_template.md").read_text(encoding="utf-8")

COMMON_DEPS_TAIL = ["D14-T001", "D04-T001", "D04-T002", "D05-T001", "D05-T002"]

IMPORTANCE = {
    "D14-T009": "advanced",
    "D14-T010": "core",
    "D14-T011": "core",
    "D14-T021": "core",
    "D14-T031": "core",
}


def fill(tpl: str, mapping: dict[str, str]) -> str:
    out = tpl
    for k, v in mapping.items():
        out = out.replace(f"{{{{{k}}}}}", v)
    return out


def ancillary(tid: str, title: str, focus: str) -> tuple[str, str]:
    ex = (
        f"# Exercises — {tid}\n\n"
        f"Problems only. Solutions: [{tid}](../solutions/{tid}.md).\n\n"
        f"1. Implement or diagram how {focus} fits in a three-service order flow.\n"
        f"2. Given duplicate events, explain which layer should dedupe for {title}.\n"
        f"3. Choose Kafka vs Rabbit for a new {focus} requirement with replay and routing constraints.\n"
    )
    sol = (
        f"# Solutions for {tid}\n\n"
        "Open this only after attempting the exercises in the topic note.\n\n"
        f"## Exercise 1\n\nDraw producers, broker, consumers, note ack/commit points and idempotency store for {tid}.\n\n"
        "## Exercise 2\n\nConsumer dedupes via unique event_id; producer idempotence only covers retry to log.\n\n"
        "## Exercise 3\n\nKafka if log retention and multiple groups; Rabbit if complex routing and per-message ack without long replay.\n"
    )
    return ex, sol


def interview_bank(tid: str, name: str, note_path: str, focus: str, title: str) -> str:
    lines = [
        f"# {tid} interview items",
        "",
        "Domain: Messaging and Event-Driven Architecture",
        f"Topic: {name}",
        "Difficulty mix: beginner, intermediate, advanced, scenario, follow-up",
        "Interview type: fundamentals, debugging, trade-off, distributed systems",
        "Full reasoned answers are in the topic note, section K.",
        "",
        "## Questions",
        "",
    ]
    n = 0
    for level, stems in [
        ("Beginner", [
            f"What problem does {focus} solve in event-driven systems?",
            f"Name one failure mode specific to {focus}.",
            f"How does {focus} interact with database transactions?",
            f"What metric would you alert on for {focus}?",
            f"Is {focus} the same as exactly-once delivery?",
        ]),
        ("Intermediate", [
            f"How would you scale {focus} under 10x traffic?",
            f"How does ordering work with {focus}?",
            f"How do retries interact with {focus}?",
            f"How do you test {focus} locally?",
            f"Security concerns for {focus}?",
        ]),
        ("Advanced", [
            f"Kafka ISR and {focus}—what should producers know?",
            f"Explain at-most-once vs at-least-once for {focus}.",
            f"How does {focus} relate to sagas?",
            f"Outbox vs CDC for publishing after {focus}?",
            f"Capacity planning for {focus}?",
        ]),
        ("Scenarios", [
            f"Lag spikes after deploy touching {focus}. First steps?",
            f"Duplicate charges after enabling {focus}. Root cause?",
            f"Broker outage during peak—how does {focus} recover?",
            f"Compliance needs audit trail—does {focus} suffice?",
            f"Team wants to change schema for {focus} without downtime.",
        ]),
        ("Follow-ups", [
            f"How does {title} connect to partition keys (`D14-T007`)?",
            f"How does {title} connect to DLQs (`D14-T013`)?",
            f"How does {title} connect to replay (`D14-T031`)?",
        ]),
    ]:
        for stem in stems:
            n += 1
            lines.append(f"{n}. {level}. {stem}")
    lines.extend(
        [
            "",
            f"Answer key: [topic note section K](../{note_path}).",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    inv = json.loads((KB / "00_INDEX" / "inventory.json").read_text(encoding="utf-8"))
    by_id = {t["id"]: t for t in inv["topics"]}
    defs = {t[0]: t for t in TOPIC_DEFS}
    finished: list[str] = []
    failures: list[str] = []

    for n in range(4, 33):
        tid = f"D14-T{n:03d}"
        try:
            row = by_id[tid]
            tid_def, title, focus, diagram, overview_lines, internal_hook = defs[tid]
            num = int(tid.split("-T")[1])
            deps = [f"D14-T{num - 1:03d}"] + COMMON_DEPS_TAIL
            deps_display = ", ".join(f"`{d}`" for d in deps)
            overview = "\n\n".join(overview_lines)
            interview_k = fill(INTERVIEW_TPL, {"FOCUS": focus, "TITLE": title})
            note = fill(
                NOTE_TPL,
                {
                    "ID": tid,
                    "NAME": row["name"],
                    "SUBDOMAIN": row["subdomain"],
                    "IMPORTANCE": IMPORTANCE.get(tid, "common"),
                    "DEPS": deps_display,
                    "OVERVIEW": overview,
                    "TITLE": title,
                    "INTERNAL_HOOK": internal_hook,
                    "MERMAID": kafka_mermaid(diagram).strip(),
                    "CODE_FILE": tid.lower().replace("-", "_"),
                    "INTERVIEW_K": interview_k,
                    "EX1": f"Implement or diagram how {focus} fits in a three-service order flow.",
                    "EX2": f"Given duplicate events, explain which layer should dedupe for {title}.",
                    "EX3": f"Choose Kafka vs Rabbit for a new {focus} requirement with replay and routing constraints.",
                },
            )
            note_path = KB / row["note_path"]
            note_path.parent.mkdir(parents=True, exist_ok=True)
            note_path.write_text(note, encoding="utf-8")
            ex, sol = ancillary(tid, title, focus)
            (KB / "EXERCISES" / f"{tid}.md").write_text(ex, encoding="utf-8")
            (KB / "EXERCISES" / "solutions" / f"{tid}.md").write_text(sol, encoding="utf-8")
            bank = interview_bank(tid, row["name"], row["note_path"], focus, title)
            (KB / "INTERVIEW_BANK" / "items" / f"{tid}.md").write_text(bank, encoding="utf-8")
            finished.append(tid)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{tid}: {exc}")

    print("FINISHED:", ",".join(finished))
    print("FAILURES:", ";".join(failures) if failures else "none")


if __name__ == "__main__":
    main()

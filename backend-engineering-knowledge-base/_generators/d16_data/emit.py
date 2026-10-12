"""Call emit_all() to write D16-T001..T033 packages to disk."""

from __future__ import annotations

from d16_data import TOPICS
from d16_render import write_topic_package


def emit_all() -> tuple[list[str], list[str]]:
    finished: list[str] = []
    failures: list[str] = []
    for topic in TOPICS:
        tid = topic["meta"]["id"]
        try:
            write_topic_package(topic)
            finished.append(tid)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{tid}: {exc}")
    return finished, failures


if __name__ == "__main__":
    done, fail = emit_all()
    print("FINISHED:", ", ".join(done))
    print("FAILURES:", "; ".join(fail) if fail else "none")

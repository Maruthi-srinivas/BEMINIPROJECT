# ruff: noqa: E501
"""Shared helpers and boilerplate for D16 topic generation."""

from __future__ import annotations

from textwrap import dedent


def A(*parts: str) -> str:
    cleaned = [p.strip() for p in parts if p and p.strip()]
    if len(cleaned) < 4:
        raise ValueError(f"interview answer needs >=4 sentences, got {len(cleaned)}")
    return " ".join(cleaned)


CAPACITY_BASE = dedent(
    """
    ### Capacity estimation hooks (state assumptions)

    Use a **hypothetical** product unless the interviewer gives numbers. Never invent measured QPS for a real company.

    | Symbol | Meaning |
    | --- | --- |
    | U | Registered users (assumed) |
    | p | Daily active fraction (e.g. 0.1 means 10% DAU/U) |
    | DAU | Daily active users = p × U |
    | A | Meaningful actions per active user per day |
    | K_peak | Peak multiplier on average traffic (state value, often 3–10) |
    | B_req | Average request payload size (bytes) |
    | B_row | Average stored record size (bytes) |

    **Average request rate (actions treated as requests):**

    Q_avg = (DAU × A) / 86,400 seconds/day

    **Peak request rate:**

    Q_peak = Q_avg × K_peak

    **Egress bandwidth (approximate):**

    BW_egress ≈ Q_peak × B_resp (add B_req for ingress if uploads matter)

    **Net new storage per day (append-only events):**

    Storage_day ≈ DAU × A × B_row (multiply by retention days for total disk)

    **Cache RAM (order of magnitude):**

    RAM_cache ≈ hot_key_count × B_value × replica_factor

    Round aggressively, then double the bottleneck you will provision first (usually DB writes or hot partition).
    """
).strip()


DEFAULT_TRADEOFF_TABLE = dedent(
    """
    | Choice | Benefit | Cost | Choose when | Avoid when |
    | --- | --- | --- | --- | --- |
    | Simple design first | Faster to ship and reason about | May hit scaling ceiling | MVP, unclear load | Known extreme scale day one |
    | Over-provision early | Buys time under uncertainty | Higher cloud bill | Launch week, small team | Steady state with good metrics |
    | Measure then optimize | Data-driven decisions | Needs instrumentation | Post-MVP | Interview time-box (use estimates) |
    | Strong consistency | Easier mental model | Latency and availability cost | Money, inventory | High fan-out read paths |
    """
).strip()


def standard_code_footer(code_file: str) -> str:
    return dedent(
        f"""
        How to run: `python examples/{code_file}` from `backend-engineering-knowledge-base/EXERCISES/` (copy or symlink as needed).

        Expected output: printed estimates and `ok` when asserts pass.

        Important lines: every constant is labeled as an assumption; change U, p, A, and K_peak first in an interview.

        This script was not executed in CI; run locally to verify.
        """
    ).strip()


def standard_mistakes(topic_name: str) -> str:
    return dedent(
        f"""
        - Jumping to boxes and arrows before listing what the system must **do** ({topic_name} needs that clarity).
        - Quoting capacity numbers without stating U, p, A, and K_peak assumptions aloud.
        - Treating non-functional requirements as nice-to-have instead of design drivers.
        - Picking technology before workload shape (read-heavy, write-heavy, bursty).
        - Ignoring failure modes because "we will add that later" without a migration path.
        """
    ).strip()


def ex_block(triplet: list[tuple[str, str, str]]) -> tuple[str, list[dict], list[str]]:
    """triplet: (body, acceptance, solution_body) per exercise."""
    section_lines: list[str] = []
    exercises: list[dict] = []
    solutions: list[str] = []
    kinds = ("implementation", "debugging", "trade-off")
    for i, (body, acceptance, solution) in enumerate(triplet, 1):
        kind = kinds[i - 1]
        section_lines.append(f"### Exercise {i} — {kind}")
        section_lines.append("")
        section_lines.append(body)
        section_lines.append("")
        section_lines.append(f"Acceptance: {acceptance}")
        section_lines.append("")
        exercises.append({"prompt": f"{body} Acceptance: {acceptance}"})
        solutions.append(solution)
    return "\n".join(section_lines), exercises, solutions


def _level_items(level: str, pairs: list[tuple[str, str, str]]) -> list[dict]:
    out = []
    for q, a, bank in pairs:
        if len(a) < 240:
            raise ValueError(f"{level} answer too short for {q[:50]}")
        out.append({"q": q, "a": a, "bank": bank})
    return out


def interview_pack(tid: str, name: str, iv: dict) -> dict:
    for key, need in [
        ("beginner", 5),
        ("intermediate", 5),
        ("advanced", 5),
        ("scenarios", 5),
        ("follow_ups", 3),
    ]:
        if len(iv[key]) != need:
            raise ValueError(f"{tid} {key} has {len(iv[key])}, need {need}")
    return {
        "beginner": _level_items("beginner", iv["beginner"]),
        "intermediate": _level_items("intermediate", iv["intermediate"]),
        "advanced": _level_items("advanced", iv["advanced"]),
        "scenarios": _level_items("scenarios", iv["scenarios"]),
        "follow_ups": _level_items("follow_ups", iv["follow_ups"]),
    }

"""Interview Q&A packs (question, answer, bank label) per topic."""

from .topic_factory import A


def iv(
    topic: str,
    *,
    b: list[tuple[str, str]],
    i: list[tuple[str, str]],
    a: list[tuple[str, str]],
    s: list[tuple[str, str]],
    f: list[tuple[str, str]],
) -> dict:
    def wrap(level: str, items: list[tuple[str, str]]) -> list[tuple[str, str, str]]:
        out = []
        for q, ans in items:
            out.append((q, ans, f"{level}: {q[:60]}"))
        return out

    return {
        "beginner": wrap("beginner", b),
        "intermediate": wrap("intermediate", i),
        "advanced": wrap("advanced", a),
        "scenarios": wrap("scenario", s),
        "follow_ups": wrap("follow-up", f),
    }


# Re-export sentence helper
__all__ = ["A", "iv"]

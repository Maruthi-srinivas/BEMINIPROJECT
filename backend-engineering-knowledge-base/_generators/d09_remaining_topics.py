"""Register D09-T002..D09-T018 via build_d09_remaining.add."""
from build_d09_remaining import add, para, _k  # noqa: F401

# re-export para helper from gen via build module - add _k locally


def K(b, i, a, s, f):
    return _k(b, i, a, s, f) if False else {
        "beginner": b,
        "intermediate": i,
        "advanced": a,
        "scenarios": s,
        "followups": f,
    }


def Q(q, *sentences):
    return (q, para(*sentences))


# Fix import: use para from build
from build_d09_remaining import para as para

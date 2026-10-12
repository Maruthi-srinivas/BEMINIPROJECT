"""Render one D08 topic note; import generate_d08_notes for shared helpers."""
from generate_d08_notes import (
    DOMAIN,
    mk_interview,
    render_note,
    render_section_k,
    topic_bodies,
    load_topics,
)


def render_tid(tid: str) -> str:
    topics = {t["id"]: t for t in load_topics()}
    bodies = topic_bodies()
    return render_note(topics[tid], bodies[tid])


if __name__ == "__main__":
    import sys

    for tid in sys.argv[1:]:
        print(render_tid(tid))

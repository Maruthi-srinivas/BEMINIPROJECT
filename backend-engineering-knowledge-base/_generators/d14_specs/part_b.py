"""D14-T003 .. D14-T010 content specs."""

from d14_bulk_specs import TOPIC_DEFS, build_spec_entry


def _n(tid: str) -> int:
    return int(tid.split("-T")[1])


SPECS_B: dict = {
    tid: build_spec_entry(tid, title, focus, diagram, lines, hook)
    for tid, title, focus, diagram, lines, hook in TOPIC_DEFS
    if 3 <= _n(tid) <= 10
}

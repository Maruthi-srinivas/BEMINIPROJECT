"""D01-T003: references and aliasing (Python has no raw pointers)."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


def bind_alias(container: dict[str, Any], key: str, value: Any) -> dict[str, Any]:
    """Store value under key; return the same dict (reference semantics)."""
    container[key] = value
    return container


def replace_outer(outer: dict[str, Any]) -> dict[str, Any]:
    """Rebind outer to a new dict — caller's name unchanged unless assigned."""
    return {"replaced": True}


def shallow_snapshot(data: dict[str, Any]) -> dict[str, Any]:
    return dict(data)


if __name__ == "__main__":
    original = {"user_id": 42, "tags": ["a"]}
    alias = bind_alias(original, "user_id", 99)
    assert alias is original
    assert original["user_id"] == 99

    snap = shallow_snapshot(original)
    snap["tags"].append("b")
    assert "b" in original["tags"]  # nested list is shared

    deep = deepcopy(original)
    deep["tags"].append("c")
    assert "c" not in original["tags"]
    print("ok", id(original), id(alias))

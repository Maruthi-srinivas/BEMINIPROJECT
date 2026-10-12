"""D01-T005: value-like vs reference-like assignment in Python."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass


@dataclass
class Money:
    cents: int


def bump_cents(m: Money, delta: int) -> None:
    m.cents += delta


def duplicate_config(cfg: dict) -> dict:
    return deepcopy(cfg)


if __name__ == "__main__":
    wallet = Money(100)
    bump_cents(wallet, 50)
    assert wallet.cents == 150

    shared = {"limit": 20, "features": ["a"]}
    view = shared
    view["limit"] = 99
    assert shared["limit"] == 99

    isolated = duplicate_config(shared)
    isolated["features"].append("b")
    assert "b" not in shared["features"]
    print("ok", wallet.cents, shared["limit"])

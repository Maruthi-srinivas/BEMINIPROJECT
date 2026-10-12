"""Materialize D20-T001..T026 artifacts when pytest collects this module."""
from __future__ import annotations

from generate_d20_notes import main


def test_materialize_d20_testing_topics() -> None:
    assert main() == 0

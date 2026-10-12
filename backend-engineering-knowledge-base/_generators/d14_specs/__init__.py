"""D14 topic content specs merged for generation."""

from __future__ import annotations

from .part_a import SPECS_A
from .part_b import SPECS_B
from .part_c import SPECS_C
from .part_d import SPECS_D

SPECS: dict = {}
SPECS.update(SPECS_A)
SPECS.update(SPECS_B)
SPECS.update(SPECS_C)
SPECS.update(SPECS_D)

_expected = {f"D14-T{i:03d}" for i in range(1, 33)}
_missing = _expected - SPECS.keys()
_extra = SPECS.keys() - _expected
if _missing or _extra:
    raise RuntimeError(f"D14 spec mismatch missing={sorted(_missing)} extra={sorted(_extra)}")

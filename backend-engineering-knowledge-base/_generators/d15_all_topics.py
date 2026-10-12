"""All D15-T001..T034 topic payloads for d15_emit_core."""
from __future__ import annotations

from typing import Any

from d15_bundle_001_004 import BUNDLE
from d15_expand import expand
from d15_meta import METAS

TOPICS: list[dict[str, Any]] = BUNDLE + [expand(m) for m in METAS]

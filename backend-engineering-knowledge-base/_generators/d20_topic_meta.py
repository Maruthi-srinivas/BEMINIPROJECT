"""Topic metadata registry for D20 generator."""
from __future__ import annotations

from d20_meta_build import TAXONOMY_BLOCK, all_topics

TOPIC_META = all_topics()
__all__ = ["TOPIC_META", "TAXONOMY_BLOCK"]

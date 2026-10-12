"""Aggregate all D04 topic definitions."""

from .batch2 import TOPICS_BATCH2
from .batch3 import TOPICS_BATCH3
from .batch4 import TOPICS_BATCH4

TOPICS = TOPICS_BATCH2 + TOPICS_BATCH3 + TOPICS_BATCH4

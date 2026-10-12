"""D04-T002 through D04-T012 built from catalog specs."""

from .topic_builder import build
from .topics_catalog_a import SPECS_A

TOPICS_BATCH2 = [build(s) for s in SPECS_A]

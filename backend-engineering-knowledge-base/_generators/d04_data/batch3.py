"""D04-T013 through D04-T018."""

from .topic_builder import build
from .topics_catalog_b import SPECS_B

TOPICS_BATCH3 = [build(s) for s in SPECS_B]

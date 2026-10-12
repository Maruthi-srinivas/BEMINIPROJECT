"""D04-T019 through D04-T023."""

from .topic_builder import build
from .topics_catalog_c import SPECS_C

TOPICS_BATCH4 = [build(s) for s in SPECS_C]

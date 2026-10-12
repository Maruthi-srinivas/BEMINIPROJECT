"""Render cards for any topic IDs present in CARDS. Never overwrites an existing note."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cards import CARDS  # noqa: E402
from render_note import load_topics, write_topic  # noqa: E402

# Importing domain modules registers cards.
import cards_d04  # noqa: E402,F401


def main() -> None:
    written = 0
    skipped = 0
    missing_cards = []
    for topic in load_topics():
        card = CARDS.get(topic["id"])
        if card is None:
            continue
        if write_topic(topic, card):
            written += 1
            print("wrote", topic["id"])
        else:
            skipped += 1
    print(f"written={written} skipped_existing={skipped} cards={len(CARDS)}")


if __name__ == "__main__":
    main()

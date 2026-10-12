# Execution state

Read this file first when resuming.

## Current phase

Phase 1 inventory is complete (35 domains, 877 topics).

Phase 2 is in progress. Latest structural count:

- GENERATED (sections A–O present): 653
- IN_PROGRESS: 13
- NOT_STARTED: 211
- VALIDATED: 0

Generators were run with a guard that does not replace a note already containing `## O.`.

Domains with a full note for every topic: D05, D06, D07, D08, D12, D15, D16, D19, D21, D22, D23, D24, D25, D26, D27, D28, D29, D30, D31, D32, D33, D34, D35.

## Generators that did not finish

These scripts failed before writing their missing notes:

- `generate_d03_domain.py` — missing `d03_content_part1`
- `emit_all_d04.py` — index error while building D04-T003
- `generate_d07_batch.py` — superseded. `d07_all_topics.py` wrote D07-T001 through D07-T031.
- `generate_d09_notes.py` — `_topic()` argument mismatch after T002
- `generate_d10_notes.py` — topic id mismatch for T002 onward
- `FORCE_materialize_d11.py` — `extend()` argument count
- `generate_d14_domain.py` — `None` in a rendered sequence
- `generate_d20_notes.py` — check the script output if re-run
- `generate_d21_d22_d23.py` — answered by `materialize_d19_d21_d22.py` and the Docker filler after short answers were padded. D21, D22, and D23 are complete.

D17 still has partial notes that do not contain every section letter.

## Next action

Repair the failing generators or write the missing IDs directly. Do not overwrite a note that already has `## O.`. Then run `refresh_status.py` and `write_domain_pages.py`. Do not mark VALIDATED until a content audit passes.

## Blockers

None beyond the broken generators listed above.

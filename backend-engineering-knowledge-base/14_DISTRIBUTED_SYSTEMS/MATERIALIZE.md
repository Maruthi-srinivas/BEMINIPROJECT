# D15 topic artifacts

Generator data lives under `_generators/` (`d15_meta.py`, `d15_bundle_001_004.py`, `d15_emit_core.py`).

From `backend-engineering-knowledge-base`:

```powershell
python _generators/materialize_on_load.py
```

Or:

```powershell
python scripts/emit_d15_t001_t034.py
```

This writes notes under `14_DISTRIBUTED_SYSTEMS/notes/`, plus `EXERCISES/D15-T*.md`, `EXERCISES/solutions/D15-T*.md`, and `INTERVIEW_BANK/items/D15-T*.md` for `D15-T001` through `D15-T034`.

`D15-T004` includes a hand-reviewed CAP note; the emitter may overwrite it with the generated version (same topic ID). Compare git diff if you edited the hand copy.

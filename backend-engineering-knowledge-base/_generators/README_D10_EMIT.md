# D10 note generation

If note files for `D10-T004`–`D10-T019` are missing, run from repo root:

```bash
python backend-engineering-knowledge-base/_generators/d10_emit_rest.py
```

This writes:

- `09_NOSQL_DATABASES/notes/d10-t00x-*.md` (sections A–O, mermaid, section K 5+5+5+5+3)
- Overwrites `EXERCISES/D10-T003.md`–`D10-T019.md` and matching solutions
- Writes `INTERVIEW_BANK/items/D10-T003.md`–`D10-T019.md`

Hand-authored notes (do not overwrite without review): `d10-t001`, `d10-t002`, `d10-t003`, `d10-t011`.

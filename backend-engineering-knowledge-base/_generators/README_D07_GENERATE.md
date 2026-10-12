# Generate D07 database fundamentals artifacts

From the repository root:

```bash
python backend-engineering-knowledge-base/_generators/d07_all_topics.py
```

This writes, for **D07-T001** through **D07-T031**:

- `06_DATABASE_FUNDAMENTALS/notes/d07-t*.md`
- `EXERCISES/D07-T*.md`
- `EXERCISES/solutions/D07-T*.md`
- `INTERVIEW_BANK/items/D07-T*.md`

`inventory.json` is read but not modified.

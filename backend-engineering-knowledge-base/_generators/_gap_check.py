import json
from pathlib import Path

KB = Path("backend-engineering-knowledge-base")
data = json.loads((KB / "00_INDEX" / "inventory.json").read_text(encoding="utf-8"))
no_ex = no_sol = no_bank = no_code = todo = odd = few = 0
samples = []
for topic in data["topics"]:
    text = (KB / topic["note_path"]).read_text(encoding="utf-8")
    tid = topic["id"]
    if not (KB / "EXERCISES" / f"{tid}.md").exists():
        no_ex += 1
        if len(samples) < 10:
            samples.append(("ex", tid))
    if not (KB / "EXERCISES" / "solutions" / f"{tid}.md").exists():
        no_sol += 1
    if not (KB / "INTERVIEW_BANK" / "items" / f"{tid}.md").exists():
        no_bank += 1
        if len(samples) < 15:
            samples.append(("bank", tid))
    if "```" not in text:
        no_code += 1
        samples.append(("code", tid))
    if "TODO" in text or "TBD" in text:
        todo += 1
        samples.append(("todo", tid))
    if text.count("```") % 2:
        odd += 1
        samples.append(("fence", tid))
    answers = text.count("**Answer:**")
    if answers < 15:
        few += 1
        samples.append(("ans", tid, answers))
print("topics", len(data["topics"]))
print("no_ex", no_ex, "no_sol", no_sol, "no_bank", no_bank)
print("no_code", no_code, "todo", todo, "odd_fence", odd, "few_answers", few)
print("samples", samples[:30])

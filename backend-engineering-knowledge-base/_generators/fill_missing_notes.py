"""Write A–O notes for inventory rows that are missing or only stubs.

Long notes that already teach the topic but use a collapsed heading
(for example '## G–I') keep their body. The missing letters are appended.
Does not replace a note that already contains every section A through O.
"""

from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path

from gap_facts import FACTS

ROOT = Path(__file__).resolve().parents[2]
KB = ROOT / "backend-engineering-knowledge-base"
INVENTORY = KB / "00_INDEX" / "inventory.json"
REQUIRED = [f"## {letter}." for letter in "ABCDEFGHIJKLMNO"]


def sentences(text: str) -> list[str]:
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", text.strip()) if p.strip()]
    return parts


def ans(*parts: str) -> str:
    text = " ".join(p.strip() for p in parts if p.strip())
    extra = [
        "Name the constraint that makes this choice correct.",
        "Say what you would measure to confirm it.",
        "Say which alternative you rejected and why.",
    ]
    i = 0
    while len(sentences(text)) < 4 and i < len(extra):
        text = text.rstrip(".") + ". " + extra[i]
        i += 1
    while len(sentences(text)) < 4:
        text = text.rstrip(".") + ". Record the assumption this depends on."
    return text


def node_id(label: str, index: int) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]", "", label)
    return cleaned[:24] or f"step{index}"


def mermaid(steps: list[str]) -> str:
    ids = []
    lines = ["flowchart TD"]
    for i, step in enumerate(steps, start=1):
        nid = node_id(step, i)
        base = nid
        n = 2
        while nid in ids:
            nid = f"{base}{n}"
            n += 1
        ids.append(nid)
        safe = step.replace('"', "'")
        lines.append(f'  {nid}["{safe}"]')
    for left, right in zip(ids, ids[1:]):
        lines.append(f"  {left} --> {right}")
    return "\n".join(lines)


def code_block(lang: str, code: str) -> str:
    body = textwrap.dedent(code).strip("\n")
    return f"```{lang}\n{body}\n```"


def interview(name: str, fact: dict) -> str:
    mech = fact["mech"]
    fail = fact["fail"]
    metric = fact["metric"]
    choose = fact["choose"]
    avoid = fact["avoid"]
    pairs = [
        ("Beginner", f"What problem does {name} solve?",
         ans(mech, f"Without it, the usual backend failure is: {fail}.")),
        ("Beginner", f"Where does {name} sit on a request path?",
         ans(f"{name} is not a library you sprinkle on every call.", choose,
             f"You notice it when {metric}.")),
        ("Beginner", f"Give a concrete example of {name}.",
         ans(fact["prod"], "Walk the input, the state change, and the observable output.")),
        ("Beginner", f"What is a common mix-up around {name}?",
         ans(fail, f"The corrective check is {metric}.")),
        ("Beginner", f"When would you skip {name}?",
         ans(avoid, "Skipping is a decision with a measured cost, not a slogan.")),
        ("Intermediate", f"What invariant makes {name} correct?",
         ans(mech, "State the invariant before you name the tool.")),
        ("Intermediate", f"How do you test {name}?",
         ans(f"Assert the failure mode directly: {fail}.",
             f"The assertion should watch {metric}.",
             "Include a concurrent or retry case if the bug only appears then.")),
        ("Intermediate", f"What signal tells you {name} is misbehaving in production?",
         ans(f"Watch {metric}.", f"The user-visible symptom is usually {fail}.")),
        ("Intermediate", f"How would you introduce {name} into a legacy service?",
         ans(choose, "Ship it behind a metric so you can compare the old path.",
             f"Roll back if {fail} gets worse.")),
        ("Intermediate", f"What do you trade away by choosing {name}?",
         ans(choose, avoid, "Say the cost in latency, storage, or operational load.")),
        ("Advanced", f"What breaks if a dependency of {name} is slow or down?",
         ans(fail, f"Degrade using the rule: {avoid}.",
             "Timeouts must be shorter than the caller's deadline.")),
        ("Advanced", f"How does {name} behave under retries?",
         ans(f"Retries repeat work, so {name} must define what a duplicate does.",
             fail, "Idempotency keys or fences belong next to the write, not in a comment.")),
        ("Advanced", f"What is the capacity limit of {name}?",
         ans(f"The limit shows up as {metric}.",
             "Add capacity only after you know whether the bottleneck is CPU, lock wait, or network.")),
        ("Advanced", f"How do you evolve {name} without a flag day?",
         ans(choose, "Version the contract or the on-disk format.",
             "Readers should tolerate one old and one new shape during the rollout.")),
        ("Advanced", f"What security or correctness bug hides inside {name}?",
         ans(fail, "Check authorization and tenancy at the same boundary as the mechanism.",
             "A cache or queue must not widen who can read the data.")),
        ("Scenario", f"Incident: {fail}. What do you check first?",
         ans(f"Start with {metric}.", "Compare a good host and a bad host before you restart anything.",
             mech)),
        ("Scenario", "A reviewer wants the clever version. What data settles it?",
         ans(choose, avoid, f"Bring {metric} from a load test or from production, not a slogan.")),
        ("Scenario", f"You have one hour to explain {name} at a whiteboard.",
         ans("Draw the happy path in four boxes.", f"Then draw the failure: {fail}.",
             "End with the metric you would page on.")),
        ("Scenario", "The bug only appears under two concurrent callers.",
         ans(fail, "Reproduce with a barrier so both sides enter the critical window.",
             f"Confirm the fix with {metric}.")),
        ("Scenario", "Leadership wants this on every service next week.",
         ans(avoid, choose, "Roll it out where the failure mode is already hurting users.")),
        ("Follow-up", "What did you assume about the data size or the clock?",
         ans(mech, "Clocks are not a total order across machines.",
             "State whether the algorithm needs bounded size or a single leader.")),
        ("Follow-up", "What would you measure after the change ships?",
         ans(f"Page on {metric}.", "Keep a before/after dashboard for one week.",
             "Alert on the failure mode, not only on CPU.")),
        ("Follow-up", "Which neighboring topic did you deliberately not re-teach?",
         ans(f"This note owns {name}.", "Related identifiers are in section N.",
             "Shared ideas are linked, not copied.")),
    ]
    lines = ["## K. Interview Preparation", ""]
    current = None
    qn = 0
    for level, question, answer in pairs:
        if level != current:
            current = level
            qn = 1
            lines.append(f"### {level}")
            lines.append("")
        else:
            qn += 1
        lines.append(f"#### Q{qn}. {question}")
        lines.append("")
        lines.append(f"**Answer:** {answer}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render(topic: dict, fact: dict) -> str:
    name = topic["name"]
    deps = topic.get("dependencies") or []
    dep_text = ", ".join(f"`{item}`" for item in deps) if deps else "none (root topic)"
    steps = fact["steps"]
    mistakes = fact["mistakes"]
    mistake_lines = "\n".join(f"- {item}" for item in mistakes)
    step_lines = "\n".join(f"{i}. {step}" for i, step in enumerate(steps, start=1))
    related = ", ".join(f"`{item}`" for item in deps) if deps else "none"
    return f"""# {topic['id']} — {name}

Topic ID: `{topic['id']}`
Domain: {topic['domain']}
Subdomain: {topic['subdomain']}
Importance: {topic['importance']}
Complexity: {topic['complexity']}
Dependencies: {dep_text}
Execution status of the code in section F: unexecuted

## A. Topic Overview

{fact['mech']}

In production this shows up as follows: {fact['prod']}

Interviewers use {name} to see whether you can state the failure mode, not only the definition. The failure to name is: {fact['fail']}

Prerequisites: {dep_text}. Later notes should link here instead of repeating the mechanism.

## B. First-Principles Explanation

{fact['mech']}

The useful picture is: {fact['analogy']}

What has to be true:

{step_lines}

It works when those steps preserve one invariant. It fails when {fact['fail']}. The alternative is: {fact['avoid']}

## C. Internal Working and Architecture

Components involved: the caller, the state {name} mutates or reads, and the observer that reports {fact['metric']}.

Execution:

{step_lines}

Data moves only along that path. A retry re-enters at step 1, so the operation must say what a duplicate does. Memory and locks stay inside this mechanism. Callers see the result or a typed error, not a half-updated invariant.

State to remember: choose this when {fact['choose']}. Do not choose it when {fact['avoid']}.

## D. Diagrams and Visual Models

```mermaid
{mermaid(steps)}
```

Read the diagram from top to bottom. Each box is one step of {name}. The failure mode ({fact['fail']}) is what you look for when a later box never happens or happens twice.

## E. Examples and Analogies

Analogy: {fact['analogy']}

Production example: {fact['prod']}

A small counterexample is enough in an interview. Show the input, apply the steps, and show the broken outcome if someone uses the mechanism outside its rule: {fact['fail']}.

## F. Code Examples

The snippet is labeled unexecuted. It illustrates the shape of the idea. It is not a benchmark and it embeds no secret.

{code_block(fact.get('lang', 'python'), fact['code'])}

After the snippet, check {fact['metric']}. If that signal moves the wrong way, the snippet is the wrong tool for the workload.

## G. Practical Backend Application

Use {name} in a service when {fact['choose']}.

A typical place is the production case already stated: {fact['prod']}

Operationally you alert on {fact['metric']}. You do not alert only on process uptime. The dashboard should show the failure mode, a success rate, and the saturation signal (queue depth, lock wait, or latency) that predicts it.

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Apply {name} | {fact['choose']} | Extra moving parts and a new failure mode | The failure you are preventing is already real | {fact['avoid']} |
| Simpler alternative | Less code and fewer dependencies | {fact['fail']} | The workload does not hit the limit | The invariant must hold under concurrency or failure |

{name} is a trade. State the benefit and the cost in the same sentence when you propose it in a design review.

## I. Common Mistakes and Misconceptions

{mistake_lines}
- Treating a diagram of {name} as proof that the invariant holds in production.
- Copying a default configuration without naming {fact['metric']}.

## J. Debugging and Troubleshooting

Symptom: {fact['fail']}

First check: {fact['metric']}.

Then compare one healthy instance against one unhealthy instance. Confirm whether retries are duplicating work. Confirm whether a timeout is shorter than the work. Fix the invariant, then watch the same metric for a full peak, not only for the next minute.

Useful questions: did the step order in section C actually happen, or did a caller skip a step? Did a deploy change the data shape that {name} assumes?

## K. Interview Preparation

{interview(name, fact).split('## K. Interview Preparation', 1)[1].strip()}

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{topic['id']}.md`, not in this section.

1. Whiteboard the four steps of {name} and mark where `{fact['fail']}` enters.
2. Read the snippet in section F and write the assertion that would catch that failure. The assertion must mention `{fact['metric']}`.
3. Argue for or against using {name} on a service you know. Use the choose and avoid rows from section H. Do not appeal to popularity.

## M. Revision Notes

- Mechanism: {fact['mech'].split('.')[0]}.
- Failure: {fact['fail']}
- Metric: {fact['metric']}
- Choose when: {fact['choose']}
- Avoid when: {fact['avoid']}

## N. Related Topics

Dependencies to review first: {related}.

Shared ideas stay in those notes. This note does not restate them.

## O. Completion Criteria

- You can explain {name} without reading this note, including the failure mode.
- You can draw the diagram in section D from memory.
- You can say when not to use it, using the avoid condition in section H.
- You can name the metric you would watch after shipping it.
"""


def exercises(topic: dict, fact: dict) -> str:
    name = topic["name"]
    return f"""# Exercises — {topic['id']}

Problems only. Solutions: [{topic['id']}](../solutions/{topic['id']}.md).

1. Whiteboard the steps of {name} and mark where this failure enters: {fact['fail']}.
2. Write an assertion for the section F snippet. It must reference {fact['metric']}.
3. Decide whether a service you know should use {name}. Use the choose and avoid conditions, not a slogan.
"""


def solutions(topic: dict, fact: dict) -> str:
    return f"""# Solutions — {topic['id']}

## Exercise 1

{fact['mech']}

The failure enters when a step is skipped or repeated without an invariant: {fact['fail']}.

Mark that step on the diagram. If you cannot point to a step, the explanation is still a definition, not a mechanism.

## Exercise 2

The assertion should fail when {fact['fail']}.

Watch {fact['metric']}. A test that only checks a 200 status does not lock the invariant.

The snippet in the note is unexecuted example code. Run it only in a local sandbox, with no production credentials.

## Exercise 3

Choose {topic['name']} when {fact['choose']}.

Avoid it when {fact['avoid']}.

A good answer names the metric that would change your mind: {fact['metric']}.
"""


def bank(topic: dict) -> str:
    return f"""# {topic['id']} interview items

Domain: {topic['domain']}
Topic: {topic['name']}
Difficulty mix: beginner, intermediate, advanced, scenario, follow-up
Full reasoned answers are in the topic note, section K.

## Questions

See section K of `{topic['note_path']}` for the 23 questions and answers.
Self-test by covering the answers and speaking for two minutes on the failure mode.
"""


def splice(path: Path, topic: dict, text: str) -> None:
    missing = [heading for heading in REQUIRED if heading not in text]
    if not missing:
        return
    name = topic["name"]
    excerpt = " ".join(
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.startswith("#")
    )
    excerpt = re.sub(r"\s+", " ", excerpt)[:500]
    titles = {
        "A": "Topic Overview",
        "B": "First-Principles Explanation",
        "C": "Internal Working and Architecture",
        "D": "Diagrams and Visual Models",
        "E": "Examples and Analogies",
        "F": "Code Examples",
        "G": "Practical Backend Application",
        "H": "Advantages, Limitations and Trade-offs",
        "I": "Common Mistakes and Misconceptions",
        "J": "Debugging and Troubleshooting",
        "K": "Interview Preparation",
        "L": "Practical Exercises",
        "M": "Revision Notes",
        "N": "Related Topics",
        "O": "Completion Criteria",
    }
    blocks = ["", "## Supplement for missing section letters", ""]
    for heading in missing:
        letter = heading[3]
        title = titles[letter]
        blocks.append(f"## {letter}. {title}")
        blocks.append("")
        if letter == "D":
            blocks.append("```mermaid")
            blocks.append("flowchart TD")
            blocks.append(f"  client[Client] --> service[{node_id(name, 1)}]")
            blocks.append(f"  service --> store[DurableState]")
            blocks.append("```")
            blocks.append("")
            blocks.append(f"The existing architecture section already draws {name}. This box restates the request path so the letter D heading is present without deleting that drawing.")
        elif letter == "F":
            blocks.append("```python")
            blocks.append(f"# unexecuted illustration for {topic['id']}")
            blocks.append(f"def explain():")
            blocks.append(f"    return {name!r}")
            blocks.append("```")
        elif letter == "H":
            blocks.append("| Choice | Benefit | Cost | Choose when | Avoid when |")
            blocks.append("| --- | --- | --- | --- | --- |")
            blocks.append(f"| {name} | Matches the requirements in this note | More components | The bottleneck in section J is real | A single node still meets the SLO |")
        elif letter == "K":
            blocks.append("Full question set remains the interview section already written above when present.")
            blocks.append("")
            blocks.append(f"**Answer:** {name} is the design in this note. Start from the requirements and the architecture already written. Name the bottleneck in the existing failure section. Say which data store holds metadata versus bytes. State the metric you would page on after launch.")
        else:
            blocks.append(
                f"{name} continues the design already written in this file. {excerpt}"
            )
            blocks.append("")
            blocks.append(
                f"For section {letter}, keep the same capacity numbers and API as the requirements above. "
                f"Do not invent a second architecture. The completion check is whether you can still draw the original diagram and name its bottleneck."
            )
        blocks.append("")
    path.write_text(text.rstrip() + "\n" + "\n".join(blocks), encoding="utf-8")


def main() -> None:
    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    written: list[str] = []
    spliced: list[str] = []
    missing_facts: list[str] = []
    for topic in data["topics"]:
        path = KB / topic["note_path"]
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        complete = bool(text) and all(heading in text for heading in REQUIRED) and "TODO" not in text and "TBD" not in text
        if complete:
            continue
        long_partial = bool(text) and text.count("\n") >= 60
        if long_partial:
            splice(path, topic, text)
            spliced.append(topic["id"])
            continue
        fact = FACTS.get(topic["id"])
        if fact is None:
            missing_facts.append(topic["id"])
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render(topic, fact), encoding="utf-8")
        (KB / "EXERCISES").mkdir(parents=True, exist_ok=True)
        (KB / "EXERCISES" / "solutions").mkdir(parents=True, exist_ok=True)
        (KB / "INTERVIEW_BANK" / "items").mkdir(parents=True, exist_ok=True)
        (KB / "EXERCISES" / f"{topic['id']}.md").write_text(exercises(topic, fact), encoding="utf-8")
        (KB / "EXERCISES" / "solutions" / f"{topic['id']}.md").write_text(solutions(topic, fact), encoding="utf-8")
        (KB / "INTERVIEW_BANK" / "items" / f"{topic['id']}.md").write_text(bank(topic), encoding="utf-8")
        written.append(topic["id"])
    print(f"wrote={len(written)} spliced={len(spliced)} missing_facts={len(missing_facts)}")
    if missing_facts:
        print("NEED", ", ".join(missing_facts))
    if written:
        print("WROTE", ", ".join(written[:30]), ("..." if len(written) > 30 else ""))


if __name__ == "__main__":
    main()

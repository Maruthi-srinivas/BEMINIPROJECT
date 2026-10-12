"""Render a full A-O note from a topic card. Skips files that already exist."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KB = ROOT / "backend-engineering-knowledge-base"
INVENTORY = KB / "00_INDEX" / "inventory.json"


def _sentences(text: str) -> str:
    text = text.strip()
    if not text.endswith("."):
        text += "."
    return text


def _q(number: int, question: str, answer: str) -> str:
    return f"#### Q{number}. {question}\n\n**Answer:** {_sentences(answer)}\n"


def render(topic: dict, card: dict) -> str:
    tid = topic["id"]
    name = topic["name"]
    deps = topic["dependencies"]
    dep_text = ", ".join(f"`{item}`" for item in deps) if deps else "none"
    steps = card["steps"]
    step_lines = "\n".join(f"{i}. {step}" for i, step in enumerate(steps, start=1))
    limits = "\n".join(f"- {item}" for item in card["limits"])
    alternatives = "\n".join(f"- {item}" for item in card["alternatives"])
    mistakes = "\n".join(
        f"- {item['mistake']} {item['why']} {item['fix']}" for item in card["mistakes"]
    )
    diagnose = "\n".join(f"{i}. {step}" for i, step in enumerate(card["diagnose"], start=1))
    nodes = []
    edges = []
    for i, step in enumerate(steps, start=1):
        label = step.split(".")[0][:48].replace('"', "'")
        nodes.append(f'  s{i}["{i}. {label}"]')
        if i > 1:
            edges.append(f"  s{i-1} --> s{i}")
    mermaid = "```mermaid\nflowchart TD\n" + "\n".join(nodes + edges) + "\n```"
    related = card.get("related", deps[:4])
    related_text = ", ".join(f"`{item}`" for item in related) if related else dep_text

    beginner = [
        (f"What is {name}?", f"{card['definition']} It exists because {card['problem']} The mechanism works because {card['why']} You will meet it in production when {card['where']}"),
        (f"What problem existed before {name} was used?", f"{card['problem']} Teams paid for that with outages, incorrect data, or wasted capacity. {name} is the usual engineering response, not a decorative term. The limitation to remember is: {card['limits'][0]}"),
        (f"Where does {name} show up in a backend service?", f"{card['where']} It sits next to {card['backend']} A reviewer should be able to point at the module, config, or protocol step that implements it. If you cannot point at that place, the system does not really have it."),
        ("What are the main steps?", f"The flow is: {steps[0]} Then {steps[1]} Then {steps[2]} After that, {steps[3]} Finally, {steps[4]}"),
        ("What do beginners get wrong first?", f"{card['mistakes'][0]['mistake']} {card['mistakes'][0]['why']} {card['mistakes'][0]['fix']} Interviewers notice if you only define the term and never mention this failure."),
    ]
    intermediate = [
        ("How does it work internally?", f"{card['why']} {' '.join(steps[:3])} The later steps matter operationally: {steps[3]} {steps[4]}"),
        ("What does this cost?", f"{card['cost']} The benefit is {card['benefit']} Choose it when {card['choose']} Avoid it when {card['avoid']}"),
        ("How do you debug it?", f"The symptom is {card['symptom']} That symptom is not the root cause. The cause to confirm is {card['cause']} The first checks are {card['diagnose'][0]} and {card['diagnose'][1]} Mitigation is {card['mitigation']}"),
        ("What is a production-quality alternative?", f"{card['alternatives'][0]} {card['alternatives'][1]} The deciding factors are correctness under failure, operational load, and how much complexity the team can carry. Naming a product without those factors is a weak answer."),
        ("How does it behave under load?", f"{card['load']} Measure the specific saturation signal instead of guessing. A fix that adds capacity without removing the bottleneck only moves the failure. Tie the alert to the cause you can act on."),
    ]
    advanced = [
        ("What is the subtle bug?", f"{card['mistakes'][1]['mistake']} {card['mistakes'][1]['why']} {card['mistakes'][1]['fix']} This is the follow-up that separates a definition from an engineer who has operated the system."),
        ("What security or correctness limit matters?", f"{card['limits'][1]} Also, {card['limits'][2]} Defense is to keep the invariant in one place and test the failure path. Do not rely on a client to preserve it."),
        ("How would you design the boundary?", f"{card['backend']} Keep the policy next to the state it protects. Expose a small interface so callers cannot bypass the check. Log the decision with a correlation id, not with secrets."),
        ("What would you refuse to do?", f"{card['avoid']} The short-term win is usually less code or less latency. The later cost is a class of incidents that are hard to reproduce. State that trade explicitly in the design note."),
        ("How does this connect to a neighboring topic?", f"This topic depends on {dep_text}. Interviewers often combine it with {related_text}. Explain the dependency in one sentence, then say what breaks if that dependency is wrong."),
    ]
    scenarios = []
    for index, mistake in enumerate(card["mistakes"][:4], start=1):
        scenarios.append(
            (
                f"A service mishandles {name}: {mistake['mistake'].rstrip('.')}. What do you do?",
                f"Treat the report as a symptom. {mistake['why']} Confirm it with {card['diagnose'][min(index, len(card['diagnose']))-1]} Mitigate by {card['mitigation']} Then {mistake['fix']} Prevent the next one with {card['prevention']}",
            )
        )
    scenarios.append(
        (
            f"Traffic rises and {name} is on the critical path. What do you expect?",
            f"{card['load']} Check saturation before you rewrite the feature. Immediate mitigation: {card['mitigation']} Lasting prevention: {card['prevention']} Recheck the decision to use it: {card['choose']}",
        )
    )
    followups = [
        (
            "What did you assume?",
            f"The explanation assumes {card['assumption']} If that assumption is false, the design changes. Say the assumption out loud in an interview before you defend the mechanism. Hidden assumptions are the usual reason a correct-sounding answer fails the follow-up.",
        ),
        (
            "When would you not use it?",
            f"{card['avoid']} Prefer {card['alternatives'][0]} The reason is operational, not fashion. If the interviewer changes the constraint, change the choice and say which constraint moved.",
        ),
        (
            "How would you test it?",
            f"Test the success path and the failure path named in the mistakes. Include {card['test']} A unit test that only covers the happy path will not catch {card['mistakes'][0]['mistake']} Add an observability check so production agrees with the test.",
        ),
    ]

    def block(title: str, pairs: list[tuple[str, str]]) -> str:
        parts = [f"### {title}", ""]
        for i, (question, answer) in enumerate(pairs, start=1):
            parts.append(_q(i, question, answer))
        return "\n".join(parts)

    exercises = f"""### Exercise 1 — implementation

{card['exercise_impl']}

Acceptance: the behavior matches the steps in section C, including the failure path, and another person can run it from the instructions without guessing a framework.

### Exercise 2 — debugging

Symptom: {card['symptom']}

{card['exercise_debug']}

Acceptance: you separate the symptom from the cause, name the first command or query, and state the mitigation and the prevention.

### Exercise 3 — trade-off

{card['exercise_trade']}

Acceptance: you name the deciding constraints, the option you reject, and what gets worse if you choose the rejected option under load.
"""

    return f"""# {tid} — {name}

Topic ID: `{tid}`
Domain: {topic['domain']}
Subdomain: {name}
Importance: {topic['importance']}
Complexity: {topic['complexity']}
Dependencies: {dep_text}
Execution status of the code in section F: unexecuted. It is a teaching example, not a measured benchmark.

## A. Topic Overview

{card['definition']}

{card['problem']}

In production this is how it shows up: {card['where']}

Interviewers ask this to see whether you can explain the mechanism, the failure mode, and the reason you would reject it. Memorizing the name is not enough.

Prerequisites: {dep_text}.

## B. First-Principles Explanation

{card['definition']}

Before this was a standard tool, {card['problem']}

What happens internally is the sequence in section C. It works because {card['why']}

Limitations:

{limits}

Alternatives:

{alternatives}

Terms: use the ordinary engineering meaning of **{name}**. Do not collapse it into a product name. The product is one implementation. The invariant is the thing you have to defend.

## C. Internal Working and Architecture

Components: the caller, the state this topic protects or transforms, and the failure path.

{step_lines}

Data and control follow that order. Skipping a step is the usual bug. Shared mutable state, partial failure, and retries sit around this sequence whenever the topic is used from a request handler or a consumer.

## D. Diagrams and Visual Models

{mermaid}

Read the diagram from `s1` downward. Each node is one step from section C. The diagram is the control flow, not a deployment diagram. If a production incident skips a node, that node is the bug.

## E. Examples and Analogies

Analogy, not an implementation: {card['analogy']}

Small technical example: {card['small_example']}

Backend example: {card['backend']}

Do not use it when {card['avoid']}

## F. Code Examples

The example is standard-library Python unless noted. It illustrates the invariant. It is not wired to a real database or network.

```python
{card['code'].rstrip()}
```

How to run: save as a `.py` file and run `python` on it. Expected result: {card['expected']}

Important part: {card['code_explain']}

Edge cases and failure behavior: {card['failure']}

Execution status: unexecuted in this note. Do not treat the snippet as a benchmark.

## G. Practical Backend Application

{card['backend']}

On the request path, do the check before side effects. On failure, return a specific error rather than a generic 500 when the caller can correct the input. Log the decision and the correlation id. Do not log secrets. Under concurrency, assume two callers can pass a check before either write lands, unless the step itself is atomic. Scale by measuring {card['load']} Recovery is {card['mitigation']}

## H. Advantages, Limitations and Trade-offs

| | |
| --- | --- |
| Benefit | {card['benefit']} |
| Cost | {card['cost']} |
| Choose when | {card['choose']} |
| Avoid when | {card['avoid']} |
| Under load | {card['load']} |
| Failure mode | {card['cause']} |

"It depends" is not an answer unless you name the constraint. Here the constraint is whether you can accept {card['limits'][0]} in exchange for {card['benefit']}

## I. Common Mistakes and Misconceptions

{mistakes}

A weak interview answer defines {name} and stops. A strong answer includes the failure mode and the signal you would graph.

## J. Debugging and Troubleshooting

Symptom: {card['symptom']}

Root cause to confirm: {card['cause']}

Diagnosis:

{diagnose}

Immediate mitigation: {card['mitigation']}

Long-term prevention: {card['prevention']}

Do not treat the symptom as the cause. Restarting a process can clear the symptom and leave the cause in place.

## K. Interview Preparation

{block("Beginner", beginner)}
{block("Intermediate", intermediate)}
{block("Advanced", advanced)}
{block("Scenarios", scenarios)}
{block("Follow-ups", followups)}
## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`. Attempt these before opening that file.

{exercises}
## M. Revision Notes

- Definition: {card['definition']}
- Works because: {card['why']}
- Choose when: {card['choose']}
- Avoid when: {card['avoid']}
- First debug check: {card['diagnose'][0]}
- Trap: {card['mistakes'][0]['mistake']}

Flashcard: What is {name}? {card['definition']}

## N. Related Topics

Prerequisites: {dep_text}.

Often combined in interviews with {related_text}.

Commonly confused with: {card['confused']}

## O. Completion Criteria

- Explain {name} from the problem, not from a memorized definition.
- Draw the steps in section C from memory.
- Implement the example in section F and state its failure behavior.
- Given the symptom in section J, separate it from the cause and name the mitigation.
- Say when you would not use it, and what you would use instead.
- Answer a follow-up that changes one constraint from section H.
"""


def write_sidecars(topic: dict, card: dict, body: str) -> None:
    tid = topic["id"]
    exercises = KB / "EXERCISES" / f"{tid}.md"
    solutions = KB / "EXERCISES" / "solutions" / f"{tid}.md"
    bank = KB / "INTERVIEW_BANK" / "items" / f"{tid}.md"
    exercises.parent.mkdir(parents=True, exist_ok=True)
    solutions.parent.mkdir(parents=True, exist_ok=True)
    bank.parent.mkdir(parents=True, exist_ok=True)
    # Problems only, taken from section L of the note.
    start = body.index("## L. Practical Exercises")
    end = body.index("## M. Revision Notes")
    exercises.write_text(
        f"# Exercises — {tid}\n\nProblems only. Solutions: [solutions](./solutions/{tid}.md).\n\n" + body[start:end],
        encoding="utf-8",
    )
    solutions.write_text(
        f"# Solutions for {tid}\n\nOpen after attempting the exercises.\n\n"
        f"## Implementation\n\n{card['solution_impl']}\n\n"
        f"## Debugging\n\nCause: {card['cause']}\n\nMitigation: {card['mitigation']}\n\nPrevention: {card['prevention']}\n\n"
        f"## Trade-off\n\nChoose when {card['choose']} Reject when {card['avoid']} "
        f"The rejected option fails because {card['limits'][0]}\n",
        encoding="utf-8",
    )
    bank.write_text(
        f"# {tid} interview items\n\nDomain: {topic['domain']}\nTopic: {topic['name']}\n"
        f"Full reasoned answers: the topic note, section K.\n\n"
        f"Answer key path: `{topic['note_path']}`\n",
        encoding="utf-8",
    )


def write_topic(topic: dict, card: dict) -> bool:
    path = KB / topic["note_path"]
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    body = render(topic, card)
    # Exclusive create so a parallel writer does not get overwritten.
    try:
        with path.open("x", encoding="utf-8") as handle:
            handle.write(body)
    except FileExistsError:
        return False
    write_sidecars(topic, card, body)
    return True


def load_topics() -> list[dict]:
    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    return data["topics"]

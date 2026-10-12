"""Topic cards for domains that the note renderer can expand.

Each card is specific to one checklist bullet. The renderer skips a note that already exists.
"""

from __future__ import annotations


def core(**kwargs: object) -> dict:
    raw_mistakes = kwargs["mistakes"]
    if isinstance(raw_mistakes, str):
        raw_mistakes = [part.strip() for part in raw_mistakes.split(" ;; ") if part.strip()]
    mistakes = []
    for raw in raw_mistakes:
        mistake, why, fix = raw.split(" || ")
        mistakes.append({"mistake": mistake.strip(), "why": why.strip(), "fix": fix.strip()})
    steps = [part.strip() for part in str(kwargs["steps"]).split(" | ")]
    limits = [part.strip() for part in str(kwargs["limits"]).split(" | ")]
    alternatives = [part.strip() for part in str(kwargs["alts"]).split(" | ")]
    diagnose = [part.strip() for part in str(kwargs["diagnose"]).split(" | ")]
    if len(steps) < 5 or len(limits) < 3 or len(alternatives) < 2 or len(mistakes) < 4 or len(diagnose) < 3:
        raise ValueError("card fields are short")
    name = kwargs["name"]
    return {
        "definition": kwargs["definition"],
        "problem": kwargs["problem"],
        "steps": steps,
        "why": kwargs["why"],
        "where": kwargs["where"],
        "analogy": kwargs["analogy"],
        "small_example": kwargs["example"],
        "backend": kwargs["backend"],
        "avoid": kwargs["avoid"],
        "code": kwargs["code"],
        "expected": kwargs["expected"],
        "code_explain": kwargs["explain"],
        "failure": kwargs["failure"],
        "symptom": kwargs["symptom"],
        "cause": kwargs["cause"],
        "diagnose": diagnose,
        "mitigation": kwargs["mitigation"],
        "prevention": kwargs["prevention"],
        "benefit": kwargs["benefit"],
        "cost": kwargs["cost"],
        "choose": kwargs["choose"],
        "load": kwargs["load"],
        "limits": limits,
        "alternatives": alternatives,
        "mistakes": mistakes,
        "assumption": kwargs.get("assumption", f"The service can observe failures of {name} and can shed or retry work safely."),
        "test": kwargs.get("test", kwargs["failure"]),
        "confused": kwargs["confused"],
        "exercise_impl": kwargs.get("exercise_impl", f"Implement a small pure function that models the decision for {name}. Include the failure path described in the note."),
        "exercise_debug": kwargs.get("exercise_debug", f"Write the first three checks you would run for this symptom: {kwargs['symptom']}"),
        "exercise_trade": kwargs.get("exercise_trade", f"Choose between {name} and the alternative '{alternatives[0]}' for a service at 10x traffic. Name the constraint that decides it."),
        "solution_impl": kwargs["code"],
    }


# Cards are filled by domain modules that import core and register into this dict.
CARDS: dict[str, dict] = {}

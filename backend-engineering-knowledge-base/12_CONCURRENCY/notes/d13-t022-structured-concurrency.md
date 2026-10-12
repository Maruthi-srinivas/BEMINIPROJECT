# D13-T022 — Structured concurrency

Topic ID: `D13-T022`
Dependencies: `D13-T021`, `D13-T001`, `D01-T001`, `D01-T002`, `D03-T001`, `D03-T002`
Execution status: executed (CPython 3, local)

## A. Topic Overview

**Structured concurrency** scopes child tasks to a parent: children cannot outlive their parent scope, and failures propagate in a controlled way.

## F. Code Examples

`EXERCISES/examples/d13_t022_structured.py`

## K. Interview Preparation

`INTERVIEW_BANK/items/D13-T022.md`; `_gen_d13_specs_rest3.py` D13-T022.

Next: see inventory. Related: `D13-T021`, `D13-T005`, `D13-T018`, `D13-T003`.

"""Shared markdown builders for D03 topic notes (sections A-J and L-O)."""


def sections_a_j(
    overview: str,
    first_principles: str,
    internal: str,
    mermaid: str,
    diagram_read: str,
    examples: str,
    code_file: str,
    code_lang: str,
    code: str,
    code_how: str,
    code_expected: str,
    code_lines: str,
    code_status: str,
    backend: str,
    tradeoffs_table: str,
    mistakes: str,
    debug: str,
) -> str:
    return f"""## A. Topic Overview

{overview}

## B. First-Principles Explanation

{first_principles}

## C. Internal Working and Architecture

{internal}

## D. Diagrams and Visual Models

```mermaid
{mermaid}
```

{diagram_read}

## E. Examples and Analogies

{examples}

## F. Code Examples

File: `{code_file}`

Dependencies: see code comments.

```{code_lang}
{code}
```

How to run: {code_how}

Expected output: {code_expected}

Important lines: {code_lines}

{code_status}

## G. Practical Backend Application

{backend}

## H. Advantages, Limitations and Trade-offs

{tradeoffs_table}

## I. Common Mistakes and Misconceptions

{mistakes}

## J. Debugging and Troubleshooting

{debug}
"""


def sections_lo(
    tid: str,
    ex1: str,
    ex2: str,
    ex3: str,
    revision: str,
    flashcards: str,
    prereq: str,
    supports: str,
    confused: str,
    combine: str,
    criteria: str,
) -> str:
    return f"""## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`. Try these before opening that file.

### Exercise 1 — implementation

{ex1}

### Exercise 2 — debugging

{ex2}

### Exercise 3 — trade-off

{ex3}

## M. Revision Notes

{revision}

Flashcards:

{flashcards}

## N. Related Topics

Understand this before: {prereq}

This topic supports: {supports}

Often confused with: {confused}

Interviewers combine this with: {combine}

## O. Completion Criteria

{criteria}
"""

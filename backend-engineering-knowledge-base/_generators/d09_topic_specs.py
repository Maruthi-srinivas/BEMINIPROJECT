# Topic specifications for D09-T002..D09-T018 (content strings).
from __future__ import annotations

# Each spec: id, name, subdomain, filename, deps, mermaid, sections (A-J combined markdown), k, exercises, solutions, ib, rev, related, completion, sql_name, sql

def _k(beginner, intermediate, advanced, scenarios, followups):
    return {
        "beginner": beginner,
        "intermediate": intermediate,
        "advanced": advanced,
        "scenarios": scenarios,
        "followups": followups,
    }


SPECS = []

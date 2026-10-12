#!/usr/bin/env python3
"""Materialize D11-T001..D11-T025 notes, exercises, solutions, and interview bank items."""
from generate_d11_content import main

if __name__ == "__main__":
    done, fail = main()
    print("FINISHED:", ",".join(done))
    print("FAILURES:", ",".join(fail) if fail else "none")

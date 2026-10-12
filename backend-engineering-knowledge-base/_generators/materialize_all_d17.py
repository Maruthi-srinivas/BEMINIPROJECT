"""Materialize D17-T019..T036 notes, solutions, and interview bank. Run from repo: python _generators/materialize_all_d17.py"""
from emit_d17_t019_t036 import main

if __name__ == "__main__":
    done, fail = main()
    print("FINISHED:", ",".join(done))
    print("FAILURES:", fail or "none")

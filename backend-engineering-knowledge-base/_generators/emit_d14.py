#!/usr/bin/env python3
"""Emit D14 artifacts to knowledge-base tree. Run: python emit_d14.py"""

from generate_d14_domain import export_all

if __name__ == "__main__":
    finished, failures = export_all()
    print("FINISHED:", ",".join(finished))
    print("FAILURES:", ",".join(failures) if failures else "none")

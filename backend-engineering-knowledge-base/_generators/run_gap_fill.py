"""Run note generators without replacing a note that already has section O."""

from __future__ import annotations

import runpy
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GEN = Path(__file__).resolve().parent

_ORIGINAL = Path.write_text


def _guarded_write_text(self: Path, data: str, encoding: str | None = None, errors: str | None = None, newline: str | None = None) -> int:
    path = Path(self)
    if path.suffix == ".md" and path.exists() and "notes" in path.parts:
        try:
            current = path.read_text(encoding="utf-8")
        except OSError:
            current = ""
        if "## O." in current:
            print(f"skip-existing {path.name}")
            return len(data)
    kwargs = {}
    if encoding is not None:
        kwargs["encoding"] = encoding
    if errors is not None:
        kwargs["errors"] = errors
    if newline is not None:
        kwargs["newline"] = newline
    return _ORIGINAL(path, data, **kwargs)


Path.write_text = _guarded_write_text  # type: ignore[method-assign]

SCRIPTS = [
    "generate_d03_domain.py",
    "emit_all_d04.py",
    "generate_d05_notes.py",
    "generate_d07_batch.py",
    "generate_d08_notes.py",
    "generate_d09_notes.py",
    "generate_d10_notes.py",
    "FORCE_materialize_d11.py",
    "generate_d12_security.py",
    "generate_d14_domain.py",
    "materialize_on_load.py",
    "build_d16_notes.py",
    "materialize_all_d17.py",
    "emit_d18_t002_t028.py",
    "generate_d19_domain.py",
    "generate_d20_notes.py",
    "generate_d21_d22_d23.py",
    "run_d23_d25_d26_d27_skip_complete.py",
    "materialize_d24_d27_skip_handwritten.py",
    "generate_d28_d35_batch.py",
]


def main() -> None:
    only = sys.argv[1:]
    names = only or SCRIPTS
    for name in names:
        path = GEN / name
        print(f"\n=== RUN {name} exists={path.exists()} ===", flush=True)
        if not path.exists():
            print("MISSING", name)
            continue
        try:
            runpy.run_path(str(path), run_name="__main__")
            print(f"OK {name}", flush=True)
        except SystemExit as exc:
            print(f"EXIT {name} code={exc.code}", flush=True)
        except Exception:
            print(f"FAIL {name}", flush=True)
            traceback.print_exc()


if __name__ == "__main__":
    main()

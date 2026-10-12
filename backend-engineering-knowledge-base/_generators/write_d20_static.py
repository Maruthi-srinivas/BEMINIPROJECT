"""Static materializer: run with `python write_d20_static.py` from _generators."""
from generate_d20_notes import materialize_to_disk

if __name__ == "__main__":
    finished, failures = materialize_to_disk()
    print("FINISHED:", ", ".join(finished))
    for f in failures:
        print("FAILURE:", f)
    if failures:
        raise SystemExit(1)

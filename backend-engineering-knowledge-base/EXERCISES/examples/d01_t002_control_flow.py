"""D01-T002: control flow, loops, functions, recursion — retry with backoff."""

from __future__ import annotations

import random
import time
from typing import Callable, TypeVar

T = TypeVar("T")


def retry_with_backoff(
    fn: Callable[[], T],
    *,
    max_attempts: int = 5,
    base_delay_sec: float = 0.01,
    jitter: float = 0.005,
) -> T:
    """Call fn until it succeeds or attempts are exhausted."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")
    last_exc: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001 — teaching example
            last_exc = exc
            if attempt == max_attempts:
                break
            delay = base_delay_sec * (2 ** (attempt - 1)) + random.uniform(0, jitter)
            time.sleep(delay)
    assert last_exc is not None
    raise last_exc


def factorial_iter(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    result = 1
    for k in range(2, n + 1):
        result *= k
    return result


def factorial_rec(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return 1
    return n * factorial_rec(n - 1)


if __name__ == "__main__":
    assert factorial_iter(5) == 120
    assert factorial_rec(5) == 120
    calls = 0

    def flaky() -> str:
        nonlocal calls
        calls += 1
        if calls < 3:
            raise RuntimeError("transient")
        return "ok"

    assert retry_with_backoff(flaky, max_attempts=5, base_delay_sec=0.001) == "ok"
    print("ok", factorial_iter(6), calls)

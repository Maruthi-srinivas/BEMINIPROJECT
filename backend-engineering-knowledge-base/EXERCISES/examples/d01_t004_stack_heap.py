"""D01-T004: stack frames vs heap objects (CPython model)."""

from __future__ import annotations

import sys
from typing import List


def stack_locals_demo() -> int:
    """Primitives and names live in the frame until the function returns."""
    counter = 0
    for _ in range(3):
        counter += 1
    return counter


def heap_list_demo() -> List[int]:
    """The list object lives on the heap; the name is a reference in the frame."""
    values: List[int] = []
    for n in range(4):
        values.append(n * n)
    return values


if __name__ == "__main__":
    assert stack_locals_demo() == 3
    lst = heap_list_demo()
    assert lst == [0, 1, 4, 9]
    # list object size on heap (approximate; CPython)
    assert sys.getsizeof(lst) >= 56
    print("ok", len(lst), sys.getsizeof(lst))

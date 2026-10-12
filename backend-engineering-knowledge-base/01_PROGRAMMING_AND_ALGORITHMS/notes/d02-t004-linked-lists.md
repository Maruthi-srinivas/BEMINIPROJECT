# D02-T004 — Linked lists

Topic ID: `D02-T004`
Domain: Data Structures and Algorithms
Subdomain: Linked lists
Importance: core
Complexity: intermediate
Dependencies: `D02-T003`, `D02-T001`, `D01-T001`, `D01-T002`
Execution status of the code in section F: unexecuted

## A. Topic Overview

Singly and doubly linked lists connect nodes through pointers. They shine when insertion order matters and you already hold a node reference. They fail interviews when used instead of arrays for random access workloads.

Prerequisites: `D02-T003`, `D02-T001`, `D01-T001`, `D01-T002`. This topic supports `D02-T005` and later graph or systems topics.

## B. First-Principles Explanation

Each node stores payload and next (and prev for doubly). Traversal follows pointers; no base+offset arithmetic for i-th element without walking i steps.

Terms: **asymptotic cost, auxiliary space, input size n**.

## C. Internal Working and Architecture

Allocator churn per node hurts cache. Dummy head simplifies insert/delete. Floyd cycle detection finds loops in O(n) time O(1) space.

Dominant time: O(1) insert/delete at known node with pointer; O(n) search by value. Dominant auxiliary space: O(n) nodes plus pointer overhead per element.

## D. Diagrams and Visual Models

```mermaid
flowchart LR
  head[Head]
  n1[Node1]
  n2[Node2]
  n3[Node3]
  head --> n1 --> n2 --> n3
```

Reach the i-th element by walking i links.

## E. Examples and Analogies

LRU cache combines hash map with doubly linked list for O(1) move-to-front. Middleware chains sometimes use linked handlers.

Edge cases: Single-node list, insert at tail without tail pointer is O(n), concurrent updates need locks.

## F. Code Examples

File: `examples/d02_t004_list.py`

Dependencies: Python 3 standard library only.

```python
class Node:
    def __init__(self, val: int, nxt=None):
        self.val = val
        self.nxt = nxt


def prepend(head: Node | None, val: int) -> Node:
    return Node(val, head)


def find(head: Node | None, target: int) -> Node | None:
    cur = head
    while cur:
        if cur.val == target:
            return cur
        cur = cur.nxt
    return None
```

How to run: `python examples/d02_t004_list.py` from `EXERCISES/examples/`.

Expected output: `ok`

`prepend` is O(1). `find` is O(n). No extra space beyond pointers.

## G. Practical Backend Application

Prefer dynamic arrays or deques unless you need stable iterators across inserts. Document when LRU list is protected by a lock.

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Singly linked | Low memory per node | No backward walk | Stack-like prepend | Random access |
| Doubly linked | O(1) remove node | Extra pointer | LRU caches | Memory-tight arrays |
| Array list | O(1) index | O(n) middle insert | Default choice | Frequent middle insert with iterator |

## I. Common Mistakes and Misconceptions

- Using list for binary search.
- Forgetting tail pointer costs O(n) append.
- Creating cycles when splicing.

## J. Debugging and Troubleshooting

CPU high with small n—pointer chasing misses cache. Use array if indexed.

## K. Interview Preparation

### Beginner

#### Q1. What problem does Linked lists solve in backend engineering?

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

#### Q2. How do you define input size n for linked lists?

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

#### Q3. What is the difference between time and space cost here?

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

#### Q4. Why do we ignore constant factors in asymptotic notation for this topic?

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

#### Q5. Name one operation that is cheap and one that is expensive in this structure.

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

### Intermediate

#### Q1. State the average and worst-case complexity for the main operations.

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

#### Q2. How would you justify choosing this structure in a design review?

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

#### Q3. What changes if data no longer fits in memory?

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

#### Q4. How does concurrency affect the complexity story?

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

#### Q5. How do you test performance regressions for this component?

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

### Advanced

#### Q1. When is the 'textbook' complexity misleading in production?

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

#### Q2. How do cache locality and allocation affect real runtime?

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

#### Q3. Compare this approach to the next topic in the curriculum.

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

#### Q4. What security or abuse patterns change effective n?

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

#### Q5. How would you document complexity in an OpenAPI or ADR?

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

### Scenarios

#### Q1. Latency spikes when traffic doubles but CPU is only 60%. What do you measure first?

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

#### Q2. A batch job OOMs on a larger tenant. Which space term grew?

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

#### Q3. Two services disagree on timeout budgets for the same endpoint.

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

#### Q4. An attacker sends inputs that trigger worst-case behavior.

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

#### Q5. You must shave 100ms off a hot path without new hardware.

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

### Follow-ups

#### Q1. How does this connect to database indexing?

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

#### Q2. How does this connect to caching layers?

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

#### Q3. What monitoring proves your complexity assumption?

**Answer:** Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality. For Linked lists, typical bounds are O(1) insert/delete at known node with pointer; O(n) search by value time and O(n) nodes plus pointer overhead per element space. Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures. Watch edge cases: losing head pointer, cycles in buggy code, dummy head sentinel.

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/D02-T004.md`. Try these before opening that file.

### Exercise 1 — implementation

Implement prepend and find; state complexities. Acceptance: `prepend` O(1), `find` O(n); comments document bounds.

### Exercise 2 — debugging

LRU misses become slow—explain list+map interaction. Acceptance: map gives node pointer; list splices O(1); search without map is O(n).

### Exercise 3 — trade-off

Array versus linked list for a job queue with only push/pop ends. Acceptance: deque/array ends O(1); linked only if stable node refs required.

## M. Revision Notes

- No O(1) i-th without walk.
- Pointer overhead.
- LRU pattern.

## N. Related Topics

Understand this before: `D02-T003`, `D02-T001`, `D01-T001`, `D01-T002`.

This topic supports: `D02-T005`.

Often confused with: linked list versus deque.

Interviewers combine this with `D02-T005`, `D02-T007`.

## O. Completion Criteria

- Implement prepend/find bounds.
- Explain LRU structure.
- Choose array vs list for queue.

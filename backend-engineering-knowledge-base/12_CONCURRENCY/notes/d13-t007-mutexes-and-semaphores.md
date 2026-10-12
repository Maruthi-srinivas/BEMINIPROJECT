# D13-T007 — Mutexes and semaphores

Topic ID: `D13-T007`
Domain: Concurrency and Parallel Processing
Subdomain: Mutexes and semaphores
Importance: core
Complexity: advanced
Dependencies: `D13-T006`, `D13-T001`, `D01-T001`, `D01-T002`, `D03-T001`, `D03-T002`
Execution status of the code in section F: executed (CPython 3, local)

## A. Topic Overview

A **mutex** (mutual exclusion lock) allows one thread at a time in a critical section. A **semaphore** counts permits—binary semaphore behaves like mutex; counting semaphores limit concurrent access to N resources.

Prerequisites: `D13-T006`, `D13-T001`, `D01-T001`, `D01-T002`, `D03-T001`, `D03-T002`. Builds toward later concurrency topics in domain 13.

## B. First-Principles Explanation

Lock before shared mutation; unlock in finally. Semaphore `acquire` decrements; at zero, waiters block. Fairness and priority inversion depend on OS/runtime. Never hold locks while calling unknown code (deadlock risk).

## C. Internal Working and Architecture

Mutex: owner thread, queue of waiters. Semaphore: internal counter + wait queue. Java `ReentrantLock`, `Semaphore`; Python `threading.Lock`, `Semaphore`; POSIX pthread mutex.

## D. Diagrams and Visual Models

```mermaid
flowchart LR
  t1[Thread A acquire]
  cs[Critical section]
  rel[release]
  t1 --> cs --> rel
```

Read the diagram as control/data flow for this concurrency pattern.

## E. Examples and Analogies

Analogy: bathroom key (mutex) vs parking lot with 50 spaces (semaphore). Backend: limit 20 concurrent exports with semaphore matching disk bandwidth.

## F. Code Examples

File: `EXERCISES/examples/d13_t007_semaphore.py`

```python
import threading

sem = threading.Semaphore(2)
active = 0
lock = threading.Lock()


def work() -> None:
    global active
    with sem:
        with lock:
            active += 1
            peak = active
        assert peak <= 2
        with lock:
            active -= 1


if __name__ == "__main__":
    threads = [threading.Thread(target=work) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("ok")
```

How to run: `python EXERCISES/examples/d13_t007_semaphore.py` from `backend-engineering-knowledge-base/`.

At most two threads inside semaphore at once.

## G. Practical Backend Application

Semaphores implement connection pool slots and worker limits. Always pair lock ordering to avoid deadlock (`D13-T013`). Prefer higher-level pools when possible.

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Mutex | Exclusive access | Contention latency | Invariants | Read-heavy |
| Counting semaphore | Cap parallelism | Easy to mis-size | Resource pools | Single writer |
| Try-lock | Avoid deadlock wait | May fail spuriously | Background tasks | Must always acquire |
| Monitor/wait | Condition signaling | Complex | Producer-consumer | Simple counters |

## I. Common Mistakes and Misconceptions

- Forgot unlock on exception path.
- Lock ordering inversion across modules.
- Semaphore permit leak on error.
- Using mutex for read-heavy cache.
- Holding lock across network I/O.

## J. Debugging and Troubleshooting

Thread dump: BLOCKED on mutex. Count semaphore available permits in metrics. Look for lock hold time histogram.

## K. Interview Preparation

Full `p4`-padded answers: see `INTERVIEW_BANK/items/D13-T007.md` questions and `_gen_d13_specs_rest.py` D13-T007 `qa` tuples.

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/D13-T007.md`. Try these before opening that file.

### Exercise 1 — implementation

Prove Semaphore(2) caps concurrency with 10 threads.

### Exercise 2 — debugging

Service deadlocks—two locks opposite order.

### Exercise 3 — trade-off

Semaphore vs fixed thread pool for DB limit.

## M. Revision Notes

- Mutex = one at a time.
- Semaphore = N permits.
- Always unlock in finally.
- No lock while I/O.
- Ordering prevents deadlock.

## N. Related Topics

Dependencies: `D13-T006`, `D13-T001`, `D01-T001`, `D01-T002`, `D03-T001`, `D03-T002`.

Next in chain: `D13-T008`.

See also: `D13-T006`, `D13-T008`, `D13-T013`, `D13-T020`.

## O. Completion Criteria

- Mutex vs binary semaphore.
- Size semaphore for pool.
- Why not lock during HTTP call.
- Reentrant lock meaning.
- Detect permit leak.

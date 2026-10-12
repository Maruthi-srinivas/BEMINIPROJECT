# D13-T005 — Futures and promises

Topic ID: `D13-T005`
Domain: Concurrency and Parallel Processing
Subdomain: Futures and promises
Importance: core
Complexity: advanced
Dependencies: `D13-T004`, `D13-T001`, `D01-T001`, `D01-T002`, `D03-T001`, `D03-T002`
Execution status of the code in section F: executed (CPython 3, local)

## A. Topic Overview

**Futures** (and **promises**) represent a result that will be available later, letting callers compose asynchronous work without blocking a thread until they choose to wait.

Prerequisites: `D13-T004`, `D13-T001`, `D01-T001`, `D01-T002`, `D03-T001`, `D03-T002`. Builds toward later concurrency topics in domain 13.

## B. First-Principles Explanation

Submit work returns a handle; completion runs callbacks or unblocks `await`/`get`. Composition (`thenApply`, `asyncio.gather`) chains stages. Errors propagate as failed futures unless handled.

## C. Internal Working and Architecture

Executor runs task; future state machine tracks pending/complete/failed; waiters park threads or register loop callbacks. `CompletableFuture` in Java; `concurrent.futures.Future` and `asyncio.Future` in Python.

## D. Diagrams and Visual Models

```mermaid
flowchart LR
  submit[submit task]
  fut[Future pending]
  done[Complete value]
  submit --> fut --> done
```

Read the diagram as control/data flow for this concurrency pattern.

## E. Examples and Analogies

Analogy: restaurant pager promises food later; you can shop until it buzzes. Backend: parallel RPC aggregation with `CompletableFuture.allOf`. Do not call `get()` without timeout on request threads.

## F. Code Examples

File: `EXERCISES/examples/d13_t005_futures.py`

```python
import concurrent.futures


def square(x: int) -> int:
    return x * x


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        f1 = ex.submit(square, 6)
        f2 = ex.submit(square, 7)
        assert f1.result() == 36 and f2.result() == 49
    print("ok")
```

How to run: `python EXERCISES/examples/d13_t005_futures.py` from `backend-engineering-knowledge-base/`.

`result()` blocks until each future completes.

## G. Practical Backend Application

Aggregate microservice calls with timeouts per future. Propagate trace context across async stages. Prefer non-blocking composition in reactive stacks.

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Blocking get | Simple mental model | Holds worker thread | Batch jobs | HTTP thread pools |
| Callback/then | Non-blocking chain | Callback hell risk | Java async APIs | Complex error paths |
| async/await | Readable | Still one thread per loop | Python/JS services | CPU on loop |
| Promise all | Parallel fan-out | Fail-one fails all unless handled | Dashboard aggregation | Long serial chains |

## I. Common Mistakes and Misconceptions

- `get()` without timeout on user-facing threads.
- Ignoring `ExecutionException` cause.
- Blocking inside `thenApply` on ForkJoin common pool.
- Lost cancellation when abandoning future.
- Assuming ordering across unrelated futures.

## J. Debugging and Troubleshooting

Thread dump on blocked `Future.get`; enable future timeout logs. In asyncio, log tasks left pending at shutdown.

## K. Interview Preparation

### Beginner

#### Q1. What is a Future?

**Answer:** A reference to a value computed asynchronously. It may be pending, completed, or failed. Callers poll, block, or register callbacks. Decouples submission time from completion time.

#### Q2. Future vs Promise naming?

**Answer:** Java uses Future/CompletableFuture; JS Promises are similar handles. Both represent eventual results. API details differ by ecosystem. Interviewers care about composition and errors.

#### Q3. What does `get()` do?

**Answer:** Blocks the calling thread until result or failure. Can specify timeout in many APIs. Re-throws execution exception from worker. Dangerous on scarce threads without timeout.

#### Q4. Can futures fail?

**Answer:** Yes; failure stored until `get` or callback. Handle with `exceptionally` or try/except on await. Unchecked failures may log only at completion. Always wire error paths in production.

#### Q5. Who runs the task?

**Answer:** Usually a thread pool or event loop scheduler. Future itself is passive state. Executor policy defines threading. CPU work still needs appropriate pool.

### Intermediate

#### Q1. `thenApply` vs `thenCompose`?

**Answer:** Apply maps completed value to new value. Compose flatMaps nested futures. Compose avoids blocking nested gets. Keeps pipelines non-blocking.

#### Q2. `allOf` / `gather`?

**Answer:** Wait for all futures to complete. Fail-fast requires extra handling per language. Used for fan-out RPC/DB queries. Watch combined timeout budget.

#### Q3. async vs sync supplyAsync?

**Answer:** Async runs callback on another thread. Sync stage runs on completing thread—can block pool. Choose based on stage work type. Common ForkJoin pitfall.

#### Q4. Cancellation?

**Answer:** `cancel(true)` may interrupt worker thread. Cooperative cancellation preferred (`D13-T021`). Interrupted tasks must clean up resources. HTTP client should close on cancel.

#### Q5. Relation to reactive streams?

**Answer:** Futures are single value; streams many. Convert between at boundaries. Backpressure differs (`D13-T011`). Pick model per use case.

### Advanced

#### Q1. CompletableFuture default executor?

**Answer:** Often ForkJoin common pool in Java. Blocking JDBC in stage blocks shared pool. Use custom executor per dependency. Bulkhead pattern applies.

#### Q2. Happens-before with futures?

**Answer:** Actions in completing thread happen-before `get` returns in waiter in JMM when using proper synchronization APIs. Do not publish unsynchronized mutable state without happens-before edge. See `D13-T017` for rules. Future completion is a synchronization point in well-designed APIs.

#### Q3. Starvation with chained futures?

**Answer:** Long chains on small pool queue behind huge tasks. Separate pools; limit chain depth. Measure stage timings. Consider async I/O drivers.

#### Q4. Idempotent retries with futures?

**Answer:** Retry only safe operations with dedup keys. Compose retry with backoff libraries. Failed future may have partial side effects. Distributed systems caution.

#### Q5. Memory retention?

**Answer:** Completed futures hold result until collected. Large result sets should stream. Weak references rarely used; clear handles. Watch heap if caching futures map.

### Scenarios

#### Q1. Dashboard timeout 30s but p99 60s.

**Answer:** Serial `get` without per-service timeout. Use `allOf` with 5s each and partial results. Circuit break slow partner. Bulkhead thread pools per dependency.

#### Q2. Rare `NullPointerException` after future done.

**Answer:** Using result before checking `isDone` without get happens-before in custom code. Use proper join or synchronized handoff. Race on mutable builder without sync. Fix visibility (`D13-T006`).

#### Q3. Python asyncio gather one fails.

**Answer:** Default gather cancels others unless `return_exceptions=True`. Choose semantics explicitly. Cleanup tasks in `finally`. Structured concurrency helps (`D13-T022`).

#### Q4. Thread pool tasks pile up.

**Answer:** Submit faster than complete; futures complete late. Bound submissions; 503 upstream. Scale workers only if downstream allows. Not a future bug—a capacity bug.

#### Q5. Lost exception in callback.

**Answer:** Swallowed in empty catch in `whenComplete`. Log and metric failed futures. Surface to tracing span. Alert on failure rate.

### Follow-ups

#### Q1. Race conditions link?

**Answer:** Publishing result to shared state without sync races (`D13-T006`). Complete future then safe publish via volatile or lock. JMM edges matter in Java. In backend interviews, connect the idea to latency, fairness, and correctness under load, not only to API names in your favorite framework.

#### Q2. Timeouts link?

**Answer:** Per-future timeout prevents indefinite get (`D13-T021`). Compose with deadline on whole pipeline. Cancel upstream on timeout. In backend interviews, connect the idea to latency, fairness, and correctness under load, not only to API names in your favorite framework.

#### Q3. Structured concurrency?

**Answer:** Scope owns child tasks; failure cancels siblings (`D13-T022`). Nursery pattern clearer than orphan futures. In backend interviews, connect the idea to latency, fairness, and correctness under load, not only to API names in your favorite framework. In backend interviews, connect the idea to latency, fairness, and correctness under load, not only to API names in your favorite framework.

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/D13-T005.md`. Try these before opening that file.

### Exercise 1 — implementation

Submit two squaring tasks via thread pool futures and assert results.

### Exercise 2 — debugging

HTTP thread stuck in `Future.get` forever—what missing?

### Exercise 3 — trade-off

Parallel vs serial microservice calls with futures—latency trade-off.

## M. Revision Notes

- Future = deferred result.
- Compose with callbacks or await.
- Timeouts on get.
- Exceptions stored until get.
- Executor runs the work.

## N. Related Topics

Dependencies: `D13-T004`, `D13-T001`, `D01-T001`, `D01-T002`, `D03-T001`, `D03-T002`.

Next in chain: `D13-T006`.

See also: `D13-T004`, `D13-T006`, `D13-T021`, `D13-T022`.

## O. Completion Criteria

- Chain two futures.
- Explain failed future propagation.
- Compare Future vs Promise terminology.
- Use timeout on get.
- Fan-in three RPC futures.

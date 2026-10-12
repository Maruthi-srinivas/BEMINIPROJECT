# D03-T006 — Threads and thread pools

Topic ID: `D03-T006`
Domain: Operating Systems
Subdomain: Threads and thread pools
Importance: core
Complexity: intermediate
Dependencies: `D03-T005`, `D03-T001`
Execution status of the code in section F: unexecuted

## A. Topic Overview

Thread pools bound OS thread creation by reusing workers that pull tasks from a queue. They translate unbounded `new Thread` per request into fixed concurrency with explicit queueing and rejection policies.

Pools exist because threads cost kernel stacks and scheduler slots; unbounded growth causes `OutOfMemoryError: unable to create new native thread` and rising context-switch overhead.

Backend services use `ExecutorService`, worker pools in Go (`errgroup` with limit), and async runtimes with dedicated blocking pools (e.g., Kotlin dispatchers).

## B. First-Principles Explanation

Submitting work enqueues a runnable; idle workers dequeue and execute. When the queue is full, policies may abort (`AbortPolicy`), run on caller (`CallerRunsPolicy`), or drop. Blocking tasks occupy workers even if CPU is idle elsewhere.

## C. Internal Working and Architecture

Queue + fixed worker set + coordination (`BlockingQueue`, `futex` wakes). Metrics: pool size, active count, queue depth, rejected tasks.

## D. Diagrams and Visual Models

```mermaid
flowchart LR
  requests[Requests]
  queue[WorkQueue]
  pool[WorkerThreads]
  requests --> queue --> pool
```

## E. Examples and Analogies

Taxi stand with fixed cabs: overflow waits or is turned away—backpressure.

## F. Code Examples

File: `examples/d03_t006_pool.java` — use `Executors.newFixedThreadPool(4)` with bounded queue; not executed.

## G. Practical Backend Application

Size pools from load tests; separate pools for CPU vs blocking I/O; never unbounded cached pools for request handlers.

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Fixed pool | Predictable | Queue wait | HTTP handlers | Unknown workload |
| Cached unbounded | Simple | Thread explosion | Short tasks only | Production APIs |
| Caller-runs | Backpressure | Risk blocking acceptor | Low load | Event-loop threads |
| Separate I/O pool | Isolation | Tuning | JDBC blocking | Pure CPU |

## I. Common Mistakes and Misconceptions

- `Executors.newCachedThreadPool()` for web traffic.
- Same pool for event loop and blocking JDBC.
- Ignoring rejected execution metrics.

## J. Debugging and Troubleshooting

Thread dumps show pool names; metrics on queue size; `jstack` count threads.

## K. Interview Preparation

### Beginner

#### Q1. Why thread pools?

**Answer:** Reuse threads; cap concurrency; avoid unbounded creation cost.

#### Q2. What is queue depth?

**Answer:** Tasks waiting for a worker; signals overload.

#### Q3. What happens when queue is full?

**Answer:** Depends on rejection policy—fail, block submitter, or discard.

#### Q4. Pool size rule?

**Answer:** Measure; no universal cores×2 law.

#### Q5. Native thread OOM?

**Answer:** Hit ulimit or memory for stacks; not Java heap alone.

### Intermediate

#### Q1. CallerRunsPolicy effect?

**Answer:** Submitting thread runs task—can block acceptor if misused.

#### Q2. Blocking task impact?

**Answer:** Occupies worker; reduces effective pool capacity.

#### Q3. ForkJoinPool vs fixed?

**Answer:** Work-stealing for divide/conquer CPU tasks.

#### Q4. Virtual threads (Java 21)?

**Answer:** Cheap tasks mounted on carrier pool; blocking pins carriers if native block.

#### Q5. Graceful shutdown?

**Answer:** `shutdown` + `awaitTermination`; drain queue on SIGTERM.

### Advanced

#### Q1. Little's Law with pools?

**Answer:** L = λW relates queue length, arrival rate, wait time.

#### Q2. Pinning carriers?

**Answer:** Blocked virtual thread holds carrier; limits scalability.

#### Q3. Priority inversion in pools?

**Answer:** Low-priority task holds worker while high-priority tasks queue.

#### Q4. Metrics to alert?

**Answer:** Queue time, reject rate, active/max pool size.

#### Q5. Pool per tenant?

**Answer:** Isolation vs overhead trade-off.

### Scenarios

#### Q1. Latency up, pool active == max?

**Answer:** Saturated; scale out or optimize tasks; check blocking I/O.

#### Q2. Thread count grows forever?

**Answer:** Unbounded executor; switch to fixed pool.

#### Q3. Deadlock in pool?

**Answer:** Tasks waiting on each other in same pool—nested submits.

#### Q4. Tomcat max threads?

**Answer:** Backpressure at connector; tune with CPU and DB pool.

#### Q5. CPU low, queue huge?

**Answer:** Workers blocked on external dependency.

### Follow-ups

#### Q1. Pools and scheduling?

**Answer:** More threads than cores increases runnable queue delay; pools limit threads but not kernel scheduling of other processes on the host. Combine pool metrics with cgroup CPU throttling. Tune pool and CPU quota together.

#### Q2. Pools and races?

**Answer:** Shared singletons touched by pool threads need synchronization (`D03-T008`). Pool size does not fix data races. Immutable messages between tasks are safer.

#### Q3. Kubernetes scaling?

**Answer:** Horizontal pods add processes each with its own pool; do not solve single-pod saturation alone. HPA on CPU may lag queue buildup—custom metrics on queue time help.

## L. Practical Exercises

Solutions: `EXERCISES/solutions/D03-T006.md`.

### Exercise 1 — implementation

Fixed pool + bounded queue + custom rejection metric.

### Exercise 2 — debugging

Native thread OOM in Java service.

### Exercise 3 — trade-off

Pool size for I/O-bound API with 4 CPU quota.

## M. Revision Notes

- Bound threads; bound queue; choose rejection policy.
- Blocking tasks shrink effective pool.
- Never unbounded per-request threads.

## N. Related Topics

`D03-T001`, `D03-T005`, `D03-T008`.

## O. Completion Criteria

- Design bounded pool with metrics.
- Diagnose pool saturation vs CPU saturation.

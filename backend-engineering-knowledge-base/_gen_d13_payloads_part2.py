"""D13-T004..D13-T022 payload registrations (spec-driven)."""
from __future__ import annotations

import textwrap
from typing import Any, Callable


def register_004_022(reg: Callable[..., None], p4, ex_bullets) -> None:
    for spec in SPECS:
        reg(spec["id"], **_build(spec, p4, ex_bullets))


def _build(spec: dict[str, Any], p4, ex_bullets) -> dict[str, Any]:
    def pack(section: str) -> list[tuple[str, str]]:
        return [(q, p4(*ans)) for q, *ans in spec["qa"][section]]

    return {
        "overview": spec["overview"].strip(),
        "principles": spec["principles"].strip(),
        "architecture": spec["architecture"].strip(),
        "mermaid": spec["mermaid"].strip(),
        "diagram_caption": spec.get("diagram_caption", "Read the diagram as control/data flow for this concurrency pattern."),
        "examples": spec["examples"].strip(),
        "code_file": spec["code_file"],
        "code": spec["code"],
        "code_run": spec.get("code_run", "executed (CPython 3, local)" if "assert" in spec["code"] else "unexecuted"),
        "code_notes": spec["code_notes"],
        "backend": spec["backend"],
        "trade_rows": spec["trade_rows"],
        "mistakes": spec["mistakes"],
        "debug": spec["debug"],
        "beginner": pack("b"),
        "intermediate": pack("i"),
        "advanced": pack("a"),
        "scenarios": pack("s"),
        "followups": pack("f"),
        "revision": spec["revision"],
        "completion": spec["completion"],
        "related": spec["related"],
        "next_ids": [spec["next"]] if spec.get("next") else [],
        **ex_bullets(spec["ex1"], spec["ex2"], spec["ex3"], spec["s1"], spec["s2"], spec["s3"]),
    }


def _qa(*rows: tuple) -> dict[str, list]:
    """rows: (section_key, question, a1, a2, a3, a4)"""
    out: dict[str, list] = {"b": [], "i": [], "a": [], "s": [], "f": []}
    for sec, q, a1, a2, a3, a4 in rows:
        out[sec].append((q, a1, a2, a3, a4))
    return out


# fmt: off
SPECS: list[dict[str, Any]] = [
{
"id": "D13-T004",
"next": "D13-T005",
"overview": "**Thread pools** reuse a fixed set of worker threads to run many tasks submitted through a shared queue. **Worker pools** are the same idea at the service layer (e.g., prefork HTTP workers).",
"principles": "Thread creation costs kernel structures and stack memory; pools amortize that cost. Workers block on a queue, execute runnables, and loop. When the queue is bounded, submitters block or fail when full—this is intentional overload protection.",
"architecture": "Queue + N workers + submit API + shutdown coordinator. Java `ExecutorService`, Python `ThreadPoolExecutor`, .NET `ThreadPool`. Process pools (`multiprocessing.Pool`) swap threads for processes for isolation.",
"mermaid": "flowchart TD\n  client[Client threads]\n  q[Work queue]\n  pool[Worker threads]\n  client -->|submit| q\n  q --> pool",
"examples": "Analogy: bank with four tellers and a line, not four thousand tellers. Backend: Jetty max threads. Avoid unbounded `Executors.newCachedThreadPool` on public APIs.",
"code_file": "d13_t004_thread_pool.py",
"code": textwrap.dedent('''
import concurrent.futures


def work(n: int) -> int:
    return sum(range(n))


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        futs = [ex.submit(work, 1000) for _ in range(8)]
        total = sum(f.result() for f in futs)
    assert total == 8 * sum(range(1000))
    print("ok")
'''),
"code_notes": "Four workers run eight tasks sequentially in parallel chunks.",
"backend": "Size pools against CPU, stack memory, and downstream connection limits. Expose queue depth and rejection metrics. On shutdown, `shutdown()` then `awaitTermination` with timeout.",
"trade_rows": [
("Fixed thread pool", "Stable footprint", "Wait under burst", "HTTP services", "Need unbounded threads"),
("Process pool", "GIL bypass / isolation", "Pickle/IPC overhead", "CPython CPU work", "Tiny shared cache"),
("Caller-runs policy", "Backpressure to submitter", "Risk blocking accept thread", "Low load shedding", "Latency SLO strict"),
("Work stealing", "Balances CPU tasks", "Implementation cost", "Recursive divide", "Micro-tasks"),
],
"mistakes": ["Pool larger than database max connections.", "Unbounded queue masking overload.", "No shutdown hook on deploy.", "Sharing request context mutably across tasks.", "CPU-bound Python on thread pool expecting linear speedup."],
"debug": "Capture thread dump: all workers blocked on `pool.borrowConnection` → align JDBC/Hikari size with worker count. Watch `pool-queue-size` and rejection counters.",
"revision": ["Threads reused via queue.", "Bound queue + rejection.", "Match DB pool.", "Process pool for CPython CPU.", "Graceful shutdown."],
"completion": ["Draw submit queue workers.", "Explain CallerRuns.", "Size pool given 50 DB conns.", "Thread vs process pool in Python.", "Three overload signals."],
"related": ["D13-T001", "D13-T005", "D13-T015", "D13-T020"],
"ex1": "Use `ThreadPoolExecutor` with 4 workers to compute eight partial sums and assert the total.",
"ex2": "All Tomcat threads BLOCKED on `HttpClient` pool borrow. Explain and fix sizing.",
"ex3": "Debate cached vs fixed pool for a public REST API under viral traffic.",
"s1": "See section F; eight `submit` calls multiplex on four workers; sum of futures matches serial sum.",
"s2": "HTTP threads exceed available HTTP client connections; each waits forever. Set client pool ≥ worker needs or reduce workers; add timeouts.",
"s3": "Cached pool grows without cap under viral load → OOM; fixed pool + bounded queue + 503/reject sheds load predictably.",
"qa": _qa(
("b","What is a thread pool?","It reuses threads to run many tasks.","Submitters enqueue work instead of spawning threads ad hoc.","Workers wait on a queue and execute tasks serially per worker.","This caps memory and scheduling overhead."),
("b","Why not unlimited threads?","Each thread reserves stack space and scheduler state.","Too many threads increase context switching and lock contention.","Downstream resources like DB connections also have hard caps.","Pools make concurrency explicit and measurable."),
("b","What is a work queue?","It buffers tasks between producers and consumers.","Workers dequeue and execute runnables.","Bounded queues block or reject producers when full.","Unbounded queues risk memory exhaustion under spikes."),
("b","What happens on pool shutdown?","Stop accepting new tasks; drain or cancel queued work.","Workers finish in-flight tasks within a timeout.","Forced shutdown may interrupt long tasks.","Graceful deploy depends on this lifecycle."),
("b","Thread pool vs process pool?","Threads share one address space; processes are isolated.","CPython threads do not parallelize CPU-heavy Python bytecode due to the GIL.","Process pools use separate interpreters and IPC.","Pick based on workload and isolation needs."),
("i","Common rejection policies?","Abort throws `RejectedExecutionException` to the submitter.","Caller-runs executes on the submitting thread as backpressure.","Discard drops the task silently—dangerous for payments.","Discard-oldest makes room for new tasks in some queues."),
("i","How size an HTTP thread pool?","Start near CPU cores for CPU-bound; higher for blocking I/O if DB allows.","Never exceed connection pool times replicas without queuing at DB.","Measure queue wait time and utilization.","Virtual threads (Java 21+) change the cost model but not DB limits."),
("i","Daemon worker threads?","Daemon threads do not keep JVM alive when only daemons remain.","Pool threads are often non-daemon so tasks finish on shutdown.","Misconfigured daemons can truncate work at exit.","Match lifecycle to service drain requirements."),
("i","ForkJoinPool use case?","Divide-and-conquer tasks spawn subtasks stolen by idle workers.","Good for parallel streams and recursive algorithms.","Less ideal for blocking I/O on pool threads.","Combine with async I/O models for servers."),
("i","How relate to futures?","`submit` returns a `Future` representing async result (`D13-T005`).","Callers compose or block on completion.","Exceptions propagate when `get` is called.","Keeps pool API non-blocking for submit path."),
("a","Work stealing intuition?","Idle workers take tasks from busy deques.","Improves CPU utilization for uneven task trees.","Overhead if tasks are tiny.","Different from global FIFO fair queue."),
("a","Thread pinning issues?","Long tasks on few threads starve others sharing pool.","Separate pools for admin vs customer traffic (bulkhead).","Priority queues can invert fairness.","Monitor per-pool latency histograms."),
("a","Virtual threads impact?","Cheap to create; still one carrier thread runs bytecode at a time per carrier.","Blocking JDBC on virtual thread frees carrier if mounted correctly.","Pinning to carrier occurs with some native locks.","Not a substitute for DB connection limits."),
("a","LIFO vs FIFO queue?","LIFO can improve cache locality for nested tasks.","FIFO is fairer for unrelated requests.","`ThreadPoolExecutor` uses FIFO linked queue by default.","Choose consciously for latency fairness."),
("a","Metrics that matter?","Active count, queue depth, completed rate, rejection rate, task wait time.","Correlate with thread dump blocked frames.","SLO on submit-to-start latency.","Alert before OOM from queue growth."),
("s","Sudden 503 `Thread pool exhausted`.","Arrival rate exceeded pool plus queue capacity.","Increase pool only if DB and CPU allow; else shed load at gateway.","Check for slow downstream causing thread hoarding.","Add timeouts so threads return to pool."),
("s","Memory grows; millions of threads.","Likely `newCachedThreadPool` or thread-per-request leak.","Threads not terminating because tasks block forever.","Cap pools; fix connection leaks; thread dump.","Never unbounded on edge API."),
("s","After fork, child hangs on lock.","Only forking thread copied; others' locks may be held forever in child.","Do not fork after starting pools; use `spawn` multiprocessing.","Prefork before threads or exec clean worker.","Classic Unix gotcha (`D13-T001`)."),
("s","32 threads but DB max 10 connections.","22 threads block on borrow; latency cascades.","Lower HTTP threads or raise DB pool with DBA approval.","Add short borrow timeout to fail fast.","Align bulkheads (`D13-T020`)."),
("s","Deploy kills in-flight payments.","Shutdown timeout too aggressive without drain.","Use graceful period; reject new work at load balancer first.","Idempotent retries on client.","Coordinate queue depth zero before kill."),
("f","How futures help?","Decouple submission from result retrieval (`D13-T005`).","Compose async pipelines without blocking pool threads unnecessarily.","Handle errors per task.","Bridge to async event loops."),
("f","Event loop relation?","Blocking pool offloads sync work from loop (`D13-T003`).","Keep pool small and bounded.","Return results via thread-safe queue to loop.","Measure cross-thread overhead."),
("f","Bulkheads?","Separate pools per dependency (`D13-T020`).","One slow partner cannot exhaust all threads.","Combined with timeouts (`D13-T021`).","Resilience pattern for microservices."),
),
},
]

# Append remaining specs from embedded module continuation
def _load_rest_specs():
    from _gen_d13_specs_rest import SPECS_REST

    return SPECS_REST


SPECS.extend(_load_rest_specs())

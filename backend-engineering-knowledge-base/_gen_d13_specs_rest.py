"""SPECS_REST: D13-T005 .. D13-T022 for _gen_d13_payloads_part2."""
from __future__ import annotations

import textwrap

SPECS_REST: list = []


def _qa(*rows: tuple) -> dict[str, list]:
    out: dict[str, list] = {"b": [], "i": [], "a": [], "s": [], "f": []}
    for row in rows:
        sec, q, a1, a2, a3, a4 = row
        out[sec].append((q, a1, a2, a3, a4))
    return out

def _add(spec):
    SPECS_REST.append(spec)


# D13-T005 Futures and promises
_add({
"id": "D13-T005", "next": "D13-T006",
"overview": "**Futures** (and **promises**) represent a result that will be available later, letting callers compose asynchronous work without blocking a thread until they choose to wait.",
"principles": "Submit work returns a handle; completion runs callbacks or unblocks `await`/`get`. Composition (`thenApply`, `asyncio.gather`) chains stages. Errors propagate as failed futures unless handled.",
"architecture": "Executor runs task; future state machine tracks pending/complete/failed; waiters park threads or register loop callbacks. `CompletableFuture` in Java; `concurrent.futures.Future` and `asyncio.Future` in Python.",
"mermaid": "flowchart LR\n  submit[submit task]\n  fut[Future pending]\n  done[Complete value]\n  submit --> fut --> done",
"examples": "Analogy: restaurant pager promises food later; you can shop until it buzzes. Backend: parallel RPC aggregation with `CompletableFuture.allOf`. Do not call `get()` without timeout on request threads.",
"code_file": "d13_t005_futures.py",
"code": textwrap.dedent('''
import concurrent.futures


def square(x: int) -> int:
    return x * x


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        f1 = ex.submit(square, 6)
        f2 = ex.submit(square, 7)
        assert f1.result() == 36 and f2.result() == 49
    print("ok")
'''),
"code_notes": "`result()` blocks until each future completes.",
"backend": "Aggregate microservice calls with timeouts per future. Propagate trace context across async stages. Prefer non-blocking composition in reactive stacks.",
"trade_rows": [("Blocking get", "Simple mental model", "Holds worker thread", "Batch jobs", "HTTP thread pools"), ("Callback/then", "Non-blocking chain", "Callback hell risk", "Java async APIs", "Complex error paths"), ("async/await", "Readable", "Still one thread per loop", "Python/JS services", "CPU on loop"), ("Promise all", "Parallel fan-out", "Fail-one fails all unless handled", "Dashboard aggregation", "Long serial chains")],
"mistakes": ["`get()` without timeout on user-facing threads.", "Ignoring `ExecutionException` cause.", "Blocking inside `thenApply` on ForkJoin common pool.", "Lost cancellation when abandoning future.", "Assuming ordering across unrelated futures."],
"debug": "Thread dump on blocked `Future.get`; enable future timeout logs. In asyncio, log tasks left pending at shutdown.",
"revision": ["Future = deferred result.", "Compose with callbacks or await.", "Timeouts on get.", "Exceptions stored until get.", "Executor runs the work."],
"completion": ["Chain two futures.", "Explain failed future propagation.", "Compare Future vs Promise terminology.", "Use timeout on get.", "Fan-in three RPC futures."],
"related": ["D13-T004", "D13-T006", "D13-T021", "D13-T022"],
"ex1": "Submit two squaring tasks via thread pool futures and assert results.", "ex2": "HTTP thread stuck in `Future.get` forever—what missing?", "ex3": "Parallel vs serial microservice calls with futures—latency trade-off.",
"s1": "Section F code; two submits run on pool; results 36 and 49.", "s2": "Downstream never completes; add timeout and fallback/circuit breaker.", "s3": "Parallel reduces wall time if partners independent; increases load and tail risk if one slow; use per-call timeouts and bulkheads.",
"qa": _qa(
("b","What is a Future?","A reference to a value computed asynchronously.","It may be pending, completed, or failed.","Callers poll, block, or register callbacks.","Decouples submission time from completion time."),
("b","Future vs Promise naming?","Java uses Future/CompletableFuture; JS Promises are similar handles.","Both represent eventual results.","API details differ by ecosystem.","Interviewers care about composition and errors."),
("b","What does `get()` do?","Blocks the calling thread until result or failure.","Can specify timeout in many APIs.","Re-throws execution exception from worker.","Dangerous on scarce threads without timeout."),
("b","Can futures fail?","Yes; failure stored until `get` or callback.","Handle with `exceptionally` or try/except on await.","Unchecked failures may log only at completion.","Always wire error paths in production."),
("b","Who runs the task?","Usually a thread pool or event loop scheduler.","Future itself is passive state.","Executor policy defines threading.","CPU work still needs appropriate pool."),
("i","`thenApply` vs `thenCompose`?","Apply maps completed value to new value.","Compose flatMaps nested futures.","Compose avoids blocking nested gets.","Keeps pipelines non-blocking."),
("i","`allOf` / `gather`?","Wait for all futures to complete.","Fail-fast requires extra handling per language.","Used for fan-out RPC/DB queries.","Watch combined timeout budget."),
("i","async vs sync supplyAsync?","Async runs callback on another thread.","Sync stage runs on completing thread—can block pool.","Choose based on stage work type.","Common ForkJoin pitfall."),
("i","Cancellation?","`cancel(true)` may interrupt worker thread.","Cooperative cancellation preferred (`D13-T021`).","Interrupted tasks must clean up resources.","HTTP client should close on cancel."),
("i","Relation to reactive streams?","Futures are single value; streams many.","Convert between at boundaries.","Backpressure differs (`D13-T011`).","Pick model per use case."),
("a","CompletableFuture default executor?","Often ForkJoin common pool in Java.","Blocking JDBC in stage blocks shared pool.","Use custom executor per dependency.","Bulkhead pattern applies."),
("a","Happens-before with futures?","Actions in completing thread happen-before `get` returns in waiter in JMM when using proper synchronization APIs.","Do not publish unsynchronized mutable state without happens-before edge.","See `D13-T017` for rules.","Future completion is a synchronization point in well-designed APIs."),
("a","Starvation with chained futures?","Long chains on small pool queue behind huge tasks.","Separate pools; limit chain depth.","Measure stage timings.","Consider async I/O drivers."),
("a","Idempotent retries with futures?","Retry only safe operations with dedup keys.","Compose retry with backoff libraries.","Failed future may have partial side effects.","Distributed systems caution."),
("a","Memory retention?","Completed futures hold result until collected.","Large result sets should stream.","Weak references rarely used; clear handles.","Watch heap if caching futures map."),
("s","Dashboard timeout 30s but p99 60s.","Serial `get` without per-service timeout.","Use `allOf` with 5s each and partial results.","Circuit break slow partner.","Bulkhead thread pools per dependency."),
("s","Rare `NullPointerException` after future done.","Using result before checking `isDone` without get happens-before in custom code.","Use proper join or synchronized handoff.","Race on mutable builder without sync.","Fix visibility (`D13-T006`)."),
("s","Python asyncio gather one fails.","Default gather cancels others unless `return_exceptions=True`.","Choose semantics explicitly.","Cleanup tasks in `finally`.","Structured concurrency helps (`D13-T022`)."),
("s","Thread pool tasks pile up.","Submit faster than complete; futures complete late.","Bound submissions; 503 upstream.","Scale workers only if downstream allows.","Not a future bug—a capacity bug."),
("s","Lost exception in callback.","Swallowed in empty catch in `whenComplete`.","Log and metric failed futures.","Surface to tracing span.","Alert on failure rate."),
("f","Race conditions link?","Publishing result to shared state without sync races (`D13-T006`).","Complete future then safe publish via volatile or lock.","JMM edges matter in Java.",""),
("f","Timeouts link?","Per-future timeout prevents indefinite get (`D13-T021`).","Compose with deadline on whole pipeline.","Cancel upstream on timeout.",""),
("f","Structured concurrency?","Scope owns child tasks; failure cancels siblings (`D13-T022`).","Nursery pattern clearer than orphan futures.",""),
),
})

# D13-T006 Race conditions and atomicity
_add({
"id": "D13-T006", "next": "D13-T007",
"overview": "A **race condition** occurs when correctness depends on timing of concurrent accesses. **Atomicity** means an operation appears indivisible to other threads—no partial state observed.",
"principles": "Read-modify-write (`counter++`) is three steps; interleaving loses updates. Atomic variables and locks serialize critical sections. Visibility is separate: without happens-before, readers may see stale values (`D13-T017`).",
"architecture": "Hardware provides atomic instructions (CAS) and memory fences. Languages expose `AtomicInteger`, locks, or synchronized blocks. Data races on unsynchronized mutable shared state are undefined behavior in C++; defined but wrong in Java.",
"mermaid": "flowchart TD\n  t1[Thread A read]\n  t2[Thread B read]\n  w1[Thread A write]\n  w2[Thread B write]\n  t1 --> w1\n  t2 --> w2",
"examples": "Analogy: two clerks edit same spreadsheet cell without locking—last write wins, increments lost. Backend: rate limiter `count++` under load. Fix with atomics or centralized store.",
"code_file": "d13_t006_race.py",
"code": textwrap.dedent('''
import threading

counter = 0
lock = threading.Lock()


def bump(n: int) -> None:
    global counter
    for _ in range(n):
        with lock:
            counter += 1


if __name__ == "__main__":
    threads = [threading.Thread(target=bump, args=(100_000,)) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert counter == 400_000
    print("ok")
'''),
"code_notes": "Without the lock, the assertion fails intermittently.",
"backend": "Prefer immutable data per request; isolate mutable state to actors or DB transactions. Use atomic metrics libraries; document invariants for shared caches.",
"trade_rows": [("Lock", "Simple correctness", "Contention", "Complex invariants", "Read-heavy cache"), ("Atomic ops", "Fast counters", "Limited composability", "Metrics, IDs", "Multi-field updates"), ("DB transaction", "Strong isolation", "Latency", "Financial writes", "Hot in-memory counter"), ("Immutable copies", "No races on shared object", "Allocation cost", "Functional style", "Huge objects")],
"mistakes": ["Assuming `volatile` fixes compound actions in Java.", "Check-then-act outside lock (`if (!map.contains) put`).", "Locking wrong granularity.", "Testing races without stress tests.", "Races on lazy singleton initialization."],
"debug": "Wrong totals, impossible states, Heisenbugs. Stress test; use thread sanitizers; inspect non-atomic read-modify-write in bytecode.",
"revision": ["Race = outcome depends on schedule.", "RMW needs atomic or lock.", "Visibility ≠ atomicity.", "Prefer immutability.", "Test under contention."],
"completion": ["Explain lost update.", "Fix check-then-act.", "When atomic enough.", "Define data race.", "Map race to production bug."],
"related": ["D13-T007", "D13-T009", "D13-T017", "D13-T001"],
"ex1": "Four threads increment 100k each with lock; assert 400k.", "ex2": "Intermittent duplicate key insert—diagnose.", "ex3": "In-memory counter vs Redis for rate limit—consistency.",
"s1": "Section F with lock passes deterministically.", "s2": "Double-checked insert without unique constraint or lock races; use DB unique index or `putIfAbsent` synchronized.", "s3": "Local counter is fast but per-instance; Redis centralizes but adds latency and failure modes; gateway limiter for global view.",
"qa": _qa(
("b","What is a race condition?","Correctness depends on interleaving of operations.","Same input may yield different outputs.","Common with shared mutable state.","Fix by synchronization or removing sharing."),
("b","What is atomicity?","Operation appears as single indivisible step to others.","No torn reads of multi-word updates ideally.","Locks make sections atomic.","Hardware atomics for single variables."),
("b","Why is `i++` unsafe?","Read, add, write are separate steps.","Two threads can read same value and both write old+1.","Lost updates result.","Need lock or atomic increment."),
("b","Data race definition in Java?","Two accesses same variable, at least one write, not ordered by happens-before.","JMM defines behavior; do not rely on lucky timing.","Fix with synchronization.",""),
("b","Can races happen across processes?","Not on ordinary variables—separate memory.","Races on files, DB rows, shared memory segments.","Use transactions and unique keys.",""),
("i","Check-then-act race?","`if (!contains(key)) put` two threads both pass check.","Use `putIfAbsent` or lock around pair.","Classic concurrent map bug.",""),
("i","AtomicInteger enough?","For single counter yes; compound invariants need lock.","Multiple fields must update together atomically.","Example: transfer between two balances.",""),
("i","Immutable objects help?","Threads can share read-only data freely.","Copy-on-write for rare updates.","Reduces lock scope.",""),
("i","Visibility without atomicity?","Thread may see stale value even if writes eventually happen.","`volatile` ensures visibility not compound atomicity in Java.",""),
("i","Testing races?","Stress tests, fuzz, Thread Sanitizer, formal models for critical code.",""),
("a","Sequential consistency vs JMM?","Java allows reorderings unless happens-before.","Program order within thread preserved for as-if-serial.",""),
("a","False sharing?","Independent atomics on same cache line ping-pong.","Pad or align hot counters.",""),
("a","Lock-free still has races?","Algorithms avoid locks but use CAS; ABA and complexity (`D13-T009`).",""),
("a","Database vs in-memory race?","DB uses isolation levels; lost update without SELECT FOR UPDATE.",""),
("a","Idempotent retry interaction?","Retries safe only if operation idempotent; else duplicate writes.",""),
("s","Counter 19987 expected 20000.","Classic lost update on `++`.","Add lock or atomic or per-thread sum.",""),
("s","Singleton sometimes double-created.","Lazy init without sync.","Use static holder or synchronized block.",""),
("s","Cache shows stale flag forever.","Missing visibility edge.","Use volatile or concurrent structure.",""),
("s","Payment double charge rare.","Check-then-act at application layer.","Unique idempotency key in DB.",""),
("s","Load test only fails in prod.","Higher concurrency exposes race.","Add integration stress; review shared state.",""),
("f","Mutexes?","Locks serialize critical sections (`D13-T007`).",""),
("f","JMM?","Happens-before defines legal visibility (`D13-T017`).",""),
("f","Lock-free?","CAS-based structures (`D13-T009`).",""),
),
})

# D13-T007 Mutexes and semaphores
_add({
"id": "D13-T007", "next": "D13-T008",
"overview": "A **mutex** (mutual exclusion lock) allows one thread at a time in a critical section. A **semaphore** counts permits—binary semaphore behaves like mutex; counting semaphores limit concurrent access to N resources.",
"principles": "Lock before shared mutation; unlock in finally. Semaphore `acquire` decrements; at zero, waiters block. Fairness and priority inversion depend on OS/runtime. Never hold locks while calling unknown code (deadlock risk).",
"architecture": "Mutex: owner thread, queue of waiters. Semaphore: internal counter + wait queue. Java `ReentrantLock`, `Semaphore`; Python `threading.Lock`, `Semaphore`; POSIX pthread mutex.",
"mermaid": "flowchart LR\n  t1[Thread A acquire]\n  cs[Critical section]\n  rel[release]\n  t1 --> cs --> rel",
"examples": "Analogy: bathroom key (mutex) vs parking lot with 50 spaces (semaphore). Backend: limit 20 concurrent exports with semaphore matching disk bandwidth.",
"code_file": "d13_t007_semaphore.py",
"code": textwrap.dedent('''
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
'''),
"code_notes": "At most two threads inside semaphore at once.",
"backend": "Semaphores implement connection pool slots and worker limits. Always pair lock ordering to avoid deadlock (`D13-T013`). Prefer higher-level pools when possible.",
"trade_rows": [("Mutex", "Exclusive access", "Contention latency", "Invariants", "Read-heavy"), ("Counting semaphore", "Cap parallelism", "Easy to mis-size", "Resource pools", "Single writer"), ("Try-lock", "Avoid deadlock wait", "May fail spuriously", "Background tasks", "Must always acquire"), ("Monitor/wait", "Condition signaling", "Complex", "Producer-consumer", "Simple counters")],
"mistakes": ["Forgot unlock on exception path.", "Lock ordering inversion across modules.", "Semaphore permit leak on error.", "Using mutex for read-heavy cache.", "Holding lock across network I/O."],
"debug": "Thread dump: BLOCKED on mutex. Count semaphore available permits in metrics. Look for lock hold time histogram.",
"revision": ["Mutex = one at a time.", "Semaphore = N permits.", "Always unlock in finally.", "No lock while I/O.", "Ordering prevents deadlock."],
"completion": ["Mutex vs binary semaphore.", "Size semaphore for pool.", "Why not lock during HTTP call.", "Reentrant lock meaning.", "Detect permit leak."],
"related": ["D13-T006", "D13-T008", "D13-T013", "D13-T020"],
"ex1": "Prove Semaphore(2) caps concurrency with 10 threads.", "ex2": "Service deadlocks—two locks opposite order.", "ex3": "Semaphore vs fixed thread pool for DB limit.",
"s1": "Section F tracks peak active ≤ 2.", "s2": "Establish global lock order A then B; refactor to single lock or try-lock timeout.", "s3": "Pool integrates queue and task semantics; semaphore only limits entry—still need queue for work.",
"qa": _qa(
("b","What does a mutex do?","Ensures only one thread in critical section.","Others block until release.","Protects shared invariants.",""),
("b","Binary vs counting semaphore?","Binary allows one; counting allows N concurrent holders.","Used to throttle parallel sections.",""),
("b","What is deadlock?","Threads wait on each other forever (`D13-T013`).","Often multiple locks wrong order.",""),
("b","Reentrant mutex?","Same thread can acquire again; must release same count.","Java synchronized is reentrant.",""),
("b","Semaphore acquire block?","Waits until permit available unless timeout.",""),
("i","Mutex vs synchronized?","Java synchronized is built-in monitor; ReentrantLock has tryLock, fairness option.",""),
("i","Fair semaphore?","FIFO wake order; lower throughput sometimes.",""),
("i","Why not hold lock during I/O?","Blocks other threads; deadlock if remote hangs.",""),
("i","Spurious wakeup?","waits can wake without condition; always recheck predicate in loop.",""),
("i","Permit leak symptom?","Eventually all acquires block; available permits zero forever.",""),
("a","Priority inversion?","Low priority holds lock high priority needs; OS priority inheritance on some systems.",""),
("a","User vs kernel mutex?","Spinlock for short; futex hybrid.",""),
("a","Semaphore for backpressure?","Limit in-flight requests (`D13-T020`).",""),
("a","Lock convoying?","Many threads wake one at a time on hot lock.",""),
("a","RW lock preview?","Many readers or one writer (`D13-T008`).",""),
("s","All threads BLOCKED on Semaphore.","Permits not released on exception path.","Use try/finally release.",""),
("s","Throughput collapsed after adding lock.","Coarse lock on hot path.","Shrink critical section or shard locks.",""),
("s","Rare deadlock on payment + ledger.","Different lock order in two code paths.","Document global order.",""),
("s","Pool size 100 but only 10 DB conns.","Semaphore should cap at 10 around borrow.",""),
("s","Spinning CPU with mutex?","Contention on short lock; consider backoff or redesign.",""),
("f","RW locks?","Optimize read-heavy (`D13-T008`).",""),
("f","Deadlock prevention?","Ordering, timeouts (`D13-T013`).",""),
("f","Lock-free?","Alternative to mutex for counters (`D13-T009`).",""),
),
})

# D13-T008 Read-write locks
_add({
"id": "D13-T008", "next": "D13-T009",
"overview": "**Read-write locks** allow many concurrent readers or one exclusive writer, optimizing read-heavy shared data when writes are rare.",
"principles": "Readers share access if no writer holds. Writer excludes all readers and writers. Starvation possible if writers wait for endless readers—fair policies exist. Still need to guard compound read-then-write upgrades.",
"architecture": "`ReadWriteLock` in Java; `pthread_rwlock`; Python lacks stdlib RW lock—use `threading.Lock` or `multiprocessing` patterns. Internal state tracks reader count and writer flag.",
"mermaid": "flowchart TD\n  r1[Readers shared]\n  w[Writer exclusive]\n  r1 -.->|blocks| w\n  w -.->|blocks| r1",
"examples": "Analogy: library many readers, one shelver reorganizing. Backend: config cache refreshed rarely, read on every request.",
"code_file": "d13_t008_rwlock.py",
"code": textwrap.dedent('''
# Conceptual RW lock using two locks (educational; production use language RW lock)
import threading

readers = 0
read_lock = threading.Lock()
write_lock = threading.Lock()


def begin_read() -> None:
    global readers
    with read_lock:
        readers += 1
        if readers == 1:
            write_lock.acquire()


def end_read() -> None:
    global readers
    with read_lock:
        readers -= 1
        if readers == 0:
            write_lock.release()
'''),
"code_notes": "Illustrates reader counting; prefer `java.util.concurrent.locks.ReentrantReadWriteLock` in Java services.",
"backend": "Use for in-memory feature flags and routing tables. For high write rates, single mutex may be simpler. Externalize config to avoid process-wide RW complexity.",
"trade_rows": [("RW lock", "Parallel reads", "Writer starvation risk", "Read-heavy config", "Write-heavy"), ("Immutable snapshot", "No locks on read path", "Copy on write cost", "Config reload", "Huge config"), ("Version stamp", "Readers never block", "Stale reads possible", "CDN style", "Strong consistency"), ("Single mutex", "Simple", "Serializes reads", "Balanced R/W", "")],
"mistakes": ["Upgrading read lock to write lock incorrectly.", "Long read sections block writers.", "Using RW lock when writes dominate.", "Nested locks causing deadlock.", "Reading mutable object while writer mutates without snapshot."],
"debug": "Writers timing out—check reader leak (forgot end_read). Metrics: read lock hold time, writer wait queue.",
"revision": ["Many readers OR one writer.", "Fairness matters.", "Snapshot avoids RW complexity.", "Not in Python stdlib.", "Write-heavy → mutex."],
"completion": ["When RW lock helps.", "Writer starvation fix.", "Read lock upgrade pitfall.", "Snapshot vs RW lock.", "Draw reader/writer timeline."],
"related": ["D13-T007", "D13-T012", "D13-T006"],
"ex1": "Implement reader counter pattern or use Java RW lock in pseudocode.", "ex2": "Config never updates—readers never release?", "ex3": "RW lock vs immutable copy for feature flags.",
"s1": "Section F shows acquire write on first reader.", "s2": "Leaked read lock blocks writer; audit try/finally on end_read.", "s3": "Immutable snapshot: atomic pointer swap on reload; readers see old or new; simpler than upgrade.",
"qa": _qa(
("b","Purpose of RW lock?","Concurrent reads, exclusive writes.",""),
("b","Can two writers share?","No; writer is exclusive.",""),
("b","Can two readers share?","Yes, when no writer.",""),
("b","Downside?","Writer may starve if readers continuous.",""),
("b","Python stdlib RW lock?","No; use lock or third-party or redesign.",""),
("i","Read lock reentrancy?","Same thread may acquire read lock multiple times per API.",""),
("i","Upgrade policy?","Many APIs forbid read-to-write upgrade while holding read.",""),
("i","When mutex better?","Similar read/write rates or small critical section.",""),
("i","Snapshot pattern?","Atomic reference to immutable map; writers publish new copy.",""),
("i","Cache coherence cost?","Many readers still hit shared memory; usually fine.",""),
("a","Fair RW lock?","Alternate or queue writers; throughput trade-off.",""),
("a","Per-bucket sharding?","Reduce contention vs one global RW lock.",""),
("a","Seqlock?","Readers retry if write occurred; kernel technique.",""),
("a","Stale read acceptable?","Version number check after read.",""),
("a","Lock-free reads?","RCU-like patterns advanced (`D13-T009`).",""),
("s","Hot reload never visible.","Readers hold lock too long or cache thread-local without refresh.",""),
("s","Latency spike on deploy.","All threads block on writer reload; use snapshot swap.",""),
("s","Deadlock with RW + mutex.","Lock ordering across subsystems.",""),
("s","Read storm blocks admin update.","Fair policy or writer priority.",""),
("s","Incorrect double-checked locking on config.","Needs proper happens-before (`D13-T017`).",""),
("f","Lock-free basics?","(`D13-T009`).",""),
("f","Concurrent collections?","(`D13-T012`).",""),
("f","Mutex foundation?","(`D13-T007`).",""),
),
})

# D13-T009 Lock-free programming basics
_add({
"id": "D13-T009", "next": "D13-T010",
"overview": "**Lock-free** algorithms guarantee system-wide progress: some thread completes in finite steps even if others are paused. Often implemented with **compare-and-swap (CAS)** retry loops.",
"principles": "CAS reads a value, if matches expected, writes new; else retry. Not wait-free; individual threads may starve retrying. ABA problem matters in lock-free stacks with memory reuse—use tagged pointers or hazard pointers in native code.",
"architecture": "Hardware `LOCK CMPXCHG`; Java `AtomicReference.update`; lock-free queue nodes linked with CAS. Progress hierarchy: blocking → lock-free → wait-free.",
"mermaid": "flowchart LR\n  read[Read current]\n  cas[CAS swap]\n  fail[Retry on fail]\n  read --> cas\n  cas -->|fail| read",
"examples": "Analogy: take-a-number dispenser where you retry if someone took your number. Backend: high-frequency counters and MPMC queues in disruptor pattern.",
"code_file": "d13_t009_cas.py",
"code": textwrap.dedent('''
import threading

value = 0
lock = threading.Lock()


def cas_increment(times: int) -> None:
    global value
    for _ in range(times):
        with lock:
            value += 1  # stand-in; real lock-free uses extension atomics


if __name__ == "__main__":
    threads = [threading.Thread(target=cas_increment, args=(50_000,)) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert value == 200_000
    print("ok")
'''),
"code_notes": "Python lacks user CAS on plain ints; production uses `atomic` extensions or moves hot path to native/Java.",
"backend": "Use JDK concurrent atomics and lock-free queues before writing your own. Profile—locks often suffice until microsecond contention.",
"trade_rows": [("Lock-free", "No deadlock from mutex order", "Complex, subtle bugs", "Ultra-hot counters", "Business logic"), ("Mutex", "Simple", "Blocking", "Most services", "Nanosecond contention"), ("Wait-free", "Strong per-thread guarantee", "Hard to build", "Real-time", "General purpose"), ("CAS retry storm", "Progress under contention", "CPU burn", "Moderate contention", "Extreme contention")],
"mistakes": ["Calling code lock-free without progress proof.", "ABA in naive lock-free stack.", "Composing multiple atomics without invariant.", "Replacing all locks prematurely.", "Ignoring GC interaction in managed languages."],
"debug": "High CPU with low throughput—CAS spin. Use profilers; consider backoff. Validate with stress + model checking for custom structures.",
"revision": ["Lock-free = someone progresses.", "CAS core primitive.", "ABA is real in pools.", "Prefer library implementations.", "Not always faster."],
"completion": ["Define lock-free vs wait-free.", "Explain CAS loop.", "ABA sketch.", "When not to use.", "Name Java atomic class."],
"related": ["D13-T006", "D13-T007", "D13-T012"],
"ex1": "Increment shared counter safely under 4 threads (lock or atomic).", "ex2": "CPU 100% low QPS—CAS spin on hot counter.", "ex3": "Lock-free queue vs `BlockingQueue` for logging.",
"s1": "Section F uses lock as Python stand-in; same invariant.", "s2": "Replace with `LongAdder` or shard counters; reduce single hot CAS.", "s3": "BlockingQueue simpler; lock-free wins at very high publish rates with expert implementation.",
"qa": _qa(
("b","What is CAS?","Compare value to expected; swap if equal atomically.",""),
("b","Lock-free meaning?","At least one thread makes progress system-wide.",""),
("b","Wait-free?","Every thread completes in bounded steps—stronger.",""),
("b","Why retry loops?","CAS fails when another thread won race.",""),
("b","Is lock-free always faster?","No; overhead and complexity; measure.",""),
("i","ABA problem?","Pointer reused looks same to CAS though structure changed.",""),
("i","Java `AtomicInteger`?","Lock-free increment for single variable.",""),
("i","Compound actions?","Still need locks for multi-field invariants.",""),
("i","Memory ordering with atomics?","Varies by language; Java atomics have happens-before rules.",""),
("i","Disruptor ring buffer?","Lock-free inter-thread messaging pattern.",""),
("a","Hazard pointers?","Safe memory reclamation in native lock-free structures.",""),
("a","Backoff strategies?","Exponential backoff on CAS fail reduces bus traffic.",""),
("a","Linearizability?","Operations appear instantaneous at some point between call and return.",""),
("a","MPMC queue difficulty?","Harder than SPSC; use proven library.",""),
("a","GC pauses vs lock-free?","Pauses stall all threads; design for jitter.",""),
("s","Rare crash in custom lock-free stack.","ABA or double free.","Use `ConcurrentLinkedQueue`.",""),
("s","Counter correct but slow.","CAS storm on single variable.","Shard or `LongAdder`.",""),
("s","Lost elements in queue.","Incorrect tail update ordering.","Code review with JMM in mind.",""),
("s","Tests pass locally fail CI.","Different timing exposes bug.","Stress + TSAN.",""),
("s","Team wants lock-free everywhere.","Push back; use where profiled hot.",""),
("f","Producer-consumer queues?","(`D13-T010`).",""),
("f","Race conditions?","(`D13-T006`).",""),
("f","Concurrent collections?","Built on locks or CAS (`D13-T012`).",""),
),
})

from _gen_d13_specs_rest2 import MORE_SPECS  # noqa: E402

SPECS_REST.extend(MORE_SPECS)

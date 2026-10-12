"""D13-T012 .. D13-T022 specs."""
import textwrap


def _qa(*rows):
    out = {"b": [], "i": [], "a": [], "s": [], "f": []}
    for row in rows:
        sec, q = row[0], row[1]
        a1 = row[2] if len(row) > 2 else ""
        a2 = row[3] if len(row) > 3 else ""
        a3 = row[4] if len(row) > 4 else ""
        a4 = row[5] if len(row) > 5 else ""
        out[sec].append((q, a1, a2, a3, a4))
    return out


def _ex(ex1, ex2, ex3, s1, s2, s3):
    return {"ex1": ex1, "ex2": ex2, "ex3": ex3, "s1": s1, "s2": s2, "s3": s3}


FINAL_SPECS = [
{
"id": "D13-T012", "next": "D13-T013",
"overview": "**Concurrent collections** provide thread-safe maps, queues, and lists without external locking on every operation—implemented with internal synchronization or lock striping.",
"principles": "`ConcurrentHashMap` uses segments/buckets with fine-grained locks or CAS. `CopyOnWriteArrayList` copies array on write for read-heavy lists. Compound operations like `if absent put` still need `compute` methods for atomicity.",
"architecture": "Java `java.util.concurrent.*`; Python `queue`, limited stdlib—often `multiprocessing` or external store. iterators may be weakly consistent.",
"mermaid": "flowchart TD\n  threads[Many threads]\n  chm[ConcurrentHashMap]\n  threads --> chm",
"examples": "Analogy: bank safety deposit boxes per customer vs one vault door. Backend: per-key rate limit counters in CHM.",
"code_file": "d13_t012_concurrent_map.py",
"code": textwrap.dedent('''
from concurrent.futures import ThreadPoolExecutor


def main() -> None:
    # Java: ConcurrentHashMap; Python: use lock around dict or concurrent external store
    counts: dict[str, int] = {}
    lock = __import__("threading").Lock()

    def hit(key: str) -> None:
        with lock:
            counts[key] = counts.get(key, 0) + 1

    with ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda _: hit("api"), range(1000)))
    assert counts["api"] == 1000
    print("ok")


if __name__ == "__main__":
    main()
'''),
"code_notes": "Illustrates synchronized dict; in Java prefer `ConcurrentHashMap` APIs.",
"backend": "Use built-in concurrent collections before rolling locks. For cross-process, Redis/DB. Document weak iterator semantics for admin UIs.",
"trade_rows": [("ConcurrentHashMap", "Scalable reads/writes", "Not compound atomic alone", "Caches", "Cross-key transactions"), ("CopyOnWriteArrayList", "Fast reads", "Expensive writes", "Listener lists", "Frequent writes"), ("BlockingQueue", "PC pattern", "Blocking", "Thread pools", ""), ("Synchronized wrapper", "Simple", "Single lock", "Low contention", "Hot path")],
"mistakes": ["Check-then-act with plain get/put on CHM.", "Iterating while mutating expecting strong consistency.", "Using concurrent collection across processes.", "Assuming size() exact under concurrency.", "Huge COW list with frequent writes."],
"debug": "Wrong counts → non-atomic compound ops. Use `merge`, `computeIfAbsent`. Profile lock stripes.",
"revision": ["Use library concurrent types.", "Compound ops need atomic methods.", "Weakly consistent iterators.", "Not for cross-process.", "COW for read-heavy."],
"completion": ["CHM vs synchronized HashMap.", "`putIfAbsent` use.", "COW trade-off.", "Weak iterator meaning.", "Python options."],
"related": ["D13-T006", "D13-T008", "D13-T007"],
**_ex(
    "1000 parallel increments to one key safely.",
    "Duplicate cache entries intermittently.",
    "CHM vs Redis for rate limit.",
    "Locked dict passes assert.",
    "Non-atomic check-then-put; use `computeIfAbsent`.",
    "CHM local fast; Redis global consistent across instances.",
),
"qa": _qa(
("b","Why concurrent collections?","Thread-safe without manual lock on every op.",""),
("b","ConcurrentHashMap thread-safe?","Yes for individual ops; compound needs care.",""),
("b","CopyOnWriteArrayList?","Readers no lock; copy on write.",""),
("b","BlockingQueue types?","Part of j.u.c for producer-consumer.",""),
("b","Python concurrent dict?","Use lock or `multiprocessing.Manager`—no CHM in stdlib.",""),
("i","`computeIfAbsent`?","Atomic compute per key.",""),
("i","Weakly consistent iterator?","May or may not see concurrent writes; no ConcurrentModificationException.",""),
("i","size() accuracy?","May be approximate under concurrency in some ops.",""),
("i","SynchronizedMap wrapper?","Single lock—simple but contended.",""),
("i","When external store?","Multi-instance shared state.",""),
("a","Lock striping?","Different locks per bucket.",""),
("a","Non-blocking CHM internals?","CAS on bins in modern JDK.",""),
("a","LinkedBlockingQueue vs ArrayBlockingQueue?","Linked unbounded optional; array fixed capacity.",""),
("a","ConcurrentSkipListMap?","Ordered concurrent map.",""),
("a","Aggregate stats?","`LongAdder` for counters.",""),
("s","Rare duplicate processing.","get then put race.","Use computeIfAbsent.",""),
("s","Admin UI skips new keys during scan.","Iterator snapshot semantics.","Snapshot copy or message.",""),
("s","Memory spike on listener list.","COW on every register.","Use concurrent set or linked structure.",""),
("s","10 instances 10x rate limit allowed.","Local CHM only per JVM.","Centralize limiter.",""),
("s","Deadlock with synchronizedMap + other lock.","Lock ordering.",""),
("f","Deadlock?","(`D13-T013`).",""),
("f","Races?","(`D13-T006`).",""),
("f","RW locks?","(`D13-T008`).",""),
),
},
{
"id": "D13-T013", "next": "D13-T014",
"overview": "**Deadlock** is circular wait on resources. **Prevention** breaks one of four Coffman conditions: mutual exclusion, hold-and-wait, no preemption, circular wait.",
"principles": "Classic fix: total lock ordering, try-lock with timeout, lock-free where possible, avoid nested locks. Detection: thread dump cycle. Banker's algorithm mostly theoretical in apps.",
"architecture": "Two threads: lock A then B vs B then A. DB deadlocks on row locks—retry transaction. Distributed deadlocks need timeouts.",
"mermaid": "flowchart TD\n  t1[Thread1 holds A wants B]\n  t2[Thread2 holds B wants A]\n  t1 --- t2",
"examples": "Analogy: two people each holding door the other needs. Backend: transfer between accounts locking rows in inconsistent order.",
"code_file": "d13_t013_deadlock.py",
"code": "# Avoid: threading.Lock a,b; thread1: a->b; thread2: b->a\nprint('deadlock prevented by global lock order')\n",
"code_notes": "Educational placeholder—always acquire locks in global order.",
"backend": "Document lock hierarchy. Use `@Transactional` ordering; retry on SQL deadlock 40001. Set lock wait timeouts.",
"trade_rows": [("Lock ordering", "Prevents cycle", "Discipline required", "Multi-lock services", ""), ("Try-lock timeout", "Fails fast", "Must handle failure", "Optional resources", ""), ("Single lock", "No ordering issue", "Contention", "Simple services", ""), ("Eliminate sharing", "No lock deadlock", "Architecture change", "Stateless", "")],
"mistakes": ["Different lock order in two code paths.", "Calling foreign code holding lock.", "DB transaction order differs per endpoint.", "Ignoring deadlock exception without retry.", "synchronized methods chaining locks."],
"debug": "jstack shows circular BLOCKED. Enable DB deadlock graph. Look for pool + connection + row locks.",
"revision": ["Four conditions for deadlock.", "Global order.", "Retry SQL deadlock.", "Try-lock timeout.", "Don't call out while holding lock."],
"completion": ["List four conditions.", "Draw AB-BA deadlock.", "Prevention tactics.", "SQL deadlock retry.", "vs livelock."],
"related": ["D13-T007", "D13-T021", "D13-T012"],
**_ex(
    "Document lock order for two resources.",
    "jstack circular BLOCKED—interpret.",
    "Retry vs prevention for DB deadlocks.",
    "Always acquire accountId ascending order before transfer.",
    "Two threads each hold one lock waiting other—reorder or timeout.",
    "Prevention via consistent row access order; retry transient deadlocks with backoff.",
),
"qa": _qa(
("b","Four deadlock conditions?","Mutual exclusion, hold and wait, no preemption, circular wait.",""),
("b","How break circular wait?","Global lock ordering.",""),
("b","What is livelock?","Threads actively retry without progress.",""),
("b","DB deadlock?","Transactions lock rows in cycle.",""),
("b","Thread dump shows?","BLOCKED waiting on monitor held by other thread.",""),
("i","tryLock timeout?","Give up and fail or retry alternative path.",""),
("i","Lock hierarchy doc?","Team-wide order A<B<C.",""),
("i","Deadlock detection JVM?","ThreadMXBean findDeadlockedThreads.",""),
("i","Hold and wait break?","Try to acquire all at once or none.",""),
("i","Connection pool deadlock?","All threads hold conn waiting another resource.",""),
("a","Distributed deadlock?","No global waiter graph; use timeouts (`D13-T021`).",""),
("a","Priority ceiling?","Real-time protocols.",""),
("a","Lock dep graph analysis?","Static analysis tools.",""),
("a","ORM lazy load deadlock?","Session holds lock while triggering queries.",""),
("a","Kafka consumer rebalance deadlock?","Rare; usually misconfigured threads.",""),
("s","Payments stuck both directions.","Opposite account lock order.","Sort account ids.",""),
("s","Only under load.","Pool exhaustion looks like deadlock.","Separate issues.",""),
("s","MySQL deadlock rate high.","Index causing gap locks.","Tune queries indexes.",""),
("s","After adding cache lock.","New edge in lock graph.","Extend hierarchy.",""),
("s","tryLock always false.","Others hold forever—fix leak not spin.",""),
("f","Timeouts?","(`D13-T021`).",""),
("f","Mutexes?","(`D13-T007`).",""),
("f","Bulkheads?","Reduce shared wait (`D13-T020`).",""),
),
},
{
"id": "D13-T014", "next": "D13-T015",
"overview": "**Task scheduling** decides which runnable work executes next on limited workers—OS scheduler, thread pool queue, cron, or distributed job systems.",
"principles": "Goals: fairness, throughput, latency, priority. Work stealing balances CPU pools. Cron fires time-based; queue handles ad hoc. `GOMAXPROCS`, `nice`, cgroup CPU shares tune OS level.",
"architecture": "Ready queue per core; delayed tasks in timer wheel. Kubernetes schedules pods; Celery/RQ schedule background jobs separately from request threads.",
"mermaid": "flowchart TD\n  tasks[Runnable tasks]\n  sched[Scheduler]\n  cpu[CPU cores]\n  tasks --> sched --> cpu",
"examples": "Analogy: ER triage vs FIFO cafe line. Backend: priority queue for premium tenants; fair round-robin across shards.",
"code_file": "d13_t014_scheduling.py",
"code": textwrap.dedent('''
import heapq
import time

q: list[tuple[float, str]] = []


def schedule(at: float, name: str) -> None:
    heapq.heappush(q, (at, name))


if __name__ == "__main__":
    now = time.time()
    schedule(now + 0.1, "b")
    schedule(now + 0.05, "a")
    while q:
        at, name = heapq.heappop(q)
        print(name)
'''),
"code_notes": "Min-heap schedules by time; prints a then b.",
"backend": "Isolate cron from request pool. Use dedicated executor for batch. Distributed schedulers need leader election to avoid duplicate runs.",
"trade_rows": [("FIFO fair", "Simple", "Head-of-line blocking", "Homogeneous jobs", "Mixed SLAs"), ("Priority", "Important first", "Starvation low priority", "Multi-tenant", ""), ("Work stealing", "CPU balance", "Complexity", "ForkJoin", ""), ("Dedicated batch pool", "Protect API latency", "More pools", "Nightly ETL", "")],
"mistakes": ["Cron on request threads.", "No leader election duplicate jobs.", "Starving background maintenance.", "Ignoring clock skew for distributed schedule.", "Huge single queue for mixed job sizes."],
"debug": "Latency outliers: long task blocking FIFO queue. Metrics: wait time in queue, schedule lag for cron.",
"revision": ["Scheduler picks next task.", "Separate batch vs online.", "Priority vs fair.", "Work stealing.", "Distributed needs leader."],
"completion": ["FIFO vs priority.", "Work stealing idea.", "Cron vs queue.", "GOMAXPROCS role.", "Prevent duplicate cron."],
"related": ["D13-T004", "D13-T015", "D13-T020"],
**_ex(
    "Heap schedule two delayed tasks order.",
    "Nightly job slows API—why?",
    "Leader election for cron.",
    "Section F output order a,b.",
    "Shared thread pool; move batch to dedicated pool.",
    "Only one leader runs scheduler; use DB lock or etcd.",
),
"qa": _qa(
("b","What does scheduler do?","Picks next task to run on workers.",""),
("b","FIFO scheduling?","First submitted first run.",""),
("b","Cron vs queue?","Time-triggered vs event-triggered.",""),
("b","OS scheduler role?","Maps threads to CPU cores.",""),
("b","Thread pool queue?","Scheduler for pool workers (`D13-T004`).",""),
("i","Work stealing?","Idle worker takes from busy deque.",""),
("i","Priority inversion scheduling?","OS may boost priority of lock holder.",""),
("i","Delayed tasks?","Timer wheel or heap.",""),
("i","Fair share across tenants?","Weighted queues.",""),
("i","Kubernetes vs in-app?","Pod placement vs request scheduling.",""),
("a","CFS in Linux?","Proportional fair CPU for threads.",""),
("a","Real-time scheduling?","RTOS guarantees; servers rarely strict RT.",""),
("a","Cooperative scheduling?","Goroutines, asyncio—yield at await.",""),
("a","Global vs local queue?","Trade locality and balance.",""),
("a","Scheduling and tail latency?","Long tasks harm FIFO p99.",""),
("s","Reports run twice.","Two cron leaders.","Add distributed lock.",""),
("s","API p99 bad 2am only.","Batch competes for CPU.","Isolate pools.",""),
("s","Low priority never runs.","Starvation.","Aging or fair policy.",""),
("s","Go uses one thread?","GOMAXPROCS>1 uses multiple OS threads.",""),
("s","Timer fires early.","Clock adjustment; use monotonic where possible.",""),
("f","CPU vs IO?","(`D13-T015`).",""),
("f","Bulkheads?","(`D13-T020`).",""),
("f","Structured concurrency?","(`D13-T022`).",""),
),
},
{
"id": "D13-T015", "next": "D13-T016",
"overview": "**CPU-bound** work spends time computing; **I/O-bound** work waits on disk, network, or DB. Concurrency model should match where threads block.",
"principles": "CPU-bound: use processes or threads ≈ cores (no GIL in Java/Go). I/O-bound: many threads or async tasks multiplex waiting. Misclassification wastes cores or memory.",
"architecture": "Profile: if runnable without I/O wait, CPU-bound. Thread pool size for I/O can be `cores * (1 + wait/service)` rough heuristic. Async excels when wait >> compute.",
"mermaid": "flowchart LR\n  cpu[CPU bound compute]\n  io[I/O wait idle CPU]\n  cpu -->|needs cores| par[Parallelism]\n  io -->|needs multiplex| many[Many tasks]",
"examples": "Analogy: chefs chopping (CPU) vs waiting for oven timer (I/O). Backend: JSON parsing CPU vs HTTP client wait.",
"code_file": "d13_t015_cpu_io.py",
"code": textwrap.dedent('''
import time
import concurrent.futures


def io_bound() -> None:
    time.sleep(0.05)


def cpu_bound(n: int) -> int:
    return sum(i * i for i in range(n))


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda _: io_bound(), range(16)))
    assert cpu_bound(10000) > 0
    print("ok")
'''),
"code_notes": "Threads help overlap I/O sleep; CPU sum still GIL-limited in CPython.",
"backend": "Measure flame graphs and I/O wait %. Scale workers for I/O; scale processes/shards for CPU in Python. Right-size K8s CPU requests.",
"trade_rows": [("Threads for I/O", "Overlap waits", "Memory stacks", "DB-heavy API", "CPU crunch"), ("Processes for CPU Python", "Bypass GIL", "IPC", "ML inference py", "Tiny tasks"), ("Async I/O", "Cheap tasks", "Blocking libs hurt", "Websockets", "CPU on loop"), ("More cores", "CPU throughput", "Cost", "Compute jobs", "I/O saturated")],
"mistakes": ["32 threads for CPU Python.", "Async with blocking ORM.", "Ignoring I/O wait in capacity plan.", "Same pool for video encode and API.", "Confusing high CPU with CPU-bound (could be spin)."],
"debug": "vmstat iowait vs us sy. profiling shows hot functions vs blocked stacks.",
"revision": ["CPU = compute limited.", "I/O = wait limited.", "Match model to bound.", "CPython CPU → processes.", "Profile don't guess."],
"completion": ["Classify workload.", "Pool size heuristic I/O.", "Why async for websockets.", "GIL interaction.", "Little's law sketch."],
"related": ["D13-T001", "D13-T016", "D13-T003", "D13-T019"],
**_ex(
    "Run parallel I/O sleeps with thread pool.",
    "One core 100% 32 threads Python compute.",
    "Async vs threads for DB API.",
    "Section F overlaps sleeps.",
    "GIL; use multiprocessing.",
    "Async if async driver and mostly wait; threads if blocking pool sized to DB.",
),
"qa": _qa(
("b","CPU-bound definition?","Limited by processor speed not waiting on I/O.",""),
("b","I/O-bound definition?","Spends time waiting on external operations.",""),
("b","Many threads help which?","I/O-bound blocking APIs.",""),
("b","Many threads help CPU Python?","No for pure Python due GIL.",""),
("b","How detect?","Profiler and I/O wait metrics.",""),
("i","Little's law?","Average items in system = arrival rate * residence time.",""),
("i","Amdahl's law?","Parallel speedup limited by serial fraction.",""),
("i","Blocking vs non-blocking I/O?","Threads block; async registers readiness.",""),
("i","Worker sizing formula?","Empirical from latency and pool utilization.",""),
("i","Mixed workload?","Split pools or offload CPU (`D13-T020`).",""),
("a","NUMA CPU bound?","Memory local to socket matters.",""),
("a","Hyperthreading?","Two logical per core—diminishing returns CPU.",""),
("a","I/O bound but high CPU?","Could be encryption or inefficient parsing.",""),
("a","Cgroup CPU throttle?","Looks like slow CPU work.",""),
("a","Event loop for CPU?","Poor unless offload workers.",""),
("s","32 threads one core CPython.","GIL CPU-bound.", "Processes or native.",""),
("s","Async still slow.","Blocking calls on loop.", "Thread pool offload.",""),
("s","Low CPU high latency.","I/O or lock wait.", "Trace waits.",""),
("s","Adding cores no gain.","I/O or serial bottleneck.", "Scale DB or shard.",""),
("s","Node CPU 100%.","JS compute on loop.", "Worker threads.",""),
("f","GIL?","(`D13-T016`).",""),
("f","Node workers?","(`D13-T019`).",""),
("f","Goroutines?","(`D13-T018`).",""),
),
},
{
"id": "D13-T016", "next": "D13-T017",
"overview": "The **CPython GIL** (Global Interpreter Lock) allows only one thread to execute Python bytecode at a time per process. **Multiprocessing** uses separate interpreters to achieve parallel CPU on multiple cores.",
"principles": "GIL simplifies C API object safety. I/O and many C extensions release GIL during waits/compute. `multiprocessing` pickles data across processes; `concurrent.futures.ProcessPoolExecutor` pools workers.",
"architecture": "Main process spawns children with `spawn` on Windows/macOS default. Shared state needs `Manager`, shared memory, or external store—not plain globals.",
"mermaid": "flowchart TD\n  p1[Process 1 GIL]\n  p2[Process 2 GIL]\n  p1 ---|separate| p2",
"examples": "Analogy: one chalkboard per classroom (process) vs one chalkboard shared by students (threads). Backend: Gunicorn workers not threads for CPU pandas work.",
"code_file": "d13_t016_gil_mp.py",
"code": textwrap.dedent('''
import multiprocessing as mp


def square(n: int) -> int:
    return n * n


if __name__ == "__main__":
    with mp.Pool(4) as pool:
        out = pool.map(square, range(10))
    assert out == [i * i for i in range(10)]
    print("ok")
'''),
"code_notes": "Requires `if __name__` guard on Windows spawn.",
"backend": "Use processes for CPU pipelines; threads/async for I/O within worker. Watch memory duplication per worker. Consider NumPy/C extensions that release GIL.",
"trade_rows": [("Threads CPython", "Low overhead sharing", "No parallel bytecode", "I/O", "CPU Python"), ("multiprocessing", "True parallel CPU", "Pickle/memory", "CPU jobs", "Huge shared RAM"), ("subinterpreters/pep554", "Evolving niche", "Ecosystem", "Future", "Prod default"), ("C extension release GIL", "Parallel native work", "FFI complexity", "Crypto/hash", "")],
"mistakes": ["Thread pool for heavy pure Python CPU.", "Passing huge objects to processes repeatedly.", "Fork on Linux with threads unsafe.", "Expecting GIL removal to fix bad algorithm.", "Shared list without Manager expecting visibility."],
"debug": "One core hot with many threads → GIL. Process count vs CPU quota. Pickle errors on unpicklable tasks.",
"revision": ["GIL one bytecode thread.", "I/O releases GIL often.", "multiprocessing for CPU.", "spawn vs fork caveats.", "Memory per worker."],
"completion": ["What GIL protects.", "When threads enough.", "Process pool API.", "Why Gunicorn processes.", "Pickle cost awareness."],
"related": ["D13-T001", "D13-T015", "D13-T004"],
**_ex(
    "Process pool map squares 0..9.",
    "4 threads 4 cores no speedup Python loop.",
    "Workers vs threads FastAPI.",
    "Section F map works with guard.",
    "GIL serializes bytecode; use Pool.",
    "Uvicorn workers processes; async single worker for I/O inside.",
),
"qa": _qa(
("b","What is the GIL?","Mutex protecting Python object access in CPython.",""),
("b","How many threads run bytecode?","One at a time per process.",""),
("b","Why multiprocessing?","Separate GIL per process.",""),
("b","Does I/O release GIL?","Often during blocking I/O in C code.",""),
("b","Jython/PyPy same?","Different implementations differ; question usually CPython.",""),
("i","ProcessPoolExecutor?","Pool of worker processes with futures.",""),
("i","spawn start method?","Clean child on Windows/macOS.",""),
("i","fork with threads?","Unsafe if parent had threads (`D13-T001`).",""),
("i","numpy parallel?","Native code may release GIL.",""),
("i","asyncio vs threads GIL?","Both one bytecode thread; async avoids thread stacks.",""),
("a","GIL and CPU count?","Only one core useful for pure Python thread CPU.",""),
("a","Shared memory Value/Array?","Cross-process with sync.",""),
("a","Pickle overhead?","Large args dominate runtime.",""),
("a","nogil builds?","Experimental; know mainstream answer.",""),
("a","Why GIL exists?","Simpler C extension object model historically.",""),
("s","8 cores 8 threads same speed.","GIL.", "Use 8 processes.",""),
("s","Child memory huge.","Copy-on-write until mutate; preload carefully.",""),
("s","Pool hang on Windows.","Missing main guard.",""),
("s","CPU work in asyncio.","Blocks loop.", "Process pool executor.",""),
("s","Laptop fans threads not procs.","Threads cheaper to spawn; still GIL bound.",""),
("f","JMM in Java?","No GIL (`D13-T017`).",""),
("f","CPU vs I/O?","(`D13-T015`).",""),
("f","Thread pools?","(`D13-T004`).",""),
),
},
{
"id": "D13-T017", "next": "D13-T018",
"overview": "The **Java Memory Model (JMM)** defines when writes by one thread are visible to another via **happens-before** rules. Without a happens-before edge, you cannot rely on ordering or visibility.",
"principles": "Standard rules: monitor unlock on `synchronized` happens-before subsequent lock on same monitor; `volatile` write happens-before volatile read; `Thread.start` happens-before actions in started thread; `join` happens-before actions after join; transitive chaining builds order. Do not invent exotic reorderings beyond the spec.",
"architecture": "Compiler and CPU may reorder within permitted bounds. `synchronized`, `volatile`, `java.util.concurrent` utilities establish edges. `final` field safe publication after construction when properly used.",
"mermaid": "flowchart LR\n  w[Thread A write]\n  hb[happens-before edge]\n  r[Thread B read sees write]\n  w --> hb --> r",
"examples": "Analogy: signed handoff form between shifts—without it, next shift may not see updates. Backend: flag `volatile boolean shutdown` visible to all worker threads.",
"code_file": "d13_t017_jmm.java",
"code": "// Java (conceptual):\n// volatile boolean running = true;\n// synchronized void publish() { data = 42; }\n// Thread B synchronized read sees 42 after unlock/lock.\n",
"code_notes": "Compile with javac in JVM services; JMM applies to all Java threads.",
"backend": "Use `java.util.concurrent`, avoid double-checked locking bugs, prefer higher-level constructs. Document happens-before for hand-built queues.",
"trade_rows": [("synchronized", "Strong visibility + atomic block", "Contention", "Invariants", "Read-heavy"), ("volatile", "Visibility for single var", "No compound atomicity", "Flags status", "Counter++"), ("j.u.c classes", "Documented memory semantics", "Learning curve", "Caches queues", ""), ("Unsafe DIY", "Flexible", "Bug prone", "Avoid", "")],
"mistakes": ["Double-checked locking without volatile.", "Assuming program order visible cross-thread.", "Using regular int for shutdown flag.", "Synchronizing only writes not reads.", "Data race on non-volatile shared fields."],
"debug": "Heisenbugs; use FindBugs, JCStress for concurrency tests. Thread dumps less help than JMM understanding.",
"revision": ["happens-before defines visibility.", "volatile for publication.", "synchronized unlock/lock edge.", "start/join edges.", "Transitive chaining."],
"completion": ["Define happens-before.", "volatile vs synchronized.", "Why DCL broken.", "Thread start rule.", "Data race JMM."],
"related": ["D13-T006", "D13-T007", "D13-T009"],
**_ex(
    "Write volatile shutdown flag pattern.",
    "Double-checked singleton broken—fix.",
    "When volatile enough vs synchronized.",
    "volatile ensures readers see latest shutdown.",
    "Need volatile instance + synchronized init or static holder.",
    "volatile for single flag; synchronized for multi-field invariants.",
),
"qa": _qa(
("b","What is happens-before?","Partial order; if A hb B, B sees A's effects.",""),
("b","Why JMM exists?","Define legal reorderings and visibility on multicore.",""),
("b","volatile does what?","Visibility and ordering for that variable's access.",""),
("b","synchronized visibility?","Unlock hb later lock on same monitor.",""),
("b","Data race in Java?","Conflicting accesses without happens-before.",""),
("i","Thread.start rule?","start hb first action in new thread.",""),
("i","Thread.join rule?","Actions in thread hb after join returns.",""),
("i","Transitive hb?","A hb B and B hb C implies A hb C.",""),
("i","final fields safe publication?","Properly constructed immutable after ctor if no escape.",""),
("i","ConcurrentHashMap visibility?","Documented concurrent semantics.",""),
("a","Program order within thread?","As-if-serial for single thread; not cross-thread alone.",""),
("a","Does volatile make ++ atomic?","No compound; use AtomicInteger.",""),
("a","lazySet vs set?","Weaker ordering in atomics API.",""),
("a","JCStress purpose?","Test JMM behaviors.",""),
("a","Do not invent edge cases?","Stick to standard hb rules in interviews.",""),
("s","Shutdown flag ignored.","Non-volatile flag.", "Use volatile or atomic.",""),
("s","Singleton double-checked NPE.","Partial construction visible.", "volatile or enum singleton.",""),
("s","Counter wrong rare.","Atomic or synchronized increment.",""),
("s","Published config partial read.","Immutable snapshot or volatile reference to immutable.",""),
("s","Works on x86 fails ARM.","Weaker memory model needs proper sync.",""),
("f","Races?","(`D13-T006`).",""),
("f","Atomics?","(`D13-T009`).",""),
("f","Go memory model?","Also happens-before (`D13-T018`).",""),
),
},
{
"id": "D13-T018", "next": "D13-T019",
"overview": "**Goroutines** are lightweight tasks scheduled by the Go runtime on OS threads. **Channels** pass typed values between goroutines—prefer *communicate through channels, don't share memory*.",
"principles": "`go fn()` starts goroutine; stacks start small grow as needed. `GOMAXPROCS` sets runnable OS threads for goroutines. Channels can be buffered or unbuffered; send/receive synchronize. `select` multiplexes channel ops.",
"architecture": "M:N scheduling: many goroutines on fewer threads. Work queues per P (processor). Blocking syscall may spawn extra thread. Channel closes signal completion.",
"mermaid": "flowchart LR\n  g1[Goroutine A]\n  ch[Channel]\n  g2[Goroutine B]\n  g1 -->|send| ch -->|recv| g2",
"examples": "Analogy: many quick errands (goroutines) carried by few couriers (OS threads). Backend: fan-out HTTP with errgroup and context.",
"code_file": "d13_t018_go_channels.go",
"code": "package main\n// func main() {\n//   ch := make(chan int, 1)\n//   go func() { ch <- 42 }()\n//   fmt.Println(<-ch)\n// }\n",
"code_notes": "Go source illustrative; channel unbuffered synchronizes handoff.",
"backend": "Use context for cancel. Limit goroutines with worker pools or semaphores—unbounded `go` can exhaust memory. Profile with pprof.",
"trade_rows": [("Goroutines", "Cheap concurrency", "Need discipline", "I/O fan-out", "Unbounded spawn"), ("Channels", "Safe communication", "Deadlock if misused", "Pipeline stages", "Shared cache"), ("Mutex in Go", "OK for shared state", "Prefer channels for ownership transfer", "Hot structs", ""), ("GOMAXPROCS", "Use CPU cores", "Default usually NumCPU", "CPU bound Go", "")],
"mistakes": ["Leaked goroutine blocked on channel.", "Closing channel from receiver side.", "Range over channel without close.", "Shared map without sync.", "Ignoring context cancel."],
"debug": "goroutine dump `debug.Stack`. Channel deadlock in select. trace scheduler.",
"revision": ["go spawns goroutine.", "channel send recv sync.", "buffered len capacity.", "close signals done.", "context cancel."],
"completion": ["Goroutine vs OS thread.", "Buffered channel.", "select use.", "When mutex ok.", "GOMAXPROCS."],
"related": ["D13-T001", "D13-T010", "D13-T021", "D13-T022"],
**_ex(
    "Sketch channel pipeline pseudocode.",
    "Goroutine leak on HTTP handler.",
    "Channel vs mutex for counter.",
    "Stage1 send to ch, stage2 recv process.",
    "Blocked send no receiver; use context timeout worker pool.",
    "Mutex or sync/atomic for simple counter; channel overkill.",
),
"qa": _qa(
("b","Goroutine vs thread?","Goroutine user-space scheduled; smaller stacks.",""),
("b","Channel purpose?","Pass data safely between goroutines.",""),
("b","Unbuffered channel?","Send blocks until recv.",""),
("b","GOMAXPROCS?","Max OS threads executing Go code simultaneously.",""),
("b","select?","Wait on multiple channel operations.",""),
("i","close channel?","Sender closes; recv gets zero value and false.",""),
("i","range channel?","Until closed and drained.",""),
("i","sync.WaitGroup?","Wait for goroutine batch.",""),
("i","errgroup?","Cancel siblings on first error pattern.",""),
("i","context.Context?","Cancellation propagation (`D13-T021`).",""),
("a","G scheduler P M G?","Processor, machine thread, goroutine model.",""),
("a","Work stealing in Go?","Runqueues stolen between Ps.",""),
("a","Mutex vs channel dogma?","Share memory by communicating when ownership clear.",""),
("a","nil channel?","Send recv block forever.",""),
("a","Leak detection?","pprof goroutine profile.",""),
("s","Service hang all requests.","Deadlock all goroutines waiting channel.",""),
("s","Memory millions goroutines.","Unbounded go per request.",""),
("s","Panic in worker.","Recover or crash process policy.",""),
("s","Slow consumer stalls API.","Unbuffered or full buffer.",""),
("s","CPU not all cores.","GOMAXPROCS or GOMAXPROCS=1 misconfig.",""),
("f","Node comparison?","(`D13-T019`).",""),
("f","Structured concurrency?","(`D13-T022`).",""),
("f","Producer-consumer?","(`D13-T010`).",""),
),
},
{
"id": "D13-T019", "next": "D13-T020",
"overview": "Node.js runs JavaScript on a **single main thread event loop** (libuv) for I/O callbacks; **worker threads** run CPU-heavy or isolated JS on additional threads.",
"principles": "Loop phases: timers, pending callbacks, poll I/O, check `setImmediate`, close callbacks. libuv thread pool handles some blocking ops (file, dns). CPU work on main thread blocks all clients.",
"architecture": "V8 executes JS; uv_async_t wakes loop from workers. `worker_threads` module shares ArrayBuffers optionally; message passing for isolation.",
"mermaid": "flowchart TD\n  loop[Event loop]\n  io[Poll I/O]\n  cb[Run callbacks]\n  wt[Worker threads CPU]\n  loop --> io --> cb\n  wt -.->|postMessage| loop",
"examples": "Analogy: one receptionist (loop) unless you hire back-office staff (workers) for heavy paperwork.",
"code_file": "d13_t019_node_event_loop.js",
"code": "// setImmediate(() => console.log('immediate'));\n// fs.readFile(...) // async, callback on loop\n",
"code_notes": "Run with Node; CPU JSON on main thread blocks loop.",
"backend": "Use cluster for multi-core HTTP; workers for bcrypt/pdf. Never sync fs on hot path. Monitor event loop delay.",
"trade_rows": [("Event loop I/O", "Efficient C10k", "CPU blocks all", "API JSON DB async", "Heavy compute"), ("Worker threads", "Parallel CPU", "Startup/IPC cost", "Image hash", "Tiny tasks"), ("Cluster processes", "Isolate memory", "Heavier than workers", "Multi-core HTTP", ""), ("Blocking sync API", "Simple dev", "Blocks loop", "Scripts", "Production server")],
"mistakes": ["Sync crypto on request path.", "CPU parse huge JSON main thread.", "Ignoring `unref` timers keeping process alive.", "Shared mutable state across workers without atomics.", "Default libuv pool size for all blocking work."],
"debug": "`--trace-event-categories node.perf` loop delay. Clinic.js diagnostics. Worker postMessage bottlenecks.",
"revision": ["One loop thread JS.", "libuv poll phase.", "workers for CPU.", "cluster for cores.", "Never block loop."],
"completion": ["Event loop phases sketch.", "worker_threads vs cluster.", "What blocks loop.", "libuv pool role.", "Measure loop lag."],
"related": ["D13-T003", "D13-T015", "D13-T016"],
**_ex(
    "Order setImmediate vs setTimeout 0.",
    "API stalls sync fs read.",
    "Cluster vs worker for bcrypt.",
    "setImmediate often before timeout 0 after I/O phase rules.",
    "Move fs to async API or worker.",
    "Workers share less; cluster duplicates memory; bcrypt fits worker pool.",
),
"qa": _qa(
("b","Node main thread runs?","JavaScript callbacks on event loop.",""),
("b","What is libuv?","Async I/O library underlying Node.",""),
("b","worker_threads purpose?","Run JS on additional threads for CPU.",""),
("b","Does async mean parallel JS on main?","No concurrent callbacks interleaved not parallel.",""),
("b","cluster module?","Multiple Node processes share port.",""),
("i","Event loop phases order?","timers, pending, idle, poll, check, close.",""),
("i","setImmediate vs process.nextTick?","nextTick runs before loop continues; higher priority.",""),
("i","libuv thread pool size?","UV_THREADPOOL_SIZE env default 4.",""),
("i","Blocking dns lookup?","May use thread pool.",""),
("i","Transferable objects?","Reduce copy to workers.",""),
("a","V8 and loop?","Runs one stack until empty then next phase.",""),
("a","SharedArrayBuffer?","Requires careful threading model.",""),
("a","Atomics in workers?","Coordinate shared memory.",""),
("a","Why not threads for all I/O?","Event loop model fits JS ecosystem.",""),
("a","Comparison Python asyncio?","Similar cooperative single-thread loop per process.",""),
("s","p99 spike periodic.","GC or timer storm on loop.",""),
("s","One core 100% node.","Sync CPU on main.",""),
("s","Handles leak.","Forgot close server or timers.",""),
("s","Worker OOM.","Huge buffer passed.",""),
("s","Thundering herd accepts.","Single accept bottleneck; reuseport cluster.",""),
("f","Event-driven?","(`D13-T003`).",""),
("f","CPU vs I/O?","(`D13-T015`).",""),
("f","Bulkheads?","(`D13-T020`).",""),
),
},
{
"id": "D13-T020", "next": "D13-T021",
"overview": "**Concurrency limits** cap in-flight work per resource. **Bulkheads** isolate pools so failure or slowness in one dependency cannot exhaust all threads or connections.",
"principles": "Semaphores, fixed pools, and rate limiters enforce limits. Hystrix-style bulkheads per downstream. Combined with timeouts and circuit breakers for resilience.",
"architecture": "Separate thread pools per partner API; Hikari max pool; Envoy max connections; Kubernetes pod concurrency limits.",
"mermaid": "flowchart TD\n  api[API threads]\n  b1[Bulkhead A]\n  b2[Bulkhead B]\n  da[Service A]\n  db[Service B]\n  api --> b1 --> da\n  api --> b2 --> db",
"examples": "Analogy: watertight ship compartments—one leak doesn't sink all. Backend: 30 threads max for payments partner regardless of 200 for catalog.",
"code_file": "d13_t020_bulkhead.py",
"code": textwrap.dedent('''
import threading
payment_sem = threading.Semaphore(5)


def call_payment() -> None:
    with payment_sem:
        pass  # invoke partner
'''),
"code_notes": "Semaphore limits concurrent payment calls to five.",
"backend": "Document limits in runbooks. Alert when bulkhead consistently full—that's early overload signal. Align with partner SLAs.",
"trade_rows": [("Per-dependency pool", "Isolation", "More threads total", "Microservices", "Tiny monolith"), ("Global pool only", "Simple", "Cross-cascade failure", "Early MVP", "Mature prod"), ("Rate limiter", "Controls arrival", "Doesn't help slow downstream alone", "Edge", ""), ("Queue + fixed workers", "Smooth bursts", "Added latency", "Async pipelines", "")],
"mistakes": ["One giant pool for all HTTP clients.", "Limit threads but not DB connections.", "No metric when bulkhead saturated.", "Limits never tuned after traffic 10x.", "Bulkhead without timeout still hangs slots."],
"debug": "Saturated semaphore with idle CPU elsewhere. Trace which dependency holds slots. Compare thread dump vs pool metrics.",
"revision": ["Bulkhead = isolated capacity.", "Limit each dependency.", "Match DB HTTP pools.", "Alert on saturation.", "Pair with timeouts."],
"completion": ["Define bulkhead.", "Semaphore example.", "vs circuit breaker.", "Size payment bulkhead.", "Cascading failure without."],
"related": ["D13-T004", "D13-T011", "D13-T021", "D13-T007"],
**_ex(
    "Semaphore limit 5 concurrent partner calls.",
    "All threads blocked one slow DB.",
    "Global vs per-tenant limits.",
    "Section F pattern.",
    "Dedicated DB bulkhead smaller than HTTP threads; timeouts release.",
    "Per-tenant prevents one tenant exhausting global budget.",
),
"qa": _qa(
("b","What is a bulkhead?","Isolated resource pool limiting blast radius.",""),
("b","Why concurrency limits?","Protect memory CPU and partners.",""),
("b","Semaphore as bulkhead?","Caps parallel calls to dependency.",""),
("b","Thread pool per service?","Bulkhead pattern.",""),
("b","What when bulkhead full?","Fail fast or queue with bound.",""),
("i","Circuit breaker relation?","Opens after failures; bulkhead prevents total exhaustion.",""),
("i","Rate limit vs concurrency?","Rate is per time; concurrency is simultaneous.",""),
("i","Connection pool size?","Bulkhead on DB.",""),
("i","Envoy max requests?","Proxy-level bulkhead.",""),
("i","Kubernetes limits?","Pod CPU mem concurrency.",""),
("a","Bulkhead saturation metric?","Reject count wait time.",""),
("a","Coordinated omission?","Don't hide latency when limiting.",""),
("a","Adaptive limits?","Reduce on error rate rise.",""),
("a","Fairness across tenants?","Weighted bulkheads.",""),
("a","Queue before bulkhead?","Adds latency smoothing.",""),
("s","Catalog slow takes down checkout.","Shared pool.", "Separate bulkheads.",""),
("s","503 when partner fine.","Your bulkhead too small mis-tuned.",""),
("s","DB connections 0 available.","HTTP threads exceed pool.",""),
("s","Retries amplify load.","Retry storm crosses bulkhead.",""),
("s","One tenant hogs API.","Per-tenant bulkhead missing.",""),
("f","Timeouts?","(`D13-T021`).",""),
("f","Backpressure?","(`D13-T011`).",""),
("f","Thread pools?","(`D13-T004`).",""),
),
},
{
"id": "D13-T021", "next": "D13-T022",
"overview": "**Cancellation** stops in-flight work when deadlines hit or clients disconnect. **Timeouts** bound wait time so threads and connections return to pools.",
"principles": "Cooperative cancel: check `context`/`CancellationToken` between steps. Forcible thread interrupt is brittle. HTTP client read timeout vs connection timeout differ. Propagate cancel to child calls.",
"architecture": "Go `context.WithTimeout`; Java `Future.cancel`; Python `asyncio.wait_for` and task.cancel(); gRPC deadline propagation.",
"mermaid": "flowchart LR\n  req[Request deadline]\n  ctx[Context]\n  work[Downstream calls]\n  req --> ctx --> work",
"examples": "Analogy: oven timer cancels bake even if you forget. Backend: 2s budget for search aggregates partial results.",
"code_file": "d13_t021_timeout.py",
"code": textwrap.dedent('''
import asyncio


async def slow() -> None:
    await asyncio.sleep(10)


async def main() -> None:
    try:
        await asyncio.wait_for(slow(), timeout=0.1)
    except asyncio.TimeoutError:
        print("cancelled by timeout")


if __name__ == "__main__":
    asyncio.run(main())
'''),
"code_notes": "wait_for cancels task on timeout.",
"backend": "Set timeouts at every hop; shorter at edge than sum of internals. On cancel, abort idempotent ops and release bulkhead slots.",
"trade_rows": [("Client timeout", "Protects caller", "May leave server running briefly", "HTTP/gRPC", ""), ("Server deadline", "Bounds resource use", "Must propagate", "Gateways", ""), ("Interrupt thread", "Forceful", "Unsafe invariants", "Rare", "Cooperative preferred"), ("No timeout", "Simple", "Hangs forever", "Never prod", "")],
"mistakes": ["Only outer timeout not inner RPCs.", "Ignoring cancel on async HTTP client.", "Timeout without closing DB statement.", "Swallowing TimeoutException.", "Same timeout connect and read."],
"debug": "Threads stuck in socket read—missing read timeout. Distributed traces show which hop exceeded budget.",
"revision": ["Always set timeouts.", "Propagate context/deadline.", "Cooperative cancel.", "Release resources on cancel.", "Partial results policy."],
"completion": ["Connect vs read timeout.", "asyncio cancel behavior.", "Go context tree.", "Why interrupt is hard.", "Client disconnect handling."],
"related": ["D13-T005", "D13-T020", "D13-T022", "D13-T018"],
**_ex(
    "asyncio wait_for timeout demo.",
    "Threads stuck in HTTP get.",
    "Cancel child RPC on parent timeout.",
    "Section F prints cancelled by timeout.",
    "Set connect and read timeouts on HttpClient.",
    "Use context cancellation token on all nested calls.",
),
"qa": _qa(
("b","Why timeouts?","Prevent indefinite resource hold.",""),
("b","Cooperative cancellation?","Task checks cancel flag between steps.",""),
("b","Client disconnect?","Server should detect and stop work.",""),
("b","Future.cancel in Java?","May interrupt if running; policy flag.",""),
("b","gRPC deadline?","Propagates remaining time to downstream.",""),
("i","Connect vs read timeout?","TCP establish vs waiting for bytes.",""),
("i","asyncio Task.cancel?","Raises CancelledError at await.",""),
("i","context.WithCancel?","Parent cancel cascades children Go.",""),
("i","Idempotent on timeout retry?","Safe retry only with idempotency keys.",""),
("i","Bulkhead release on timeout?","Must exit finally block.",""),
("a","Distributed deadline budget?","Subtract elapsed at each hop.",""),
("a","Orphan work after timeout?","Continue unless explicit cancel propagation.",""),
("a","HTTP 504 vs 408?","Gateway timeout vs client request timeout.",""),
("a","Watchdog thread?","Dangerous kill; prefer cooperative.",""),
("a","Partial aggregate on timeout?","Product decision return 206 or error.",""),
("s","Pool exhausted all waiting HTTP.","No read timeout to slow partner.",""),
("s","CPU still after 504.","Server didn't cancel background task.",""),
("s","CancelledError logged error.","Treat cancel as normal on shutdown.",""),
("s","Child runs 60s parent 5s.","Deadline not passed to child.",""),
("s","DB lock held after timeout.","Must rollback transaction.",""),
("f","Structured concurrency?","(`D13-T022`).",""),
("f","Futures?","(`D13-T005`).",""),
("f","Bulkheads?","(`D13-T020`).",""),
),
},
{
"id": "D13-T022", "next": "",
"overview": "**Structured concurrency** scopes child tasks to a parent: children cannot outlive their parent scope, and failures propagate in a controlled way (nursery, `asyncio.TaskGroup`, Kotlin coroutineScope).",
"principles": "Contrast with fire-and-forget goroutines or orphan futures. Parent awaits all children; error in one cancels siblings. Makes lifetimes and cancellation trees explicit.",
"architecture": "Python 3.11+ `TaskGroup`; Java structuredTaskScope preview; Go errgroup with context; Kotlin coroutineScope. Goal: no leaked background tasks.",
"mermaid": "flowchart TD\n  parent[Parent scope]\n  c1[Child task 1]\n  c2[Child task 2]\n  parent --> c1\n  parent --> c2\n  parent -->|waits all| done[Scope exit]",
"examples": "Analogy: manager waits for all interns before leaving office—no stragglers. Backend: HTTP handler spawns parallel fetches inside TaskGroup; client disconnect cancels group.",
"code_file": "d13_t022_structured.py",
"code": textwrap.dedent('''
import asyncio


async def child(x: int) -> int:
    return x * 2


async def main() -> None:
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(child(3))
        t2 = tg.create_task(child(4))
    assert t1.result() + t2.result() == 14
    print("ok")


if __name__ == "__main__":
    asyncio.run(main())
'''),
"code_notes": "Requires Python 3.11+ TaskGroup.",
"backend": "Prefer structured scopes over dangling `create_task` without reference. Tie to request context for cancel on disconnect.",
"trade_rows": [("Structured scope", "Clear lifetimes", "API newer", "Handler fan-out", "Long daemon jobs"), ("Fire-and-forget", "Simple spawn", "Leaks and orphans", "Background cron", "Request path"), ("Supervisor restarts", "Fault tolerance", "Complex", "Erlang style", ""), ("Manual future list", "Flexible", "Easy to forget join", "Legacy", "")],
"mistakes": ["create_task without await on shutdown.", "Exception in child not cancelling siblings when needed.", "Mixing structured and global background tasks.", "Scope shorter than slow child.", "Ignoring TaskGroup ExceptionGroup."],
"debug": "Rising goroutine/task count after requests. Leak detectors. Ensure scope exit logs pending children.",
"revision": ["Parent owns child lifetime.", "Fail fast cancel siblings.", "TaskGroup/errgroup.", "No orphan tasks.", "Link to cancel context."],
"completion": ["Structured vs unstructured.", "TaskGroup behavior.", "Go errgroup pattern.", "Why leaks matter.", "Client disconnect story."],
"related": ["D13-T021", "D13-T005", "D13-T018", "D13-T003"],
**_ex(
    "TaskGroup two children sum results.",
    "Goroutines leak after HTTP done.",
    "errgroup vs waitgroup.",
    "Section F TaskGroup.",
    "Handler returned without waiting; tie to request context cancel.",
    "errgroup cancels context on first error; WaitGroup only waits no cancel.",
),
"qa": _qa(
("b","Structured concurrency idea?","Child tasks bound to parent scope lifetime.",""),
("b","Why avoid fire-and-forget?","Orphan tasks leak resources.",""),
("b","TaskGroup Python?","async with waits all children.",""),
("b","Failure propagation?","One child error can cancel others.",""),
("b","Relation to cancellation?","Scope exit triggers cancel (`D13-T021`).",""),
("i","ExceptionGroup?","Multiple errors from children.",""),
("i","Kotlin coroutineScope?","Structured concurrency in JVM.",""),
("i","Go errgroup?","Wait and cancel on error.",""),
("i","vs WaitGroup?","WaitGroup no automatic cancel.",""),
("i","Nursery trio Python library?","Prior art before TaskGroup.",""),
("a","Daemon tasks?","Outlive scope—use only deliberate services.",""),
("a","Structured across services?","Hard; use distributed tracing + cancel signals.",""),
("a","Long running child?","Detach only with clear ownership.",""),
("a","Java structuredTaskScope?","Preview API join shutdown.",""),
("a","Testing structured scopes?","Assert no pending tasks after.",""),
("s","Memory grows per request.","Leaked tasks.",""),
("s","One failed fetch fails page.","TaskGroup default; handle partial.",""),
("s","Shutdown hang.","Await TaskGroup with timeout.",""),
("s","Child survives parent HTTP.", "Missing scope boundary.",""),
("s","Exception swallowed child.","Log ExceptionGroup causes.",""),
("f","Futures unstructured?","(`D13-T005`).",""),
("f","Goroutines?","(`D13-T018`).",""),
("f","async event loop?","(`D13-T003`).",""),
),
},
]

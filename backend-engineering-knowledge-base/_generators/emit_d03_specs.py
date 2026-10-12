"""Specs for D03-T004..T024 used by emit_d03_004_024.py"""
import textwrap

def _bank(beg, int_, adv, scn, fu):
    return {"beg": beg, "int": int_, "adv": adv, "scn": scn, "fu": fu}


def mk(
    tid,
    slug,
    title,
    deps,
    focus,
    mermaid,
    code_file,
    code,
    code_run,
    code_out,
    code_lines,
    bank,
    exercises,
    solutions,
    related,
):
    ov = (
        f"{title} is a core operating-system concept for backend engineers: {focus} "
        "Production services depend on the kernel to enforce fairness, isolation, and correct I/O behavior. "
        "Interviewers expect you to connect textbook definitions to latency, throughput, and incident debugging. "
        f"Prerequisites are earlier D03 topics; this note builds toward {related['sup']}."
    )
    fp = (
        f"At the hardware level, {title.lower()} involves the kernel's scheduler, memory manager, or I/O stack coordinating with CPU and devices. "
        "User programs observe behavior through syscalls, errno, and metrics rather than direct hardware access. "
        "Correctness often depends on atomicity, ordering, and resource limits enforced in kernel mode. "
        "Performance tuning requires knowing what is O(1) in user space versus what always traps to the kernel."
    )
    internal = (
        f"Linux implements {title.lower()} using per-CPU run queues, wait queues, reference-counted kernel objects, and cgroup policies. "
        "A typical backend request path crosses this topic when threads block, when memory is faulted in, or when file descriptors are used concurrently. "
        "Observability hooks include ftrace, perf, eBPF tracepoints, and /proc interfaces. "
        "Containers share the host kernel implementation; namespaces change what processes see, not the core algorithms."
    )
    dia = "Read the diagram as the primary control flow for this topic on Linux; names are logical, not every distro detail."
    ex = (
        f"Analogy: treat {title.lower()} like traffic control for a city—rules prevent gridlock but misconfiguration still causes jams. "
        "Backend example: tail latency spikes often trace here combined with lock contention or disk/network wait. "
        "Do not confuse this topic with a language feature alone; the OS semantics remain even in managed runtimes."
    )
    be = (
        "Instrument p50/p99 latency, run-queue length, syscall rates, and memory fault counters. "
        "Load tests should include realistic concurrency and cgroup limits matching production Kubernetes requests/limits. "
        "Incidents: capture thread dumps, `perf record`, and `strace` samples on canary pods before restarting everything."
    )
    tr = [
        ("Kernel-default policy", "Works broadly", "May not fit SLA", "General services", "Hard real-time"),
        ("Explicit tuning", "Meets SLO", "Ops burden", "Known bottlenecks", "Unknown workload"),
        ("More isolation", "Blast radius down", "Overhead up", "Multi-tenant", "Single trusted tenant"),
        ("More sharing", "Efficiency", "Contention risk", "Single service heap", "Untrusted code"),
    ]
    mi = (
        "- Ignoring that managed runtimes still sit on OS semantics.\n"
        "- Tuning without measuring p99 and saturation.\n"
        "- Assuming more threads always increase throughput.\n"
        "- Forgetting EINTR, partial I/O, and errno on syscalls.\n"
    )
    de = (
        "Symptoms: rising latency at moderate CPU, stuck workers, OOM, hung pods. "
        "Steps: check run queue, blocked threads, fault rates, FD usage, cgroup throttling, dmesg. "
        "Mitigate with backpressure, pool limits, and kernel/host upgrades for confirmed kernel bugs."
    )
    rev = (
        f"- {title}: {focus}\n"
        "- Link behavior to syscalls and kernel objects.\n"
        "- Measure before changing pool sizes or ulimits."
    )
    fl = (
        f"- Define {title.lower()} in one sentence?\n"
        "- Name one Linux tool to observe it?"
    )
    cri = (
        f"- Explain {title.lower()} without notes.\n"
        "- Draw or walk through the mermaid flow.\n"
        "- Answer one scenario from section K.\n"
        "- Propose a production metric and alert."
    )
    return (
        slug,
        title,
        {
            "deps": deps,
            "ov": ov,
            "fp": fp,
            "in": internal,
            "mer": mermaid,
            "dia": dia,
            "ex": ex,
            "cf": code_file,
            "code": code,
            "cr": code_run,
            "co": code_out,
            "cl": code_lines,
            "be": be,
            "tr": tr,
            "mi": mi,
            "de": de,
            "bank": bank,
            "e1": exercises[0],
            "e2": exercises[1],
            "e3": exercises[2],
            "s1": solutions[0],
            "s2": solutions[1],
            "s3": solutions[2],
            "rev": rev,
            "fl": fl,
            "pre": related["pre"],
            "sup": related["sup"],
            "con": related["con"],
            "com": related["com"],
            "cri": cri,
        },
    )


def q_banks(title):
    t = title.lower()
    return _bank(
        [
            (f"What is {title}?", f"The OS mechanism behind {t} that user programs interact with via syscalls and kernel policy."),
            (f"Why does {title} matter for servers?", "It affects latency, fairness, isolation, and stability under concurrent load."),
            (f"Name one syscall or tool related to {title}.", "Depends on topic: strace, perf, futex, mmap, epoll, kill, ulimit, ip."),
            (f"User or kernel mode for {title}?", "Policy and enforcement occur in kernel mode; applications observe results in user mode."),
            (f"One failure mode of {title}?", "Contention, starvation, deadlock, thrashing, or resource exhaustion depending on subtopic."),
        ],
        [
            (f"How does Linux implement {title} at a high level?", "Through scheduler, MMU, VFS, networking stack, and synchronization primitives in the kernel."),
            (f"How do threads affect {title}?", "Threads share address space and FDs, amplifying races and shared resource use."),
            (f"How do cgroups relate to {title}?", "They limit and account CPU, memory, and I/O, changing effective scheduling and OOM behavior."),
            (f"Container vs VM for {title}?", "Containers share the kernel; VMs add a hypervisor layer with separate kernels."),
            (f"One metric for {title}?", "Run-queue latency, page faults, syscall rate, lock wait time, or FD count."),
        ],
        [
            (f"Advanced trade-off in {title}?", "Throughput vs tail latency vs isolation—tuning shifts who pays under overload."),
            (f"How does eBPF help {title}?", "Programmable kernel probes for latency histograms without recompiling the kernel."),
            (f"NUMA interaction with {title}?", "Memory and CPU locality change fault and scheduling costs on large hosts."),
            (f"Realtime vs CFS regarding {title}?", "RT priorities can starve CFS tasks; needs careful capacity planning."),
            (f"Security angle of {title}?", "Misconfiguration can leak data across tenants or enable denial of service."),
        ],
        [
            (f"p99 latency rises; how could {title} be involved?", "Measure run queue, blocking, faults, or lock waits tied to this mechanism."),
            (f"Incident after kernel upgrade touching {title}?", "Compare perf profiles, rollback canary, check known CVE/mitigations."),
            (f"One pod noisy-neighbor story for {title}?", "Shared node kernel state causes contention; use limits and isolation."),
            (f"Load test passes, prod fails—{title} angle?", "Prod has higher parallelism, colder caches, or stricter cgroups."),
            (f"Developer says OS is irrelevant to {title}?", "Show syscall trace or JVM/native thread blocked in kernel stack."),
        ],
        [
            (
                f"How does {title} connect to the next D03 topics?",
                f"It composes with synchronization, memory, and I/O models across the curriculum. "
                "Interviewers chain questions from processes to locks to epoll to IPC. "
                "You should narrate an end-to-end request touching each layer. "
                "Use metrics at each boundary to prove understanding.",
            ),
            (
                f"How does {title} appear in Kubernetes?",
                "Pods set requests/limits and security contexts that change cgroup behavior and syscall allow lists. "
                "Node problems are kernel problems for all pods on the node. "
                "Horizontal scaling adds processes; vertical scaling changes contention on shared kernel resources. "
                "Liveness probes must reflect the event loop or worker threads you rely on.",
            ),
            (
                f"How would you debug {title} in production?",
                "Start with saturation signals, then sample stacks and syscalls on a canary before fleet-wide changes. "
                "Reproduce with load tests that match concurrency and payload size. "
                "Document mitigations: backpressure, pool bounds, kernel tuning, or architecture split. "
                "Verify fixes with before/after histograms, not only average CPU.",
            ),
        ],
    )


SPECS = {}

_C = """#include <stdio.h>
int main(void) { printf("d03 demo\\n"); return 0; }"""

def add(tid, slug, title, deps, focus, mer, ex, sol, rel):
    SPECS[tid] = mk(
        tid,
        slug,
        title,
        deps,
        focus,
        mermaid=mer,
        code_file=f"examples/{slug.replace('.md','')}.c",
        code=_C,
        code_run=f"cc examples/{slug.replace('.md','')}.c && ./a.out",
        code_out="d03 demo",
        code_lines="Placeholder demo; replace with topic-specific syscall sample when extending.",
        bank=q_banks(title),
        exercises=ex,
        solutions=sol,
        related=rel,
    )


add(
    "D03-T004",
    "d03-t004-system-calls.md",
    "System calls",
    "`D03-T003`, `D03-T001`",
    "controlled kernel entry for I/O, memory mapping, and process control; errno and EINTR semantics.",
    "sequenceDiagram\n  participant App\n  participant Kernel\n  App->>Kernel: syscall_enter\n  Kernel-->>App: result_or_errno",
    (
        "Loop read() retrying EINTR.",
        "strace shows excessive write syscalls from logging.",
        "Buffered vs direct socket writes for metrics.",
    ),
    ("Retry loop on EINTR.", "Add log buffer/async appender.", "Batch writes 64KB."),
    {"pre": "`D03-T003`", "sup": "`D03-T019`", "con": "libc call vs syscall", "com": "networking and containers"},
)

add("D03-T005", "d03-t005-cpu-scheduling.md", "CPU scheduling", "`D03-T004`, `D03-T001`",
    "CFS vruntime, priorities, preemption, and cgroup CPU throttling affecting p99.",
    "flowchart TD\n  runnable[RunnableQueue]\n  cpu[CPU]\n  runnable -->|schedule| cpu\n  cpu -->|preempt_or_block| runnable",
    ("Print policy via sched_getscheduler on self.", "Run queue high, CPU low—explain.", "Fixed threads vs GOMAXPROCS tuning."),
    ("sched_getscheduler PID.", "Too many runnable threads or cgroup throttle.", "Match threads to quota and workload."),
    {"pre": "`D03-T002`", "sup": "`D03-T006`", "con": "parallelism", "com": "JVM GC pauses"},
)

add("D03-T006", "d03-t006-threads-and-thread-pools.md", "Threads and thread pools", "`D03-T005`, `D03-T001`",
    "bounded executors, queueing, and rejection policies to avoid unbounded thread growth.",
    "flowchart LR\n  req[Requests]\n  q[Queue]\n  pool[ThreadPool]\n  req --> q --> pool",
    ("Implement fixed pool with bounded queue.", "OutOfMemoryError native threads.", "Pool size vs CPU cores for I/O bound API."),
    ("ExecutorService fixed + ArrayBlockingQueue.", "Unbounded new Thread per task.", "Size ~ cores*2 for mixed I/O; measure."),
    {"pre": "`D03-T001`", "sup": "`D03-T008`", "con": "goroutines", "com": "backpressure"},
)

add("D03-T007", "d03-t007-concurrency-vs-parallelism.md", "Concurrency vs parallelism", "`D03-T006`, `D03-T001`",
    "interleaved progress versus simultaneous execution on multiple cores.",
    "flowchart TD\n  cores[MultipleCPUs]\n  tasks[ManyTasks]\n  tasks --> cores",
    ("Demonstrate concurrent but not parallel on one core.", "CPU 100% one thread—parallel?", "Async vs threads for 10k connections."),
    ("time sleep tasks single core.", "Not parallel; single runnable.", "epoll async for idle connections."),
    {"pre": "`D03-T001`", "sup": "`D03-T021`", "con": "async vs parallel", "com": "event loops"},
)

add("D03-T008", "d03-t008-race-conditions.md", "Race conditions", "`D03-T007`, `D03-T001`",
    "undefined outcomes from unsynchronized access to shared mutable state.",
    "flowchart TD\n  t1[ThreadA_read_write]\n  t2[ThreadB_read_write]\n  shared[SharedVariable]\n  t1 --> shared\n  t2 --> shared",
    ("Increment shared counter without locks; observe loss.", "Rare wrong balance in ledger.", "Lock vs atomic for a counter."),
    ("Race demo < expected sum.", "Missing synchronization on shared map.", "AtomicLong or synchronized block."),
    {"pre": "`D03-T001`", "sup": "`D03-T009`", "con": "data race vs race condition", "com": "database transactions"},
)

add("D03-T009", "d03-t009-critical-sections-and-synchronization.md", "Critical sections and synchronization", "`D03-T008`, `D03-T001`",
    "mutual exclusion around invariants; locks protect regions not types.",
    "flowchart LR\n  enter[EnterCS]\n  work[MutateInvariant]\n  exit[ExitCS]\n  enter --> work --> exit",
    ("Protect linked-list insert with mutex.", "Deadlock in logs—two locks order.", "Coarse vs fine-grained lock trade-off."),
    ("pthread_mutex around list.", "Fixed lock ordering.", "Coarse for small critical region."),
    {"pre": "`D03-T008`", "sup": "`D03-T010`", "con": "immutable data", "com": "DB isolation levels"},
)

add("D03-T010", "d03-t010-mutexes-semaphores-read-write-locks.md", "Mutexes, semaphores, read-write locks", "`D03-T009`, `D03-T001`",
    "mutex for exclusion, semaphore for counting, rwlock for read-heavy caches.",
    "flowchart TD\n  mutex[Mutex_one_owner]\n  sem[Semaphore_count]\n  rw[RWLock_readers]",
    ("Producer-consumer with semaphores.", "Writer starvation on rwlock.", "Mutex vs RWLock for read-mostly cache."),
    ("sem_post/sem_wait bounded buffer.", "Fairness policy or mutex for writers.", "RWLock if reads dominate."),
    {"pre": "`D03-T009`", "sup": "`D03-T011`", "con": "spinlock vs mutex", "com": "connection pools"},
)

add("D03-T011", "d03-t011-deadlocks-prevention-detection-recovery.md", "Deadlocks: prevention, detection, recovery", "`D03-T010`, `D03-T001`",
    "Coffman conditions; ordering, timeouts, and banker's algorithm intuition.",
    "flowchart TD\n  A[Thread1_lock_L1]\n  B[Thread2_lock_L2]\n  A -->|waits L2| B\n  B -->|waits L1| A",
    ("Create deadlock with two mutexes.", "DB pool hung—graph locks.", "Prevent vs detect for payments."),
    ("Opposite lock order demo.", "jstack circular wait.", "Strict lock order + timeouts."),
    {"pre": "`D03-T010`", "sup": "`D03-T012`", "con": "livelock", "com": "distributed deadlocks"},
)

add("D03-T012", "d03-t012-starvation-and-livelocks.md", "Starvation and livelocks", "`D03-T011`, `D03-T001`",
    "threads never proceed despite activity; fairness and backoff.",
    "flowchart LR\n  low[LowPriority]\n  high[HighPriority]\n  high -->|always_runs| cpu[CPU]",
    ("Starve low-priority thread.", "Livelock retry storm.", "Fair queue vs throughput."),
    ("Busy high-priority loop.", "Exponential backoff on conflict.", "Fair semaphores."),
    {"pre": "`D03-T011`", "sup": "`D03-T013`", "con": "deadlock", "com": "retry policies"},
)

add("D03-T013", "d03-t013-atomic-operations-and-compare-and-swap.md", "Atomic operations and compare-and-swap", "`D03-T012`, `D03-T001`",
    "lock-free counters and CAS retry loops; ABA problem awareness.",
    "flowchart TD\n  read[ReadValue]\n  cas[CAS_update]\n  read --> cas\n  cas -->|fail_retry| read",
    ("Atomic increment benchmark vs mutex.", "CAS retry hot loop burns CPU.", "When lock-free is worth it."),
    ("__atomic_fetch_add.", "High contention CAS spin.", "Mutex under heavy contention."),
    {"pre": "`D03-T010`", "sup": "`D03-T014`", "con": "volatile", "com": "java.util.concurrent"},
)

add("D03-T014", "d03-t014-memory-management-and-virtual-memory.md", "Memory management and virtual memory", "`D03-T013`, `D03-T001`",
    "virtual addresses, page tables, and per-process isolation.",
    "flowchart TD\n  va[VirtualAddress]\n  pt[PageTable]\n  pa[PhysicalFrame]\n  va --> pt --> pa",
    ("Print /proc/self/maps.", "RSS high but heap small—stacks?", "overcommit and OOM killer."),
    ("parse maps regions.", "thread stacks + mapped jars.", "set memory limits cgroups."),
    {"pre": "`D03-T001`", "sup": "`D03-T015`", "con": "heap vs VSZ", "com": "JVM heap tuning"},
)

add("D03-T015", "d03-t015-paging-and-segmentation.md", "Paging and segmentation", "`D03-T014`, `D03-T001`",
    "fixed-size pages, TLB, and modern x86 using paging primarily.",
    "flowchart LR\n  tlb[TLB]\n  ram[RAM_frames]\n  tlb --> ram",
    ("Page size impact on fragmentation.", "TLB miss latency.", "huge pages for JVM heap."),
    ("getconf PAGESIZE.", "perf tlb-misses.", "transparent huge pages cautiously."),
    {"pre": "`D03-T014`", "sup": "`D03-T016`", "con": "segmentation legacy", "com": "databases buffer pool"},
)

add("D03-T016", "d03-t016-page-faults.md", "Page faults", "`D03-T015`, `D03-T001`",
    "minor vs major faults, demand paging, and swap latency.",
    "flowchart TD\n  access[MemoryAccess]\n  fault[PageFault]\n  disk[DiskRead]\n  access -->|missing| fault\n  fault -->|major| disk",
    ("Measure minor/major faults under load.", "Cold start latency after deploy.", "mlock vs swap for latency SLO."),
    ("perf stat page-faults.", "new pods fault heavy.", "warmup + limits."),
    {"pre": "`D03-T015`", "sup": "`D03-T017`", "con": "cache miss", "com": "GC vs fault"},
)

add("D03-T017", "d03-t017-file-descriptors-and-file-systems.md", "File descriptors and file systems", "`D03-T016`, `D03-T001`",
    "integer handles, inode metadata, and per-process FD tables.",
    "flowchart TD\n  proc[Process]\n  fdtable[FDTable]\n  inode[Inode_or_socket]\n  proc --> fdtable --> inode",
    ("List FDs via /proc/self/fd.", "EMFILE too many open files.", "FD leaks in long-running workers."),
    ("ls -l /proc/$PID/fd.", "raise ulimit + fix leak.", "try-with-resources/close-on-exec."),
    {"pre": "`D03-T004`", "sup": "`D03-T018`", "con": "FILE pointer", "com": "zero-copy sendfile"},
)

add("D03-T018", "d03-t018-i-o-buffering.md", "I/O buffering", "`D03-T017`, `D03-T001`",
    "kernel page cache, stdio buffers, and socket send buffers.",
    "flowchart LR\n  app[AppBuffer]\n  kernel[KernelCache]\n  disk[Disk]\n  app --> kernel --> disk",
    ("Compare fread vs read syscall counts.", "fsync latency spikes.", "line-buffered logs vs throughput."),
    ("strace counts.", "group commit DB.", "buffered logging agent."),
    {"pre": "`D03-T017`", "sup": "`D03-T019`", "con": "application cache", "com": "streaming APIs"},
)

add("D03-T019", "d03-t019-blocking-vs-non-blocking-i-o.md", "Blocking vs non-blocking I/O", "`D03-T018`, `D03-T001`",
    "O_NONBLOCK, EAGAIN, and readiness notification via epoll/kqueue.",
    "flowchart TD\n  block[BlockingRead_waits]\n  nonblock[Nonblocking_EAGAIN]\n  epoll[epoll_wait_ready]",
    ("Set O_NONBLOCK; handle EAGAIN.", "Thread pool exhausted blocking on DB.", "non-blocking driver support limits."),
    ("fcntl O_NONBLOCK.", "async DB client + smaller pool.", "threads for blocking JDBC unavoidable."),
    {"pre": "`D03-T004`", "sup": "`D03-T021`", "con": "async/await syntax", "com": "reactive streams"},
)

add("D03-T020", "d03-t020-synchronous-vs-asynchronous-execution.md", "Synchronous vs asynchronous execution", "`D03-T019`, `D03-T001`",
    "caller waits for completion versus callback/future completion.",
    "flowchart LR\n  sync[Sync_call_waits]\n  async[Async_callback_later]",
    ("Compare sync HTTP client vs async.", "Thread explosion on sync I/O.", "async all the way vs thread pool."),
    ("blocking client threads grow.", "use async client + loop.", "hybrid for CPU work."),
    {"pre": "`D03-T019`", "sup": "`D03-T021`", "con": "parallel async", "com": "message queues"},
)

add("D03-T021", "d03-t021-event-loops.md", "Event loops", "`D03-T020`, `D03-T001`",
    "reactor pattern: epoll_wait dispatch handlers; avoid blocking the loop.",
    "flowchart TD\n  wait[epoll_wait]\n  dispatch[HandleReadyFDs]\n  wait --> dispatch --> wait",
    ("Pseudo echo server event loop.", "Event loop blocked by CPU work.", "thread pool offload for CPU."),
    ("register accept/read handlers.", "move hash to worker pool.", "separate compute pool."),
    {"pre": "`D03-T019`", "sup": "`D03-T022`", "con": "multithreaded accept", "com": "Node/nginx"},
)

add("D03-T022", "d03-t022-signals-and-inter-process-communication.md", "Signals and inter-process communication", "`D03-T021`, `D03-T001`",
    "SIGTERM graceful shutdown, pipes, Unix domain sockets, and shared memory trade-offs.",
    "flowchart TD\n  sig[Signal_SIGTERM]\n  handler[Handler_runs]\n  ipc[Pipe_or_UDS]\n  sig --> handler\n  ipc --> peer[PeerProcess]",
    ("Install SIGTERM handler to drain.", "Zombie child on SIGCHLD ignored.", "pipe vs UDS for local RPC."),
    ("flag + graceful stop.", "waitpid loop.", "UDS for stream + credentials."),
    {"pre": "`D03-T002`", "sup": "`D03-T023`", "con": "Kafka vs pipe", "com": "graceful K8s shutdown"},
)

add("D03-T023", "d03-t023-linux-process-and-networking-commands.md", "Linux process and networking commands", "`D03-T022`, `D03-T001`",
    "ps, top, ss, lsof, strace, perf for incident response.",
    "flowchart LR\n  ps[ps_top]\n  ss[ss_lsof]\n  trace[strace_perf]",
    ("Document triage playbook commands.", "High TIME_WAIT ss output.", "strace in prod risks."),
    ("cheat sheet for on-call.", "tune tcp_tw_reuse carefully.", "use perf/eBPF instead at scale."),
    {"pre": "`D03-T001`", "sup": "`D03-T024`", "con": "metrics server only", "com": "SRE runbooks"},
)

add("D03-T024", "d03-t024-resource-limits-and-process-isolation.md", "Resource limits and process isolation", "`D03-T023`, `D03-T001`",
    "rlimit, cgroups v2, namespaces, and capabilities for blast radius.",
    "flowchart TD\n  ulimit[rlimit_nofile]\n  cgroup[cgroup_cpu_mem]\n  ns[namespaces]\n  ulimit --> cgroup --> ns",
    ("Set nofile ulimit in systemd unit.", "OOMKilled but memory chart low.", "capabilities vs privileged pod."),
    ("LimitNOFILE in unit.", "RSS vs page cache accounting.", "drop CAP_SYS_ADMIN."),
    {"pre": "`D03-T001`", "sup": "container security", "con": "JVM -Xmx only", "com": "Kubernetes limits"},
)


if __name__ == "__main__":
    from emit_d03_004_024 import emit

    for tid, (slug, name, spec) in SPECS.items():
        emit(tid, slug, name, spec)
    print("materialized", len(SPECS), "topics (D03-T004..T024)")

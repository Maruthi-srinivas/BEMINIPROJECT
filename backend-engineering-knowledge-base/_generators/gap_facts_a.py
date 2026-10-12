"""Topic facts for algorithms, operating systems, and networking gaps."""

from __future__ import annotations

FACTS: dict[str, dict] = {}


def add(
    tid: str,
    mech: str,
    steps: list[str],
    fail: str,
    metric: str,
    code: str,
    analogy: str,
    prod: str,
    choose: str,
    avoid: str,
    mistakes: list[str],
    lang: str = "python",
) -> None:
    FACTS[tid] = {
        "mech": mech,
        "steps": steps,
        "fail": fail,
        "metric": metric,
        "code": code,
        "analogy": analogy,
        "prod": prod,
        "choose": choose,
        "avoid": avoid,
        "mistakes": mistakes,
        "lang": lang,
    }


add(
    "D02-T020",
    "A greedy algorithm locks in the locally best feasible choice and never revisits it. It is correct only when a greedy-choice property holds: some optimal solution starts with that local choice, and the remainder is itself an optimal subproblem. Interval scheduling by earliest finish time, Huffman coding, and Dijkstra with non-negative edge weights are the usual cases. A coin system that is not canonical is the usual counterexample.",
    ["Sort candidates by the greedy key", "Pick the best feasible candidate", "Shrink the remaining problem", "Prove a later swap cannot improve the answer"],
    "the local choice blocks a better global solution, as with a non-canonical coin system or Dijkstra on a negative edge",
    "the gap between the greedy answer and a dynamic-programming answer on a small counterexample",
    "def earliest_finish(intervals):\n    chosen = []\n    last = float('-inf')\n    for start, end in sorted(intervals, key=lambda it: it[1]):\n        if start >= last:\n            chosen.append((start, end))\n            last = end\n    return chosen\n",
    "It is like packing a suitcase by always taking the next item that finishes soonest, which works only if that rule cannot paint you into a corner.",
    "A batch job scheduler that always runs the shortest remaining task can starve long tasks. Earliest-deadline-first is a different greedy rule and needs its own proof.",
    "you can state the exchange argument that swapping in the greedy choice never worsens an optimal solution",
    "the problem has overlapping choices that must be compared, which is dynamic programming or search instead",
    ["Using greedy because it is fast, without a proof.", "Applying Dijkstra to negative weights.", "Sorting by the wrong key and still calling it optimal."],
)

add(
    "D02-T021",
    "Backtracking searches a decision tree and undoes a choice when it violates a constraint. It is depth-first enumeration with pruning. Correctness comes from exploring every feasible partial assignment, not from greediness. Pruning is safe only when a partial assignment can never be extended to a solution.",
    ["Choose a value for the next variable", "Check the constraint on the partial assignment", "Recurse when the partial assignment is still feasible", "Undo the choice and try the next value"],
    "pruning a branch that still contains a solution, or exploring a tree so large that latency exceeds the request deadline",
    "nodes visited versus solutions found, and p99 latency of the search call",
    "def subsets(nums):\n    out = []\n    def dfs(i, path):\n        if i == len(nums):\n            out.append(list(path))\n            return\n        path.append(nums[i])\n        dfs(i + 1, path)\n        path.pop()\n        dfs(i + 1, path)\n    dfs(0, [])\n    return out\n",
    "It is walking a maze and stepping back to the last junction when a corridor is blocked.",
    "A constraint solver that places shipments into trucks backtracks when weight or delivery windows fail. Without a timeout it can pin a worker for the whole request.",
    "the search space is small after pruning, or you need every feasible answer",
    "a closed-form or greedy rule already exists, or n is large and you only need one good answer",
    ["Forgetting to undo state after the recursive call.", "Pruning on a heuristic that is not a real constraint.", "Using recursion depth as an excuse to skip an explicit stack and a deadline."],
)

add(
    "D02-T022",
    "Dynamic programming solves a problem by combining answers to overlapping subproblems and storing each answer once. It needs optimal substructure and a recurrence you can evaluate in an order that respects dependencies. Memoization is top-down. Tabulation is bottom-up. The state must be small enough to store.",
    ["Define the state and the recurrence", "Order states so dependencies are already known", "Store each state once", "Read the answer from the designated final state"],
    "a state that forgets a dimension the recurrence needs, so two different futures share one stored answer",
    "number of states times work per transition, and whether the cached answer matches a brute-force oracle on small n",
    "def coin_change(coins, amount):\n    inf = amount + 1\n    dp = [0] + [inf] * amount\n    for a in range(1, amount + 1):\n        for c in coins:\n            if c <= a:\n                dp[a] = min(dp[a], dp[a - c] + 1)\n    return dp[amount] if dp[amount] < inf else -1\n",
    "It is filling a spreadsheet where each cell is a formula over earlier cells, and you never recompute a cell.",
    "A pricing service that computes the cheapest way to cover a cart with promotions uses a knapsack-style recurrence. If the state omits the promotion stack, two carts collide in one cell.",
    "subproblems overlap and the state fits in memory",
    "the recurrence is wrong or the state space is exponential in a dimension you cannot drop",
    ["Caching a function of too few arguments.", "Iterating coins and amounts in an order the recurrence does not allow.", "Calling memoization and tabulation different algorithms when they share one recurrence."],
)

add(
    "D02-T023",
    "Bit manipulation uses bitwise AND, OR, XOR, shifts, and masks to represent sets and flags in a word. XOR is its own inverse, so a^a is 0 and a^0 is a. Shifts move bits and are not arithmetic multiply once the sign bit or a discarded bit matters. A mask isolates a field.",
    ["Decide the meaning of each bit", "Combine values with a mask", "Update with OR to set, AND NOT to clear, XOR to toggle", "Test with AND against the mask"],
    "signed right shift, off-by-one mask width, or treating a bitset as a bigint across languages with different word sizes",
    "round-trip tests that set, clear, and read each flag, plus property tests that XOR twice returns the input",
    "def set_bit(mask, i):\n    return mask | (1 << i)\n\ndef has_bit(mask, i):\n    return (mask & (1 << i)) != 0\n",
    "A bit mask is a row of switches on one integer. XOR is flipping a switch twice and ending where you started.",
    "Feature flags packed into a permissions integer on a session row. A mask that is one bit too wide grants an admin capability.",
    "the domain is a small set of flags or a bitset algorithm such as subset enumeration",
    "the flags need names, auditing, and independent rollout, which a column or a set stores more safely",
    ["Using arithmetic plus instead of OR.", "Shifting into the sign bit and then dividing.", "Assuming Python's unlimited ints match a 32-bit language."],
)

add(
    "D02-T024",
    "Interval algorithms keep segments on a line. Sorting by start or end, then scanning once, answers overlap, merge, and minimum meeting rooms. A sweep line moves a cursor and updates a counter or a heap at each start and end event. A segment tree answers stabbing queries when the scan is not enough.",
    ["Represent each interval as a start event and an end event", "Sort events with a tie-break that ends before starts or the reverse, and state which", "Walk the cursor and update active count", "Emit a merge or a peak when the count changes"],
    "a tie-break that closes an interval before it opens at the same timestamp, so a meeting that ends when another starts looks like an overlap",
    "maximum active count against a brute-force overlap matrix on small inputs",
    "def max_overlap(intervals):\n    events = []\n    for start, end in intervals:\n        events.append((start, 1))\n        events.append((end, -1))\n    events.sort()\n    cur = best = 0\n    for _, delta in events:\n        cur += delta\n        best = max(best, cur)\n    return best\n",
    "A sweep line is a cursor moving across a calendar, counting how many meetings are open at each instant.",
    "A booking service merges overlapping maintenance windows and counts concurrent reservations. An off-by-one at equal timestamps double-books a room that frees at noon and is reserved at noon.",
    "queries are overlap, merge, or peak concurrency on a line",
    "the geometry is two-dimensional or the predicate is not an interval overlap",
    ["Sorting only by start and missing a nested interval.", "Using a half-open convention in one service and closed in another.", "Forgetting that a sweep's tie-break is part of the spec."],
)

add(
    "D02-T025",
    "A randomized algorithm draws bits to simplify a decision or to reach a good answer with high probability. A Las Vegas algorithm always returns a correct answer and bets on runtime. A Monte Carlo algorithm bets on correctness and is fast. Quicksort's random pivot and randomized hashing are the standard examples. The guarantee is a probability bound, not a promise about one unlucky draw.",
    ["Identify which quantity is random", "State whether the answer is always correct", "Bound the failure probability or the expected cost", "Re-run or amplify if the bound is too weak"],
    "treating one lucky sample as a proof, or shipping a Monte Carlo check that can accept a wrong answer with no amplification",
    "observed failure rate versus the published probability bound, over many seeds",
    "import random\n\ndef randomized_partition_pivot(n):\n    return random.randrange(n)\n",
    "Drawing a random pivot is shuffling the deck before you cut it, so an adversary cannot hand you the worst order every time.",
    "A load balancer that picks two random backends and keeps the shorter queue beats a single random pick. One unlucky sample is not a capacity plan.",
    "an adversary controls input order, or an expected-time bound is enough",
    "you need a worst-case latency for a tail SLO, unless you add a deterministic fallback",
    ["Using a seed that is constant in production.", "Confusing expected time with a p99 bound.", "Skipping amplification on a Monte Carlo predicate."],
)

add(
    "D02-T026",
    "Amortized analysis averages the cost of an operation over a sequence, so a rare expensive step can be charged to many cheap ones. Aggregate analysis divides total cost by the number of operations. The accounting method stores credit on objects. The potential method tracks a function of the whole structure. A dynamic array's doubling is the textbook case: most pushes are O(1), and the copy is paid for by the unused capacity.",
    ["Write the costly event and how often it happens", "Charge its cost to earlier cheap operations or to a potential", "Show the potential never goes negative", "State the amortized bound separately from the worst single call"],
    "using an amortized O(1) claim as a tail-latency SLO, then watching one resize stall a request",
    "the latency of the rare expensive call, not only the average over a benchmark that hides it",
    "class DynArray:\n    def __init__(self):\n        self._a = [None]\n        self.n = 0\n    def push(self, value):\n        if self.n == len(self._a):\n            self._a = self._a + [None] * len(self._a)\n        self._a[self.n] = value\n        self.n += 1\n",
    "Buying a stack of cups in bulk is expensive once, and each later coffee looks cheap if you spread that receipt across them.",
    "A log buffer that flushes every megabyte has a cheap append and a rare fsync. The SLO has to budget the flush, or a request that hits it times out.",
    "you can tolerate an occasional expensive operation and you need a bound on the sequence",
    "a single call has a hard deadline, in which case you need the worst-case cost or a background flush",
    ["Quoting amortized cost as worst-case latency.", "Forgetting that potential must stay non-negative.", "Resizing by one element and still claiming doubling's bound."],
)

add(
    "D02-T027",
    "Problem-solving patterns are reusable shapes: two pointers, sliding window, binary search on a predicate, monotonic stack, BFS for shortest unweighted paths, and checking edges before the happy path. A pattern is a hypothesis about the input's structure. Edge cases are empty input, one element, duplicates, overflow, and the off-by-one at the boundary.",
    ["Restate the input shape and the output", "Name the pattern and the property that justifies it", "Write the boundary tests before the implementation", "Compare against a slower oracle on tiny inputs"],
    "forcing a pattern onto an input that lacks the required property, then missing the empty or duplicate case",
    "a table of edge cases with expected outputs, including empty, one element, and the boundary index",
    "def binary_search(a, target):\n    lo, hi = 0, len(a)\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if a[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid\n    return lo if lo < len(a) and a[lo] == target else -1\n",
    "Patterns are tools on a bench. You pick the saw because the cut is straight, not because the saw is familiar.",
    "An interview or a production bugfix starts by listing empty input, duplicates, and integer overflow before optimizing the inner loop.",
    "the input really has the structure the pattern needs",
    "you have not named that structure yet, in which case a brute force oracle is the honest first step",
    ["Matching a problem to a pattern by keyword.", "Skipping the empty input.", "Optimizing before an oracle exists."],
)

add(
    "D03-T007",
    "Concurrency is dealing with multiple tasks that can be in progress at once, including by interleaving on one core. Parallelism is actually executing on more than one core at the same instant. You can have concurrent code that never runs in parallel, and parallel code that does not share state. The distinction decides whether a lock or a process boundary is the tool.",
    ["Classify the work as waiting or computing", "Decide if tasks share mutable state", "Pick interleaving or true parallel hardware", "Measure speedup against a single worker"],
    "adding threads to a CPU-bound Python workload and expecting parallelism from code the GIL serializes",
    "CPU time versus wall time, and whether throughput scales with core count",
    "import concurrent.futures\n\ndef classify(io_bound: bool, cores: int) -> str:\n    if io_bound:\n        return 'threads or async'\n    return f'processes up to {cores}'\n",
    "Concurrency is several conversations you switch between. Parallelism is several people talking at the same time.",
    "A web handler waiting on a database is concurrent I/O. A video transcode is parallel CPU. Mixing the two thread pools is how a service stalls both.",
    "you need to name whether the spare time is waiting or spare cores",
    "you use the words as synonyms and then pick the wrong pool",
    ["Equating async with parallel.", "Sizing a CPU pool to the number of database connections.", "Ignoring shared-state bugs because the machine has one core."],
)

add(
    "D03-T008",
    "A race condition is a bug whose outcome depends on the timing of unsynchronized accesses, at least one of which writes. The read-modify-write of a counter is the classic case: two threads read the same value and both write value plus one, so one increment disappears. Data races are the language-level version. Logical races can exist even with atomic stores if the invariant spans two variables.",
    ["Find the shared mutable location", "Name the interleaving that loses an update", "Make the critical sequence atomic", "Replay the interleaving under a test barrier"],
    "lost updates or torn reads that disappear when you add logging and change the timing",
    "a stress test that fails without the lock and passes with it, counted as lost increments",
    "import threading\ncounter = 0\nlock = threading.Lock()\n\ndef increment():\n    global counter\n    with lock:\n        counter += 1\n",
    "Two people editing the same line of a shared document without merging will overwrite each other.",
    "A balance update that reads a row, adds a deposit in the app, and writes the row back loses money when two deposits interleave. The fix is a single SQL update or a transaction, not a hope.",
    "two actors can touch the same mutable state",
    "the state is immutable or confined to one thread, so there is nothing to race",
    ["Adding a lock around only the write.", "Calling a bug a race without naming the interleaving.", "Using a lock in the app and a separate read-modify-write in SQL."],
)

add(
    "D03-T009",
    "A critical section is the stretch of code that must not interleave with another actor on the same data. Synchronization is the mechanism that enforces that exclusion or that orders two events. The section should be short. The invariant is whatever must be true before and after it, not the lock itself.",
    ["Name the invariant", "Shrink the code that must hold the lock", "Enter and leave on every path including errors", "Do not call out to the network while holding it"],
    "a lock that is held across a remote call, or an early return that skips the unlock",
    "lock hold time and the rate of lock-order waits",
    "lock = threading.Lock()\n\ndef transfer(src, dst, amount):\n    with lock:\n        if src.balance < amount:\n            return False\n        src.balance -= amount\n        dst.balance += amount\n        return True\n",
    "A fitting room is a critical section. The lock is the occupied sign. The invariant is that only one person is inside.",
    "A connection pool's checkout updates a free list. That update is the critical section. Health-checking a socket must happen outside the lock or every caller waits on the network.",
    "a data invariant spans more than one write",
    "you can use an atomic structure or a single database statement instead",
    ["Holding a lock during I/O.", "Synchronizing code instead of data.", "Forgetting the error path leaves the lock held."],
)

add(
    "D03-T010",
    "A mutex gives exclusive ownership of a critical section to one holder. A semaphore counts permits and can allow a fixed number of concurrent entrants. A read-write lock allows either many readers or one writer. None of them chooses lock order for you. A mutex is not a semaphore you happened to initialize to one if the API allows an extra release.",
    ["Pick exclusion, a counted permit, or reader sharing", "Name who acquires and who releases", "Bound the wait", "Detect misuse with ownership checks"],
    "a semaphore released once too often, or a writer starved by a continuous stream of readers",
    "wait time per acquire, permit count, and writer starvation time",
    "import threading\nmutex = threading.Lock()\nsemaphores = threading.Semaphore(4)\nrw = threading.RLock()\n",
    "A mutex is one bathroom key. A semaphore is a stack of four keys. A read-write lock is a library room that is either full of readers or closed for one writer.",
    "A pool of four outbound HTTP calls uses a semaphore of four. Using a mutex there serializes throughput. Using an unbounded thread per call exhausts file descriptors.",
    "you need exclusion, a concurrency cap, or shared readers with rare writers",
    "the resource is already serialized by the database or by a single-threaded event loop",
    ["Unlocking a mutex from another thread where the runtime forbids it.", "Using a read-write lock for a write-heavy map.", "Treating semaphore release as idempotent."],
)

add(
    "D03-T011",
    "A deadlock is a cycle of actors each waiting for a resource another holds. Prevention breaks one Coffman condition, usually by acquiring locks in a global order or by using try-lock with backoff. Detection waits for a cycle in the wait-for graph and aborts one waiter. Recovery rolls back the victim's work. A lock timeout is a crude detector, not a proof you are deadlock-free.",
    ["List every lock a request can take", "Impose one global order", "Avoid holding a lock while waiting for another unordered lock", "On a cycle, abort one waiter and retry at the boundary"],
    "two transactions lock rows in opposite orders and wait forever, or a timeout retry storms the database",
    "lock-wait timeouts and deadlock rollback counters from the database",
    "def ordered(locks):\n    return sorted(locks, key=id)\n",
    "Two people in a hallway each step aside in a different direction and block each other. Agreeing on one direction prevents it.",
    "Transferring money from account A to B and from B to A deadlocks if each transaction locks the source first. Locking by account id order removes the cycle.",
    "a request can hold one lock and wait for another",
    "you can take all resources in one ordered batch, or use a single lock",
    ["Detecting deadlocks in production instead of ordering locks.", "Retrying a deadlock without a bound.", "Locking in UI or map iteration order."],
)

add(
    "D03-T012",
    "Starvation means a ready actor never runs because others always win the scheduler or the lock. A livelock means actors are busy responding to each other and still make no progress, often because both sides retry in the same pattern. Fairness, queues, and randomized backoff are the usual fixes. A timeout that always expires together can turn a retry into a livelock.",
    ["Name who is ready but not progressing", "See whether they are blocked or spinning", "Add fairness or jitter", "Cap retries and shed load"],
    "a low-priority queue that never drains, or two services retrying in lockstep and both failing",
    "age of the oldest queued item, and retry correlation across instances",
    "import random, time\n\ndef backoff(attempt):\n    base = min(2 ** attempt, 30)\n    return base / 2 + random.random() * base / 2\n",
    "Starvation is the person who never gets the microphone because others talk first. Livelock is two people sidestepping forever in a doorway.",
    "A writer thread starved by readers on an unfair read-write lock, or two consumers nacking and requeueing the same poison message as fast as they can.",
    "scheduling or lock admission can prefer the same waiters forever",
    "the system is merely slow, which is latency, not starvation",
    ["Adding priority without an aging rule.", "Retrying immediately on contention.", "Calling a saturated thread pool starvation when the queue is just unbounded and growing."],
)

add(
    "D03-T013",
    "An atomic operation completes as a single step with respect to other threads. Compare-and-swap takes an address, an expected value, and a new value, and updates the address only if it still holds the expected value. It is the building block of lock-free stacks and counters. ABA is the bug where the value changes from A to B and back to A, so a CAS succeeds and misses the intervening mutation.",
    ["Read the current value", "Compute the new value locally", "CAS expected to new", "Retry if another writer won"],
    "ABA on a pointer, or a CAS loop that burns a core under contention",
    "CAS failure rate and the number of retries per successful update",
    "def cas_loop(get, cas, delta):\n    while True:\n        cur = get()\n        if cas(cur, cur + delta):\n            return cur + delta\n",
    "CAS is checking that a luggage tag still shows your name before you replace it. If someone swapped the bag and put your tag back, you are fooled. That is ABA.",
    "A lock-free request counter increments with an atomic add. A lock-free stack that reuses nodes without a version tag can pop the wrong generation.",
    "the update is a single word and the critical section is tiny",
    "the invariant spans two words, unless you have a double-width CAS or a lock",
    ["Assuming CAS of a pointer is safe without a generation.", "Spinning without backoff on a hot counter.", "Using atomicity for one field and forgetting the neighboring field."],
)

add(
    "D03-T014",
    "Virtual memory gives each process its own address space. The CPU translates virtual pages to physical frames through page tables. The process cannot name another process's memory except through an explicit shared mapping. Overcommit and swap let the OS promise more virtual memory than RAM, and then the promise fails under pressure.",
    ["Allocate virtual address space", "Fault a page in on first touch", "Map it to a physical frame", "Reclaim a frame when RAM is scarce"],
    "the OOM killer, or latency spikes when anonymous memory is swapped out",
    "major page faults, swap in/out, and RSS versus the cgroup limit",
    "# unexecuted: inspect a process map\n# ps -o pid,rss,vsz -p <pid>\n",
    "Virtual memory is a set of named mailboxes that the post office remaps onto a smaller wall of real boxes.",
    "A JVM or a Python process whose RSS crosses a container limit is killed even though virtual size looked fine for weeks. The metric that matters is resident set and the cgroup cap.",
    "you are explaining a crash, a leak, or a container limit",
    "you only needed an application-level cache bound, which virtual memory will not enforce for you",
    ["Treating virtual size as RAM used.", "Disabling swap and assuming latency can never spike.", "Ignoring the container limit and looking only at the host."],
    lang="text",
)

add(
    "D03-T015",
    "Paging splits address space into fixed-size pages, usually 4 KiB, and maps them independently. Segmentation uses variable-sized logical segments. Modern general-purpose systems are paged. Huge pages reduce TLB misses for large contiguous heaps. Internal fragmentation is the unused tail of a page. External fragmentation is the historical segment problem of holes that are too small.",
    ["Split the address space into pages", "Translate through a page table cached by the TLB", "Pick a page size for TLB reach versus waste", "Compact or use huge pages only for large stable regions"],
    "TLB shootdowns and extra page-table memory after turning on huge pages for a tiny, short-lived allocation",
    "TLB miss rate and the fraction of anonymous memory backed by huge pages",
    "# page size is a kernel fact, not an application toggle in this snippet\nPAGE = 4096\ndef pages_for(nbytes):\n    return (nbytes + PAGE - 1) // PAGE\n",
    "Paging is graph paper. Segmentation is custom-length shelves. Graph paper wastes the last cell of a short line and never needs to slide shelves together.",
    "A database buffer pool sized to a multiple of the huge-page size avoids fragmenting the TLB. A service that mmaps millions of tiny files should stay on base pages.",
    "you are sizing memory or explaining TLB cost",
    "you are picking a data structure, where page size is a constant you should not retune per request",
    ["Assuming the application page size is the disk block size.", "Enabling transparent huge pages on a latency-sensitive allocator without measuring stalls.", "Confusing fragmentation with a leak."],
)

add(
    "D03-T016",
    "A page fault is a trap when a virtual page has no present mapping. A minor fault fills a page already in memory, such as a copy-on-write after fork. A major fault reads from disk or swap. The handler finds a frame, fills it, updates the page table, and resumes the instruction. A storm of major faults means the working set does not fit.",
    ["Touch a missing page", "Trap into the kernel", "Fill a frame from zero, cache, or disk", "Resume the faulting instruction"],
    "a latency spike or an OOM while the process allocates faster than faults can be satisfied",
    "major faults per second and the time spent in iowait during the spike",
    "def working_set_warning(major_faults, limit):\n    return major_faults > limit\n",
    "A page fault is reaching for a book and finding a placeholder card. A minor fault means the book is already in the building. A major fault means someone has to fetch it from the warehouse.",
    "A deploy that forks a large Python process pays copy-on-write minor faults as children dirty pages. A cache bigger than RAM pays major faults and the request latency falls apart.",
    "you are explaining a stall at first touch or under memory pressure",
    "the stall is a lock or a network call, which will not show up as a major fault",
    ["Calling every fault a disk read.", "Pre-touching a multi-gigabyte cache on the request path.", "Ignoring copy-on-write after fork."],
)

add(
    "D03-T017",
    "A file descriptor is a small integer in a process that names an open file, socket, or pipe in the kernel's file table. The descriptor points at a description that holds the offset and status flags. Two descriptors can share one offset, which is why dup changes both reads. File systems map names to inodes and inodes to blocks. Closing a descriptor releases the process's reference, not necessarily the underlying inode if another process still holds it.",
    ["Open a path or a socket and receive a descriptor", "Read or write through the kernel file table", "Share carefully if you dup or pass the descriptor to a child", "Close it on every path, including errors"],
    "descriptor exhaustion, a leaked socket, or two threads sharing one file offset and corrupting a read",
    "open file count against ulimit, and the identity of descriptors that survive a request",
    "def leaky_example():\n    # unexecuted shape: always close\n    f = open('data.txt', 'rb')\n    try:\n        return f.read(8)\n    finally:\n        f.close()\n",
    "A file descriptor is a coat-check ticket. Losing the ticket leaks the coat from your point of view. Two people holding tickets to the same coat share one hanger position.",
    "A service that opens a log file per request eventually hits EMFILE. The fix is one shared logger, not a higher ulimit alone.",
    "you are debugging leaks, accidental sharing, or filesystem behavior",
    "you needed an application buffer, which is not a descriptor",
    ["Raising the ulimit without finding the leak.", "Assuming close is optional because the process will exit.", "Sharing one file object across threads without a position lock."],
)

add(
    "D03-T018",
    "I/O buffering gathers bytes in memory so a device is touched in larger chunks. User-space stdio buffers, the kernel page cache, and a disk controller cache are different layers. A write can sit in a buffer and not be durable. Flush pushes the buffer toward the device. fsync asks the device to persist. Line buffering and full buffering change when a log line becomes visible.",
    ["Write into a buffer", "Flush when the buffer fills or the API says so", "Sync if durability is required", "Size the buffer against latency and syscall rate"],
    "a log line missing after a crash because it was still in a user-space buffer, or a tiny write syscall per record",
    "write syscall rate, flush latency, and whether a crash test still contains the last record",
    "def write_record(f, line):\n    f.write(line + '\\n')\n    f.flush()\n",
    "Buffering is stacking letters until the envelope is worth a trip to the mailbox. Flush is walking to the mailbox. It is not the same as the post office promising the letter is in the vault.",
    "An audit log that write()s without flush or fsync loses the last transactions on a kill -9. A payment ledger cannot treat a buffered write as a commit.",
    "you need fewer syscalls or you need to define durability",
    "you need every record durable before the acknowledgment, unless you also sync",
    ["Confusing flush with fsync.", "Disabling buffering and then wondering why the disk is saturated.", "Assuming the page cache is durable."],
)

add(
    "D03-T019",
    "Blocking I/O puts the calling thread to sleep until the kernel finishes the operation. Non-blocking I/O returns immediately with a partial result or EAGAIN, and the caller polls or waits in an event demultiplexer. Non-blocking is not faster bytes. It lets one thread wait for many sockets. A blocking call hidden inside a non-blocking loop stalls every connection on that thread.",
    ["Set the socket non-blocking or use a blocking pool on purpose", "Attempt the read or write", "If the kernel would wait, register interest and yield", "Resume when the demultiplexer says the socket is ready"],
    "a DNS lookup or a disk read that blocks the event thread and stalls every other connection",
    "event-loop lag and the number of sockets handled per thread",
    "def on_readable(conn, buf):\n    chunk = conn.recv(4096)\n    if chunk == b'':\n        return 'closed'\n    buf.extend(chunk)\n    return 'again' if len(chunk) == 4096 else 'done'\n",
    "Blocking is standing at the counter until your order is ready. Non-blocking is taking a buzzer and talking to other customers until it rings.",
    "A Node or Java NIO server handles many idle sockets on one thread until a library call does a blocking file read. Event-loop lag jumps and health checks fail.",
    "many connections are idle most of the time",
    "the work is CPU-heavy, where a thread per core is the honest model",
    ["Calling a blocking library from the event thread.", "Equating non-blocking with parallel.", "Busy-polling instead of waiting in the demultiplexer."],
)

add(
    "D03-T020",
    "Synchronous execution means the caller waits for the result before continuing. Asynchronous execution means the caller starts the work and resumes on a callback, future, or later poll. Async does not imply another CPU. A synchronous API can wrap asynchronous machinery, and an async keyword can still block if the callee does. The contract that matters is whether the caller’s thread is occupied.",
    ["Start the operation", "Decide whether the caller waits", "Represent the pending result", "Resume exactly once with a value or an error"],
    "an async function that blocks, or a callback that runs twice",
    "thread occupancy during the wait, and duplicate completion count",
    "import asyncio\n\nasync def fetch(n):\n    await asyncio.sleep(0)  # yields; a real service awaits I/O\n    return n\n",
    "Synchronous is waiting on the phone. Asynchronous is asking someone to call you back. If they still make you stand there, the call was not asynchronous.",
    "A request handler marked async that then calls a blocking database driver occupies the event loop for the whole query. The fix is a real async driver or a bounded worker pool.",
    "the caller has other useful work during the wait",
    "the operation is CPU-bound and short, where the callback machinery costs more than the work",
    ["Assuming async means parallel.", "Completing a future twice.", "Swallowing the error on the callback path."],
)

add(
    "D03-T021",
    "An event loop waits for readiness events, then runs the callbacks that are already runnable, then repeats. It is one thread unless you add workers. Phases typically separate timers, pending I/O callbacks, and idle work. A long callback delays every timer. The loop is a scheduler for tasks, not a thread pool.",
    ["Wait for I/O or timer readiness", "Queue the callbacks that became runnable", "Run each callback to completion", "Schedule workers only for CPU-bound or blocking calls"],
    "one callback that parses a huge payload and delays every other timer on the loop",
    "event-loop lag, the delay between a timer's due time and its actual run",
    "def loop(ready_callbacks):\n    for cb in ready_callbacks:\n        cb()\n",
    "An event loop is a single clerk who only talks to the person whose number is lit, and who must finish that conversation before looking at the board again.",
    "A Node process serving HTTP stalls because a JSON parse of a multi-megabyte body runs on the loop. The health check, which is a timer, fires late.",
    "the workload is many small I/O tasks",
    "a callback does unbounded CPU work",
    ["Offloading nothing and hoping the loop scales.", "Sharing the loop across a blocking ORM.", "Using loop lag as a vanity metric and not paging on it."],
)

add(
    "D03-T022",
    "Signals are asynchronous notifications to a process, such as SIGTERM for a polite stop and SIGKILL which cannot be caught. Handlers must be async-signal-safe. Inter-process communication moves bytes or messages between processes: pipes, Unix sockets, shared memory, and message queues. Shared memory still needs synchronization. A pipe is a byte stream with a buffer and blocking behavior when it fills.",
    ["Choose a signal for lifecycle or a channel for data", "Install a handler that only sets a flag", "Do the real work on the normal control path", "Bound the IPC buffer so a slow reader applies backpressure"],
    "doing malloc or logging inside a signal handler, or a full pipe that deadlocks a writer the reader is waiting on",
    "time to notice SIGTERM and the depth of the IPC buffer",
    "import signal\nstop = False\n\ndef handle(signum, frame):\n    global stop\n    stop = True\n\nsignal.signal(signal.SIGTERM, handle)\n",
    "A signal is someone tapping your shoulder. IPC is passing a note. The tap must stay tiny. The note can be long, but the mailbox can fill up.",
    "A container entrypoint that traps SIGTERM and finishes the current request drains cleanly. A handler that flushes logs in the signal context deadlocks on the allocator.",
    "you need process lifecycle or a simple byte channel between processes",
    "you needed a durable queue, which a pipe is not",
    ["Catching SIGKILL.", "Doing non-trivial work in the handler.", "Using shared memory without a protocol for who writes."],
)

add(
    "D03-T023",
    "Linux process and networking commands inspect what the kernel is already doing. ps and top show processes. ss shows sockets. lsof shows descriptors. strace shows syscalls. tcpdump shows packets. These tools read state. They are not a substitute for application metrics, and tcpdump on a busy host can drop packets or cost CPU.",
    ["Start from the symptom, not from a favorite tool", "Identify the process and its sockets", "Trace only if the metric is not enough", "Stop the capture when you have the evidence"],
    "running tcpdump or strace in production without a filter and making the outage worse",
    "the specific socket state or syscall error that matches the client symptom",
    "# unexecuted examples, run only against a process you own\n# ss -lntp\n# ps -o pid,stat,wchan,cmd -p <pid>\n",
    "These commands are looking at the kitchen board, the order tickets, and the door, not redesigning the restaurant.",
    "A service that is up but not accepting connections shows a listen socket in the wrong state or a process stuck in a syscall. ss answers that faster than another deploy.",
    "you are on a host and need kernel-visible evidence",
    "the question is an application invariant, which belongs in logs and traces",
    ["Pasting strace of a production payment worker into a ticket with secrets in the arguments.", "Capturing all packets on a busy NIC.", "Killing a process to 'see if it comes back' before you record its state."],
    lang="text",
)

add(
    "D03-T024",
    "Resource limits cap what a process can consume: open files, address space, CPU time, and process count. cgroups on Linux group processes and apply the container's real limit. Isolation reduces what a fault can touch: namespaces, separate users, and read-only filesystems. A limit that is hit should fail the allocation, not stall the host.",
    ["Set the limit at the boundary you can enforce", "Measure usage against that limit", "Fail the caller when the limit is reached", "Keep a neighbor from eating the host"],
    "a container with no memory limit taking the node down, or a file-descriptor limit so low that health checks cannot open a socket",
    "cgroup memory.current versus memory.max, and the rate of EMFILE or OOM kills",
    "def over_budget(used, limit):\n    return used > limit\n",
    "A limit is a fuse. Isolation is a separate apartment. The fuse trips one circuit. The apartment wall stops the fire next door.",
    "Kubernetes memory limits are cgroup limits. A pod that exceeds it is OOMKilled. A pod with only a request and no limit can still hurt the node.",
    "you are drawing a tenant or a container boundary",
    "you are micro-optimizing a function, where a limit will not make it faster",
    ["Setting a request and calling it a limit.", "Raising nofile without a leak fix.", "Running everything as root in one namespace."],
)

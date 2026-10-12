# Generates D02-T001..D02-T014 artifacts. Run: python render_d02.py
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def A(topic):
    tid, name, sub = topic["id"], topic["name"], topic["subdomain"]
    return f"""# {tid} — {name}

Topic ID: `{tid}`
Domain: Data Structures and Algorithms
Subdomain: {sub}
Importance: core
Complexity: intermediate
Dependencies: {", ".join(f"`{d}`" for d in topic["deps"])}
Execution status of the code in section F: {topic.get("code_run", "unexecuted")}

## A. Topic Overview

{topic["overview"]}

Prerequisites: {", ".join(f"`{d}`" for d in topic["deps"])}. This topic supports {", ".join(f"`{n}`" for n in topic["next"])} and later graph or systems topics.

## B. First-Principles Explanation

{topic["first_principles"]}

Terms: **{topic.get("terms", "asymptotic cost, auxiliary space, input size n")}**.

## C. Internal Working and Architecture

{topic["internal"]}

Dominant time: {topic["time"]}. Dominant auxiliary space: {topic["space"]}.

## D. Diagrams and Visual Models

```mermaid
{topic["mermaid"]}
```

{topic["diagram_caption"]}

## E. Examples and Analogies

{topic["examples"]}

Edge cases: {topic["edge"]}.

## F. Code Examples

File: `examples/{topic["code_file"]}`

Dependencies: Python 3 standard library only.

```python
{topic["code"]}
```

How to run: `python examples/{topic["code_file"]}` from `EXERCISES/examples/`.

Expected output: `{topic.get("expected_out", "ok")}`

{topic["code_notes"]}

## G. Practical Backend Application

{topic["backend"]}

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
{topic["table_rows"]}

## I. Common Mistakes and Misconceptions

{topic["mistakes"]}

## J. Debugging and Troubleshooting

{topic["debug"]}

## K. Interview Preparation

### Beginner

{topic["k_beginner"]}

### Intermediate

{topic["k_intermediate"]}

### Advanced

{topic["k_advanced"]}

### Scenarios

{topic["k_scenario"]}

### Follow-ups

{topic["k_followup"]}

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`. Try these before opening that file.

### Exercise 1 — implementation

{topic["ex1"]}

### Exercise 2 — debugging

{topic["ex2"]}

### Exercise 3 — trade-off

{topic["ex3"]}

## M. Revision Notes

{topic["revision"]}

## N. Related Topics

Understand this before: {", ".join(f"`{d}`" for d in topic["deps"])}.

This topic supports: {", ".join(f"`{n}`" for n in topic["next"])}.

Often confused with: {topic["confused"]}.

Interviewers combine this with {", ".join(f"`{r}`" for r in topic["related"])}.

## O. Completion Criteria

{topic["completion"]}
"""


def qa_block(items):
    out = []
    for i, (q, a) in enumerate(items, 1):
        out.append(f"#### Q{i}. {q}\n\n**Answer:** {a}\n")
    return "\n".join(out)


def mk_k(topic):
    def pack(level, qs):
        items = []
        for q in qs:
            a = (
                f"{topic['k_core']} "
                f"For {topic['name']}, typical bounds are {topic['time']} time and {topic['space']} space. "
                f"{topic['backend_short']} "
                f"Watch edge cases: {topic['edge_short']}."
            )
            items.append((q, a))
        return qa_block(items)

    b = [
        f"What problem does {topic['name']} solve in backend engineering?",
        f"How do you define input size n for {topic['subdomain'].lower()}?",
        f"What is the difference between time and space cost here?",
        f"Why do we ignore constant factors in asymptotic notation for this topic?",
        f"Name one operation that is cheap and one that is expensive in this structure.",
    ]
    i = [
        f"State the average and worst-case complexity for the main operations.",
        f"How would you justify choosing this structure in a design review?",
        f"What changes if data no longer fits in memory?",
        f"How does concurrency affect the complexity story?",
        f"How do you test performance regressions for this component?",
    ]
    a = [
        f"When is the 'textbook' complexity misleading in production?",
        f"How do cache locality and allocation affect real runtime?",
        f"Compare this approach to the next topic in the curriculum.",
        f"What security or abuse patterns change effective n?",
        f"How would you document complexity in an OpenAPI or ADR?",
    ]
    s = [
        f"Latency spikes when traffic doubles but CPU is only 60%. What do you measure first?",
        f"A batch job OOMs on a larger tenant. Which space term grew?",
        f"Two services disagree on timeout budgets for the same endpoint.",
        f"An attacker sends inputs that trigger worst-case behavior.",
        f"You must shave 100ms off a hot path without new hardware.",
    ]
    f = [
        "How does this connect to database indexing?",
        "How does this connect to caching layers?",
        "What monitoring proves your complexity assumption?",
    ]
    topic["k_beginner"] = pack("b", b)
    topic["k_intermediate"] = pack("i", i)
    topic["k_advanced"] = pack("a", a)
    topic["k_scenario"] = pack("s", s)
    topic["k_followup"] = pack("f", f)


TOPICS = []

def T(**kw):
    TOPICS.append(kw)

# D02-T001
T(
    id="D02-T001", slug="d02-t001-time-and-space-complexity",
    name="Time and space complexity", subdomain="Time and space complexity",
    deps=["D01-T001", "D01-T002"], next=["D02-T002"], related=["D02-T015", "D13-T003"],
    time="O(n) for a single pass; O(n^2) when every pair is compared",
    space="O(1) extra for in-place scans; O(n) when every element is stored in a new structure",
    k_core="Complexity describes how resource use scales when input size n grows, not the exact millisecond on one machine.",
    backend_short="Profile hot handlers and size n by records per request, queue depth, or bytes parsed.",
    edge_short="empty input, n=1, duplicated work hidden inside library calls",
    overview="Time complexity counts the dominant steps as input grows. Space complexity counts extra memory beyond the input. Together they predict whether a service survives 10x traffic without a rewrite.",
    first_principles="A CPU executes a bounded number of instructions per second. An algorithm that doubles work when input doubles is linear. One that compares every pair is quadratic. Memory is similar: an auxiliary array proportional to n adds O(n) space even if the algorithm is a single pass over the input.",
    internal="Count the innermost loop that runs the most often. Drop lower-order terms and constants. For space, count allocations that survive across iterations (hash tables, output buffers), not loop indices.",
    mermaid="""flowchart TD
  n[InputSizeN]
  timeCount[CountStepsVsN]
  spaceCount[PeakAuxMemory]
  report[AsymptoticClass]
  n --> timeCount
  n --> spaceCount
  timeCount --> report
  spaceCount --> report""",
    diagram_caption="Read left to right: measure both time and space, then classify growth.",
    examples="Analogy: complexity is the slope of a hill, not your walking speed today. Backend: scanning all orders per checkout is O(orders); indexing by user id turns repeat lookups into O(1) average with a hash map (`D02-T006`).",
    edge="n=0, n=1, hidden O(n) copies when slicing strings or arrays, and log factors from balanced trees.",
    code_file="d02_t001_complexity.py",
    code='''def count_distinct(events: list[str]) -> int:\n    seen: set[str] = set()\n    for e in events:\n        seen.add(e)\n    return len(seen)\n\n\ndef has_pair_duplicate(nums: list[int]) -> bool:\n    n = len(nums)\n    for i in range(n):\n        for j in range(i + 1, n):\n            if nums[i] == nums[j]:\n                return True\n    return False\n\n\nif __name__ == "__main__":\n    assert count_distinct(["a","b","a"]) == 2\n    assert has_pair_duplicate([1,2,2]) is True\n    print("ok")''',
    code_run="unexecuted",
    code_notes="`count_distinct` is O(n) time and O(n) space. `has_pair_duplicate` is O(n^2) time and O(1) extra space. Prefer the set when n can be large.",
    backend="Size endpoints by expected n: batch exports, fan-out queries, and JSON array length. Set timeouts from measured growth, not gut feel. Document Big-O in ADRs when choosing nested loops versus indexing.",
    table_rows="""| Single pass | Simple, cache-friendly | Cannot answer pair questions | Streaming metrics | Need all-pairs |
| Hash index | O(1) average lookups | O(n) memory | Hot keys | Memory cap |
| Nested loops | No extra memory | O(n^2) time | Tiny n only | Production lists |
| Sort then scan | O(n log n) | Mutates order | Order statistics | Need stable order |""",
    mistakes="- Claiming O(1) because the loop runs 100 times regardless of n.\n- Ignoring space for 'small' caches that grow with tenants.\n- Using wall clock on cold JVM as proof of O(log n).",
    debug="Symptoms: CPU pegged while DB is idle (CPU-bound algorithm), or GC churn (too many allocations). Capture n from logs, reproduce offline, replace inner loop with map or sort.",
    ex1="Implement `count_distinct` and `has_pair_duplicate` and document time/space for each in comments.",
    ex2="Endpoint times out at n=8000 with nested loops over the JSON array. Name complexity and one fix.",
    ex3="Choose between recomputing a report O(n) per request versus caching O(n) memory per tenant.",
    ex2_acc="Acceptance: identify O(n^2), propose hash-based dedup O(n) or sort+scan O(n log n).",
    ex3_acc="Acceptance: discuss hit rate, staleness, memory cap, eviction.",
    revision="- Count dominant loops.\n- Space includes auxiliary structures.\n- Constants matter in production; classes matter for scaling.",
    confused="wall-clock profiling versus asymptotic class",
    completion="- State time and space for a given code snippet.\n- Explain why nested loops on request arrays are dangerous.\n- Pick a structure given n and memory budget.",
)

T(id="D02-T002", slug="d02-t002-big-o-big-theta-big-omega", name="Big-O, Big-Theta, Big-Omega", subdomain="Big-O, Big-Theta, Big-Omega",
  deps=["D02-T001", "D01-T001", "D01-T002"], next=["D02-T003"], related=["D02-T001", "D02-T015"],
  time="O(log n) search on sorted data; Theta(n) when every element must be touched",
  space="O(1) for iterative binary search; O(log n) call stack for recursive divide",
  k_core="Big-O is an upper bound, Big-Omega a lower bound, and Big-Theta a tight bound when both match.",
  backend_short="SLAs should cite measured percentiles plus the asymptotic class of the hot path.",
  edge_short="best-case hits first element, adversarial quicksort, hash table rehash spikes",
  overview="Asymptotic notation describes growth without pinning constants. Big-O answers 'will it blow up'; Big-Theta answers 'does it always pay n'; Big-Omega answers 'can it be faster than n'. Interviews test whether you quote the right bound for the question asked.",
  first_principles="Functions f(n) and g(n) compare through limits and inequalities. O(g) hides constants and lower-order terms. Theta requires matching upper and lower polynomials. Omega captures best-case floors when inputs are friendly.",
  internal="When analyzing code, identify the loop whose iteration count scales with n. Recurrence T(n)=T(n/2)+O(1) yields Theta(log n). Nested loops often yield Theta(n^2). Amortized bounds average expensive rare steps across many cheap ones.",
  mermaid="""flowchart LR
  algo[Algorithm]
  bigO[BigO_Upper]
  theta[BigTheta_Tight]
  omega[BigOmega_Lower]
  algo --> bigO
  algo --> theta
  algo --> omega""",
  diagram_caption="One algorithm can have different bounds depending on which question you ask.",
  examples="Saying 'sort is O(n log n)' is an upper bound for comparison sorts. Saying 'must read every byte' is Omega(n) for any correct parser. Hash map insert is O(1) amortized but O(n) worst case when the table rehashes.",
  edge="Duplicate keys, already sorted input, empty graph, single vertex.",
  code_file="d02_t002_bounds.py",
  code='''def linear_find(a: list[int], x: int) -> int:\n    for i, v in enumerate(a):\n        if v == x:\n            return i\n    return -1\n\n\ndef binary_find(a: list[int], x: int) -> int:\n    lo, hi = 0, len(a) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if a[mid] == x:\n            return mid\n        if a[mid] < x:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return -1''',
  code_notes="Linear search is O(n) worst case, Omega(1) best. Binary search on sorted arrays is O(log n) worst case. Neither uses extra space beyond indices.",
  backend="Publish Big-O of public batch endpoints. Pair with p99 latency because O(n) with a tiny constant can beat O(log n) with huge constants for small n.",
  table_rows="""| Big-O only | Easy to communicate | Hides best case | Capacity planning | Tight SLAs on best case |
| Big-Theta | Honest typical cost | Harder to prove | Must-touch-all-input | Cache hits dominate |
| Amortized | Models real structures | Worst spike still exists | Hash tables, vectors | Real-time hard limits |""",
  mistakes="- Using O for both upper and exact cost.\n- Forgetting amortized versus worst for hash maps.\n- Claiming O(log n) without sorted precondition.",
  debug="If latency is flat while n grows, you are not on the Theta(n) path—cache, index, or early exit dominates. Capture distribution of n.",
  ex1="Argue bounds for `linear_find` and `binary_find` in comments.",
  ex2="Team says endpoint is O(n) but p99 flat. Explain notation mismatch.",
  ex3="Document Theta versus O for a full-table scan versus indexed lookup.",
  ex2_acc="Acceptance: distinguish worst-case class from cached/indexed typical path; mention measurement.",
  ex3_acc="Acceptance: scan is Theta(n) rows; index lookup O(log n) pages with O(1) hash if in memory.",
  revision="- O upper, Omega lower, Theta tight.\n- State preconditions (sorted, hash load).\n- Amortized != worst case.",
  confused="average case versus amortized",
  completion="- Give O, Omega, and Theta where applicable.\n- Explain flat p99 with growing n.\n- Write bounds in an ADR paragraph.")

T(id="D02-T003", slug="d02-t003-arrays-and-strings", name="Arrays and strings", subdomain="Arrays and strings",
  deps=["D02-T002", "D02-T001", "D01-T001", "D01-T002"], next=["D02-T004"], related=["D02-T006", "D06-T005"],
  time="O(1) index access; O(n) full scan; O(n) or O(n+m) concatenation depending on immutability",
  space="O(1) in-place index; O(n) when copying for immutable strings",
  k_core="Arrays offer contiguous O(1) random access; strings are sequences with encoding and immutability rules that affect copies.",
  backend_short="Parsing HTTP bodies and CSV rows is linear in bytes; repeated concatenation in loops can become quadratic.",
  edge_short="UTF-8 multibyte chars, empty string, slicing sharing versus copy",
  overview="Arrays and strings are the default carriers for request payloads, log lines, and columnar batches. Knowing when access is O(1) and when a 'small' string operation allocates O(n) prevents surprise latency in parsers and serializers.",
  first_principles="Contiguous memory lets address arithmetic implement index in O(1). Variable-length strings track length and encoding. Immutable strings mean each concat may allocate a new buffer of size sum of parts.",
  internal="Dynamic arrays over-allocate capacity so append is amortized O(1). String builders batch writes. Slicing in Python creates views or copies depending on type; in Java `substring` historically copied.",
  mermaid="""flowchart TD
  bytes[ByteBuffer]
  index[O1_RandomAccess]
  scan[On_FullScan]
  concat[Concat_Cost]
  bytes --> index
  bytes --> scan
  bytes --> concat""",
  diagram_caption="Random access is cheap; whole-buffer work is linear.",
  examples="Checking JWT segment length is O(1) per segment but O(n) over the token. Building SQL with `+=` in a loop is O(n^2) total characters moved.",
  edge="Surrogate pairs, null bytes in binary, out-of-range index, immutability causing hidden copies.",
  code_file="d02_t003_strings.py",
  code='''def join_fields(fields: list[str]) -> str:\n    return ",".join(fields)\n\n\ndef bad_join(fields: list[str]) -> str:\n    out = ""\n    for f in fields:\n        out += f + ","\n    return out.rstrip(",")''',
  code_notes="`join` is O(total chars). `bad_join` is quadratic in field count for large lists. Use builders for hot paths.",
  backend="Validate max body size before O(n) parse. Stream large uploads instead of `read()` entire file. Prefer views into buffers for metrics labels.",
  table_rows="""| Contiguous array | Cache-friendly scans | Resize cost | Column batches | Sparse maps |
| Immutable string | Safe sharing | Concat cost | HTTP headers | Hot loop concat |
| StringBuilder | O(n) build | Mutable buffer | Log assembly | Concurrent sharing |""",
  mistakes="- O(n^2) string concat in tight loops.\n- Treating UTF-8 byte length as char count.\n- Assuming slice is always O(1) without allocation.",
  debug="Profile allocations on parse path. Compare `join` versus `+=`. Log payload bytes, not char count, for limits.",
  ex1="Rewrite `bad_join` to O(n) total using `join` or `io.StringIO`.",
  ex2="API CPU rises with log line length even for constant QPS—find the quadratic pattern.",
  ex3="Choose streaming parser versus load-all for 500MB CSV upload.",
  ex2_acc="Acceptance: identify repeated concat or regex recompile per line.",
  ex3_acc="Acceptance: stream O(1) memory per row window versus O(file) RAM.",
  revision="- Index O(1); scan O(n).\n- Immutable concat may copy.\n- Bound input bytes early.",
  confused="character versus byte length",
  completion="- Analyze concat loop cost.\n- State bounds for scan and index.\n- Pick streaming versus buffer.")

T(id="D02-T004", slug="d02-t004-linked-lists", name="Linked lists", subdomain="Linked lists",
  deps=["D02-T003", "D02-T001", "D01-T001", "D01-T002"], next=["D02-T005"], related=["D02-T005", "D02-T007"],
  time="O(1) insert/delete at known node with pointer; O(n) search by value",
  space="O(n) nodes plus pointer overhead per element",
  k_core="Linked lists trade O(1) structural edits at a pointer for O(n) random access and poor cache locality.",
  backend_short="Rare in hot data paths; appear in LRU implementations, work queues, and lock-free structures.",
  edge_short="losing head pointer, cycles in buggy code, dummy head sentinel",
  overview="Singly and doubly linked lists connect nodes through pointers. They shine when insertion order matters and you already hold a node reference. They fail interviews when used instead of arrays for random access workloads.",
  first_principles="Each node stores payload and next (and prev for doubly). Traversal follows pointers; no base+offset arithmetic for i-th element without walking i steps.",
  internal="Allocator churn per node hurts cache. Dummy head simplifies insert/delete. Floyd cycle detection finds loops in O(n) time O(1) space.",
  mermaid="""flowchart LR
  head[Head]
  n1[Node1]
  n2[Node2]
  n3[Node3]
  head --> n1 --> n2 --> n3""",
  diagram_caption="Reach the i-th element by walking i links.",
  examples="LRU cache combines hash map with doubly linked list for O(1) move-to-front. Middleware chains sometimes use linked handlers.",
  edge="Single-node list, insert at tail without tail pointer is O(n), concurrent updates need locks.",
  code_file="d02_t004_list.py",
  code='''class Node:\n    def __init__(self, val: int, nxt=None):\n        self.val = val\n        self.nxt = nxt\n\n\ndef prepend(head: Node | None, val: int) -> Node:\n    return Node(val, head)\n\n\ndef find(head: Node | None, target: int) -> Node | None:\n    cur = head\n    while cur:\n        if cur.val == target:\n            return cur\n        cur = cur.nxt\n    return None''',
  code_notes="`prepend` is O(1). `find` is O(n). No extra space beyond pointers.",
  backend="Prefer dynamic arrays or deques unless you need stable iterators across inserts. Document when LRU list is protected by a lock.",
  table_rows="""| Singly linked | Low memory per node | No backward walk | Stack-like prepend | Random access |
| Doubly linked | O(1) remove node | Extra pointer | LRU caches | Memory-tight arrays |
| Array list | O(1) index | O(n) middle insert | Default choice | Frequent middle insert with iterator |""",
  mistakes="- Using list for binary search.\n- Forgetting tail pointer costs O(n) append.\n- Creating cycles when splicing.",
  debug="CPU high with small n—pointer chasing misses cache. Use array if indexed.",
  ex1="Implement prepend and find; state complexities.",
  ex2="LRU misses become slow—explain list+map interaction.",
  ex3="Array versus linked list for a job queue with only push/pop ends.",
  ex2_acc="Acceptance: map gives node pointer; list splices O(1); search without map is O(n).",
  ex3_acc="Acceptance: deque/array ends O(1); linked only if stable node refs required.",
  revision="- No O(1) i-th without walk.\n- Pointer overhead.\n- LRU pattern.",
  confused="linked list versus deque",
  completion="- Implement prepend/find bounds.\n- Explain LRU structure.\n- Choose array vs list for queue.")

T(id="D02-T005", slug="d02-t005-stacks-and-queues", name="Stacks and queues", subdomain="Stacks and queues",
  deps=["D02-T004", "D02-T001", "D01-T001", "D01-T002"], next=["D02-T006"], related=["D02-T011", "D13-T006"],
  time="O(1) amortized push/pop for stack; O(1) enqueue/dequeue with proper ring buffer",
  space="O(n) stored elements",
  k_core="Stacks are LIFO; queues are FIFO. Both restrict access to ends, enabling O(1) structural operations.",
  backend_short="Request middleware stacks, undo buffers, and worker pools use these disciplines.",
  edge_short="pop from empty, unbounded queue memory, priority inversion not handled by basic queue",
  overview="Stacks model nested calls and backtracking. Queues model fair waiting lines and BFS frontiers. Backend services use both for rate limiting windows, task dispatch, and parsing.",
  first_principles="Restricting operations to one or two ends lets implementations use arrays with pointers without shifting middle elements.",
  internal="Array-backed deque doubles capacity on growth. Linked implementation avoids resize spikes but allocates per node. BFS queue order determines level-by-level graph expansion.",
  mermaid="""flowchart TD
  push[Push]
  stack[StackLIFO]
  pop[Pop]
  push --> stack --> pop""",
  diagram_caption="Last in is first out.",
  examples="Matching parentheses uses a stack O(n). Printer job queue is FIFO. Call stack depth limits recursion depth in languages.",
  edge="Empty pop, queue size unbounded under spike, concurrent queue needs locks or MPMC structure.",
  code_file="d02_t005_stack.py",
  code='''class Stack:\n    def __init__(self):\n        self._a: list[int] = []\n\n    def push(self, x: int) -> None:\n        self._a.append(x)\n\n    def pop(self) -> int:\n        if not self._a:\n            raise IndexError("empty")\n        return self._a.pop()\n\n\ndef balanced_parens(s: str) -> bool:\n    st: list[str] = []\n    pairs = {")": "(", "]": "[", "}": "{"}\n    for ch in s:\n        if ch in "([{":\n            st.append(ch)\n        elif ch in ")]}":\n            if not st or st.pop() != pairs[ch]:\n                return False\n    return not st''',
  code_notes="Stack ops amortized O(1). `balanced_parens` O(n) time O(n) space worst case.",
  backend="Bound queue depth; drop or shed load when full. Use stack depth limits to prevent parser blow-up on nested JSON.",
  table_rows="""| Array stack | Fast, simple | Growth copies | DFS, parsing | Thread-safe without sync |
| Ring buffer queue | O(1) FIFO | Fixed capacity | Metrics windows | Unbounded backlog |
| Linked queue | No resize spike | Pointer overhead | Rare | Hot path FIFO |""",
  mistakes="- Using recursion without depth guard.\n- Unbounded in-memory queue on traffic spike.\n- Popping empty without error handling.",
  debug="OOM with stable QPS—queue never drains. Check consumer lag and depth metric.",
  ex1="Implement `balanced_parens` and stack with empty-pop error.",
  ex2="Worker queue grows unbounded during outage—mitigations?",
  ex3="Stack versus queue for retry ordering (LIFO vs FIFO).",
  ex2_acc="Acceptance: bounded queue, drop policy, backpressure, dead-letter.",
  ex3_acc="Acceptance: FIFO fairness vs LIFO stack depth for nested retries.",
  revision="- LIFO vs FIFO.\n- O(1) ends.\n- Bound depth in prod.",
  confused="deque versus queue interface",
  completion="- Implement paren check.\n- Explain BFS queue role.\n- Design bounded worker queue.")

T(id="D02-T006", slug="d02-t006-hash-maps-and-hash-sets", name="Hash maps and hash sets", subdomain="Hash maps and hash sets",
  deps=["D02-T005", "D02-T001", "D01-T001", "D01-T002"], next=["D02-T007"], related=["D02-T003", "D07-T002"],
  time="O(1) average insert/lookup; O(n) worst case under heavy collisions or rehash",
  space="O(n) buckets and entries",
  k_core="Hash functions map keys to buckets; equality resolves collisions. Sets are maps without values.",
  backend_short="Indexes for id lookups, deduplication, rate-limit counters, and session tables rely on hash tables.",
  edge_short="mutable keys, poor hash on user strings, rehash pause, concurrent resize",
  overview="Hash maps give expected constant-time membership and update, which is why they back most in-memory indexes. Interviews probe average versus worst case and what makes a key hashable.",
  first_principles="Hash compresses key to integer; modulo bucket count picks slot. Collisions chain or open-address. Load factor triggers grow and rehash.",
  internal="Python dicts are highly optimized open addressing. Java HashMap resizes at load threshold. Concurrent maps use striping or lock-free bins.",
  mermaid="""flowchart TD
  key[Key]
  hashFn[HashFunction]
  bucket[BucketArray]
  chain[CollisionChain]
  key --> hashFn --> bucket --> chain""",
  diagram_caption="Collisions keep correctness; they hurt worst-case time.",
  examples="Dedup event ids in a request batch with a set O(n) expected. Count API keys per minute with a map.",
  edge="All keys collide adversarially, non-hashable list as key, iteration order change on resize.",
  code_file="d02_t006_hashmap.py",
  code='''def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:\n    seen: dict[int, int] = {}\n    for i, v in enumerate(nums):\n        need = target - v\n        if need in seen:\n            return seen[need], i\n        seen[v] = i\n    return None''',
  code_notes="Single pass O(n) time, O(n) space. Lookup/insert average O(1).",
  backend="Choose stable hash keys (ids as strings/int). Shard maps by tenant for memory. Watch rehash GC pauses on large maps.",
  table_rows="""| Hash map | Fast lookups | Memory, worst collisions | Id indexes | Ordered traversal need |
| Tree map | O(log n) guaranteed | Slower | Ordered ranges | Pure speed |
| DB index | Persistent | Disk latency | Large data | Tiny hot set |""",
  mistakes="- Mutating a key after insert.\n- Assuming O(1) without hash quality.\n- Storing unbounded keys from clients.",
  debug="Spiky latency on map grow—log size and resize events. Collision attacks—use random seed per process.",
  ex1="Implement `two_sum` and explain average-case bounds.",
  ex2="CPU spike when inserting attacker-controlled strings—cause?",
  ex3="In-memory map versus Redis for session store at 1M users.",
  ex2_acc="Acceptance: hash flooding/collision degradation; mitigation salted hash or tree fallback.",
  ex3_acc="Acceptance: memory per node, eviction, persistence, network hop.",
  revision="- Average O(1), worst O(n).\n- Keys must be hashable/stable.\n- Rehash cost.",
  confused="hash map versus B-tree index",
  completion="- Implement two-sum.\n- Explain collision impact.\n- Size session map memory.")

T(id="D02-T007", slug="d02-t007-trees-and-binary-search-trees", name="Trees and binary search trees", subdomain="Trees and binary search trees",
  deps=["D02-T006", "D02-T001", "D01-T001", "D01-T002"], next=["D02-T008"], related=["D02-T008", "D07-T002"],
  time="O(log n) balanced BST ops; O(n) skewed height",
  space="O(n) nodes; O(log n) stack for recursive traversal",
  k_core="BST property: left < node < right enables ordered search if height stays logarithmic.",
  backend_short="In-memory ordered indexes, interval trees for scheduling, and database B-trees are production tree variants.",
  edge_short="duplicate keys policy, unbalanced insert order, null children",
  overview="Trees represent hierarchical and ordered data. BSTs support search, insert, and delete in time proportional to height. Balance (AVL, red-black) keeps height O(log n).",
  first_principles="Each node branches; recursion or stack walks subtrees. BST invariant lets you discard half the tree per comparison when balanced.",
  internal="Rotations restore balance after insert/delete. B-trees widen nodes for disk pages. Trie is not a BST but shares pointer structure.",
  mermaid="""flowchart TD
  root[Root]
  left[LeftSubtree]
  right[RightSubtree]
  root --> left
  root --> right""",
  diagram_caption="Height determines search cost.",
  examples="Filesystem paths are trees. Priority scheduling sometimes uses tree maps for ordered keys.",
  edge="Sorted ascending insert into plain BST becomes linked list height n.",
  code_file="d02_t007_bst.py",
  code='''class BSTNode:\n    def __init__(self, key: int):\n        self.key = key\n        self.left = None\n        self.right = None\n\n\ndef insert(root: BSTNode | None, key: int) -> BSTNode:\n    if root is None:\n        return BSTNode(key)\n    if key < root.key:\n        root.left = insert(root.left, key)\n    elif key > root.key:\n        root.right = insert(root.right, key)\n    return root\n\n\ndef search(root: BSTNode | None, key: int) -> bool:\n    cur = root\n    while cur:\n        if key == cur.key:\n            return True\n        cur = cur.left if key < cur.key else cur.right\n    return False''',
  code_notes="Insert/search O(h) where h is height; O(log n) if balanced, O(n) if skewed.",
  backend="Prefer library balanced trees or DB indexes instead of hand-rolled BST in services.",
  table_rows="""| Plain BST | Simple | Skew risk | Teaching | Adversarial insert |
| Balanced BST | O(log n) ops | Rotation cost | Ordered map | O(1) needs |
| B-tree | Disk-friendly | Complex | Databases | Pure RAM tiny n |""",
  mistakes="- Assuming BST is always log n.\n- Ignoring duplicate key rules.\n- Deep recursion without stack guard.",
  debug="Latency grows with table size though RAM fits—check index balance stats in DB.",
  ex1="Implement insert and search; state height dependence.",
  ex2="Sorted inserts kill performance—fix?",
  ex3="BST versus hash for range queries `BETWEEN a AND b`.",
  ex2_acc="Acceptance: shuffle, red-black/AVL, or use tree map library.",
  ex3_acc="Acceptance: tree in-order O(k+log n); hash cannot range cheaply.",
  revision="- Height drives cost.\n- Balance matters.\n- DB B-tree is on disk.",
  confused="BST versus binary heap",
  completion="- Write BST search bounds.\n- Explain skew.\n- Pick structure for ranges.")

T(id="D02-T008", slug="d02-t008-heaps-and-priority-queues", name="Heaps and priority queues", subdomain="Heaps and priority queues",
  deps=["D02-T007", "D02-T001", "D01-T001", "D01-T002"], next=["D02-T009"], related=["D02-T013", "D13-T006"],
  time="O(log n) insert and extract-min/max; O(1) peek at root",
  space="O(n) array-backed heap",
  k_core="A binary heap is a complete tree with heap order stored in an array; it implements priority queues.",
  backend_short="Task schedulers, timeout wheels, and Dijkstra frontier use heaps for 'best next' retrieval.",
  edge_short="tie-breaking stability, decrease-key optional, empty extract",
  overview="Heaps retrieve the extreme element quickly while supporting dynamic insert. They underpin schedulers and many graph algorithms.",
  first_principles="Parent compares with children; sift up on insert, sift down on extract. Index arithmetic maps tree to array without pointers.",
  internal="`heapq` in Python is min-heap. Fibonacci heap improves theoretical decrease-key but rarely beats binary heap in practice.",
  mermaid="""flowchart TD
  insert[Insert]
  heap[BinaryHeap]
  peek[PeekMin]
  extract[ExtractMin]
  insert --> heap
  heap --> peek
  heap --> extract""",
  diagram_caption="Root holds the minimum in a min-heap.",
  examples="Process retries with earliest deadline first. Merge k sorted log streams with a heap of size k.",
  edge="Equal priorities arbitrary order, large k in k-way merge memory O(k).",
  code_file="d02_t008_heap.py",
  code='''import heapq\n\n\ndef k_smallest(nums: list[int], k: int) -> list[int]:\n    h = nums[:k]\n    heapq.heapify(h)\n    for v in nums[k:]:\n        if v > h[0]:\n            heapq.heapreplace(h, v)\n    return sorted(h)''',
  code_notes="Time O(n log k), space O(k). Each heap op O(log k).",
  backend="Cap heap size for top-K metrics. Combine with TTL map to drop stale tasks.",
  table_rows="""| Binary heap | Simple, fast | Not stable | Schedulers | Need stable sort |
| Sorted list | O(1) min if sorted | O(n) insert | Tiny sets | Dynamic n |
| Timing wheel | O(1) amortized timeouts | Approximate | Network timeouts | Exact ms ordering |""",
  mistakes="- Using sort O(n log n) when only top-k needed.\n- Forgetting heap is not fully sorted.\n- Unbounded priority queue.",
  debug="Scheduler lag—compare heap size to worker throughput. Stale tasks—missing cancel.",
  ex1="Implement `k_smallest` and state O(n log k).",
  ex2="Top-100 latency samples memory too high—optimize?",
  ex3="Heap versus sorted array for 10-element priority buffer.",
  ex2_acc="Acceptance: maintain size-k heap not full sort.",
  ex3_acc="Acceptance: heap for dynamic; array sort if static small.",
  revision="- log n per push/pop.\n- Array storage.\n- Top-k trick.",
  confused="heap versus BST",
  completion="- Explain heapify and extract.\n- Analyze k-smallest.\n- Design deadline scheduler.")

T(id="D02-T009", slug="d02-t009-tries", name="Tries", subdomain="Tries",
  deps=["D02-T008", "D02-T001", "D01-T001", "D01-T002"], next=["D02-T010"], related=["D02-T003", "D06-T005"],
  time="O(L) insert/search where L is key length; prefix queries O(L + matches)",
  space="O(total characters stored) with sharing prefixes",
  k_core="Tries branch on characters or bits; shared prefixes compress storage for dictionary-like keys.",
  backend_short="Routing tables, autocomplete, IP lookups, and banned-word filters use trie or radix variants.",
  edge_short="dense alphabet blow-up, Unicode code points vs bytes, empty prefix matches all",
  overview="Unlike hash maps, tries expose prefix structure. Search time depends on key length, not number of keys, which helps autocomplete and longest-prefix match.",
  first_principles="Each edge labels a character; paths spell keys. Terminal flag marks complete words. Radix trees compress single-child chains.",
  internal="Array of 26 children is fast for ASCII letters but sparse. Map children save space for general alphabets.",
  mermaid="""flowchart TD
  root[TrieRoot]
  a[BranchA]
  p[BranchP]
  root --> a --> p""",
  diagram_caption="Shared prefixes reuse nodes.",
  examples="Suggest DNS labels, filter profanity streams, match URL path prefixes in routers.",
  edge="Key `a` is prefix of `ab`; memory for 26-wide nodes, case folding changes structure.",
  code_file="d02_t009_trie.py",
  code='''class TrieNode:\n    def __init__(self):\n        self.children: dict[str, TrieNode] = {}\n        self.end = False\n\n\ndef insert(root: TrieNode, word: str) -> None:\n    cur = root\n    for ch in word:\n        cur = cur.children.setdefault(ch, TrieNode())\n    cur.end = True\n\n\ndef starts_with(root: TrieNode, prefix: str) -> bool:\n    cur = root\n    for ch in prefix:\n        if ch not in cur.children:\n            return False\n        cur = cur.children[ch]\n    return True''',
  code_notes="Insert and prefix check O(L) time; space O(nodes) proportional to stored text.",
  backend="Normalize case and Unicode before trie insert. Bound autocomplete results to prevent enumeration attacks.",
  table_rows="""| Trie | Prefix queries | Memory | Autocomplete | Exact-only lookups |
| Hash set | O(1) exact | No prefix | Membership | Prefix search |
| DB LIKE | Persistent | Slow scan | Ad hoc | Hot path prefix |""",
  mistakes="- Assuming O(1) because 'hash fast'.\n- 26-array for Unicode.\n- Returning unbounded autocomplete.",
  debug="Memory high on random keys—prefix sharing fails; consider hash if no prefix need.",
  ex1="Implement insert and `starts_with`.",
  ex2="Autocomplete endpoint enumerates all users—risk and fix?",
  ex3="Trie versus bloom filter for banned token list.",
  ex2_acc="Acceptance: rate limit, min prefix length, cap results, auth.",
  ex3_acc="Acceptance: trie exact/prefix; bloom false positives unacceptable for blocklist.",
  revision="- O(L) not O(n keys).\n- Prefix sharing.\n- Abuse caps.",
  confused="trie versus hash map",
  completion="- Write trie ops bounds.\n- Design autocomplete limits.\n- Pick trie vs hash.")

T(id="D02-T010", slug="d02-t010-graphs-and-graph-representations", name="Graphs and graph representations", subdomain="Graphs and graph representations",
  deps=["D02-T009", "D02-T001", "D01-T001", "D01-T002"], next=["D02-T011"], related=["D02-T011", "D02-T013"],
  time="O(V+E) to traverse adjacency list; O(V^2) space for adjacency matrix dense",
  space="O(V+E) list; O(V^2) matrix",
  k_core="Graphs model entities (vertices) and relationships (edges). Representation choice drives memory and neighbor iteration cost.",
  backend_short="Service dependency graphs, permission graphs, and network topologies are graphs; storage shape affects traversal budgets.",
  edge_short="self-loops, multi-edges, disconnected components, directed vs undirected",
  overview="Choosing adjacency list, matrix, or edge list determines whether algorithms like BFS and Dijkstra are practical at your scale.",
  first_principles="List stores neighbors per vertex—sparse graphs use O(V+E). Matrix stores all pairs—fast edge test O(1) but heavy when sparse.",
  internal="Compress with integer vertex ids. Store weights on edges for shortest path. Bidirectional edges may be stored once or twice.",
  mermaid="""flowchart LR
  v1[Vertex]
  adj[AdjacencyList]
  e1[NeighborA]
  e2[NeighborB]
  v1 --> adj --> e1
  adj --> e2""",
  diagram_caption="Lists favor sparse graphs.",
  examples="Microservice mesh: vertices services, edges RPC calls. Shard graph by tenant if V is huge.",
  edge="Isolated nodes, parallel edges, memory if V^2 matrix with millions of vertices.",
  code_file="d02_t010_graph.py",
  code='''def build_adj(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:\n    adj: list[list[int]] = [[] for _ in range(n)]\n    for u, v in edges:\n        adj[u].append(v)\n        adj[v].append(u)\n    return adj\n\n\ndef degree(adj: list[list[int]], u: int) -> int:\n    return len(adj[u])''',
  code_notes="Build O(E), space O(V+E). Undirected edges stored twice.",
  backend="Persist edges in join table; load adjacency in memory only for analytics jobs with bounded V.",
  table_rows="""| Adjacency list | Sparse efficient | Slow edge test | Social, mesh | Dense clique |
| Adjacency matrix | O(1) edge query | O(V^2) memory | Tiny V | Large sparse |
| Edge list | Compact stream | Slow neighbors | ETL | Frequent neighbor scan |""",
  mistakes="- Matrix for million-node sparse graph.\n- Forgetting directed orientation.\n- Rebuilding adjacency per request O(E).",
  debug="OOM building graph—check representation and duplicate edge load.",
  ex1="Build undirected adjacency list from edge list.",
  ex2="Service map API loads full graph per call—optimize representation pipeline.",
  ex3="List versus matrix for 200-node internal mesh.",
  ex2_acc="Acceptance: cache adjacency, incremental updates, DB edge query.",
  ex3_acc="Acceptance: matrix 40k cells fine; list if sparser later.",
  revision="- V and E notation.\n- List for sparse.\n- Matrix for dense small V.",
  confused="graph versus tree",
  completion="- Build adj list bounds.\n- Compare representations.\n- Size memory for V,E.")

T(id="D02-T011", slug="d02-t011-bfs-and-dfs", name="BFS and DFS", subdomain="BFS and DFS",
  deps=["D02-T010", "D02-T001", "D01-T001", "D01-T002"], next=["D02-T012"], related=["D02-T013", "D02-T012"],
  time="O(V+E) for adjacency list traversal",
  space="O(V) visited set plus O(V) queue or stack",
  k_core="BFS explores layer by layer with a queue; DFS goes deep first with a stack or recursion.",
  backend_short="Reachability in dependency graphs, cycle detection, and connected components use these traversals.",
  edge_short="revisiting without visited set, recursion depth, disconnected graph",
  overview="Both visit each vertex and edge once in the list model. BFS gives shortest unweighted paths; DFS suits topological exploration and maze-like backtracking.",
  first_principles="Mark visited to avoid exponential revisits. BFS queue FIFO processes increasing distance from source. DFS stack LIFO finishes subtrees before siblings.",
  internal="Iterative DFS avoids recursion limit. Color marking (white/gray/black) detects cycles in directed graphs.",
  mermaid="""flowchart TD
  start[StartNode]
  bfs[BFS_Queue]
  dfs[DFS_Stack]
  start --> bfs
  start --> dfs""",
  diagram_caption="Same graph, different visit order.",
  examples="Find if service A can reach service B in outage graph. Crawl internal links with depth cap (DFS).",
  edge="Multiple components—run from each unvisited. Huge graphs—stream edges.",
  code_file="d02_t011_bfs.py",
  code='''from collections import deque\n\n\ndef bfs_dist(adj: list[list[int]], src: int) -> list[int]:\n    n = len(adj)\n    dist = [-1] * n\n    q: deque[int] = deque([src])\n    dist[src] = 0\n    while q:\n        u = q.popleft()\n        for v in adj[u]:\n            if dist[v] == -1:\n                dist[v] = dist[u] + 1\n                q.append(v)\n    return dist''',
  code_notes="O(V+E) time, O(V) space for dist, queue, and visited implicit in dist.",
  backend="Cap BFS depth in user-triggered graph walks. Timeout traversal in API handlers.",
  table_rows="""| BFS | Shortest unweighted path | More memory queue | Dependency level | Deep narrow tree |
| DFS | Less memory stack | Not shortest | Cycle detect | Shortest path unweighted |
| Bidirectional BFS | Faster meet-in-middle | Setup cost | Social distance | General DAG |""",
  mistakes="- No visited set.\n- Using DFS for shortest unweighted path.\n- Unbounded recursion.",
  debug="Traversal hangs—cycle without visited. Stack overflow—switch iterative.",
  ex1="Implement `bfs_dist` for unweighted graph.",
  ex2="Permission check DFS cycles wrongly grants access—debug approach.",
  ex3="BFS versus DFS for nightly batch component labeling.",
  ex2_acc="Acceptance: detect cycle, deny or break edge, visited coloring.",
  ex3_acc="Acceptance: either O(V+E); BFS if levels needed.",
  revision="- O(V+E).\n- visited required.\n- BFS shortest unweighted.",
  confused="BFS versus Dijkstra",
  completion="- Write BFS bounds.\n- Explain visited.\n- Pick BFS vs DFS scenario.")

T(id="D02-T012", slug="d02-t012-topological-sorting", name="Topological sorting", subdomain="Topological sorting",
  deps=["D02-T011", "D02-T001", "D01-T001", "D01-T002"], next=["D02-T013"], related=["D02-T011", "D13-T006"],
  time="O(V+E) Kahn or DFS-based algorithms",
  space="O(V) indegree queue plus output list",
  k_core="Topological order exists only on DAGs; it aligns edges from earlier to later tasks.",
  backend_short="Build pipelines, migration ordering, and task dependencies require topo sort or cycle detection.",
  edge_short="cycle makes sort impossible, multiple valid orders, disconnected DAG",
  overview="Ordering tasks with prerequisites is topo sort. Detecting cycles prevents deadlocked deploy scripts.",
  first_principles="Kahn: peel vertices with indegree zero. DFS: finish times reverse postorder. Both linear in vertices and edges.",
  internal="If cycle exists, Kahn leaves leftover vertices; DFS finds back edges.",
  mermaid="""flowchart TD
  indeg[IndegreeZero]
  queue[KahnQueue]
  order[TopoOrder]
  indeg --> queue --> order""",
  diagram_caption="Only DAGs yield full order.",
  examples="Apply DB migrations in dependency order. Schedule ETL jobs with edges 'job B after A'.",
  edge="Parallel tasks same level—any order among them valid.",
  code_file="d02_t012_topo.py",
  code='''from collections import deque\n\n\ndef topo_kahn(n: int, edges: list[tuple[int, int]]) -> list[int] | None:\n    adj: list[list[int]] = [[] for _ in range(n)]\n    indeg = [0] * n\n    for u, v in edges:\n        adj[u].append(v)\n        indeg[v] += 1\n    q: deque[int] = deque([i for i in range(n) if indeg[i] == 0])\n    order: list[int] = []\n    while q:\n        u = q.popleft()\n        order.append(u)\n        for v in adj[u]:\n            indeg[v] -= 1\n            if indeg[v] == 0:\n                q.append(v)\n    return order if len(order) == n else None''',
  code_notes="Returns None if cycle. Time O(V+E), space O(V+E).",
  backend="Fail deploy if cycle detected. Emit parallelizable layers for CI fan-out.",
  table_rows="""| Kahn BFS | Intuitive layers | Extra indegree array | CI pipelines | Recursive depth fear |
| DFS postorder | Compact code | Cycle via colors | Scripts | Need explicit layers |
| Manual sort | None | Wrong | Never | DAG deps |""",
  mistakes="- Topo on cyclic graph silently wrong.\n- Missing nodes with zero indegree handling.\n- Confusing any DFS order with topo.",
  debug="Deploy stuck—run cycle detection on dependency graph.",
  ex1="Implement Kahn topo with cycle detection via `None`.",
  ex2="Migration tool runs scripts in wrong order—fix graph model.",
  ex3="Topo layers for parallel CI versus single total order.",
  ex2_acc="Acceptance: build DAG from manifest, topo or fail.",
  ex3_acc="Acceptance: group by indegree waves.",
  revision="- DAG only.\n- O(V+E).\n- Cycle => no topo.",
  confused="topo sort versus shortest path",
  completion="- Implement Kahn.\n- Detect cycle.\n- Explain deploy ordering.")

T(id="D02-T013", slug="d02-t013-shortest-path-algorithms", name="Shortest-path algorithms", subdomain="Shortest-path algorithms",
  deps=["D02-T012", "D02-T001", "D01-T001", "D01-T002"], next=["D02-T014"], related=["D02-T008", "D02-T011"],
  time="BFS O(V+E) unweighted; Dijkstra O((V+E) log V) with heap; Bellman-Ford O(VE) with negative edges",
  space="O(V) distance map plus heap",
  k_core="Shortest path minimizes sum of edge weights subject to graph rules; algorithm choice depends on weights and negativity.",
  backend_short="Route planning, latency-aware routing, and cost minimization in workflows use shortest-path variants.",
  edge_short="negative cycles, disconnected targets, zero-weight edges, integer overflow on distance",
  overview="Unweighted graphs use BFS. Non-negative weights use Dijkstra. Negative edges need Bellman-Ford. Wrong algorithm choice breaks correctness or performance.",
  first_principles="Relax edges: if dist[u]+w < dist[v], improve dist[v]. Dijkstra greedily settles min vertex with non-negative weights.",
  internal="Priority queue stores frontier. Early exit when target popped. A* adds heuristic for maps.",
  mermaid="""flowchart TD
  src[Source]
  relax[RelaxEdges]
  heap[MinHeapFrontier]
  src --> relax --> heap""",
  diagram_caption="Non-negative weights enable Dijkstra.",
  examples="Pick lowest-latency path between services with measured edge weights. Cap hops with BFS level.",
  edge="Unreachable node dist infinity, self-loop weight 0, overflow on large weights.",
  code_file="d02_t013_dijkstra.py",
  code='''import heapq\n\n\ndef dijkstra(adj: list[list[tuple[int, int]]], src: int) -> list[int]:\n    n = len(adj)\n    dist = [10**18] * n\n    dist[src] = 0\n    pq: list[tuple[int, int]] = [(0, src)]\n    while pq:\n        d, u = heapq.heappop(pq)\n        if d != dist[u]:\n            continue\n        for v, w in adj[u]:\n            nd = d + w\n            if nd < dist[v]:\n                dist[v] = nd\n                heapq.heappush(pq, (nd, v))\n    return dist''',
  code_notes="Weighted adjacency list of (neighbor, weight). O((V+E) log V) with binary heap.",
  backend="Refresh edge weights from metrics; stale weights misroute. Bound graph size per query.",
  table_rows="""| BFS | Unweighted shortest | Not for weights | Hop count | Latency weights |
| Dijkstra | Non-negative weights | No negative edges | Service mesh | Negative cost |
| Bellman-Ford | Negative edges | Slower | Finance nets | Non-negative only |""",
  mistakes="- Dijkstra with negative weight.\n- Using BFS on weighted graph.\n- Not handling unreachable nodes.",
  debug="Routes absurd—check weight sign and units. Slow—dense graph without heap.",
  ex1="Implement Dijkstra with stale-entry skip (`d != dist[u]`).",
  ex2="Negative 'credit' edge breaks routing—which algorithm?",
  ex3="Precompute all-pairs versus per-query Dijkstra in API.",
  ex2_acc="Acceptance: Bellman-Ford or remove negative; Dijkstra invalid.",
  ex3_acc="Acceptance: Floyd-Warshall O(V^3) rare; cache for static graph.",
  revision="- BFS unweighted.\n- Dijkstra non-negative.\n- Heap frontier.",
  confused="Dijkstra versus BFS",
  completion="- Implement Dijkstra.\n- Choose algorithm by weights.\n- State unreachable handling.")

T(id="D02-T014", slug="d02-t014-union-find-disjoint-set-union", name="Union-Find / Disjoint Set Union", subdomain="Union-Find / Disjoint Set Union",
  deps=["D02-T013", "D02-T001", "D01-T001", "D01-T002"], next=["D02-T015"], related=["D02-T010", "D02-T011"],
  time="O(alpha(n)) amortized per union/find with rank and path compression",
  space="O(n) parent and rank arrays",
  k_core="Union-Find maintains disjoint sets with near-constant merge and same-set queries.",
  backend_short="Connectivity, Kruskal MST, network merge, and duplicate account clustering use DSU.",
  edge_short="union before find on wrong elements, 1-indexed vs 0-indexed, need component sizes",
  overview="Instead of explicit graphs per query, DSU tracks components dynamically as edges arrive. Path compression and union by rank keep operations almost constant.",
  first_principles="Each element points to parent; root identifies set. Find walks to root; union attaches one root under another by rank.",
  internal="Amortized analysis uses inverse Ackermann alpha(n), effectively constant for practical n.",
  mermaid="""flowchart TD
  findOp[FindWithCompression]
  unionOp[UnionByRank]
  comp[ConnectedComponents]
  findOp --> comp
  unionOp --> comp""",
  diagram_caption="Two operations maintain components.",
  examples="Detect if adding network link creates single connected datacenter partition. Cluster user accounts by verified edges offline.",
  edge="Union on last element only without find roots; counting components after unions.",
  code_file="d02_t014_dsu.py",
  code='''class DSU:\n    def __init__(self, n: int):\n        self.p = list(range(n))\n        self.r = [0] * n\n\n    def find(self, x: int) -> int:\n        while self.p[x] != x:\n            self.p[x] = self.p[self.p[x]]\n            x = self.p[x]\n        return x\n\n    def union(self, a: int, b: int) -> bool:\n        ra, rb = self.find(a), self.find(b)\n        if ra == rb:\n            return False\n        if self.r[ra] < self.r[rb]:\n            ra, rb = rb, ra\n        self.p[rb] = ra\n        if self.r[ra] == self.r[rb]:\n            self.r[ra] += 1\n        return True''',
  code_notes="Union returns False if already connected. Amortized O(alpha(n)) per op.",
  backend="Batch union-find offline; online queries may need graph DB. Validate vertex ids before union.",
  table_rows="""| DSU | Near O(1) connectivity | Offline dynamic | Kruskal, clustering | Need full path list |
| BFS each query | Finds paths | O(V+E) per query | Single query | Millions unions |
| Graph DB | Expressive | Ops cost | Persistent graph | Simple connectivity |""",
  mistakes="- Union without compressing paths.\n- O(n) find each time in loops.\n- Wrong index base.",
  debug="Slow connectivity—missing path compression. Wrong component count—union on non-roots.",
  ex1="Implement DSU with path compression and union by rank.",
  ex2="Kruskal MST step needs DSU—explain why.",
  ex3="DSU versus BFS for 1M union queries streaming.",
  ex2_acc="Acceptance: reject cycle edge when endpoints same component.",
  ex3_acc="Acceptance: DSU O(m alpha(n)); BFS per edge too slow.",
  revision="- find + union.\n- compress + rank.\n- alpha(n) amortized.",
  confused="DSU versus connected components BFS",
  completion="- Write DSU ops.\n- Explain Kruskal use.\n- Compare streaming unions.")

def exercise_md(t):
    return f"""# Exercises — {t["id"]}

Problems only. Solutions: [{t["id"]}](../solutions/{t["id"]}.md).

1. {t["ex1"]}
2. {t["ex2"]}
3. {t["ex3"]}
"""

def solution_md(t):
    return f"""# Solutions for {t["id"]}

Open this only after attempting the exercises in the topic note.

## Exercise 1

```python
{t["code"]}
```

{t.get("sol1_extra", "Add complexity comments as required by the exercise.")}

## Exercise 2

{t["ex2_acc"]}

## Exercise 3

{t["ex3_acc"]}
"""

def interview_md(t):
    return f"""# {t["id"]} interview items

Domain: Data Structures and Algorithms
Topic: {t["name"]}
Difficulty mix: beginner, intermediate, advanced, scenario, follow-up
Interview type: fundamentals, complexity, system design
Full reasoned answers are in the topic note, section K.

## Questions

1. Beginner. What problem does {t["name"]} solve?
2. Beginner. How do you define n here?
3. Beginner. Time versus space trade-off?
4. Beginner. Why ignore constants?
5. Beginner. One cheap and one expensive operation?
6. Intermediate. Average versus worst case?
7. Intermediate. Justify this structure in a design review?
8. Intermediate. Data larger than RAM?
9. Intermediate. Concurrency impact?
10. Intermediate. Performance regression tests?
11. Advanced. When is textbook complexity misleading?
12. Advanced. Cache and allocation effects?
13. Advanced. Compare to the next curriculum topic?
14. Advanced. Abuse patterns on effective n?
15. Advanced. Document complexity in ADR/OpenAPI?
16. Scenario. Latency spikes at 2x traffic?
17. Scenario. Batch job OOM?
18. Scenario. Timeout budget disagreement?
19. Scenario. Worst-case attacker input?
20. Scenario. Shave 100ms on hot path?
21. Follow-up. Database indexing connection?
22. Follow-up. Caching layers connection?
23. Follow-up. Monitoring proof?

Answer key: [topic note section K](../01_PROGRAMMING_AND_ALGORITHMS/notes/{t["slug"]}.md).
"""

def main():
    notes_dir = ROOT / "01_PROGRAMMING_AND_ALGORITHMS" / "notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    for t in TOPICS:
        mk_k(t)
        t["ex2_acc"] = t.get("ex2_acc", "See topic note section J.")
        t["ex3_acc"] = t.get("ex3_acc", "See topic note section H.")
        note = A(t)
        (notes_dir / f"{t['slug']}.md").write_text(note, encoding="utf-8")
        (ROOT / "EXERCISES").mkdir(exist_ok=True)
        (ROOT / "EXERCISES" / f"{t['id']}.md").write_text(exercise_md(t), encoding="utf-8")
        (ROOT / "EXERCISES" / "solutions").mkdir(exist_ok=True)
        (ROOT / "EXERCISES" / "solutions" / f"{t['id']}.md").write_text(solution_md(t), encoding="utf-8")
        (ROOT / "INTERVIEW_BANK" / "items").mkdir(parents=True, exist_ok=True)
        (ROOT / "INTERVIEW_BANK" / "items" / f"{t['id']}.md").write_text(interview_md(t), encoding="utf-8")
    print("wrote", len(TOPICS), "topics")

if __name__ == "__main__":
    main()


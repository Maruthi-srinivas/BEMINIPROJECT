"""Topic facts for concurrency stubs and messaging gaps."""

from __future__ import annotations

from gap_facts_a import add

add(
    "D13-T009",
    "Lock-free programming updates shared data with atomic primitives such as compare-and-swap instead of a mutex. A thread that fails a CAS retries. Progress for the system continues even if one thread stalls, which is the usual lock-free guarantee. It is not wait-free, which would bound each thread's own steps. ABA, memory ordering, and a retry loop that livelocks under contention are the real bugs.",
    ["Read the current word", "Compute the next value", "CAS it into place", "Retry or back off if another writer won"],
    "an ABA bug or a CAS loop saturating a core while a mutex would have queued quietly",
    "CAS failure rate and the number of retries before success",
    "def cas(expected, new, cell):\n    if cell[0] == expected:\n        cell[0] = new\n        return True\n    return False\n",
    "Lock-free code is changing a number on the board only if it still shows the number you read. If someone else wrote first, you read again. Nobody holds a pen exclusively.",
    "A metrics counter uses an atomic add, which is lock-free and the right size. A multi-field account update does not, because two words are not one CAS.",
    "the update is one word and the critical section is tiny",
    "the invariant spans multiple words or the contention is high enough that a queueing lock is kinder",
    ["Calling a retry loop wait-free.", "Ignoring memory ordering.", "Using lock-free structures without a linearization argument."],
)

add(
    "D13-T010",
    "The producer-consumer pattern separates work creation from work execution through a queue. Producers enqueue. Consumers dequeue. The queue is the synchronization point. An unbounded queue hides a slow consumer until memory dies. Closing the queue is a signal that no more work is coming, and consumers must exit after draining.",
    ["Producer creates a unit of work", "Enqueue it", "Consumer dequeues it", "Consumer signals completion or failure"],
    "an unbounded queue that grows until the process is killed, or a consumer that exits and leaves the queue unowned",
    "queue depth and the age of the oldest item",
    "import queue\nq = queue.Queue(maxsize=100)\n\ndef produce(item):\n    q.put(item, timeout=1)\n",
    "Producers are cooks. Consumers are servers. The pass is the queue. If the pass has no limit, plates hit the floor as a pile, not as a handoff.",
    "A web request validates quickly and enqueues an email job. Worker processes consume the queue. When the queue age exceeds a minute, the API starts rejecting new jobs instead of pretending they will send.",
    "creation and execution have different speeds or lifetimes",
    "the work is so small that the queue costs more than doing it inline",
    ["An unbounded queue.", "No poison-message handling.", "Assuming the enqueue is the same as the work being done."],
)

add(
    "D13-T011",
    "A bounded queue has a fixed capacity. When it is full, a producer blocks, fails, or drops, which is backpressure. Backpressure pushes the overload to the edge that can say no, instead of letting it pile up in memory. The bound is part of the SLO. A timeout on put tells the caller the system is saturated.",
    ["Set a capacity from the consumer's rate", "Block, fail, or drop when full", "Alert on depth before the bound", "Shed at the entrance"],
    "a full queue whose producers block forever and stall request threads, or a drop policy that loses the one message you needed",
    "queue depth versus capacity, and the rate of rejected puts",
    "def offer(q, item, capacity):\n    if len(q) >= capacity:\n        return False\n    q.append(item)\n    return True\n",
    "A bounded queue is a restaurant that stops seating when every table is full. Backpressure is the host saying 'not tonight' instead of stacking guests in the kitchen.",
    "An API puts jobs on a queue of 1,000. When the offer fails, it returns 429. Callers retry. The worker pool stays at a size the database can handle.",
    "producers can outrun consumers",
    "you block request threads on a full queue with no timeout",
    ["An infinite buffer called a safety net.", "Dropping payments.", "No metric on depth."],
)

add(
    "D13-T012",
    "Concurrent collections provide atomic operations on a data structure so callers do not wrap every access in the same coarse lock. A concurrent hash map can update one key without locking the whole map. Iteration may be weakly consistent and miss or duplicate an entry that is updated mid-scan. They do not make a compound check-then-act atomic. Size is approximate on some implementations.",
    ["Pick a structure whose single operations are atomic", "Do not assume a compound action is atomic", "Avoid locking around the collection and also using its internal locks in a different order", "Know the iteration guarantee"],
    "a check-then-put that two threads both pass, or a deadlock between the collection lock and an external lock",
    "lost updates in a stress test of a compound action, and lock-order deadlocks",
    "box = {}\nlock = __import__('threading').Lock()\n\ndef put_if_absent(key, value):\n    with lock:\n        if key not in box:\n            box[key] = value\n            return True\n        return False\n",
    "A concurrent map is a set of drawers that each close individually. Looking in a drawer and then deciding to fill it is two actions, and someone else can slip a folder in between.",
    "A request deduplicator uses put-if-absent on an idempotency key. Two separate calls, contains then put, both create the charge. One atomic put-if-absent does not.",
    "many keys are updated by different threads and each update is one operation",
    "the invariant covers two keys or a check followed by an action",
    ["Assuming iteration locks a snapshot.", "Coarse-locking a concurrent structure and deadlocking.", "Using a plain dict from many threads."],
)

add(
    "D13-T013",
    "Deadlock prevention stops a wait cycle from forming. The practical rule is a global lock order: every thread acquires locks in the same sequence. Try-lock with a timeout plus releasing what you hold also prevents a permanent cycle, at the cost of retries. You prevent deadlock by breaking circular wait, not by detecting it after users are stuck. Nested lock acquisition is the moment to audit.",
    ["List the locks", "Sort them in one global order", "Acquire only in that order", "Do not call out while holding a lock that another ordered lock might need"],
    "two services locking rows in opposite orders, or a timeout retry that livelocks",
    "deadlock rollback count and lock-wait timeouts",
    "def order(locks):\n    return sorted(locks, key=lambda item: item.name)\n",
    "Prevention is everyone agreeing to pick up the left shoe before the right shoe, so nobody is holding the right shoe and waiting for the left.",
    "Account transfers lock the lower account id first. The cycle between A-to-B and B-to-A disappears. A new code path that locks 'the one in the request first' reintroduces it.",
    "a thread may hold more than one lock",
    "you can take one lock, or the database can lock a sorted set of rows in one statement",
    ["Detection as the only strategy.", "Lock order that depends on a map's iteration.", "Holding locks across RPC."],
)

add(
    "D13-T014",
    "Task scheduling decides which runnable task a worker executes next. A FIFO queue is fair and can suffer head-of-line blocking. Priorities help latency and can starve low priority unless you age them. Work stealing lets an idle worker take a task from a busy worker's deque. The scheduler does not create CPU. A blocking task occupies a worker until it returns.",
    ["Queue the task", "Pick a worker", "Run until the task blocks or finishes", "Stop accepting when the queue bound is hit"],
    "a priority policy that never runs low-priority cleanup, or a blocking call that shrinks the effective pool to zero",
    "queue age by priority, worker utilization, and starved-task count",
    "import heapq\n\ndef pop(ready):\n    return heapq.heappop(ready)\n",
    "Scheduling is the host choosing the next table. Priority seating without a rule for waiting guests is how a quiet table never gets served.",
    "A worker pool runs HTTP handlers FIFO. A few slow report tasks at the head delay health checks. Splitting interactive and batch pools is the scheduling decision.",
    "more runnable tasks exist than workers",
    "you have one task, where a queue only adds latency",
    ["Unbounded queues.", "Priorities without aging.", "Blocking the only worker."],
)

add(
    "D13-T015",
    "CPU-bound work spends its time computing, so more progress needs more cores until the machine is saturated. I/O-bound work spends its time waiting on disk, network, or another service, so more concurrent waiters can improve throughput on one core. The split decides threads versus async versus processes. A pool sized for the wrong class either thrashes or leaves the database idle.",
    ["Profile where the time goes", "If it is CPU, add cores and stop at saturation", "If it is I/O, add concurrency up to the dependency's limit", "Put each class on its own pool"],
    "CPU work on an event loop, or thousands of threads for a CPU-bound hash",
    "CPU utilization versus wait time, and throughput as concurrency increases",
    "def pool_kind(cpu_bound: bool) -> str:\n    return 'process-or-core-threads' if cpu_bound else 'async-or-io-threads'\n",
    "CPU-bound is chopping vegetables. More knives need more people. I/O-bound is waiting for the oven, and one person can watch several ovens.",
    "Image resizing goes to a process pool sized to cores. Database calls stay on an I/O pool sized to the connection limit. One shared pool of 200 threads makes the resizes slower and the database overloaded.",
    "you are sizing workers",
    "you guess from the language default",
    ["Async for CPU-bound work.", "A thread per request for heavy compute.", "One pool for both."],
)

add(
    "D13-T016",
    "CPython's GIL lets one thread execute Python bytecode at a time in a process. Threads still help for I/O, because a thread releases the GIL while it waits. CPU-bound Python does not speed up with threads. Processes, native extensions that release the GIL, or another runtime do. The GIL is not a substitute for locks on your own invariants.",
    ["Classify the work", "Use threads for I/O-bound Python", "Use processes or native code for CPU-bound Python", "Still lock shared objects"],
    "expecting a CPU-bound Python loop to scale across threads, or skipping locks because 'the GIL makes it safe'",
    "cores used during a CPU benchmark with threads versus processes",
    "from multiprocessing import Pool\n\ndef cpu_pool(n, fn, items):\n    with Pool(n) as pool:\n        return pool.map(fn, items)\n",
    "The GIL is one microphone for the bytecode. Threads can put the microphone down while they wait on the network. They cannot sing a CPU chorus with it.",
    "A Flask or Django handler that waits on SQL benefits from threads. A pure-Python image filter needs processes. A list append from two threads still needs synchronization for the application's invariant.",
    "you are choosing concurrency inside CPython",
    "you assume another interpreter has the same GIL",
    ["Threads for CPU-bound loops.", "No locks because of the GIL.", "Processes that share memory by accident through a parent fork."],
)

add(
    "D13-T017",
    "The Java Memory Model defines when a write in one thread becomes visible to a read in another. Without a happens-before edge, a read may see a stale value and may see writes out of order. Locks, volatile, thread start and join, and atomic classes create those edges. A data race is a bug even if the test passed on one laptop. Declaring a field volatile does not make a compound increment atomic.",
    ["Name the writing thread and the reading thread", "Establish happens-before", "Use a lock or an atomic for compound updates", "Do not publish an object before it is constructed"],
    "a flag that never appears true to another thread, or a compound increment lost under volatile",
    "a stress test that fails when a visibility bug is forced, not only a green run on one core",
    "import java.util.concurrent.atomic.AtomicInteger;\nclass C { final AtomicInteger n = new AtomicInteger(); }\n",
    "The memory model is the rule for when a note stuck on one desk is required to be seen from another desk. Without the rule, the other desk may keep looking at a blank page.",
    "A stopped boolean in a Java service is volatile or the worker never sees the shutdown. A request counter uses AtomicInteger or LongAdder, not a volatile int plus plus.",
    "two Java threads share mutable state",
    "the state is confined to one thread or is immutable and safely published",
    ["Volatile for increment.", "Assuming a lock-free read of a long is atomic on every hardware platform without the JMM tools.", "Publishing this before the constructor finishes."],
    lang="java",
)

add(
    "D13-T018",
    "A goroutine is a lightweight task scheduled by the Go runtime onto OS threads. Channels pass values between goroutines. An unbuffered channel synchronizes sender and receiver. A buffered channel queues a bounded number of values. Closing a channel signals no more sends. Sending on a closed channel panics. Select waits on several operations. The runtime does not prevent a blocked goroutine leak.",
    ["Start a goroutine with a clear owner", "Communicate completion on a channel or a context", "Bound buffers", "Make sure something receives or the goroutine exits"],
    "a goroutine blocked forever on a send to a channel nobody receives, leaking until the process dies",
    "goroutine count over time and blocked-send age",
    "func worker(jobs <-chan int, done chan<- struct{}) {\n    for range jobs {\n    }\n    done <- struct{}{}\n}\n",
    "A goroutine is a slip of work. A channel is a handoff. If you hand someone a slip and walk away, and they are not there, you stand in the hallway forever.",
    "An HTTP handler starts a goroutine to call a webhook and returns without a timeout. Under load the process holds millions of stuck goroutines. A context with a deadline and a bounded worker pool fixes the lifetime.",
    "you want many concurrent tasks in one Go process",
    "you start a goroutine per item with no bound and no cancellation",
    ["Unbuffered sends from a request with no receiver.", "Ranging a channel that is never closed.", "Shared maps without synchronization."],
    lang="go",
)

add(
    "D13-T019",
    "Node.js runs JavaScript on one thread with an event loop. I/O uses a non-blocking interface and callbacks or promises. CPU-heavy JavaScript blocks the loop. Worker threads run JavaScript in parallel and communicate by message, not by shared objects. The libuv thread pool is a small pool for some blocking filesystem and DNS calls. A blocking call in the main thread delays every client.",
    ["Keep the main thread on short callbacks and I/O", "Move CPU work to worker threads or another process", "Bound the libuv pool", "Watch event-loop lag"],
    "JSON parsing or compression on the main thread so health checks time out",
    "event-loop lag and libuv pool queue length",
    "const { Worker } = require('worker_threads');\nfunction offload(path) { return new Worker(path); }\n",
    "The main thread is one clerk at a window. Worker threads are extra rooms. If the clerk starts doing a long calculation, the line does not move, even though the phones are modern.",
    "A Node API that gzip-compresses large payloads on the request path blocks every other request. Moving compression to a worker or to a proxy brings loop lag back down.",
    "the service is I/O with small bursts of JavaScript",
    "the hot path is CPU-bound JavaScript on the main thread",
    ["Worker threads for every tiny function.", "Blocking fs calls in the request path.", "Ignoring DNS as a blocking path when it hits the pool."],
    lang="javascript",
)

add(
    "D13-T020",
    "A concurrency limit caps how many operations of one kind may run at once. A bulkhead isolates that cap so a failure in one dependency cannot consume every thread. Separate pools for separate dependencies stop a slow payments call from occupying the threads the health check needs. The limit should match the dependency, not the size of the machine.",
    ["Give each dependency its own limit", "Queue or reject past the limit", "Do not share one pool across unrelated calls", "Trip a fallback when the bulkhead is full"],
    "one slow dependency occupying the only thread pool so the process cannot serve even cached reads",
    "pool saturation per dependency, and success of an isolated health check during that saturation",
    "limits = {'db': 20, 'payments': 5, 'health': 2}\n",
    "A bulkhead is a wall in a ship. A concurrency limit is how many people may stand in that compartment. When one compartment floods, the wall is what keeps the rest of the ship working.",
    "The checkout service allows 20 in-flight database calls and 5 payment calls. When the payment provider stalls, new checkouts fail fast and the product-read path still has its own pool.",
    "one dependency can get slow",
    "you use one shared unbounded pool for every outbound call",
    ["A limit larger than the dependency can handle.", "No rejection policy.", "Health checks sharing the saturated pool."],
)

add(
    "D13-T021",
    "A timeout bounds how long a caller waits. Cancellation tells the callee to stop. A timeout without cancellation leaves the callee running and holding resources. Deadlines should shrink as they propagate so the inner call gives up before the outer call does. Retries need the remaining budget. A cancelled operation must still leave data consistent.",
    ["Set a deadline at the edge", "Pass the remaining time inward", "Cancel or abandon the inner work on expiry", "Make the side effect idempotent or fenced"],
    "a timed-out request that still charges a card because nobody told the worker to stop, and the client retries",
    "cancel latency and duplicate side effects after a timeout",
    "def remaining(deadline, now):\n    return max(0, deadline - now)\n",
    "A timeout is deciding you will leave the restaurant at 1:00. Cancellation is telling the kitchen to stop cooking. Leaving without telling them wastes the meal and you may be billed.",
    "An API gateway sets a 800 ms deadline. The handler gives the database 500 ms and the rest to rendering. On timeout it cancels the query. The write path uses an idempotency key because cancel may arrive after the commit.",
    "a call can exceed the user's patience or the caller's deadline",
    "you time out and retry a non-idempotent charge with no key",
    ["Timeouts that do not cancel.", "Inner timeouts longer than the outer deadline.", "Ignoring the work that already committed."],
)

add(
    "D13-T022",
    "Structured concurrency keeps child tasks inside a parent's lifetime. The parent waits for the children, or cancels them, before it returns. Errors surface to the parent instead of disappearing into a detached callback. A nursery or a scope is the usual API. It stops the leak where a request ends and a background task still writes.",
    ["Open a scope", "Start children inside it", "Wait or cancel all of them before leaving the scope", "Propagate the first error with a defined policy for the siblings"],
    "a detached task that outlives the request and writes a response nobody needs, or an error that is never observed",
    "tasks still running after the parent scope ends",
    "import asyncio\n\nasync def parent():\n    async with asyncio.TaskGroup() as group:\n        group.create_task(asyncio.sleep(0))\n",
    "Structured concurrency is a teacher who does not leave the museum until every student is back on the bus. Detached tasks are students you hope find their own way home.",
    "A request handler fans out two lookups in a task group. If the client disconnects, the scope cancels both lookups. A fire-and-forget task that writes an audit row needs its own scope owned by a worker, not by the request.",
    "a unit of work has subtasks that must finish or be cancelled with it",
    "you detach a task and hope the process exit cleans it up",
    ["Fire-and-forget on a request.", "Swallowing child errors.", "A scope that waits with no cancellation path."],
)

add(
    "D14-T004",
    "A topic is a named log. A partition is an ordered, append-only shard of that topic. An offset is a consumer's position in a partition. Ordering is guaranteed inside one partition, not across partitions. The partition count bounds consumer parallelism. Keys choose a partition. Changing the partition count changes key placement.",
    ["Append a record to a partition", "Assign it an offset", "Let a consumer read from its stored offset", "Scale consumers up to the partition count"],
    "assuming a global order across partitions, or adding partitions and silently changing which consumer sees a key",
    "consumer lag per partition and whether key order still matches the business rule",
    "def partition_for(key, n):\n    return hash(key) % n\n",
    "A topic is a newspaper. Partitions are separate printing presses. Offsets are the edition number on one press. Two presses do not share a single edition number.",
    "Orders are partitioned by customer id so one customer's events stay ordered. A dashboard that needs a global sequence cannot read two partitions and assume their offsets compare.",
    "you need an ordered log that several consumers can share",
    "you need a total order for every event in the system",
    ["One partition for everything.", "Using offsets as timestamps.", "Changing partition count without a migration plan."],
)

add(
    "D14-T005",
    "A producer appends records to a topic. A consumer reads them. The producer's ack setting decides when a send is successful: leader only, or all in-sync replicas. The consumer's offset decides what it will see again after a crash. Producers and consumers fail independently. A successful produce does not mean a consumer has handled the record.",
    ["Producer sends a record", "Broker appends it", "Consumer fetches it", "Consumer commits an offset after handling"],
    "acking on the leader only and losing the record on a leader failure, or committing an offset before the handler finishes",
    "produce error rate, consumer lag, and duplicate handling after restart",
    "def commit_after(handled):\n    if not handled:\n        raise RuntimeError('do not commit')\n    return 'commit'\n",
    "The producer is the reporter filing a story. The consumer is a reader with a bookmark. The bookmark moving before the reader finishes the story is how they skip a chapter after a nap.",
    "A payment service produces with acks=all. The ledger consumer commits the offset only after the database transaction commits. A crash in between redelivers, and the ledger upsert is idempotent.",
    "work crosses a process boundary through a log",
    "you commit offsets first and do the work second",
    ["Fire-and-forget produces.", "Auto-commit on receive.", "No key and no idempotency."],
)

add(
    "D14-T006",
    "A consumer group divides partitions among its members so each partition is handled by one member at a time. Rebalancing runs when members join, leave, or die, and it moves partition assignments. During a rebalance, progress can pause. A rebalance that is too eager, or a session timeout that is too short, causes a storm. Cooperative protocols move fewer partitions.",
    ["Join the group", "Receive a partition assignment", "Revoke and commit before a rebalance takes partitions away", "Resume from the committed offset"],
    "a long handler that misses the poll timeout, so the member is declared dead and the group rebalances forever",
    "rebalance count and processing pause during rebalance",
    "def assignment(partitions, members):\n    return {m: partitions[i::members] for i, m in enumerate(range(members))}\n",
    "A consumer group is a set of clerks sharing a stack of inboxes. A rebalance is reshuffling the inboxes when a clerk leaves. If you reshuffle every minute, nobody reads.",
    "A deploy restarts consumers one at a time. A short session timeout makes the group rebalance on each restart and lag spikes. A longer timeout and cooperative assignment keep most partitions moving.",
    "several instances should split a topic without double-processing a partition",
    "two groups accidentally share a group id and steal each other's partitions",
    ["Poll intervals shorter than processing.", "Committing during revocation too late.", "One group id for two different applications."],
)

add(
    "D14-T007",
    "A partition key hashes to a partition. All records with the same key share that partition's order. Different keys do not. A null key spreads records and loses per-entity order. A hot key pins a partition. The key should be the entity whose order you care about, and it should have enough cardinality.",
    ["Name the entity that must stay ordered", "Key by that entity", "Check cardinality", "Do not change the hash without a plan"],
    "a hot key that makes one partition lag while others are idle, or a missing key that reorders a user's events",
    "bytes and lag per partition, and the hottest key's share",
    "def key_for(order):\n    return order['customer_id']\n",
    "The key is the label that decides which single-file line you stand in. Everyone with the same label keeps their order. A celebrity label makes one line enormous.",
    "Order events are keyed by order id. Customer-wide order is not guaranteed across orders, and that is acceptable. Keying every event by a constant puts the whole topic on one partition.",
    "you can name the stream that must be ordered",
    "you need global order, which one key cannot scale",
    ["A constant key.", "A key with a time prefix that changes hash.", "Assuming order across keys."],
)

add(
    "D14-T008",
    "Replication copies each partition to several brokers. The leader handles writes. In-sync replicas have caught up within the allowed lag. An ack of all means the in-sync set has the record. If the only in-sync replica is the leader, acks=all does not tolerate a leader loss. Under-replicated partitions are the metric. Unclean leader election can serve a replica that missed writes.",
    ["Write to the leader", "Replicate to followers", "Count a replica in the ISR only when it is caught up", "Acknowledge based on the configured ISR rule"],
    "acks=all with min in-sync replicas of 1, so a single leader acknowledges and then dies with the data",
    "under-replicated partition count and produce errors when the ISR shrinks",
    "def acked(isr_size, min_isr):\n    return isr_size >= min_isr\n",
    "The ISR is the set of clerks who have copied the page. If you accept a promise from a room with one clerk, and that clerk leaves, the page is gone.",
    "A topic uses replication factor 3 and min.insync.replicas 2. A produce with acks=all fails when only one replica remains, which is louder and safer than accepting a write that cannot survive another failure.",
    "a committed message must survive a broker loss",
    "you enable unclean leader election to keep producing at the cost of silent data loss",
    ["Replication factor 1.", "min.insync.replicas left at 1.", "Ignoring under-replicated partitions."],
)

add(
    "D14-T009",
    "At-most-once processing commits the offset before handling, so a crash skips the record. At-least-once handles and then commits, so a crash repeats the record. Exactly-once in a log system is a transactional handshake between the consume offset and the output write, and it still needs an idempotent effect on the real world. The words describe delivery into your handler, not the business outcome, unless the handler participates.",
    ["Choose the commit point", "Make the handler tolerate the resulting duplicate or loss", "Use a transaction only if the output is in the same protocol", "Say the business effect separately"],
    "calling a path exactly-once while the email provider is called outside the transaction and can double-send",
    "duplicate side effects and skipped offsets after a crash test",
    "def effect_key(event):\n    return event['event_id']\n",
    "At-most-once is throwing away the receipt before you file it. At-least-once is filing it and sometimes filing a copy. Exactly-once is one atomic staple around the receipt and the filing cabinet, and only if both are in the cabinet.",
    "A consumer writes a ledger row and commits the Kafka offset in one transaction, which is exactly-once between those two. The subsequent SMS is at-least-once and uses a provider idempotency key.",
    "you can point at where the offset is committed",
    "you promise exactly-once to a third party that has no idempotency key",
    ["Equating broker acks with exactly-once processing.", "Committing before a non-idempotent write.", "Ignoring duplicates because they are rare."],
)

add(
    "D14-T010",
    "An idempotent producer attaches a producer id and a sequence number so the broker can drop a retried send that it already appended. It prevents duplicates from producer retries within that session. It does not make the consumer idempotent. It does not dedupe two different producer instances that both mean the same business event. Enable it when retries are on.",
    ["Assign a producer id", "Sequence each send", "Retry a failed send", "Let the broker reject a duplicate sequence"],
    "two application instances producing the same logical event with different producer ids, so both are stored",
    "duplicate offsets for one logical send after a retry",
    "def same_send(producer_id, seq, seen):\n    return (producer_id, seq) in seen\n",
    "An idempotent producer is a courier with a badge number and a parcel number. The dock refuses a parcel it already scanned from that courier. A different courier with a copy of the letter is a different parcel.",
    "A service enables idempotent produce and retries on timeout. The topic does not grow a duplicate from that retry. The consumer still upserts by order id because a second process may emit the same order.",
    "the producer retries sends",
    "you treat it as business-level deduplication across services",
    ["Retries without idempotence.", "Assuming it covers consumer redelivery.", "Reusing state across a process restart incorrectly."],
)

add(
    "D14-T011",
    "An idempotent consumer can handle the same record more than once and leave the same business state. The usual tools are a unique key, an upsert, or a processed-event table in the same transaction as the side effect. Redelivery is normal after a crash that happened after the write and before the offset commit. Idempotency is a property of the effect, not of the broker.",
    ["Derive a stable id for the event", "Write the effect and the id in one transaction", "Treat a repeated id as success", "Commit the offset after that transaction"],
    "a second email or a second charge because the handler's effect was not keyed",
    "unique-constraint hits on the processed-event table, and duplicate charges",
    "def already_done(db, event_id):\n    return db.insert_ignore('processed', event_id)\n",
    "An idempotent consumer is a clerk who stamps each invoice number and refuses to pay the same number twice, even if the envelope arrives again.",
    "A refund consumer inserts refund_id as a primary key and applies the balance change in that transaction. The second delivery hits the key and does nothing. The offset commit follows the commit.",
    "delivery is at-least-once",
    "the side effect has no stable id and is not safe to repeat",
    ["Deduping only in memory.", "Committing the offset before the transaction.", "Using a random id per receive."],
)

add(
    "D14-T012",
    "A retry repeats a failed handler after a delay. Immediate retries amplify an outage. Backoff and jitter spread them. A retry topic or a delayed queue holds the record off the main partition so one bad record does not block its neighbors forever, depending on ordering needs. Retries must stop. The record then goes to a dead-letter path. A retry of a non-idempotent handler doubles the effect.",
    ["Detect a transient failure", "Wait with backoff and jitter", "Retry a bounded number of times", "Leave the main partition's order story explicit"],
    "a poison record blocking a partition, or a retry storm against a down dependency",
    "retry count per event and the age of the oldest retrying event",
    "def delay(attempt):\n    return min(60, 2 ** attempt)\n",
    "A retry is knocking again later, not pounding the door. A retry topic is a side corridor so the main line can keep moving while one guest waits.",
    "A notification consumer retries three times with jitter when the provider returns 503, then publishes to a retry topic. A 400 is not retried. The send uses an idempotency key.",
    "the failure is transient and the effect is safe to repeat",
    "you retry validation errors or you block the partition on the first failure",
    ["Retrying forever.", "No jitter.", "Blocking every key behind one bad record when order among keys does not matter."],
)

add(
    "D14-T013",
    "A dead-letter queue holds messages a consumer could not process after the retry policy ended, or that failed validation. It is a parking lot, not a trash can. Operators need the reason, the original payload, and a way to replay after a fix. A DLQ that nobody reads is a silent data loss. Poison messages should arrive there without stopping healthy traffic.",
    ["Exhaust retries or fail validation", "Publish to the DLQ with the error", "Alert on depth", "Replay only after the handler is fixed"],
    "an unmonitored DLQ, or a replay that sends the same poison back in a loop",
    "DLQ depth and age of the oldest dead-lettered message",
    "def dead_letter(event, reason):\n    return {'event': event, 'reason': reason}\n",
    "A dead-letter queue is the tray for forms the clerk could not file. Someone still has to look at the tray. Shredding it because it is out of the way loses the form.",
    "A consumer DLQs a message after five tries and pages when the queue is non-empty. A human or a tool replays it once the bug fix is deployed. Automatic replay without a fix recreates the outage.",
    "some messages will fail for a reason a retry cannot cure",
    "you drop them on the floor or you retry them forever on the main path",
    ["No alert.", "Replay without a fix.", "Stripping the failure reason."],
)

add(
    "D14-T014",
    "A delayed message becomes visible to consumers only after a timestamp. Implementations use a delay queue that a timer moves onto the real queue, or broker features such as delayed topics. The delay is for scheduled work, not for sleeping inside a handler. Order with non-delayed messages is not guaranteed. A delay longer than retention disappears.",
    ["Record the not-before time", "Keep the message out of the main consumer until then", "Move it when the time arrives", "Handle clock and retention limits"],
    "a consumer sleeping in-process so a restart loses the delay, or a message whose delay exceeds retention",
    "on-time delivery rate and messages whose visible time is late",
    "def visible(now, not_before):\n    return now >= not_before\n",
    "A delayed message is a letter with a 'do not open until' date sitting in a side drawer, not a clerk staring at the clock.",
    "A trial-ending email is published with a visible time of fourteen days later. A scheduler moves due messages onto the send topic. The worker does not hold a thread asleep for fourteen days.",
    "work must wait without occupying a handler",
    "you sleep in the consumer and call it a delay queue",
    ["In-memory timers as the only copy.", "Delay past retention.", "Assuming FIFO with immediate messages."],
)

add(
    "D14-T015",
    "Backpressure in a log means consumers fall behind and the lag grows. The broker keeps the bytes until retention. That protects producers and risks disk fill and stale processing. A consumer applies backpressure by not fetching more than it can handle. A producer applies it by blocking or failing when the broker rejects. Lag is the age of unprocessed records, not only the count.",
    ["Measure lag in time", "Bound how far a consumer prefetches", "Scale consumers or partitions if the work is parallel", "Shed or slow producers if the lag budget breaks"],
    "a disk full of retained bytes, or a consumer that prefetches a huge batch and then stalls the group",
    "time lag per partition and disk usage of the log",
    "def over_budget(lag_seconds, budget):\n    return lag_seconds > budget\n",
    "Backpressure is the line of unwashed plates. Lag in minutes is how long the oldest plate has been sitting. A count of plates without the age hides a stuck burner.",
    "An orders topic gains ten minutes of lag. Autoscaling consumers helps only up to the partition count. If one key is hot, scaling does nothing and the fix is the key design.",
    "producers and consumers run at different speeds",
    "you alert on message count and miss a stuck partition whose count looks small",
    ["Infinite retention with no disk alarm.", "Prefetch far beyond the handler.", "Adding consumers beyond partitions and expecting speed."],
)

add(
    "D14-T016",
    "An offset commit records how far a consumer group has processed a partition. Committing after a successful handle gives at-least-once. Committing before gives at-most-once. Auto-commit on an interval commits whatever was fetched, which can skip failed records or replay a large batch. Commits are per partition. A commit during a rebalance must happen before the partition is given away.",
    ["Fetch a batch", "Handle each record", "Commit the offsets that are done", "On revocation, commit or accept a replay"],
    "auto-commit marking a failed record as done, or a commit of a later offset while an earlier one failed",
    "replayed records after a restart, and skipped records after a crash",
    "def next_commit(succeeded_offset):\n    return succeeded_offset + 1\n",
    "The offset is a bookmark. Moving the bookmark past a chapter you did not understand is how that chapter is never read again.",
    "The consumer commits offsets for records whose database transaction committed. It does not auto-commit on a timer. After a crash, only the uncommitted tail is replayed.",
    "a group must resume after a restart",
    "you commit the highest offset even though a middle record failed",
    ["Auto-commit with a slow handler.", "Committing before the side effect.", "One commit covering a batch that partially failed."],
)

add(
    "D14-T017",
    "A message schema describes the fields of a record. A schema registry stores those descriptions and their versions under an id. Producers and consumers embed the id and look up the schema, instead of hoping both sides deployed the same class. The registry is a dependency of the produce path if registration is required. A schema without compatibility rules is only documentation.",
    ["Register the schema", "Write the record with the schema id", "Let the consumer resolve the id", "Reject an incompatible change"],
    "a consumer that cannot deserialize a new field or a removed field, stopping the partition",
    "schema registration failures and deserialize errors",
    "def envelope(schema_id, payload):\n    return {'schema_id': schema_id, 'payload': payload}\n",
    "A schema registry is the style guide both the writer and the reader check out by number. The number travels with the article. The guide stays in the library.",
    "An order event uses a registry id. The consumer looks up the id and decodes. A deploy of the producer that adds a required field without a default fails the compatibility check before it ships.",
    "more than one service writes or reads the topic",
    "you serialize language-specific objects with no contract",
    ["No compatibility checks.", "Breaking changes as 'just a deploy'.", "Embedding secrets in schema docs."],
)

add(
    "D14-T018",
    "Schema evolution is changing a contract while old and new code both exist. Backward compatibility lets a new consumer read old data. Forward compatibility lets an old consumer read new data. Full compatibility is both. Adding an optional field with a default is usually safe. Removing a required field or changing a type is not. The order of deploys follows the compatibility direction.",
    ["Classify the change", "Check it against the registry rules", "Deploy consumers or producers in the order the rule requires", "Keep one previous version readable"],
    "a producer rolling out a breaking field before consumers can skip it, halting the group",
    "compatibility-check failures and deserialize errors during a deploy",
    "def backward_ok(added_optional, removed_required):\n    return added_optional and not removed_required\n",
    "Evolution is editing a form so last year's forms still make sense. Adding an optional box works. Renaming a box in place is a new form, whether you meant it to be or not.",
    "A team adds an optional discount_code with a default. Old consumers ignore it. New consumers understand old events. Removing price in the same release would strand old consumers, so that is a new topic or a major version.",
    "rolling deploys of producers and consumers overlap",
    "you change types in place and call it agile",
    ["Deploying a breaking producer first.", "Reusing a field number for a new meaning.", "No default on a newly required field."],
)

add(
    "D14-T019",
    "Event sourcing stores the state of an entity as a sequence of events and rebuilds state by folding them. The log is the source of truth. A projection is a read model derived from the log and can be rebuilt. Snapshots speed the fold. Concurrency uses an expected version. It is a poor fit when you only needed a row and a history table.",
    ["Append an event only if the expected version matches", "Fold events to answer a command", "Update projections asynchronously", "Snapshot so a fold stays cheap"],
    "a projection treated as the source of truth, or a version conflict ignored so two events both think they were next",
    "fold time, projection lag, and version-conflict rate",
    "def fold(events):\n    state = {'balance': 0}\n    for event in events:\n        if event['type'] == 'credited':\n            state['balance'] += event['amount']\n    return state\n",
    "Event sourcing is keeping the receipts and totaling them when you need the balance, instead of erasing the receipts and keeping only the total.",
    "A ledger appends credited and debited events and rejects an event whose expected version is stale. The balance query can use a projection, and a bug in the projection is fixed by replaying the log.",
    "the history is the product or the audit requirement, and you can rebuild state",
    "you only need current state and a simple update",
    ["Updating a row and also emitting an event that can disagree.", "No version check.", "A projection nobody can rebuild."],
)

add(
    "D14-T020",
    "CQRS separates the model that handles commands from the model that handles queries. They can be the same database with different schemas, or a write log and a read projection. The read side is allowed to lag. Commands are not 'create a row shaped like the screen.' The split pays off when reads and writes scale or change differently. It costs consistency and operational surface.",
    ["Handle the command on the write model", "Publish the result as a fact", "Update the read model", "Serve queries from the read model and say if it can lag"],
    "a user who writes and then reads their own change from a lagged view and thinks the write failed",
    "projection lag and read-your-writes failures",
    "def route(op):\n    return 'write-model' if op == 'command' else 'read-model'\n",
    "CQRS is a kitchen that does not plate food from the prep board. The dining room has its own menu copy, and that copy can be a minute behind the kitchen.",
    "An order command writes the order aggregate. The customer list page reads a denormalized table updated by a consumer. The confirmation screen reads the write model so the user sees their own order.",
    "read and write shapes or rates genuinely differ",
    "you split a CRUD form into two services on day one and double the failure modes",
    ["Read-your-writes against a lagged projection.", "Two sources of truth.", "CQRS without a lag budget."],
)

add(
    "D14-T021",
    "The transactional outbox writes the business row and the message row in the same database transaction. A separate publisher reads the outbox and publishes to the broker, then marks the row sent. If the process crashes after the commit and before the publish, the message is still in the table and will be sent. Consumers must be idempotent because the publisher may send twice. Polling or a log reader can drain the outbox.",
    ["Commit state and outbox row together", "Publish the outbox row after commit", "Mark it sent", "Let consumers ignore duplicates"],
    "publishing to the broker inside the database transaction, which can commit the business row and fail the message, or the reverse",
    "outbox rows older than the publish interval, and duplicate publishes",
    "def same_transaction(state_write, outbox_write):\n    return 'commit both or neither'\n",
    "The outbox is a letter copied into the same ledger as the sale. A clerk later carries the letters to the post office. If the clerk trips, the letter is still in the ledger.",
    "An order insert and an outbox row commit together. A worker publishes order.created and sets published_at. A crash retries the publish. The inventory consumer upserts by event id.",
    "a database change must be accompanied by a message",
    "you send the message first and then commit, or the reverse, without a shared transaction",
    ["Dual writes without an outbox.", "No idempotent consumer.", "An outbox nobody polls."],
)

add(
    "D14-T022",
    "Change data capture reads a database's log and emits row changes to another system. It avoids a second write in the application. It sees committed changes, including those from other writers and manual SQL. Schema changes and bulk loads show up. The capture must not fall so far behind that the database cannot recycle its log. It is not a business-level event unless you map rows back to a meaning.",
    ["Read the database log", "Emit inserts, updates, and deletes", "Retain the log until the capture confirms", "Map rows to a contract the consumer understands"],
    "the database deleting WAL a capture has not read, or a consumer treating a raw update as a clean domain event",
    "CDC lag versus log retention, and schema-change failures",
    "def map_row(change):\n    return {'id': change['after']['id'], 'op': change['op']}\n",
    "CDC is photocopying the diary as it is written, instead of asking the clerk to also drop a note in a box. You see every line, including the ones the clerk did not mean as announcements.",
    "A connector streams the orders table into a search index. A migration that updates every row creates a huge change stream. The search pipeline has to tolerate that backfill.",
    "you need to react to committed rows without a dual write",
    "you needed a domain event with intent the row image does not carry",
    ["No retention for the log.", "Assuming CDC events are exactly the domain language.", "Ignoring snapshot plus stream ordering."],
)

add(
    "D14-T023",
    "A saga is a sequence of local transactions with a compensating action for each step that can fail later. It is used when one database transaction cannot span the services. Choreography lets each service react to events. Orchestration gives one coordinator the next step. Compensations must be idempotent and possible. A saga does not give isolation. Other readers can see intermediate states.",
    ["Define each local commit", "Define the compensation", "On failure, run compensations for the steps that committed", "Make intermediate states explicit"],
    "a compensation that cannot undo a real-world effect, such as an email already read, or two sagas interleaving without a semantic lock",
    "saga completion time and compensation failure count",
    "def compensate(steps_done):\n    for step in reversed(steps_done):\n        step.undo()\n",
    "A saga is a trip with a plan for turning around at each station. It is not a single ticket that can be unprinted from every station at once.",
    "An order charges a card, reserves stock, and books a shipment. If shipment fails, the saga refunds the card and releases stock. The customer may have seen 'paid' in between. The API says so.",
    "a business process spans services that cannot share one transaction",
    "one database could have done it atomically",
    ["No compensation.", "Assuming serializability.", "A compensation that is not idempotent."],
)

add(
    "D14-T024",
    "In RabbitMQ, an exchange receives a publish and routes it to queues using bindings. A direct exchange matches a routing key. A topic exchange matches a pattern. A fanout delivers to every bound queue. A queue is what consumers read. The broker, not the consumer group protocol, pushes messages. Durability of exchange, queue, and message are separate flags.",
    ["Publish to an exchange", "Route by the binding", "Store on the queue if durable", "Deliver to a consumer"],
    "a non-durable queue that vanishes on restart, or a binding so wide that every consumer gets every message",
    "queue depth, unroutable message count, and consumer utilisation",
    "def route(exchange, key, bindings):\n    return [q for pattern, q in bindings if pattern == key]\n",
    "An exchange is a sorting table. Bindings are the rules painted on the bins. A queue is one bin. Publishing straight into a bin is a special case, not the whole model.",
    "An order service publishes to an orders exchange with routing key order.created. The email queue and the warehouse queue bind to that key or a pattern. A missing binding returns the message if the publisher asked for it.",
    "you want routing and competing consumers on a broker queue",
    "you need a replayable log of every event for a new consumer next month",
    ["Durable queues with transient messages.", "A fanout you did not mean.", "No dead-letter policy on the queue."],
)

add(
    "D14-T025",
    "A RabbitMQ consumer acknowledges a delivery after handling it. Automatic ack on delivery loses the message if the consumer crashes mid-handler. Manual ack after the work can redeliver if the consumer dies first. A nack or reject can requeue or dead-letter. Redelivery can reorder relative to later messages. Prefetch limits how many unacked deliveries a consumer holds.",
    ["Deliver with a prefetch limit", "Handle the message", "Ack on success", "Nack to requeue or dead-letter on failure"],
    "auto-ack and a crash that loses the message, or a requeue loop of a poison message",
    "unacked count, redelivery rate, and prefetch versus processing time",
    "def should_ack(success, redelivered, attempts, limit):\n    if success:\n        return 'ack'\n    return 'dead-letter' if attempts >= limit else 'requeue'\n",
    "An ack is signing that you filed the paper. If the clerk signs when the paper hits the desk and then faints, the paper is gone. If the clerk signs after filing, a faint means the desk hands the paper out again.",
    "A worker sets prefetch to 10, writes the database, then acks. A poison message is nacked to a dead-letter exchange after three redeliveries so it does not spin at the head of the queue.",
    "the broker is RabbitMQ-style and delivery is at-least-once unless you auto-ack",
    "you auto-ack work you cannot lose",
    ["Unlimited prefetch.", "Requeue forever.", "Ack before the transaction commits."],
)

add(
    "D14-T026",
    "RabbitMQ is a message broker with exchanges, queues, and push delivery. Kafka is a distributed log with partitions, retention, and pull consumers. RabbitMQ is a strong fit for task queues and routing. Kafka is a strong fit for replay, high throughput streams, and several independent consumer groups reading the same history. You can outgrow either by using it as the other.",
    ["Decide whether you need a queue or a replayable log", "Check ordering, retention, and routing", "Match the consumer model", "Do not pick both without a boundary"],
    "using Kafka as a per-task work queue with millions of tiny topics, or using RabbitMQ as an event log you cannot replay",
    "whether a new consumer can read last week's data, and routing complexity",
    "def pick(need_replay, need_routing):\n    if need_replay:\n        return 'log'\n    if need_routing:\n        return 'broker-queue'\n    return 'either-with-a-reason'\n",
    "RabbitMQ is a post office that sorts letters into slots and hands them over. Kafka is a set of bound journals you can reread. Asking the post office for last month's letters fails if they were thrown away after delivery.",
    "Email jobs go to RabbitMQ or a similar queue. The order event history goes to a log so a new fraud service can replay the quarter. Putting both in one technology is fine only if the retention and consumer model still match.",
    "you can say replay versus task routing",
    "you standardize on one broker to avoid thinking about the workload",
    ["Kafka for a single RPC.", "RabbitMQ for a long audit log.", "A religious choice with no requirement."],
)

add(
    "D14-T027",
    "Publish-subscribe delivers each message to every subscriber that asked for that class of message. It is a fan-out. It is different from a work queue, where one of several workers takes the job. If subscribers are offline, a log retains the message and a pure pub/sub bus may not. The subscriber, not the publisher, decides what it cares about, within the filters offered.",
    ["Publish once", "Fan out to current subscriptions", "Retain if offline subscribers matter", "Keep work queues as a separate path"],
    "two workers in a pub/sub both sending the same email because the channel was not a competing-consumer queue",
    "subscriber count versus copies sent, and messages missed while disconnected",
    "def copies(subscribers, competing):\n    return 1 if competing else len(subscribers)\n",
    "Pub/sub is a radio broadcast. A work queue is one walkie-talkie passed to whichever guard is free. Broadcasting a job makes every guard do it.",
    "A price-change event is published so the search index and the cache invalidator each get a copy. The 'send receipt' job is a queue with competing consumers, not a second subscription on the same fan-out.",
    "several independent components must each see the event",
    "exactly one worker must do the job",
    ["Using pub/sub as a work queue.", "No retention for a subscriber that deploys.", "Filters so broad they become a second full copy of every topic."],
)

add(
    "D14-T028",
    "Ordering guarantees say which events a consumer will see in the order they were written. A partition orders its own key. A queue with one consumer orders that queue until redelivery or multiple consumers shuffle it. Global order across partitions does not exist unless you use one partition. Gaps appear when a consumer fails and retries. The business rule should name the entity that needs order.",
    ["Name the stream that must be ordered", "Put it on one partition or one single-consumer queue", "Handle redelivery without breaking the invariant", "Do not promise order you did not build"],
    "two partitions merged by timestamp with clock skew, so a refund is applied before the charge",
    "inversions observed per key in a contract test",
    "def ordered(events):\n    return events == sorted(events, key=lambda e: e['seq'])\n",
    "Ordering is a single-file line. Two doors into the same room do not preserve one line. A person who steps out and comes back through retry can stand in a new place.",
    "Charges and refunds for one payment share a partition key. Across payments, the ledger sorts by its own sequence after applying idempotent events. The team does not promise a global Kafka order.",
    "a business invariant requires one sequence",
    "you need that sequence globally at high throughput",
    ["Sorting by wall clock across machines.", "Multiple consumers on a queue that must stay ordered.", "Ignoring redelivery."],
)

add(
    "D14-T029",
    "A poison message is one a consumer will fail on every time, such as a payload that cannot be parsed or a business rule that will never pass. Retries do not help. If it stays at the head of an ordered partition, it blocks every later message. The handler should detect a deterministic failure and dead-letter it. A crash loop is the symptom.",
    ["Classify the error as deterministic or transient", "Dead-letter deterministic failures immediately", "Retry only transient ones", "Unblock the partition"],
    "one bad payload stalling a partition for the whole tenant or key",
    "retry rate on a single offset, and consumer crash loops",
    "def poison(error):\n    return error in ('decode', 'validation')\n",
    "A poison message is a package that will never fit through the door. Leaving it on the threshold means nobody behind it can enter.",
    "A consumer throws on a negative quantity forever and the partition lag grows. The fix is to DLQ decode and validation errors and alert, while retrying only timeouts from the database.",
    "some failures are properties of the payload",
    "you retry them until the retry budget and the partition are both exhausted",
    ["An unbounded retry.", "No classification of errors.", "Skipping the offset and losing the message with no record."],
)

add(
    "D14-T030",
    "Message deduplication drops a repeat of a message the system already accepted. Brokers can dedupe producer retries for a window. Business dedupe stores the idempotency key for longer than the retry window, in the same transaction as the effect. A short broker window does not cover a consumer that replays yesterday's log. The key must be stable across retries.",
    ["Assign a stable idempotency key at the origin", "Store it with the effect", "Drop a repeat inside the retention of that store", "Do not generate a new key on receive"],
    "a dedupe window shorter than the replay, so the second handling charges the customer again",
    "duplicate effects whose keys arrived twice outside the window",
    "def duplicate(store, key):\n    return not store.add(key)\n",
    "Deduplication is recognizing a receipt number. If you only remember receipt numbers until lunch, the same receipt after lunch gets paid again.",
    "The API gateway stamps Idempotency-Key. The outbox carries it. The consumer inserts it into a unique column kept for thirty days, which covers the broker's retry window and a manual replay.",
    "the same logical event can be delivered more than once",
    "the dedupe memory is shorter than the ways a duplicate can appear",
    ["A new UUID per attempt.", "In-memory sets.", "Broker dedupe only, with a five-minute window, for a financial effect."],
)

add(
    "D14-T031",
    "Replay rereads a log from an earlier offset. Reprocessing applies the handler again. Both are safe only if the handler is idempotent or the output is rebuilt from scratch into a new projection. Replay is how you fix a bug in a consumer or seed a new one. It is not free: it can overload the database and reorder relative to live traffic if you are not careful.",
    ["Choose the offset or the time", "Run the handler in a mode that can repeat", "Isolate a rebuild from live outputs if needed", "Throttle so the source of truth survives"],
    "a replay that sends a second email for every historical order, or that overwrites a newer live update with an older event",
    "duplicate side effects during replay, and load on the database",
    "def replay_mode(rebuild):\n    return 'new-projection' if rebuild else 'idempotent-handler'\n",
    "Replay is reading the diary from March again. Reprocessing is doing the chores written there. If the chores include mailing a letter, you mail it again unless the chore knows the letter already went.",
    "A new search index is built by replaying the order log into a new index name, then swapping. The live email consumer is not pointed at the old offset. A bugfix in the projection is deployed before the replay.",
    "the log still has the history and the handler can repeat or write to a new output",
    "you rewind a live side-effecting consumer with no idempotency",
    ["Replay into production email.", "No throttle.", "Old events overwriting newer state."],
)

add(
    "D14-T032",
    "Orchestration puts a coordinator in charge of the next step of a workflow. The steps are explicit and easier to see, and the coordinator is a dependency. Choreography lets each service react to events and decide its own next step. It avoids a central brain and makes the overall flow harder to see and to change. Many systems orchestrate the business process and choreograph the notifications around it.",
    ["Draw the steps and the failure path", "Choose a coordinator if the sequence is the product", "Choose events if each service can react independently", "Make the whole flow observable either way"],
    "a choreography nobody can draw, or an orchestrator that stores no state and cannot resume",
    "time to answer 'where is this order stuck', and failed workflow count",
    "def style(steps_are_strict):\n    return 'orchestrate' if steps_are_strict else 'choreograph'\n",
    "Orchestration is a conductor with a score. Choreography is dancers who move when they hear a cue. The conductor is easier to follow and is a person who can faint. The dancers keep going and can collide.",
    "Order fulfillment is an orchestrated workflow with a row per step, so support can see 'waiting on warehouse'. A cache invalidation is choreographed from the order event. Mixing them without a picture is how steps get skipped.",
    "you need to see and change a multi-step process",
    "you add a central orchestrator for a single notification",
    ["An orchestrator with no durable state.", "Choreography with no trace of the flow.", "A religious split instead of a per-process choice."],
)

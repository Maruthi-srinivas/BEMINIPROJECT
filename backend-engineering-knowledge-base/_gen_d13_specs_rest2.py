"""D13-T010 .. D13-T022 specs."""
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


MORE_SPECS = [
{
"id": "D13-T010", "next": "D13-T011",
"overview": "The **producer-consumer** pattern decouples stages: producers enqueue items; consumers dequeue and process. A queue is the boundary that absorbs rate differences.",
"principles": "Producers block or drop when queue full (bounded) or grow memory (unbounded). Consumers wait on empty queue. Enables parallel pipelines and thread pool work queues.",
"architecture": "Queue + sync (mutex/condvar or `BlockingQueue`). Multiple producers/consumers common. Kafka topics are distributed producer-consumer at system scale.",
"mermaid": "flowchart LR\n  p[Producers]\n  q[Queue]\n  c[Consumers]\n  p --> q --> c",
"examples": "Analogy: kitchen tickets on a rail. Backend: log ingestion workers draining a buffer.",
"code_file": "d13_t010_producer_consumer.py",
"code": textwrap.dedent('''
import queue
import threading

q: queue.Queue[str] = queue.Queue()


def producer() -> None:
    for i in range(5):
        q.put(f"item-{i}")


def consumer() -> None:
    for _ in range(5):
        print(q.get())


if __name__ == "__main__":
    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    t1.start(); t2.start(); t1.join(); t2.join()
'''),
"code_notes": "Unbounded `Queue` for demo; production uses `maxsize` for backpressure.",
"backend": "Worker pools are producer-consumer with thread pool as consumer side. Stream processors use partitioned consumer groups.",
"trade_rows": [("Unbounded queue", "Never block producer", "OOM risk", "Low spike risk", "Traffic bursts"), ("Bounded queue", "Memory cap", "Producer blocks", "Stable latency", "Must drop/shed"), ("Single consumer", "Ordering simple", "Throughput limit", "Partition key", ""), ("Multiple consumers", "Parallelism", "Ordering complex", "Stateless tasks", "Strict order")],
"mistakes": ["Unbounded queue under traffic spike.", "Poison pill missing for shutdown.", "Shared consumer state without sync.", "One slow consumer blocks head-of-line in single queue.", "Ignoring graceful drain."],
"debug": "Queue depth metric rising → consumers slow or too few. CPU idle with full queue → blocking on I/O in consumer.",
"revision": ["Queue decouples rates.", "Bounded = backpressure.", "Poison pill ends workers.", "Partition for order.", "Pool is special case."],
"completion": ["Draw producer-consumer.", "Shutdown pattern.", "Bounded vs unbounded.", "Kafka as distributed PC.", "Head-of-line blocking."],
"related": ["D13-T004", "D13-T011", "D13-T007"],
**_ex("Bounded queue with 2 producers 1 consumer counting items.", "Queue grows unbounded during spike—fix.", "Kafka vs in-memory queue trade-offs.",
"Use `queue.Queue(maxsize=N)`; producers `put` with timeout or block.", "Bound queue; block producers; scale consumers; shed load at edge.", "Kafka: durability, replay, partitions; memory queue: low latency, no persistence."),
"qa": _qa(
("b","What problem does it solve?","Decouples production rate from consumption rate.",""),
("b","What sits between them?","A queue buffer.",""),
("b","Multiple consumers?","Parallel processing if tasks independent.",""),
("b","Ordering?","Single consumer preserves FIFO; partitions preserve per-key order.",""),
("b","Thread pool relation?","Submitters produce; workers consume (`D13-T004`).",""),
("i","Poison pill?","Special sentinel tells consumers to exit after drain.",""),
("i","BlockingQueue API?","`put` blocks when full; `take` when empty.",""),
("i","Fan-out?","One producer many consumers via shared queue.",""),
("i","Fan-in?","Many producers one consumer aggregates.",""),
("i","Backpressure link?","Bounded queue (`D13-T011`).",""),
("a","Disruptor vs BlockingQueue?","Ring buffer lock-free; lower latency niche.",""),
("a","Priority queue consumers?","Urgent tasks first; starvation risk.",""),
("a","Batch consume?","Amortize lock overhead.",""),
("a","Distributed log as queue?","Offset per consumer group.",""),
("a","Exactly-once processing?","Requires idempotency and transactions.",""),
("s","Memory alert during import job.","Unbounded internal queue.","Bound and throttle producers.",""),
("s","Consumers idle, queue empty, producers error.","Producer crashed; add monitoring.",""),
("s","One poison message loops failures.","Dead letter queue pattern.",""),
("s","Lag grows linearly.","Under-provisioned consumers.",""),
("s","Shutdown loses tasks.","Drain queue before kill.",""),
("f","Backpressure?","(`D13-T011`).",""),
("f","Concurrent collections?","(`D13-T012`).",""),
("f","Scheduling?","(`D13-T014`).",""),
),
},
{
"id": "D13-T011", "next": "D13-T012",
"overview": "**Bounded queues** cap in-flight work; when full, producers slow down—**backpressure** signals upstream to stop overwhelming downstream.",
"principles": "Without bounds, memory grows with arrival rate minus service rate. Reactive streams use `request(n)` credit. TCP window is network backpressure. Block, drop, or shed load explicitly.",
"architecture": "`ArrayBlockingQueue`, asyncio `Queue(maxsize)`, gRPC flow control, HTTP 503 when saturated.",
"mermaid": "flowchart LR\n  fast[Fast producer]\n  buf[Bounded buffer]\n  slow[Slow consumer]\n  fast -->|blocks when full| buf --> slow",
"examples": "Analogy: narrow pipe—water piles up until inlet valve closes. Backend: pause Kafka consumer when DB write lag high.",
"code_file": "d13_t011_bounded_queue.py",
"code": textwrap.dedent('''
import queue
q = queue.Queue(maxsize=2)
q.put(1); q.put(2)
try:
    q.put_nowait(3)
except queue.Full:
    print("backpressure")
'''),
"code_notes": "Third put fails immediately with `put_nowait` when full.",
"backend": "Align HTTP accept rate, in-app queue, thread pool, and DB pool. Propagate 429/503 with Retry-After. Monitor queue depth SLO.",
"trade_rows": [("Block on full", "No drops", "Latency upstream", "Consistency", "SLA strict drop"), ("Drop newest", "Protect system", "Data loss", "Metrics", "Payments"), ("Shed at gateway", "Protect core", "Partial outage", "Overload", ""), ("Unbounded", "Simple code", "OOM death", "Never prod", "")],
"mistakes": ["Unbounded buffers 'temporarily'.", "Backpressure only in one layer.", "Ignoring TCP backpressure while app queues grow.", "No metric on reject rate.", "Blocking producer on event loop thread."],
"debug": "Rising queue depth, GC pressure, latency climb together. Trace where buffer is unbounded.",
"revision": ["Bound every buffer.", "Block drop or shed consciously.", "Pressure propagates upstream.", "Credit-based flow.", "503 is backpressure."],
"completion": ["Define backpressure.", "Three policies when full.", "Reactive `request(n)`.", "Map to thread pool queue.", "TCP window analogy."],
"related": ["D13-T010", "D13-T020", "D13-T003"],
**_ex(
    "Demonstrate Full on bounded queue size 2.",
    "Service OOM despite low CPU.",
    "Block vs drop under viral traffic.",
    "Section F prints backpressure on third item.",
    "Unbounded request body or queue buffering; add limits and streaming.",
    "Block protects correctness; drop protects survival—product decision with retry idempotency.",
),
"qa": _qa(
("b","What is backpressure?","Slowing producers when consumers cannot keep up.",""),
("b","Why bound queues?","Prevent unbounded memory growth.",""),
("b","What when queue full?","Block, fail, or drop depending on policy.",""),
("b","HTTP example?","503/429 tells clients to retry slower.",""),
("b","asyncio Queue maxsize?","`await put` blocks when full.",""),
("i","Reactive Streams credit?","Subscriber requests n items.",""),
("i","Pressure across services?","Propagate via latency or explicit signals.",""),
("i","Little's law intuition?","L = λW; bound L by bounding queue.",""),
("i","Kafka consumer pause?","Stop fetch when processing lag high.",""),
("i","write buffer drain?","Pause reads on socket (`D13-T003`).",""),
("a","End-to-end backpressure?","Hard across many hops; need coordinated limits.",""),
("a","Coalescing vs dropping?","Merge updates reduces load.",""),
("a","Priority shedding?","Drop low-priority traffic first.",""),
("a","Adaptive concurrency?","Lower limits when error rate rises.",""),
("a","Queueing theory for sizing?","Use measured service time distribution.",""),
("s","OOM during file upload spike.","Unbounded read buffer.","Stream with size cap.",""),
("s","Clients retry 503 amplifying load.","Retry storm.","Jittered backoff; rate limit.",""),
("s","Internal queue fine but DB melts.","Missing bulkhead on DB (`D13-T020`).",""),
("s","Event loop blocked on put.","Full queue on same thread.","Use thread-safe offload.",""),
("s","Lag metric flat but memory grows.","Buffer off-heap or native.",""),
("f","Bulkheads?","(`D13-T020`).",""),
("f","Producer-consumer?","(`D13-T010`).",""),
("f","Cancellation?","Drain on shutdown (`D13-T021`).",""),
),
},
]

# Append T012-T022 via import side effect
from _gen_d13_specs_rest3 import FINAL_SPECS  # noqa: E402

MORE_SPECS.extend(FINAL_SPECS)

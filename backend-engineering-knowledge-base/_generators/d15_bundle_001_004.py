"""Topic bundles D15-T001..T004."""
from d15_topic_factory import T, interview_pack, iq

BUNDLE = [
    T(
        id="D15-T001",
        slug="d15-t001-distributed-system-fundamentals",
        name="Distributed system fundamentals",
        subdomain="Distributed system fundamentals",
        deps=["D03-T001", "D03-T002", "D04-T001", "D04-T002", "D13-T001", "D13-T002"],
        related=["D15-T002", "D15-T009", "D16-T001"],
        confused_with=["D13-T016", "D05-T001"],
        overview=(
            "A distributed system is a collection of independent computers that cooperate by exchanging messages over a network. "
            "No single process has a complete view of global state or synchronized clocks. "
            "The concept exists because one machine cannot hold all data, survive all failures, or serve all users with acceptable latency. "
            "In production you see this in microservices, replicated databases, caches, and job workers. "
            "Interviewers use fundamentals to see whether you reason about partial failure, latency, and consistency instead of pretending the cluster is one big computer."
        ),
        principles=(
            "Each node has local memory and a local clock. Cooperation happens through unreliable links: messages can be delayed, duplicated, or lost. "
            "There is no shared memory unless you build it with protocols on top of the network. "
            "A request crosses process boundaries, serialization, load balancers, and possibly several data stores. "
            "Correctness is therefore a property of the protocol and the failure model, not of a single try/except block. "
            "Design starts by naming invariants (for example, an account balance must not go negative) and asking which failures can violate them. "
            "Alternatives to distribution are bigger machines (vertical scale) or batch ETL (eventual consolidation); distribution trades operational complexity for scale and fault isolation."
        ),
        architecture=(
            "Typical components: clients, stateless app tiers, stateful stores, message brokers, and coordination services (discovery, locks, config). "
            "A write path often flows client → API → primary database → async replication → search index. "
            "Each hop adds latency variance and independent failure modes. "
            "State is partitioned or replicated; metadata services track who owns which shard. "
            "Observability spans correlation IDs across hops because a single user action becomes many log lines. "
            "Scaling adds nodes, which increases the chance that at least one node is slow or partitioned at any moment."
        ),
        mermaid="""flowchart LR
  client[Client]
  lb[LoadBalancer]
  api[ServiceInstance]
  db[(PrimaryDB)]
  replica[(Replica)]
  client --> lb --> api --> db
  db -. replication .-> replica""",
        examples=(
            "Analogy: a distributed system is a committee without a shared whiteboard. Members mail minutes to each other; some letters arrive late. "
            "Backend example: checkout calls inventory, payments, and notifications. Any one can time out while the others succeed. "
            "Do not assume a single global order of events unless a protocol provides it. "
            "Do not treat RPC as a local function call; timeouts mean the outcome may be unknown."
        ),
        code_file="d15_t001_unknown_outcome.py",
        code="""
def charge_with_timeout(payment_client, order_id: str, timeout_s: float) -> str:
    \"\"\"Return 'ok', 'failed', or 'unknown' when the network can hide the result.\"\"\"
    try:
        payment_client.charge(order_id, timeout=timeout_s)
        return "ok"
    except payment_client.Timeout:
        return "unknown"
    except payment_client.PaymentError:
        return "failed"


class FakePay:
    class Timeout(Exception):
        pass

    class PaymentError(Exception):
        pass

    def charge(self, order_id: str, timeout: float) -> None:
        if order_id.endswith("slow"):
            raise self.Timeout()
        if order_id.endswith("bad"):
            raise self.PaymentError()
""",
        backend=(
            "Treat every outbound call as having three outcomes: success, definitive failure, and unknown (timeout). "
            "Persist intent before irreversible side effects when possible. "
            "Use health checks per dependency, not one global flag. "
            "Capacity planning includes cross-service fan-out: one API request may become ten internal calls. "
            "Security boundaries repeat at each hop (authn/z, TLS, input validation)."
        ),
        tradeoffs_table="""| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Monolith | Simple reasoning | Limited scale | Early product | Independent scaling needs |
| Microservices | Isolation, team scale | Partial failures, ops load | Clear domain seams | No platform maturity |
| Sync RPC | Simple flow | Cascading latency | Low fan-out | Deep call chains |
| Async messaging | Decoupling | Complexity, ordering | Peak smoothing | Need immediate read-your-writes |""",
        mistakes=[
            "Assuming if a client got no error, the server definitely committed work.",
            "Using wall-clock timestamps across regions as if they were a total order.",
            "Sharing mutable process-global caches without invalidation across instances.",
            "Ignoring tail latency when setting synchronous timeouts.",
        ],
        debug=(
            "Symptoms: mysterious duplicates, stuck orders, or users seeing different data on refresh. "
            "Root causes often include retries without idempotency, missing correlation IDs, or reading from a lagging replica. "
            "Diagnosis: trace one request ID across services, check replication lag metrics, and compare primary versus replica reads. "
            "Mitigation: tighten timeouts with budgets, add idempotency keys, and document unknown-outcome handling."
        ),
        revision=[
            "Distribution adds message passing, not shared memory.",
            "Timeouts create unknown outcomes.",
            "Each hop can fail independently.",
            "Invariants must be enforced by protocols.",
        ],
        flashcards=[
            "What is partial failure? Some components fail while others keep running.",
            "Why correlate logs? One user action spans many services.",
        ],
        completion=[
            "Explain why RPC is not a local call.",
            "Name three outcomes of an external call under timeout.",
            "Sketch client → LB → service → DB with replication.",
        ],
        interview=interview_pack(
            iq(
                (
                    "What is a distributed system?",
                    "Independent computers cooperating via messages without shared memory or a perfect global clock. "
                    "Scale and fault tolerance motivate the split. "
                    "Correctness depends on protocols handling delay and loss. "
                    "Backend work is mostly about boundaries and failure modes.",
                ),
                (
                    "Why can't we treat a cluster as one computer?",
                    "There is no atomic read of all RAM, clocks drift, and networks partition. "
                    "A single slow disk on one replica affects only part of the system but clients still see anomalies. "
                    "Software must explicitly coordinate. "
                    "That coordination has latency and availability costs.",
                ),
                (
                    "What is a partial failure?",
                    "Some nodes or links fail while others continue. "
                    "Unlike a single process crash, the system may be half alive. "
                    "Callers can hang, succeed locally, or see stale data. "
                    "Design assumes this is normal, not exceptional.",
                ),
                (
                    "What is latency variance and why does it matter?",
                    "Most requests are fast but a fraction are very slow (tail). "
                    "Synchronous chains multiply tail risk. "
                    "Users experience the slowest hop in a critical path. "
                    "You set deadlines and shed load based on tails, not averages.",
                ),
                (
                    "What is the difference between scale-up and scale-out?",
                    "Scale-up uses a bigger machine; scale-out adds machines. "
                    "Scale-out needs partitioning or replication. "
                    "Scale-out increases coordination overhead. "
                    "Most large backends combine both until economics favor out.",
                ),
            ),
            iq(
                (
                    "How does a load balancer change failure semantics?",
                    "It retries on another instance when one fails or times out. "
                    "That can convert a crash into a duplicate request if the first attempt actually succeeded. "
                    "Health checks may lag real failure. "
                    "Idempotency and outbox patterns address the duplicate risk.",
                ),
                (
                    "Why are correlation IDs necessary?",
                    "They stitch logs across services for one user action. "
                    "Without them, debugging partial failure is guesswork. "
                    "They should propagate on every outbound call. "
                    "They do not fix correctness by themselves.",
                ),
                (
                    "What is fan-out and its risk?",
                    "One inbound request triggers many outbound calls. "
                    "Failure probability grows with the number of dependencies. "
                    "Parallel calls reduce latency but increase load spikes. "
                    "Bulkheads and circuit breakers limit blast radius.",
                ),
                (
                    "How do you reason about unknown outcomes?",
                    "After a timeout you do not know if the server committed. "
                    "Safe systems reconcile with idempotent retries or a durable workflow state. "
                    "Blind retries can double-charge. "
                    "Never map unknown to success for money movement.",
                ),
                (
                    "What is the role of a message broker here?",
                    "It decouples producers and consumers in time. "
                    "It enables at-least-once delivery unless you add deduplication. "
                    "Ordering guarantees are limited to partitions. "
                    "It is not a replacement for a transactional database.",
                ),
            ),
            iq(
                (
                    "How does the fallacies of distributed computing show up in APIs?",
                    "Developers assume latency is zero, bandwidth infinite, and the network secure. "
                    "Production violates each assumption daily. "
                    "APIs need timeouts, payload limits, and auth on every hop. "
                    "Client SDKs should surface retryable versus fatal errors.",
                ),
                (
                    "What is tail-at-scale?",
                    "As you add machines, the chance that some machine is slow rises. "
                    "A request touching many machines waits on the slowest. "
                    "Mitigations include hedged requests, backup requests, and smaller cells. "
                    "You still need backpressure.",
                ),
                (
                    "Why is determinism hard across nodes?",
                    "Threads on one machine share ordering via locks; remote nodes do not. "
                    "Race outcomes depend on message delivery order. "
                    "You need explicit concurrency control or CRDT-style merges. "
                    "Tests must inject delays and reorderings.",
                ),
                (
                    "How does caching interact with distribution?",
                    "Each instance may cache different values. "
                    "Invalidation must cross process boundaries. "
                    "TTL alone allows stale reads. "
                    "Choose cache aside or write-through with clear consistency goals.",
                ),
                (
                    "What is a cell-based architecture?",
                    "Partition users or tenants into isolated stacks. "
                    "Failures stay inside a cell. "
                    "Cross-cell operations are rarer and more expensive. "
                    "Useful at very large scale, not day one.",
                ),
            ),
            iq(
                (
                    "Checkout times out after payment but inventory deducted. What happened?",
                    "Likely partial success: inventory service committed while payment RPC timed out. "
                    "Without a saga or compensating action, stock is wrong. "
                    "Check idempotency keys and workflow state. "
                    "Reconcile with payment provider before refunding blindly.",
                ),
                (
                    "Users see alternating values on refresh. First diagnosis?",
                    "They may hit different app instances reading different replica lag. "
                    "Or a cache without shared invalidation. "
                    "Compare read path: primary vs replica vs CDN. "
                    "Fix by sticky consistency or read-your-writes routing.",
                ),
                (
                    "Deploy doubles error rate only on one region. Why?",
                    "Partial rollout or regional dependency failure. "
                    "Check per-region health of downstream databases. "
                    "A partition can isolate region from primary writer. "
                    "Failover rules may route writes incorrectly.",
                ),
                (
                    "p99 latency spikes after adding a microservice. Explain?",
                    "Extra network hop and serialization added tail risk. "
                    "Cold JVM or connection pool churn may contribute. "
                    "Synchronous chains amplify tails. "
                    "Consider async handoff or colocate hot path.",
                ),
                (
                    "Logs show success but customer says action failed. Next step?",
                    "Client may have timed out before response arrived. "
                    "Verify server-side idempotency record and client retry behavior. "
                    "Align on whether unknown timeout means failure to user. "
                    "Add end-to-end acknowledgment if business requires it.",
                ),
            ),
            iq(
                (
                    "How does this connect to OS threads?",
                    "Threads share memory on one host; distributed nodes do not. "
                    "Mutexes do not protect remote state. "
                    "See `D03-T001` for local concurrency.",
                ),
                (
                    "How does this connect to TCP?",
                    "TCP gives reliable byte streams between two endpoints, not end-to-end business guarantees. "
                    "Connections reset mid-request still create unknown outcomes.",
                ),
                (
                    "How does this connect to API gateways?",
                    "Gateways terminate TLS, enforce auth, and aggregate calls. "
                    "They add another failure point and timeout budget consumer.",
                ),
            ),
        ),
        ex1="Implement `charge_with_timeout` and classify three order_ids: normal, slow (timeout), bad (failed). Document why 'unknown' must not be treated as paid.",
        ex2="A support ticket says payment failed but finance shows a capture. List three log fields you need across services and the reconciliation order.",
        ex3="Choose sync RPC versus async event for post-checkout email. State consistency and failure handling for each.",
        ex1_short="Implement charge_with_timeout with ok/failed/unknown outcomes.",
        ex2_short="Debug payment failed vs captured with cross-service logs.",
        ex3_short="Compare sync vs async for post-checkout email.",
        sol1="Return unknown on timeout; only 'ok' marks paid. Tests: order_ok→ok, order_slow→unknown, order_bad→failed.",
        sol2="Need correlation_id, idempotency_key, payment_provider_id; reconcile provider ledger before mutating local refund state.",
        sol3="Email can be async at-least-once with idempotent send; sync RPC blocks checkout and couples availability.",
    ),
]

"""D14-T001 .. D14-T008 content specs."""

from d14_helpers import completion, paragraphs, qa
from d14_spec_utils import interview_from_levels, sent, spec

S = sent

SPECS_A: dict = {}

SPECS_A["D14-T001"] = spec(
    overview=paragraphs(
        "A message queue is a broker-mediated buffer where producers send messages and consumers compete to process them; once acknowledged, the message is typically removed from the queue.",
        "An event stream is an append-only, partitioned log (Kafka is the canonical example) where records stay for a retention period and many consumer groups read independently at their own offsets.",
        "Queues optimize for task distribution and decoupling in time: work is handed off and drained. Streams optimize for durable history, fan-out, and replay for new consumers or bug fixes.",
        "Interviewers contrast them because teams pick the wrong tool: using a queue when they need replay and audit, or using a stream when they need strict per-message deletion and classic competing consumers without log semantics.",
    ),
    first_principles=paragraphs(
        "Both patterns solve coupling: the producer does not need the consumer online at send time. The difference is what happens to data after delivery.",
        "In a queue mental model, the message is a unit of work with a single successful consumer in many designs (point-to-point). Durability exists, but the primary lifecycle ends at consumption.",
        "In a stream mental model, the message is a fact appended to a timeline. Consumers are cursors into that timeline. Reprocessing is a feature, not a failure mode.",
        "Backpressure appears in both: queue depth grows when consumers are slow; stream consumer lag grows when poll loops cannot keep up with append rate.",
    ),
    internal=paragraphs(
        "Queue brokers (RabbitMQ, SQS, Azure Service Bus) route through exchanges or topics into queues, track unacked deliveries, and delete or dead-letter after ack.",
        "Stream brokers (Kafka, Pulsar log, Kinesis) assign each record an offset per partition, replicate segments to followers, and expose fetch APIs keyed by offset.",
        "Operational components differ: queues emphasize binding topology and redelivery counts; streams emphasize partition count, ISR health, and consumer group coordination.",
        "Hybrid products blur lines (Kafka with compacted topics vs Rabbit streams), but interview answers should state the default semantics of each family.",
    ),
    mermaid="""flowchart LR
  producer[ProducerService]
  queueBroker[QueueBroker]
  workerA[ConsumerWorkerA]
  workerB[ConsumerWorkerB]
  streamBroker[StreamLog]
  group1[ConsumerGroupAlpha]
  group2[ConsumerGroupBeta]
  producer --> queueBroker
  queueBroker --> workerA
  queueBroker --> workerB
  producer --> streamBroker
  streamBroker --> group1
  streamBroker --> group2""",
    diagram_caption="Left path: competing consumers on a queue. Right path: one log, multiple independent consumer groups with separate offsets.",
    examples=paragraphs(
        "Analogy: a queue is a to-do tray where one person takes a ticket and the ticket leaves the tray. A stream is a ledger everyone can read from different pages; copying a page does not erase the ledger.",
        "Backend: enqueue `SendEmail` jobs on SQS for workers. Publish `OrderPlaced` events to Kafka so billing, analytics, and search each consume from the same topic with different groups.",
        "Do not call Kafka a queue just because it buffers work. Competing consumers within one group share partitions, but the log remains and replay is always possible within retention.",
    ),
    practical=paragraphs(
        "Choose a queue when you need simple work distribution, per-message TTL, and clear removal after success without retaining full history.",
        "Choose a stream when multiple teams need the same events, you need ordered partitions per key, or you must rebuild state by replay.",
        "Observability: queue depth and age of oldest message; stream consumer lag per partition and rebalance frequency.",
        "Failure handling: both need idempotent consumers for at-least-once; streams additionally need careful offset commit strategy.",
    ),
    trade_rows=[
        ("Classic queue", "Simple competing consumers", "Weak replay story", "Task queues, RPC async", "Audit log of all facts"),
        ("Event stream", "Replay and fan-out", "Operational complexity", "Event backbone, CDC", "Single consumer deletes work"),
        ("Managed queue (SQS)", "Low ops", "Vendor limits, visibility timeout quirks", "Cloud-native workers", "Custom ordering across shards"),
        ("Kafka stream", "Throughput and retention", "Partition and ISR tuning", "High-volume domain events", "Tiny side-effect jobs only"),
    ],
    mistake_list=[
        "Assuming Kafka deletes messages on read like SQS after ack.",
        "Using a queue for event sourcing without an external store of facts.",
        "Ignoring ordering: only partition-key order is guaranteed in Kafka, not global topic order.",
        "Treating fan-out as multiple queues duplicating publish logic instead of one stream and multiple groups.",
    ],
    debugging=[
        "Symptom: duplicate processing. Check delivery semantics and idempotency keys, not only broker settings.",
        "Symptom: lost messages. For queues, verify ack before delete; for Kafka, check `acks`, `min.insync.replicas`, and producer retries.",
        "Compare end-to-end latency vs broker latency to see if consumers or network bound.",
    ],
    interview=interview_from_levels(
        beginner=[
            ("What is the main difference between a queue and an event stream?", S(
                "A queue usually hands a message to one competing consumer and removes it after successful processing.",
                "A stream appends records to a durable log retained for a policy window.",
                "Multiple consumer groups can read the same stream independently at different offsets.",
                "Queues emphasize work distribution; streams emphasize history and fan-out.",
            )),
            ("Why decouple with messaging instead of synchronous HTTP?", S(
                "The producer can finish when the broker accepts the message instead of waiting for downstream slowness or outages.",
                "Consumers can scale independently and absorb bursts via backlog.",
                "You still pay complexity in delivery guarantees and observability.",
                "It is a latency and availability trade-off, not a free performance win.",
            )),
            ("What is consumer lag in streaming systems?", S(
                "Lag is how far a consumer group's committed offset trails the log end.",
                "High lag means processing cannot keep up with publish rate or consumers are stalled.",
                "Lag is per partition in Kafka, so one hot partition can dominate.",
                "Alerts on max lag across partitions catch partial skew.",
            )),
            ("Can multiple services read the same message in a queue?", S(
                "Classic point-to-point queues deliver to one consumer per message.",
                "Fan-out requires multiple queues, pub/sub, or a stream.",
                "Duplicate reads from one queue usually mean redelivery after failure, not intentional broadcast.",
                "Design explicit topology instead of relying on accidental duplicates.",
            )),
            ("What does retention mean for a stream?", S(
                "Retention is how long records remain addressable by offset or time.",
                "After retention, old segments are deleted and replay before that horizon is impossible.",
                "Compacted topics keep latest key value but still obey compaction rules.",
                "Retention is a storage cost knob tied to replay requirements.",
            )),
        ],
        intermediate=[
            ("When would you pick SQS over Kafka?", S(
                "SQS fits when you want managed ops, moderate throughput, and clear queue semantics without running a cluster.",
                "Kafka fits when you need very high throughput, long retention, and many independent readers on one log.",
                "SQS visibility timeout and at-least-once semantics require idempotent workers.",
                "Cost models differ: per-request vs cluster storage and cross-AZ traffic.",
            )),
            ("How does competing consumption differ in Kafka vs RabbitMQ?", S(
                "Rabbit delivers messages to one consumer on a queue unless you duplicate bindings.",
                "Kafka assigns each partition to at most one consumer in a group at a time.",
                "Parallelism in Kafka is bounded by partition count for a group.",
                "Adding consumers beyond partitions leaves some idle until repartitioning.",
            )),
            ("What is the replay cost of choosing a stream?", S(
                "Replay re-reads bytes from disk and re-executes side effects unless consumers are idempotent.",
                "Downstream databases may see duplicate writes without dedupe keys.",
                "You must cap retention and monitor storage growth.",
                "Replay is powerful for fixes but dangerous without idempotent handlers.",
            )),
            ("How do poison messages differ between queue and stream?", S(
                "Queues often move poison messages to a DLQ after N redeliveries.",
                "Streams keep the record; a failing consumer loops or stalls lag unless you skip with care.",
                "Both need classification of transient vs permanent errors.",
                "Streams may use side topics for quarantine while preserving the log.",
            )),
            ("What metrics prove you chose the wrong pattern?", S(
                "Needing historical events you no longer have suggests queue without archive.",
                "Operating many duplicate publisher-to-queue fan-out paths suggests missing stream.",
                "Extremely low volume with heavy Kafka ops may be over-engineering.",
                "Metrics: duplicate rate, lag, DLQ rate, and cost per million messages.",
            )),
        ],
        advanced=[
            ("How do transactions change the queue vs stream decision?", S(
                "Neither broker participates in your database transaction by default.",
                "Outbox or CDC bridges DB commits to messaging.",
                "Kafka transactions coordinate consume-transform-produce within the cluster but not your RDBMS.",
                "Exactly-once end-to-end still requires application design; it is not free.",
            )),
            ("Explain log compaction vs queue deletion.", S(
                "Compaction retains the latest record per key for changelog topics.",
                "Queues delete on ack regardless of key history.",
                "Compaction supports rebuilding state from Kafka for KV-style stores.",
                "It is unsuitable when you need every event instance retained.",
            )),
            ("How does ordering interact with horizontal scale?", S(
                "Global order requires a single shard or single partition.",
                "Partition by business key to get per-entity order with parallel partitions.",
                "Queues with multiple consumers lose global order unless sharded.",
                "Interviewers want partition key design, not vague 'Kafka is ordered'.",
            )),
            ("What failure domain does the broker add?", S(
                "Brokers become availability dependencies for async paths.",
                "Multi-AZ and replication reduce risk but add latency and ops.",
                "Split-brain and misconfigured ISR can still lose writes if producers ack too early.",
                "Runbooks must cover broker loss and consumer group rebalance storms.",
            )),
            ("When is dual-write acceptable?", S(
                "Dual-write (DB then message) is simple but can diverge on partial failure.",
                "Prefer outbox or CDC for consistency.",
                "Dual-write may be tolerated for non-critical notifications with reconciliation jobs.",
                "Document the accepted inconsistency window explicitly.",
            )),
        ],
        scenarios=[
            ("Product wants analytics on every click but also a task queue for emails. One broker or two?", S(
                "Use a stream for click facts with long retention and a queue or dedicated topic for email jobs.",
                "Do not overload one SQS queue as analytics history.",
                "Email workers need retries and DLQ; analytics may tolerate lag.",
                "Separate failure domains and scaling knobs.",
            )),
            ("After deploy, finance sees duplicate charges. Queue or stream more likely culprit?", S(
                "Duplicates happen with at-least-once and missing idempotency on either pattern.",
                "Streams make duplicates visible on replay; queues on redelivery.",
                "Check idempotency keys and whether ack happened before side effect commit.",
                "Fix consumer semantics before blaming the broker brand.",
            )),
            ("You must rebuild search index from past orders. Current system uses Rabbit only.", S(
                "Rabbit without archived messages cannot replay history.",
                "Migrate publishing to Kafka or store events in an event store.",
                "Backfill from database snapshots plus CDC going forward.",
                "This is why streams exist alongside queues.",
            )),
            ("Traffic 10x for one hour. Which pattern absorbs burst better?", S(
                "Both absorb via backlog if consumers scale.",
                "Queues may throttle producers when full depending on product.",
                "Kafka absorbs in log segments if disk and ISR healthy; lag rises.",
                "Autoscale consumers/partitions ahead of time; lag alerts page before disk full.",
            )),
            ("Compliance requires 7-year audit of domain events. Retention on Kafka?", S(
                "Seven years on hot Kafka is expensive; tiered storage or archive to object store.",
                "Queues are wrong as sole audit store.",
                "Consider event store or warehouse ingest with immutability controls.",
                "Legal hold may forbid compaction that drops records.",
            )),
        ],
        follow_ups=[
            ("How does this relate to `D14-T026` RabbitMQ vs Kafka?", S(
                "That topic compares products directly; this one establishes pattern vocabulary.",
                "Bring concrete exchange types and partition math there.",
                "Here, anchor on lifecycle: delete vs retain.",
                "Interviewers chain both questions in system design loops.",
            )),
            ("What networking topics matter?", S(
                "TCP connection pools to brokers, TLS, and cross-AZ latency affect producer batching.",
                "See `D04-T004` TCP vs UDP; Kafka uses long-lived TCP.",
                "Timeouts must align with retry policies.",
                "Network partitions trigger consumer rebalance and ISR shrink.",
            )),
            ("Does async messaging remove need for idempotency?", S(
                "No. At-least-once is the practical default.",
                "Idempotent consumers are mandatory for money and inventory.",
                "Exactly-once in Kafka costs transactions and still needs external idempotency for side effects.",
                "See `D14-T011` for consumer patterns.",
            )),
        ],
    ),
    ex1_section="Sketch a decision table: for `OrderPlaced`, choose queue vs stream and list one metric per choice.",
    ex2_section="Logs show messages processed twice after a consumer crash. Name whether queue redelivery or stream offset commit is more likely and the fix.",
    ex3_section="Argue for Kafka vs SQS for a new notification worker at 500 msgs/sec with no replay requirement.",
    ex1_prompt="Write the decision table for OrderPlaced (queue vs stream) with metrics.",
    ex2_prompt="Diagnose duplicate processing after consumer crash (queue vs stream).",
    ex3_prompt="Kafka vs SQS for notification workers at 500 msg/s without replay.",
    ex1_solution="Stream if multiple subscribers need the same event or replay; queue if single worker pool and delete-on-success. Metrics: consumer lag vs queue depth.",
    ex2_solution="Likely at-least-once redelivery or commit-after-process failure; fix with idempotent handler and commit offsets after side effects or use outbox.",
    ex3_solution="SQS is reasonable at 500/s with managed ops; Kafka if you already operate a cluster or anticipate fan-out/replay soon.",
    revision="- Queue: compete and remove. Stream: append, retain, multiple groups.\n- Pick stream for replay/fan-out; queue for task distribution.\n- Lag vs depth metrics.\n- Idempotency required either way.",
    related="Understand before: `D04-T001`, `D05-T001`. Supports: `D14-T003`, `D14-T024`, `D14-T026`. Often confused with: pub/sub product names vs log semantics.",
    completion=completion(
        "Contrast queue and stream lifecycle without hand-waving.",
        "Pick a broker pattern for a given fan-out and replay requirement.",
        "Name metrics that show consumer overload.",
        "Explain why duplicates appear under at-least-once.",
    ),
)

# Additional topics D14-T002 .. T008 continue in same file
SPECS_A["D14-T002"] = spec(
    overview=paragraphs(
        "Synchronous communication blocks the caller until the callee responds: HTTP/gRPC with the caller waiting on the wire.",
        "Asynchronous communication returns after the message is accepted by a broker or local executor; completion happens later via callback, poll, or event.",
        "Event-driven architecture composes services through events rather than chained RPC, improving autonomy at the cost of distributed tracing and consistency.",
        "Interviews test whether you know when async hides failures until later and how that changes SLAs and user experience.",
    ),
    first_principles=paragraphs(
        "Coupling dimensions include time (must both be up?), space (must know address?), and semantics (who owns the contract?).",
        "Sync couples time tightly: timeouts define partial failure. Async decouples time but shifts failure to consumer processing.",
        "Backpressure in sync manifests as thread pool exhaustion and latency SLO breaches; in async as queue depth and lag.",
        "Consistency: sync read-your-writes is easier to reason about; async needs sagas, outbox, or eventual consistency narratives.",
    ),
    internal=paragraphs(
        "Sync path: DNS, LB, connection pool, handler, DB, response serialization. Circuit breakers short-circuit downstream sync calls.",
        "Async path: producer serializes envelope, broker persists, consumer deserializes, idempotent handler, offset ack.",
        "Hybrid is common: HTTP command returns 202 Accepted with a resource id while work continues via queue.",
        "Correlation ids must flow across both styles for observability.",
    ),
    mermaid="""sequenceDiagram
  participant Client
  participant Api as ApiService
  participant Broker
  participant Worker
  Client->>Api: POST_sync
  Api-->>Client: 200_with_result
  Client->>Api: POST_accepted
  Api->>Broker: publish_event
  Api-->>Client: 202_accepted
  Broker->>Worker: deliver_message
  Worker-->>Broker: ack""",
    examples=paragraphs(
        "Sync: payment authorization that must approve or decline before showing UI. Async: send receipt email after payment captured.",
        "Do not make checkout async without telling the user; do make fraud scoring async if you can ship with a hold.",
        "Anti-pattern: long HTTP chains of five services without timeouts—async events reduce blast radius.",
    ),
    practical=paragraphs(
        "Use sync for queries needing immediate authoritative answer and user-blocking commands with small latency budget.",
        "Use async for side effects, notifications, analytics, and peak shaving.",
        "Define SLAs per path: API p99 vs processing p99 for background work.",
        "Implement health that covers broker connectivity and consumer lag, not only HTTP /health.",
    ),
    trade_rows=[
        ("Sync RPC", "Simple mental model", "Cascading failure", "User-facing reads", "Long side-effect chains"),
        ("Async events", "Decouples teams", "Harder debugging", "Notifications, ETL", "Need immediate strong consistency"),
        ("202 + polling", "Clear UX contract", "Client complexity", "Long jobs minutes+", "Sub-second results"),
        ("Webhook callback", "Push completion", "Retry security", "Partner integrations", "Internal only traffic"),
    ],
    mistake_list=[
        "Calling async 'faster' when it only moves latency to the consumer.",
        "Missing timeout and cancellation on sync calls.",
        "No idempotency on async handlers.",
        "Returning 200 before work is durable in the broker.",
    ],
    debugging=[
        "Trace stuck orders: follow correlation id from HTTP through outbox publish to consumer logs.",
        "Spiky 503s: sync dependency down; check circuit breaker metrics.",
        "User sees success but email missing: async path failed after HTTP committed—need outbox or status API.",
    ],
    interview=interview_from_levels(
        beginner=[
            ("What is synchronous vs asynchronous communication?", S(
                "Sync waits for the response before continuing the caller logic.",
                "Async hands off work and continues; result arrives later.",
                "The distinction is about caller blocking, not necessarily multi-threading.",
                "HTTP can be async on the server while the client still waits unless using callbacks or events.",
            )),
            ("Why use async between microservices?", S(
                "It reduces cascading latency when downstream is slow.",
                "It lets each service scale consumers independently.",
                "It avoids tight uptime coupling during deploys.",
                "You trade immediate consistency for resilience.",
            )),
            ("What is an event in event-driven architecture?", S(
                "An immutable notification that something happened in the past tense domain language.",
                "Consumers react without the producer calling them by name.",
                "Events carry schema version and correlation identifiers.",
                "Commands differ: they request action and often use sync or dedicated command channels.",
            )),
            ("Does async imply eventual consistency?", S(
                "Often yes for cross-service reads.",
                "You can still read your own writes in the same service database.",
                "Cross-service strong consistency usually needs distributed transactions, which are rare.",
                "Document which reads are stale-tolerant.",
            )),
            ("What HTTP status suggests async acceptance?", S(
                "202 Accepted means accepted for processing, not completed.",
                "Clients should poll a status resource or wait for webhook.",
                "200 implies the operation finished unless documented otherwise.",
                "Misused 200 causes UX bugs when work fails later.",
            )),
        ],
        intermediate=[
            ("How do timeouts differ sync vs async?", S(
                "Sync timeouts bound user-visible latency and trigger retries at caller.",
                "Async timeouts apply to broker publish and consumer processing separately.",
                "Consumer processing may exceed HTTP timeout by design.",
                "Align retry policies to avoid duplicate side effects.",
            )),
            ("When is choreography preferable to orchestration?", S(
                "Choreography uses events between services without a central controller.",
                "It scales team autonomy when flows are simple and well bounded.",
                "Complex compensations favor orchestrator or saga manager.",
                "See `D14-T032` for workflow comparison.",
            )),
            ("How does async affect API versioning?", S(
                "Events are contracts like REST schemas.",
                "Additive schema changes with compatibility rules prevent consumer breaks.",
                "Dual publishing during migration is common.",
                "Registry and consumer-driven contracts reduce surprises.",
            )),
            ("What is the thundering herd after recovery?", S(
                "Many consumers or clients retry simultaneously when a dependency returns.",
                "Async backlog drains suddenly and can overload DB.",
                "Use jittered backoff and rate limits on consumers.",
                "Sync clients exhibit the same on HTTP retries.",
            )),
            ("How do you test async flows?", S(
                "Contract tests on event schemas plus integration tests with embedded broker.",
                "End-to-end tests need deterministic wait on lag or test hooks.",
                "Load tests must include consumer scale, not only producer TPS.",
                "Chaos on broker partitions validates rebalance behavior.",
            )),
        ],
        advanced=[
            ("How does CAP apply to async pipelines?", S(
                "Under partition, you choose between availability of accepting messages and consistency of ordering duplicates.",
                "Brokers may remain available while consumers see lag or duplicates.",
                "Design idempotency and monotonic offsets.",
                "CAP is about trade-offs, not a slogan.",
            )),
            ("Explain sync-over-async anti-pattern.", S(
                "Blocking HTTP thread waiting on internal queue drain mimics sync with extra hops.",
                "It adds latency without decoupling benefits.",
                "Prefer direct sync or true async with 202.",
                "Measure thread pool utilization to detect this.",
            )),
            ("How do sagas relate to async?", S(
                "Sagas coordinate long-running business transactions via events and compensations.",
                "They assume partial failure and at-least-once delivery.",
                "Orchestrated sagas use a coordinator; choreographed use event chains.",
                "See `D14-T023`.",
            )),
            ("What is causal ordering across services?", S(
                "Not guaranteed globally without shared partition key or sequencing layer.",
                "Use correlation ids and version fields in events.",
                "Consumers must tolerate reordering within slack window.",
                "Violations show up as impossible states in domain logs.",
            )),
            ("How does backpressure propagate async?", S(
                "Slow consumers increase lag; some brokers push back on producers via errors or throttling.",
                "Without backpressure, disks fill and brokers reject publishes.",
                "Apply rate limits at ingress and scale consumers with lag SLO.",
                "See `D14-T015`.",
            )),
        ],
        scenarios=[
            ("Checkout must show paid within 2s but fraud check takes 10s.", S(
                "Authorize payment sync within budget or show pending state.",
                "Run fraud scoring async with hold or capture later.",
                "Do not block UI on 10s HTTP chain.",
                "Communicate state machine clearly to client.",
            )),
            ("Partner API requires synchronous SLA but your engine is queue-based.", S(
                "Expose sync facade that polls internal status with timeout.",
                "Or refactor hot path to sync read model updated by consumers.",
                "Document max wait and error codes.",
                "Hide internal queue behind adapter.",
            )),
            ("Deploy breaks only async consumers; HTTP APIs green.", S(
                "Health checks ignored consumer lag and schema mismatch.",
                "Roll back consumer or forward-compatible schema.",
                "DLQ spike indicates poison messages from new code.",
                "Separate deploy pipelines for producers and consumers.",
            )),
            ("Mobile app fires 50 parallel HTTP calls on launch.", S(
                "Replace with one sync bootstrap plus async push updates.",
                "Or batch via GraphQL/BFF.",
                "Reduces connection overhead and thundering herd.",
                "Async events update cache after first paint.",
            )),
            ("Audit asks who triggered refund.", S(
                "Correlation id from original HTTP through refund event required.",
                "Async without tracing loses causality.",
                "OpenTelemetry across publish and consume spans.",
                "Immutable audit log in stream or DB.",
            )),
        ],
        follow_ups=[
            ("Link to `D05-T001` request lifecycle.", S(
                "HTTP lifecycle is sync entry; messaging continues after response.",
                "Middleware auth applies before publish.",
                "Same identity context should attach to events.",
                "Timeouts at gateway differ from consumer processing time.",
            )),
            ("Link to `D13-T001` concurrency.", S(
                "Consumer thread pools parallelize partition consumption.",
                "Shared mutable state in handlers still races.",
                "Ordering per partition constrains parallelism.",
                "Structured concurrency helps shutdown drains.",
            )),
            ("Link to outbox `D14-T021`.", S(
                "Outbox makes DB commit and event emission atomic in application DB.",
                "Without it, async amplifies dual-write bugs.",
                "Relay process publishes reliably.",
                "Interviewers love this after async basics.",
            )),
        ],
    ),
    ex1_section="Design HTTP + async for `PlaceOrder`: which steps sync, which events, status codes.",
    ex2_section="Users see order confirmed but warehouse never got message. List three checkpoints on the async path.",
    ex3_section="Choose sync gRPC vs event for `InventoryReserved` between Order and Warehouse services.",
    ex1_prompt="PlaceOrder sync vs async steps and status codes.",
    ex2_prompt="Confirmed order missing downstream—three async checkpoints.",
    ex3_prompt="gRPC vs event for InventoryReserved.",
    ex1_solution="Sync: payment auth and stock check or 409. Async: email, analytics via outbox. Return 201 with id or 202 if only queued.",
    ex2_solution="Check outbox relay, broker ACL/topic, consumer group lag/DLQ, schema deserialize errors.",
    ex3_solution="Event if many subscribers and tolerate lag; sync if order must block on reservation confirmation within HTTP timeout.",
    revision="- Sync blocks; async decouples time.\n- 202 vs 200 semantics.\n- Correlation ids across boundaries.\n- Async needs idempotency and lag monitoring.",
    related="Before: `D14-T001`. Supports: `D14-T021`, `D14-T023`, `D14-T032`. Confused with: parallel HTTP vs messaging.",
    completion=completion(
        "Place sync vs async steps on a flow diagram.",
        "Explain 202 Accepted UX implications.",
        "Debug missing downstream work with correlation ids.",
    ),
)

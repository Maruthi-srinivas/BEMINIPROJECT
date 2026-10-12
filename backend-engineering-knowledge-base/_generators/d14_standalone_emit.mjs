#!/usr/bin/env node
/** Standalone D14 emitter (mirrors d14_render + d14_factory + d14_bulk_specs). */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const KB = path.resolve(__dirname, "..");
const DOMAIN = "Messaging and Event-Driven Architecture";

const DEFAULT_CODE = `def dedupe_processed(event_id: str, seen: set[str]) -> bool:
    """Return True if this event_id was already applied (idempotent consumer sketch)."""
    if event_id in seen:
        return False
    seen.add(event_id)
    return True


if __name__ == "__main__":
    processed: set[str] = set()
    assert dedupe_processed("evt-1", processed) is True
    assert dedupe_processed("evt-1", processed) is False
    print("ok")`;

const PAD =
  "In backend interviews, connect the mechanism to consumer lag, duplicate side effects, or broker failure modes instead of treating messaging as fire-and-forget.";

function answer(...sentences) {
  const s = sentences.map((x) => x.trim()).filter(Boolean);
  while (s.length < 4) s.push(PAD);
  return s.join(" ");
}

function qa(q, sentences, bank) {
  return { q, a: answer(...sentences), bank: bank || q };
}

function tradeoffs(...rows) {
  const lines = [
    "| Choice | Benefit | Cost | Choose when | Avoid when |",
    "| --- | --- | --- | --- | --- |",
  ];
  for (const r of rows) lines.push("| " + r.join(" | ") + " |");
  return lines.join("\n");
}

function mistakes(...items) {
  return items.map((i) => `- ${i.trim()}`).join("\n");
}

function exSection(e1, e2, e3) {
  return `### Exercise 1 — implementation

${e1}

### Exercise 2 — debugging

${e2}

### Exercise 3 — trade-off

${e3}`;
}

function completion(...bullets) {
  return bullets.map((b) => `- ${b.trim()}`).join("\n");
}

const DIAGRAMS = {
  cluster: `flowchart TB
  producer[ProducerClient]
  broker0[Broker0_Leader]
  broker1[Broker1_Follower]
  broker2[Broker2_Follower]
  zk[ControllerMetadata]
  producer --> broker0
  broker0 --> broker1
  broker0 --> broker2
  zk -.-> broker0`,
  partition: `flowchart LR
  topic[TopicOrders]
  p0[Partition0]
  p1[Partition1]
  p2[Partition2]
  topic --> p0
  topic --> p1
  topic --> p2`,
  group: `flowchart TB
  p0[Partition0]
  p1[Partition1]
  c1[ConsumerInstance1]
  c2[ConsumerInstance2]
  p0 --> c1
  p1 --> c2`,
  rabbit: `flowchart LR
  pub[Publisher]
  ex[Exchange]
  q1[QueueA]
  q2[QueueB]
  sub1[ConsumerA]
  sub2[ConsumerB]
  pub --> ex
  ex --> q1
  ex --> q2
  q1 --> sub1
  q2 --> sub2`,
  outbox: `flowchart LR
  api[ApiHandler]
  db[(PrimaryDB)]
  outbox[(OutboxTable)]
  relay[OutboxRelay]
  broker[MessageBroker]
  api --> db
  api --> outbox
  relay --> outbox
  relay --> broker`,
  saga: `flowchart LR
  order[OrderService]
  pay[PaymentService]
  ship[ShippingService]
  order -->|OrderCreated| pay
  pay -->|PaymentFailed| order
  pay -->|PaymentCaptured| ship`,
};

function kafkaMermaid(kind) {
  return DIAGRAMS[kind] || DIAGRAMS.cluster;
}

function stdInterview(topic, focus) {
  const beg = [
    qa(
      `What problem does ${focus} solve in event-driven systems?`,
      [
        `It addresses ${focus} so services can evolve without tight synchronous coupling.`,
        "Producers and consumers agree on contracts while the broker handles buffering and delivery attempts.",
        "Operational teams monitor lag, errors, and broker health separately from application CPU.",
        "It is a building block, not a substitute for domain modeling or idempotent handlers.",
      ]
    ),
    qa(
      `Name one failure mode specific to ${focus}.`,
      [
        "Partial failures include broker unavailability, consumer crashes mid-processing, and network partitions.",
        "At-least-once delivery means duplicates unless consumers deduplicate or use idempotency keys.",
        "Misconfigured acknowledgments can cause message loss or unbounded redelivery.",
        "Runbooks should distinguish transient errors from poison messages.",
      ]
    ),
    qa(
      `How does ${focus} interact with database transactions?`,
      [
        "Brokers do not join your local database transaction automatically.",
        "Patterns like transactional outbox or CDC bridge the commit boundary.",
        "Dual-write without outbox risks events never published or published without commit.",
        "Exactly-once across DB and broker requires careful design and still has limits.",
      ]
    ),
    qa(
      `What metric would you alert on for ${focus}?`,
      [
        "Consumer lag, queue depth, DLQ rate, and error ratio are common starting alerts.",
        "Broker disk usage and ISR shrink matter for Kafka clusters.",
        "Sudden publish rate drops may indicate producer failures or throttling.",
        "Correlate metrics with deployment times to catch regressions.",
      ]
    ),
    qa(
      `Is ${focus} the same as exactly-once delivery?`,
      [
        "No. Exactly-once is an end-to-end property with cost and scope limits.",
        "Kafka offers idempotent producers and transactions within the cluster, not free global exactly-once.",
        "Application side effects still need idempotent consumers or deduplication stores.",
        "Interviewers expect you to say at-least-once plus idempotency is the pragmatic default.",
      ]
    ),
  ];
  const inter = [
    qa(
      `How would you scale ${focus} under 10x traffic?`,
      [
        "Scale consumers horizontally within partition or queue limits.",
        "For Kafka, increasing partitions requires planning because keys and ordering change.",
        "Tune batching, fetch sizes, and processing parallelism without breaking ordering guarantees.",
        "Load test producers and consumers together, not in isolation.",
      ]
    ),
    qa(
      `How does ordering work with ${focus}?`,
      [
        "Global order is expensive; per-key or per-partition order is the usual compromise.",
        "Multiple consumers on one partition are not allowed in Kafka groups.",
        "RabbitMQ ordering holds per queue only with a single active consumer.",
        "Design partition keys around entities that must serialize.",
      ]
    ),
    qa(
      `How do retries interact with ${focus}?`,
      [
        "Retries amplify duplicates under at-least-once.",
        "Use exponential backoff and max attempts before DLQ.",
        "Retry storms can starve healthy messages unless isolated topics or queues.",
        "Classify errors: 4xx domain bugs should not infinite retry.",
      ]
    ),
    qa(
      `How do you test ${focus} locally?`,
      [
        "Use docker-compose with broker plus testcontainers in CI.",
        "Contract tests validate schema compatibility before deploy.",
        "Integration tests should assert offset commit and side effects with idempotency.",
        "Chaos tests restart brokers during consumption to surface rebalance bugs.",
      ]
    ),
    qa(
      `Security concerns for ${focus}?`,
      [
        "TLS, authentication (SASL), and ACLs on topics or queues.",
        "Prevent arbitrary publish by compromised services via IAM or ACL least privilege.",
        "Encrypt sensitive payloads or use field-level encryption when needed.",
        "Audit admin operations on cluster configuration.",
      ]
    ),
  ];
  const adv = [
    qa(
      `Kafka ISR and ${focus}—what should producers know?`,
      [
        "In-sync replicas (ISR) are followers caught up within lag bounds.",
        "Producers with `acks=all` wait for ISR acknowledgment; `min.insync.replicas` gates durability.",
        "If ISR shrinks below min ISR, producers may fail rather than accept data loss risk.",
        "This is durability configuration, not application idempotency.",
      ]
    ),
    qa(
      `Explain at-most-once vs at-least-once for ${focus}.`,
      [
        "At-most-once may commit offset before processing or ack before handling, risking loss.",
        "At-least-once processes then commits, risking duplicates on crash.",
        "Exactly-once streaming needs transactions and still does not cover all external systems.",
        "Pick semantics consciously per use case; do not assume broker defaults are correct.",
      ]
    ),
    qa(
      `How does ${focus} relate to sagas?`,
      [
        "Sagas coordinate multi-step business flows with compensations.",
        "They assume messages arrive at-least-once and handlers are idempotent.",
        "Choreography publishes events; orchestration drives commands via a coordinator.",
        "Failure in one step triggers compensating events or rollback policies.",
      ]
    ),
    qa(
      `Outbox vs CDC for publishing after ${focus}?`,
      [
        "Transactional outbox writes events in the same DB transaction as domain rows.",
        "A relay publishes to the broker; duplicates possible, consumers must dedupe.",
        "CDC reads database WAL/binlog and streams changes; captures all mutations including legacy writers.",
        "CDC adds operational complexity but avoids application double-write bugs.",
      ]
    ),
    qa(
      `Capacity planning for ${focus}?`,
      [
        "Estimate peak publish TPS, average message size, retention, and consumer processing time.",
        "Kafka disk is retention times ingress; consumers need CPU for deserialization and IO for writes.",
        "Rabbit memory can fill if consumers slow unless quotas and TTLs exist.",
        "Plan partition count up front; increasing partitions later changes key distribution.",
      ]
    ),
  ];
  const scen = [
    qa(
      `Lag spikes after deploy touching ${focus}. First steps?`,
      [
        "Check consumer error logs, schema compatibility, and rebalance storms.",
        "Compare publish rate vs consume rate per partition.",
        "Roll back if deserialization fails across all instances.",
        "Pause processing and drain DLQ after fix if poison messages appeared.",
      ]
    ),
    qa(
      `Duplicate charges after enabling ${focus}. Root cause?`,
      [
        "At-least-once redelivery without idempotent payment handler is the usual culprit.",
        "Offset committed before DB transaction creates duplicates on replay.",
        "Add business idempotency key stored in database unique constraint.",
        "Exactly-once Kafka does not fix external payment API duplicates alone.",
      ]
    ),
    qa(
      `Broker outage during peak—how does ${focus} recover?`,
      [
        "Producers should retry with backoff; surface degraded mode if broker down too long.",
        "Consumers rebalance when cluster returns; expect duplicate delivery.",
        "Verify ISR and leader election completed before declaring healthy.",
        "Replay backlog may take hours; communicate SLA impact.",
      ]
    ),
    qa(
      `Compliance needs audit trail—does ${focus} suffice?`,
      [
        "Immutable retained logs or warehouse ingest may be required beyond short retention queues.",
        "Encrypt and restrict access to topics with PII.",
        "Compaction drops history per key—unsuitable for full audit.",
        "Pair streaming with long-term object storage if mandated.",
      ]
    ),
    qa(
      `Team wants to change schema for ${focus} without downtime.`,
      [
        "Use backward/forward compatible schema rules in registry.",
        "Deploy consumers before producers or vice versa per compatibility mode.",
        "Dual-write two event versions during migration window.",
        "Monitor deserialization errors as canary.",
      ]
    ),
  ];
  const fol = [
    qa(
      `How does ${topic} connect to partition keys (\`D14-T007\`)?`,
      [
        "Partition keys route related events to one partition for order.",
        "Changing key strategy reshuffles ordering guarantees.",
        "Hot keys create partition skew and lag hotspots.",
        "Design keys around aggregate ids, not random UUIDs when order matters.",
      ]
    ),
    qa(
      `How does ${topic} connect to DLQs (\`D14-T013\`)?`,
      [
        "DLQs quarantine poison messages after retry exhaustion.",
        "Operators inspect DLQ to fix data or code before replay.",
        "Kafka may use dead-letter topics with separate consumer.",
        "DLQ without alerting rots failures silently.",
      ]
    ),
    qa(
      `How does ${topic} connect to replay (\`D14-T031\`)?`,
      [
        "Replay resets offsets or consumes from timestamp to reprocess history.",
        "Idempotent sinks required to avoid duplicate side effects.",
        "Retention window bounds how far back replay reaches.",
        "Use separate replay consumer group to avoid disturbing production offsets.",
      ]
    ),
  ];
  return {
    beginner: beg,
    intermediate: inter,
    advanced: adv,
    scenarios: scen,
    follow_ups: fol,
  };
}

const TOPIC_DEFS = [
  [
    "D14-T004",
    "Topics, partitions and offsets",
    "topic partitions and offsets",
    "partition",
    [
      "A topic is a logical stream split into partitions, each an independent ordered log identified by monotonically increasing offsets.",
      "Offsets are broker-assigned per partition; consumers track position as an integer cursor.",
      "Partition count bounds parallelism for a consumer group: at most one consumer per partition per group.",
      "Increasing partitions later redistributes keys; plan count from expected throughput and ordering needs.",
    ],
    "partition offsets and log segments",
  ],
  [
    "D14-T005",
    "Producers and consumers",
    "Kafka producers and consumers",
    "cluster",
    [
      "Producers partition records via key hash or sticky batching, compress batches, and receive acknowledgment from leaders.",
      "Consumers poll records, process, then commit offsets synchronously or asynchronously to the group coordinator.",
      "Consumer protocol uses heartbeats; slow processing must not block polling beyond `max.poll.interval.ms`.",
      "Both sides batch for throughput; tuning linger.ms and batch.size trades latency for efficiency.",
    ],
    "producer batching and consumer poll loop",
  ],
  [
    "D14-T006",
    "Consumer groups and rebalancing",
    "consumer groups",
    "group",
    [
      "A consumer group is a set of consumers sharing one logical subscription; each partition is assigned to at most one member.",
      "Rebalance occurs when members join, leave, or session times out; during rebalance consumption pauses (classic stop-the-world).",
      "Cooperative sticky assignors reduce partition movement compared to range assignor.",
      "Too frequent rebalance causes lag spikes; fix slow consumers and heartbeat timeouts.",
    ],
    "group coordinator and partition assignment",
  ],
  [
    "D14-T007",
    "Partition keys and ordering",
    "partition keys",
    "partition",
    [
      "Records with the same key hash to the same partition, giving per-key ordering.",
      "Null keys round-robin across partitions, sacrificing order for even spread.",
      "Hot keys create skew: one partition lagging while others are idle.",
      "Changing partition count changes key-to-partition mapping unless using fixed partitioner strategies carefully.",
    ],
    "key-based routing and ordering guarantees",
  ],
  [
    "D14-T008",
    "Replication and ISR",
    "replication and ISR",
    "cluster",
    [
      "Each partition has one leader and zero or more followers replicating the log.",
      "ISR (in-sync replicas) lists followers sufficiently caught up; only ISR members may become leaders without data loss policies.",
      "If followers fall behind, they drop from ISR; producers with `acks=all` fail if min ISR not met.",
      "`unclean.leader.election.enable=false` prevents promoting out-of-sync replicas and losing committed data.",
    ],
    "leader election and ISR shrink",
  ],
  [
    "D14-T009",
    "Delivery semantics: at-most-once, at-least-once, exactly-once",
    "delivery semantics",
    "cluster",
    [
      "At-most-once: commit offset before process or never retry—may lose messages.",
      "At-least-once: process then commit—duplicates on failure after processing.",
      "Exactly-once in Kafka uses idempotent producer plus transactions for read-process-write within cluster boundaries.",
      "End-to-end exactly-once to external databases is not free; idempotent consumers and dedupe tables remain necessary.",
    ],
    "acknowledgment and offset commit trade-offs",
  ],
  [
    "D14-T010",
    "Idempotent producers",
    "idempotent producers",
    "cluster",
    [
      "Idempotent producer assigns PID and sequence numbers per partition so broker deduplicates retries.",
      "Enabling `enable.idempotence=true` implies `acks=all` and safe retries without duplicate sequence in log.",
      "Scope is single producer instance per PID; new producer session gets new PID.",
      "Does not make consumers idempotent; only prevents duplicate writes from producer retries to the log.",
    ],
    "producer sequence numbers and broker dedupe",
  ],
  [
    "D14-T011",
    "Idempotent consumers",
    "idempotent consumers",
    "group",
    [
      "Consumers achieve effective exactly-once processing by deduplicating on business id or offset store in DB transaction.",
      "Store processed message ids with unique constraint before applying side effects.",
      "Commit Kafka offset in same transaction as domain write when using transactional consume patterns.",
      "Retries must produce the same outcome, not double charge or double ship.",
    ],
    "consumer deduplication and transactional writes",
  ],
  [
    "D14-T012",
    "Retries and retry topics",
    "retry topics",
    "rabbit",
    [
      "Retry topics or delay queues isolate failing messages from main flow.",
      "Exponential backoff reduces load on failing dependencies.",
      "Cap max attempts and route to DLQ afterward.",
      "Kafka retry pattern often uses separate topic plus consumer with delay headers or external scheduler.",
    ],
    "retry routing and backoff",
  ],
  [
    "D14-T013",
    "Dead-letter queues (DLQs)",
    "DLQs",
    "rabbit",
    [
      "DLQ holds messages that exceeded retry policy or failed validation permanently.",
      "Operators analyze DLQ payloads to fix code or data and replay safely.",
      "Without DLQ, poison messages block head-of-line processing in queues.",
      "Alert on DLQ depth; treat growth as incident.",
    ],
    "dead-letter routing",
  ],
  [
    "D14-T014",
    "Delayed messages",
    "delayed delivery",
    "rabbit",
    [
      "Delayed delivery schedules visibility in future: Rabbit delayed message plugin, SQS delay seconds, or timer service.",
      "Kafka has no native delay per message; use timestamp indexing, scheduled jobs, or external workflow engine.",
      "Delay queues risk clock skew and backlog if workers underestimate volume.",
      "Use idempotency when timer fires duplicate triggers.",
    ],
    "scheduled visibility and timers",
  ],
  [
    "D14-T015",
    "Backpressure and consumer lag",
    "backpressure",
    "group",
    [
      "Backpressure signals producers or clients to slow when consumers cannot keep up.",
      "Consumer lag is offset difference between log end and committed group offset.",
      "Mitigate by scaling consumers within partition limits, optimizing handler, or shedding load.",
      "Unbounded lag risks retention expiry before processing—data loss by retention, not ack.",
    ],
    "lag metrics and flow control",
  ],
  [
    "D14-T016",
    "Offset commits",
    "offset commits",
    "group",
    [
      "Offsets record progress; auto-commit may commit before processing finishes.",
      "Manual commit after successful side effects gives at-least-once with correct ordering of operations.",
      "Committing synchronously blocks poll loop; async commit risks crash window duplicates.",
      "Reset offsets only with ops approval; `earliest` replay can duplicate massively.",
    ],
    "offset storage and commit timing",
  ],
  [
    "D14-T017",
    "Message schemas and schema registry",
    "schema registry",
    "cluster",
    [
      "Schemas define payload structure; registry stores Avro/Protobuf/JSON schema versions with ids embedded in messages.",
      "Consumers fetch schema by id to deserialize; incompatible schemas break consumers at runtime.",
      "Registry enforces compatibility policies on registration.",
      "Schema is part of the API contract across teams.",
    ],
    "schema registration and serialization",
  ],
  [
    "D14-T018",
    "Schema evolution and compatibility",
    "schema evolution",
    "cluster",
    [
      "Backward compatible: new schema, old consumers can read new data (add optional fields).",
      "Forward compatible: old schema data readable by new consumers.",
      "Full transitive compatibility required for safe rolling upgrades both directions.",
      "Breaking changes need new topic or versioned subject strategy.",
    ],
    "compatibility modes",
  ],
  [
    "D14-T019",
    "Event sourcing",
    "event sourcing",
    "outbox",
    [
      "Event sourcing persists state as sequence of domain events, not only current row image.",
      "Current state is derived by replaying events or snapshots plus delta.",
      "Enables audit and temporal queries but complicates queries and schema migration.",
      "Often paired with Kafka or event store as the log.",
    ],
    "event store as source of truth",
  ],
  [
    "D14-T020",
    "CQRS",
    "CQRS",
    "outbox",
    [
      "Command Query Responsibility Segregation separates write model from optimized read models.",
      "Writes emit events; projectors build read databases asynchronously.",
      "Read side may lag; UI must tolerate staleness or use read-after-write tricks.",
      "Adds moving parts but scales reads independently.",
    ],
    "command vs query paths",
  ],
  [
    "D14-T021",
    "Transactional outbox",
    "transactional outbox",
    "outbox",
    [
      "Outbox table stores outbound events in same DB transaction as business data.",
      "Relay process polls outbox and publishes to broker, marking rows sent.",
      "Relay duplicates possible; consumers must dedupe by event id.",
      "Avoids dual-write inconsistency between DB commit and publish.",
    ],
    "outbox relay pattern",
  ],
  [
    "D14-T022",
    "CDC (Change Data Capture)",
    "CDC",
    "outbox",
    [
      "CDC streams row-level changes from database WAL/binlog to Kafka via connectors like Debezium.",
      "Captures changes from all writers including ad-hoc SQL, not only application outbox.",
      "Ordering per table primary key partition; schema changes need migration care.",
      "Operational overhead: connector lag, heartbeats, and snapshotting.",
    ],
    "log-based CDC pipelines",
  ],
  [
    "D14-T023",
    "Sagas and compensating actions",
    "sagas",
    "saga",
    [
      "Sagas manage distributed transactions as sequence of local transactions with compensations.",
      "Choreography: services react to events; orchestration: central coordinator issues commands.",
      "Each step must be compensatable or retryable with idempotency.",
      "Failures trigger compensating events like `PaymentRefunded` to undo prior steps.",
    ],
    "distributed saga flows",
  ],
  [
    "D14-T024",
    "RabbitMQ exchanges, queues and bindings",
    "RabbitMQ routing",
    "rabbit",
    [
      "Publishers send to exchanges; bindings route to queues via routing key and exchange type.",
      "Direct exchange: exact routing key match. Fanout: broadcast to all bound queues. Topic: pattern match. Headers: header attributes.",
      "Queues buffer messages; consumers ack to remove or requeue.",
      "Prefetch limits unacked messages per consumer for fair dispatch.",
    ],
    "exchange types and bindings",
  ],
  [
    "D14-T025",
    "Acknowledgments and redelivery",
    "acknowledgments",
    "rabbit",
    [
      "Manual ack after successful processing gives at-least-once; ack before process risks loss.",
      "Nack with requeue=true redelivers; false sends to DLX if configured.",
      "Consumer crash before ack causes redelivery to another consumer.",
      "Poison messages spin until DLQ or drop policy.",
    ],
    "ack/nack semantics",
  ],
  [
    "D14-T026",
    "RabbitMQ vs Kafka",
    "broker comparison",
    "rabbit",
    [
      "RabbitMQ excels at flexible routing, per-message ack, and task queues with moderate throughput.",
      "Kafka excels at high-throughput durable logs, replay, and multiple consumer groups.",
      "Rabbit deletes messages on ack; Kafka retains by policy.",
      "Choose based on routing complexity vs log retention and fan-out scale.",
    ],
    "RabbitMQ vs Kafka trade-offs",
  ],
  [
    "D14-T027",
    "Pub/Sub systems",
    "pub/sub",
    "rabbit",
    [
      "Pub/sub decouples publishers from subscriber identities; broker fans out copies.",
      "Google Pub/Sub, SNS, and Kafka consumer groups are variations with different ordering and ack models.",
      "Subscribers may be push or pull; push needs endpoint availability and auth.",
      "Fan-out cost grows with subscriber count and message size.",
    ],
    "publish subscribe fan-out",
  ],
  [
    "D14-T028",
    "Ordering guarantees",
    "ordering guarantees",
    "partition",
    [
      "Only single-threaded single partition or single queue consumer gives strict order.",
      "Partition by entity id for per-entity serialization.",
      "Cross-partition events have no global order without sequencing service.",
      "Out-of-order handling may need version vectors or discard stale updates.",
    ],
    "order scopes",
  ],
  [
    "D14-T029",
    "Poison messages",
    "poison messages",
    "rabbit",
    [
      "Poison messages fail processing repeatedly due to bad payload or bug.",
      "They block queues or inflate lag if retried forever.",
      "Detect via delivery count headers and route to DLQ.",
      "Fix code or data before replay from DLQ with safeguards.",
    ],
    "poison message handling",
  ],
  [
    "D14-T030",
    "Message deduplication",
    "deduplication",
    "group",
    [
      "Deduplication uses unique business keys, bloom filters, or broker features (SQS FIFO dedup window).",
      "Kafka idempotent producer dedupes producer retries only.",
      "Store idempotency keys in database with TTL matching retry horizon.",
      "Dedup window must exceed max redelivery time.",
    ],
    "idempotency and dedupe stores",
  ],
  [
    "D14-T031",
    "Replay and reprocessing",
    "replay",
    "group",
    [
      "Replay resets consumer offsets or consumes from timestamp to rebuild projections.",
      "Requires idempotent sinks and often separate consumer group to avoid clobbering production offsets.",
      "Retention and compaction limit how far back replay reaches.",
      "Large replay loads DB; throttle and monitor.",
    ],
    "offset reset and reprocessing",
  ],
  [
    "D14-T032",
    "Workflow orchestration vs choreography",
    "orchestration vs choreography",
    "saga",
    [
      "Orchestration: central workflow engine issues commands and tracks state (Temporal, Camunda).",
      "Choreography: services publish and react to events without central brain.",
      "Orchestration simplifies visibility and timeouts; choreography reduces coupling and single point of failure.",
      "Hybrid patterns common at scale.",
    ],
    "workflow styles",
  ],
];

function buildSpecEntry(tid, title, focus, diagram, overviewLines, internalHook) {
  const tradeRows = [
    ["Strict ordering", "Correct per-entity timeline", "Limits scale", "Inventory per SKU", "Global analytics"],
    ["More partitions", "Higher parallelism", "Rebalance cost", "Kafka throughput", "Tiny ordered log"],
    ["Manual ack", "Safer processing", "Slower on failure", "Rabbit tasks", "Fire-and-forget metrics"],
    ["Long retention", "Replay for fixes", "Disk cost", "Compliance, CDC", "Ephemeral tasks"],
  ];
  const exCommon = [
    `Implement or diagram how ${focus} fits in a three-service order flow.`,
    `Given duplicate events, explain which layer should dedupe for ${title}.`,
    `Choose Kafka vs Rabbit for a new ${focus} requirement with replay and routing constraints.`,
  ];
  return {
    overview: overviewLines,
    first_principles: [
      `${title} sits in the messaging layer between domain services and operational observability.`,
      "Brokers provide durability and fan-out but do not understand your business invariants.",
      "Application code must define retries, idempotency, and schema contracts explicitly.",
      "Failure is normal; design for at-least-once and measurable lag.",
    ],
    internal: [
      internalHook,
      "Leaders, coordinators, and client libraries implement the wire protocol; operators tune JVM heap, disk, and network.",
      "Client configuration (acks, commits, prefetch) often matters more than broker version bumps.",
      "Cross-region replication adds latency to ISR acknowledgment and consumer fetch.",
    ],
    mermaid: kafkaMermaid(diagram),
    examples: [
      `When discussing ${title}, use concrete nouns: orders topic, payments queue, outbox relay, DLQ alert.`,
      "Weak answers stay product-marketing level; strong answers mention partitions, acks, or exchange type.",
      "Tie to a user-visible symptom: duplicate email, stale dashboard, or lost refund event.",
    ],
    practical: [
      "Document delivery semantics and idempotency strategy in service README.",
      "Dashboard lag per partition and DLQ depth for on-call.",
      "Load test with broker failures, not only happy path.",
      "Version schemas before rolling producers.",
    ],
    tradeoffs_table: tradeoffs(...tradeRows),
    mistakes: mistakes(
      `Treating ${title} as guaranteeing exactly-once end-to-end without application deduplication.`,
      "Committing offsets before side effects complete.",
      "Ignoring hot partition skew.",
      "Skipping schema compatibility checks on deploy."
    ),
    debugging: [
      `Correlate producer trace id through ${title} to consumer logs.`,
      "Compare broker metric with application error rate during incidents.",
      "Inspect DLQ sample messages for schema or poison payloads.",
    ],
    interview: stdInterview(title, focus),
    ex1_section: exCommon[0],
    ex2_section: exCommon[1],
    ex3_section: exCommon[2],
    ex1_prompt: exCommon[0],
    ex2_prompt: exCommon[1],
    ex3_prompt: exCommon[2],
    ex1_solution: `Draw producers, broker, consumers, note ack/commit points and idempotency store for ${tid}.`,
    ex2_solution: "Consumer dedupes via unique event_id; producer idempotence only covers retry to log.",
    ex3_solution:
      "Kafka if log retention and multiple groups; Rabbit if complex routing and per-message ack without long replay.",
    revision: `- ${title}: know failure modes and metrics.\n- At-least-once + idempotency default.\n- Exactly-once is scoped and costly.`,
    related: `See \`D14-T001\` and neighbors in domain 14. Depends on inventory deps for \`${tid}\`.`,
    completion: completion(
      `Explain ${title} without confusing broker guarantees and app idempotency.`,
      "Name one metric and one failure mode.",
      "Sketch architecture with ack or offset commit placement."
    ),
    code: DEFAULT_CODE,
    code_intro: `File: \`examples/${tid.toLowerCase().replace(/-/g, "_")}.py\` (illustrative; not executed in CI).`,
    code_footer:
      "Run locally with Python 3. The snippet models application-side patterns; wire real brokers in integration tests.",
  };
}

function joinParagraphs(parts) {
  return parts.filter((p) => p && p.trim()).map((p) => p.trim()).join("\n\n");
}

function renderInterviewSection(k) {
  const parts = ["## K. Interview Preparation\n"];
  for (const [level, count] of [
    ["Beginner", 5],
    ["Intermediate", 5],
    ["Advanced", 5],
    ["Scenarios", 5],
    ["Follow-ups", 3],
  ]) {
    parts.push(`### ${level}\n`);
    const key = level.toLowerCase().replace(/-/g, "_");
    for (let i = 0; i < Math.min(count, k[key].length); i++) {
      const item = k[key][i];
      parts.push(`#### Q${i + 1}. ${item.q}\n\n**Answer:** ${item.a}\n`);
    }
  }
  return parts.join("\n");
}

function renderNote(topic) {
  const t = topic;
  const meta = t.meta;
  const lines = [
    `# ${meta.id} — ${meta.name}`,
    "",
    `Topic ID: \`${meta.id}\``,
    `Domain: ${DOMAIN}`,
    `Subdomain: ${meta.subdomain}`,
    `Importance: ${meta.importance}`,
    `Complexity: ${meta.complexity}`,
    `Dependencies: ${meta.deps_display}`,
    "Execution status of the code in section F: not executed (local)",
    "",
    "## A. Topic Overview",
    "",
    joinParagraphs(t.overview),
    "",
    "## B. First-Principles Explanation",
    "",
    joinParagraphs(t.first_principles),
    "",
    "## C. Internal Working and Architecture",
    "",
    joinParagraphs(t.internal),
    "",
    "## D. Diagrams and Visual Models",
    "",
    "```mermaid",
    t.mermaid.trim(),
    "```",
    "",
    t.diagram_caption || "Read the diagram as a data-flow or lifecycle model for this topic.",
    "",
    "## E. Examples and Analogies",
    "",
    joinParagraphs(t.examples),
    "",
    "## F. Code Examples",
    "",
    t.code_intro,
    "",
    "```python",
    t.code.trim(),
    "```",
    "",
    t.code_footer,
    "",
    "## G. Practical Backend Application",
    "",
    joinParagraphs(t.practical),
    "",
    "## H. Advantages, Limitations and Trade-offs",
    "",
    t.tradeoffs_table,
    "",
    "## I. Common Mistakes and Misconceptions",
    "",
    t.mistakes,
    "",
    "## J. Debugging and Troubleshooting",
    "",
    joinParagraphs(t.debugging),
    "",
    renderInterviewSection(t.interview),
    "",
    "## L. Practical Exercises",
    "",
    `Solutions are in \`EXERCISES/solutions/${meta.id}.md\`. Try these before opening that file.`,
    "",
    t.exercises_section,
    "",
    "## M. Revision Notes",
    "",
    t.revision,
    "",
    "## N. Related Topics",
    "",
    t.related,
    "",
    "## O. Completion Criteria",
    "",
    t.completion,
    "",
  ];
  return lines.join("\n");
}

function renderExerciseFile(meta, exercises) {
  const body = [
    `# Exercises — ${meta.id}`,
    "",
    `Problems only. Solutions: [${meta.id}](../solutions/${meta.id}.md).`,
    "",
  ];
  exercises.forEach((ex, i) => body.push(`${i + 1}. ${ex.prompt}`));
  return body.join("\n") + "\n";
}

function renderSolutionFile(meta, solutions) {
  const body = [
    `# Solutions for ${meta.id}`,
    "",
    "Open this only after attempting the exercises in the topic note.",
    "",
  ];
  solutions.forEach((sol, i) => {
    body.push(`## Exercise ${i + 1}`, "", sol.text.trim(), "");
  });
  return body.join("\n");
}

function renderInterviewBank(meta, interview) {
  const questions = [];
  let n = 0;
  for (const [level, count] of [
    ["Beginner", 5],
    ["Intermediate", 5],
    ["Advanced", 5],
    ["Scenarios", 5],
    ["Follow-ups", 3],
  ]) {
    const key = level.toLowerCase().replace(/-/g, "_");
    for (const item of interview[key].slice(0, count)) {
      n += 1;
      questions.push(`${n}. ${level}. ${item.bank}`);
    }
  }
  const rel = `../${meta.note_path}`;
  return [
    `# ${meta.id} interview items`,
    "",
    `Domain: ${DOMAIN}`,
    `Topic: ${meta.name}`,
    "Difficulty mix: beginner, intermediate, advanced, scenario, follow-up",
    "Interview type: fundamentals, debugging, trade-off, distributed systems",
    "Full reasoned answers are in the topic note, section K.",
    "",
    "## Questions",
    "",
    ...questions,
    "",
    `Answer key: [topic note section K](${rel}).`,
    "",
  ].join("\n");
}

function buildTopicPackage(row, spec) {
  const deps_display = row.dependencies.map((d) => `\`${d}\``).join(", ");
  const meta = {
    id: row.id,
    name: row.name,
    subdomain: row.subdomain,
    importance: row.importance,
    complexity: row.complexity,
    deps_display,
    note_path: row.note_path,
  };
  return {
    meta,
    overview: spec.overview,
    first_principles: spec.first_principles,
    internal: spec.internal,
    mermaid: spec.mermaid,
    diagram_caption: spec.diagram_caption || "",
    examples: spec.examples,
    code_intro: spec.code_intro,
    code: spec.code,
    code_footer: spec.code_footer,
    practical: spec.practical,
    tradeoffs_table: spec.tradeoffs_table,
    mistakes: spec.mistakes,
    debugging: spec.debugging,
    interview: spec.interview,
    exercises_section: exSection(spec.ex1_section, spec.ex2_section, spec.ex3_section),
    exercises: [{ prompt: spec.ex1_prompt }, { prompt: spec.ex2_prompt }, { prompt: spec.ex3_prompt }],
    solutions: [{ text: spec.ex1_solution }, { text: spec.ex2_solution }, { text: spec.ex3_solution }],
    revision: spec.revision,
    related: spec.related,
    completion: spec.completion,
  };
}

function writeFile(rel, content) {
  const full = path.join(KB, rel);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, content, "utf8");
}

const inv = JSON.parse(fs.readFileSync(path.join(KB, "00_INDEX", "inventory.json"), "utf8"));
const rows = inv.topics.filter((t) => t.id.startsWith("D14-T")).sort((a, b) => a.id.localeCompare(b.id));
const defMap = Object.fromEntries(
  TOPIC_DEFS.map(([tid, title, focus, diagram, lines, hook]) => [
    tid,
    buildSpecEntry(tid, title, focus, diagram, lines, hook),
  ])
);

const TARGET = new Set(
  Array.from({ length: 29 }, (_, i) => `D14-T${String(i + 4).padStart(3, "0")}`)
);
const finished = [];
const failures = [];

for (const row of rows) {
  if (!TARGET.has(row.id)) continue;
  try {
    const spec = defMap[row.id];
    if (!spec) throw new Error("missing spec");
    const pkg = buildTopicPackage(row, spec);
    const meta = pkg.meta;
    writeFile(meta.note_path, renderNote(pkg));
    writeFile(`EXERCISES/${meta.id}.md`, renderExerciseFile(meta, pkg.exercises));
    writeFile(`EXERCISES/solutions/${meta.id}.md`, renderSolutionFile(meta, pkg.solutions));
    writeFile(`INTERVIEW_BANK/items/${meta.id}.md`, renderInterviewBank(meta, pkg.interview));
    finished.push(meta.id);
  } catch (e) {
    failures.push(`${row.id}: ${e.message}`);
  }
}

const JSONL = path.join(__dirname, "d14_export.jsonl");
const jh = fs.createWriteStream(JSONL, { encoding: "utf8" });
for (const row of rows) {
  if (!TARGET.has(row.id)) continue;
  try {
    const spec = defMap[row.id];
    const pkg = buildTopicPackage(row, spec);
    const meta = pkg.meta;
    const files = [
      [meta.note_path, renderNote(pkg)],
      [`EXERCISES/${meta.id}.md`, renderExerciseFile(meta, pkg.exercises)],
      [`EXERCISES/solutions/${meta.id}.md`, renderSolutionFile(meta, pkg.solutions)],
      [`INTERVIEW_BANK/items/${meta.id}.md`, renderInterviewBank(meta, pkg.interview)],
    ];
    for (const [rel, content] of files) {
      jh.write(JSON.stringify({ path: rel, content }) + "\n");
    }
  } catch (_) {
    /* skip jsonl on error */
  }
}
jh.end();

console.log("FINISHED:", finished.join(","));
console.log("FAILURES:", failures.length ? failures.join(";") : "none");
console.log("JSONL:", JSONL);

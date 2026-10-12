# ruff: noqa: E501
"""Per-topic seeds for D19 Microservices generator."""

from __future__ import annotations

TOPIC_SPECS: dict[str, dict] = {
    "D19-T001": {
        "thesis": "Microservices trade a single deployable monolith for independently deployable services that align with business capabilities and team ownership.",
        "pillars": ["single responsibility per service", "autonomous teams", "decentralized data", "design for failure", "evolutionary architecture"],
        "diagram": """flowchart LR
  client[Client]
  gw[Edge gateway]
  s1[Orders]
  s2[Payments]
  s3[Inventory]
  client --> gw
  gw --> s1
  gw --> s2
  s1 --> s3
  s2 --> s3""",
        "scenario": "checkout spans three services",
        "pitfall": "splitting by technical layer instead of business capability",
        "prev": None,
        "next": "D19-T002",
    },
    "D19-T002": {
        "thesis": "Service boundaries define what changes together, who owns the data, and which APIs are stable contracts between teams.",
        "pillars": ["bounded context", "cohesion", "loose coupling", "published language", "anti-corruption layer"],
        "diagram": """flowchart TB
  subgraph orderBC[Order context]
    O[Order service]
    Odb[(Order DB)]
    O --> Odb
  end
  subgraph catalogBC[Catalog context]
    C[Catalog service]
    Cdb[(Catalog DB)]
    C --> Cdb
  end
  O -->|SKU ids only| C""",
        "scenario": "catalog price changes must not require order schema migration",
        "pitfall": "shared tables between two services",
        "prev": "D19-T001",
        "next": "D19-T003",
    },
    "D19-T003": {
        "thesis": "Domain-driven decomposition uses ubiquitous language and bounded contexts to cut services where the domain model naturally fractures.",
        "pillars": ["ubiquitous language", "aggregates", "context map", "subdomain classification", "event storming"],
        "diagram": """flowchart LR
  subgraph core[Core domain]
    Checkout[Checkout]
  end
  subgraph support[Supporting]
    Notify[Notifications]
  end
  Checkout -->|OrderPlaced| Notify""",
        "scenario": "event storming reveals checkout vs fulfillment lifecycles",
        "pitfall": "one service per entity (OrderService, LineItemService)",
        "prev": "D19-T002",
        "next": "D19-T004",
    },
    "D19-T004": {
        "thesis": "An API gateway is the outward-facing façade that routes, secures, and shapes traffic before it reaches fine-grained services.",
        "pillars": ["routing", "TLS termination", "authN/Z", "rate limits", "request aggregation"],
        "diagram": """flowchart TD
  mobile[Mobile app]
  gw[API Gateway]
  auth[Auth filter]
  route[Router]
  svcA[Service A]
  svcB[Service B]
  mobile --> gw
  gw --> auth --> route
  route --> svcA
  route --> svcB""",
        "scenario": "mobile clients see one base URL while backends scale independently",
        "pitfall": "putting domain logic in the gateway",
        "prev": "D19-T003",
        "next": "D19-T005",
    },
    "D19-T005": {
        "thesis": "Service discovery lets callers find healthy instances without hard-coded host lists as pods churn behind load balancers.",
        "pillars": ["registry", "health checks", "client-side vs server-side LB", "DNS SRV", "control plane"],
        "diagram": """sequenceDiagram
  participant C as Caller
  participant R as Registry
  participant I as Instance
  I->>R: register + heartbeat
  C->>R: resolve orders-service
  R-->>C: instance list
  C->>I: request""",
        "scenario": "Kubernetes rolls a deployment while traffic stays on ready endpoints",
        "pitfall": "caching stale endpoints after scale-in",
        "prev": "D19-T004",
        "next": "D19-T006",
    },
    "D19-T006": {
        "thesis": "Inter-service communication chooses protocols and coupling styles that match consistency needs, latency budgets, and team boundaries.",
        "pillars": ["sync RPC", "async messaging", "idempotency", "contracts", "backpressure"],
        "diagram": """flowchart LR
  A[Service A] -->|HTTP/gRPC| B[Service B]
  A -->|publish| Q[Message broker]
  Q -->|consume| C[Service C]""",
        "scenario": "payment authorization is sync; receipt email is async",
        "pitfall": "chatty fine-grained RPC chains",
        "prev": "D19-T005",
        "next": "D19-T007",
    },
    "D19-T007": {
        "thesis": "REST and gRPC differ in payload shape, streaming, browser friendliness, and how strictly contracts are enforced between services.",
        "pillars": ["protobuf", "HTTP/2", "resource modeling", "code generation", "grpc-gateway"],
        "diagram": """flowchart TB
  rest[REST JSON over HTTP/1.1 or HTTP/2]
  grpc[gRPC protobuf over HTTP/2]
  rest --> human[Humans and browsers]
  grpc --> internal[Internal east-west]""",
        "scenario": "public mobile API stays REST; internal inventory uses gRPC",
        "pitfall": "exposing gRPC directly to browsers without a gateway",
        "prev": "D19-T006",
        "next": "D19-T008",
    },
    "D19-T008": {
        "thesis": "Synchronous calls preserve immediate feedback but propagate latency and failure; asynchronous calls decouple at the cost of complexity and eventual consistency.",
        "pillars": ["request-reply", "message queues", "event notification", "temporal coupling", "sagas"],
        "diagram": """flowchart LR
  sync[Sync chain A to B to C]
  async[Async A publishes event]
  async --> B2[B consumer]
  async --> C2[C consumer]""",
        "scenario": "order placement waits on inventory sync; analytics consumes async",
        "pitfall": "using sync for every side effect",
        "prev": "D19-T007",
        "next": "D19-T009",
    },
    "D19-T009": {
        "thesis": "Centralized configuration distributes feature flags and connection strings consistently while keeping secrets out of images.",
        "pillars": ["config server", "git-backed config", "refresh without rebuild", "namespaces per env", "secret stores"],
        "diagram": """flowchart TD
  git[Config repo]
  server[Config server]
  s1[Service pod]
  vault[Secret store]
  git --> server
  server -->|pull| s1
  vault -->|inject| s1""",
        "scenario": "toggle new tax rule without redeploying all pods",
        "pitfall": "storing secrets in plain config repos",
        "prev": "D19-T008",
        "next": "D19-T010",
    },
    "D19-T010": {
        "thesis": "Distributed tracing correlates logs and spans across services so you can debug latency and errors in a call graph, not a single JVM stack trace.",
        "pillars": ["trace id", "span parent-child", "sampling", "W3C tracecontext", "service map"],
        "diagram": """flowchart LR
  gw[Gateway span]
  o[Order span]
  p[Payment span]
  gw --> o --> p""",
        "scenario": "p95 checkout latency spikes in payment, visible in one trace",
        "pitfall": "new trace id per internal hop",
        "prev": "D19-T009",
        "next": "D19-T011",
    },
    "D19-T011": {
        "thesis": "Service authentication proves caller identity machine-to-machine using tokens, mTLS, or workload identity rather than shared passwords.",
        "pillars": ["OAuth2 client credentials", "JWT validation", "mTLS", "SPIFFE", "least privilege"],
        "diagram": """sequenceDiagram
  participant A as Service A
  participant T as Token issuer
  participant B as Service B
  A->>T: client credentials
  T-->>A: access token
  A->>B: request + bearer token
  B->>B: validate audience and scope""",
        "scenario": "only billing service may call payment capture API",
        "pitfall": "long-lived shared API keys in every repo",
        "prev": "D19-T010",
        "next": "D19-T012",
    },
    "D19-T012": {
        "thesis": "Resilience patterns keep partial failures from becoming total outages by limiting blast radius and providing graceful degradation paths.",
        "pillars": ["timeouts", "retries with jitter", "circuit breakers", "bulkheads", "fallbacks"],
        "diagram": """flowchart TD
  req[Incoming request]
  pool[Thread pool bulkhead]
  cb[Circuit breaker]
  dep[Dependency]
  req --> pool --> cb --> dep""",
        "scenario": "recommendations fail open while checkout stays up",
        "pitfall": "retry storms on overloaded dependencies",
        "prev": "D19-T011",
        "next": "D19-T013",
    },
    "D19-T013": {
        "thesis": "Circuit breakers stop calling a failing dependency; bulkheads isolate resource pools so one slow client cannot exhaust shared threads.",
        "pillars": ["closed open half-open", "failure rate window", "separate pools", "queue limits", "hedged requests"],
        "diagram": """stateDiagram-v2
  [*] --> Closed
  Closed --> Open: failures exceed threshold
  Open --> HalfOpen: after cooldown
  HalfOpen --> Closed: probe succeeds
  HalfOpen --> Open: probe fails""",
        "scenario": "inventory DB slow; breaker opens and catalog serves cached stock",
        "pitfall": "one global thread pool for all outbound calls",
        "prev": "D19-T012",
        "next": "D19-T014",
    },
    "D19-T014": {
        "thesis": "Timeouts bound waiting; retries recover transient faults but must be idempotent and capped to avoid amplifying load.",
        "pillars": ["deadline propagation", "exponential backoff", "retry budgets", "idempotency keys", "hedging"],
        "diagram": """sequenceDiagram
  participant C as Client
  participant S as Server
  C->>S: attempt 1
  Note over C: timeout
  C->>S: attempt 2 after backoff
  S-->>C: 200""",
        "scenario": "network blip during payment authorize gets one safe retry",
        "pitfall": "retrying POST without idempotency key",
        "prev": "D19-T013",
        "next": "D19-T015",
    },
    "D19-T015": {
        "thesis": "Sagas coordinate long-running business transactions across services using compensating actions instead of a single ACID database transaction.",
        "pillars": ["choreography", "orchestration", "compensating transactions", "saga log", "timeouts"],
        "diagram": """sequenceDiagram
  participant O as Orders
  participant P as Payments
  participant I as Inventory
  O->>P: reserve funds
  P-->>O: ok
  O->>I: reserve stock
  I-->>O: fail
  O->>P: release funds""",
        "scenario": "checkout saga rolls back payment when inventory is empty",
        "pitfall": "assuming saga steps are instantly consistent",
        "prev": "D19-T014",
        "next": "D19-T016",
    },
    "D19-T016": {
        "thesis": "The transactional outbox writes domain state and outbound messages in one local transaction, then a relay publishes reliably to the broker.",
        "pillars": ["same DB transaction", "outbox table", "relay process", "at-least-once publish", "idempotent consumers"],
        "diagram": """flowchart LR
  svc[Service]
  db[(DB + outbox)]
  relay[Outbox relay]
  bus[Message bus]
  svc -->|BEGIN txn| db
  relay -->|poll| db
  relay --> bus""",
        "scenario": "order saved and OrderCreated event never lost on crash",
        "pitfall": "dual write to DB and broker without outbox",
        "prev": "D19-T015",
        "next": "D19-T017",
    },
    "D19-T017": {
        "thesis": "CQRS separates read and write models; event sourcing stores state as an append-only event log rebuilt by projections.",
        "pillars": ["command model", "query model", "projections", "event store", "snapshots"],
        "diagram": """flowchart TB
  cmd[Commands] --> w[Write model]
  w --> es[(Event store)]
  es --> proj[Projections]
  proj --> r[Read model]""",
        "scenario": "order history audit trail from events; dashboard from read replica",
        "pitfall": "CQRS everywhere when CRUD would suffice",
        "prev": "D19-T016",
        "next": "D19-T018",
    },
    "D19-T018": {
        "thesis": "Distributed data ownership means each service is the system of record for its data; others reference IDs, not foreign keys across databases.",
        "pillars": ["single writer", "API not table sharing", "eventual replicas", "data products", "governance"],
        "diagram": """flowchart LR
  A[(Service A data)]
  B[(Service B data)]
  A -->|events| B
  Note1[No cross-DB joins]""",
        "scenario": "shipping stores address snapshot, not live user profile row",
        "pitfall": "distributed joins in the API gateway",
        "prev": "D19-T017",
        "next": "D19-T019",
    },
    "D19-T019": {
        "thesis": "Database-per-service enforces encapsulation: schema migrations stay local and teams choose storage fit for their workload.",
        "pillars": ["private schema", "polyglot persistence", "migration independence", "backup per service", "connection limits"],
        "diagram": """flowchart TB
  s1[Users service] --> db1[(Postgres)]
  s2[Catalog service] --> db2[(Mongo)]
  s3[Search service] --> db3[(OpenSearch)]""",
        "scenario": "search reindexes without locking orders table",
        "pitfall": "two services sharing one logical database for convenience",
        "prev": "D19-T018",
        "next": "D19-T020",
    },
    "D19-T020": {
        "thesis": "Cross-service consistency accepts eventual alignment and uses sagas, outbox, and idempotency instead of distributed two-phase commit.",
        "pillars": ["BASE vs ACID", "read-your-writes tricks", "version vectors", "reconciliation jobs", "SLAs on staleness"],
        "diagram": """flowchart LR
  w[Write in service A]
  e[Event]
  r[Replica in service B]
  w --> e --> r""",
        "scenario": "wallet balance lags ledger by seconds with documented SLA",
        "pitfall": "expecting global strong consistency everywhere",
        "prev": "D19-T019",
        "next": "D19-T021",
    },
    "D19-T021": {
        "thesis": "API composition implements a read model by calling multiple services and merging results, often at a BFF or dedicated composer.",
        "pillars": ["BFF", "parallel fetch", "partial results", "caching", "timeout per leg"],
        "diagram": """flowchart TD
  client[Client]
  comp[Composer]
  u[Users]
  o[Orders]
  client --> comp
  comp --> u
  comp --> o""",
        "scenario": "order detail page merges user profile and line items",
        "pitfall": "sequential N+1 service calls without deadlines",
        "prev": "D19-T020",
        "next": "D19-T022",
    },
    "D19-T022": {
        "thesis": "Aggregation and fan-out parallelize calls to many services but multiply tail latency and failure modes unless bounded.",
        "pillars": ["fan-out", "fan-in", "scatter-gather", "bulkhead per dependency", "hedged requests"],
        "diagram": """flowchart LR
  gw[Gateway]
  gw --> s1[S1]
  gw --> s2[S2]
  gw --> s3[S3]
  gw --> merge[Merge responses]""",
        "scenario": "home feed gathers tiles from five microservices",
        "pitfall": "unbounded parallel calls on every request",
        "prev": "D19-T021",
        "next": "D19-T023",
    },
    "D19-T023": {
        "thesis": "Service versioning lets teams deploy independently while consumers migrate on compatible contract rules.",
        "pillars": ["semantic versioning", "URL vs header version", "consumer-driven contracts", "deprecation windows", "schema registry"],
        "diagram": """flowchart LR
  v1[orders v1]
  v2[orders v2]
  clients[Clients]
  clients -->|Accept v1| v1
  clients -->|Accept v2| v2""",
        "scenario": "add optional field without breaking old mobile clients",
        "pitfall": "breaking JSON contracts without a version bump",
        "prev": "D19-T022",
        "next": "D19-T024",
    },
    "D19-T024": {
        "thesis": "Backward-compatible deployments expand and contract schemas so old and new binaries coexist during rolling updates.",
        "pillars": ["expand-contract", "feature flags", "dual write period", "blue-green", "canary"],
        "diagram": """flowchart TD
  old[Old pods]
  new[New pods]
  lb[Load balancer]
  lb --> old
  lb --> new""",
        "scenario": "rename column via expand-add-backfill-switch-drop",
        "pitfall": "deploying breaking API and DB change same release",
        "prev": "D19-T023",
        "next": "D19-T025",
    },
    "D19-T025": {
        "thesis": "The strangler fig pattern incrementally routes traffic from a legacy monolith to new services until the monolith can be retired.",
        "pillars": ["facade router", "incremental slices", "parallel run", "feature parity checklist", "decommission plan"],
        "diagram": """flowchart LR
  client[Client]
  facade[Strangler facade]
  leg[Legacy monolith]
  neo[New service]
  client --> facade
  facade -->|old paths| leg
  facade -->|new paths| neo""",
        "scenario": "new returns flow go to Returns service; rest stays on monolith",
        "pitfall": "big-bang rewrite with no traffic switch",
        "prev": "D19-T024",
        "next": "D19-T026",
    },
    "D19-T026": {
        "thesis": "A service mesh moves cross-cutting connectivity—mTLS, retries, telemetry—to a data plane of sidecar proxies controlled by a mesh control plane.",
        "pillars": ["data plane", "control plane", "mutual TLS", "traffic policies", "observability"],
        "diagram": """flowchart TB
  cp[Control plane]
  subgraph mesh[Data plane]
    a[App + sidecar]
    b[App + sidecar]
    a <--> b
  end
  cp --> mesh""",
        "scenario": "uniform retry policy without patching every service library",
        "pitfall": "mesh before you need uniform policy at scale",
        "prev": "D19-T025",
        "next": "D19-T027",
    },
    "D19-T027": {
        "thesis": "Sidecars and proxies intercept pod traffic to enforce policy without changing application bytecode for every concern.",
        "pillars": ["Envoy", "iptables redirect", "init containers", "resource overhead", "upgrade cadence"],
        "diagram": """flowchart LR
  app[Application container]
  sc[Sidecar proxy]
  net[Pod network]
  app --> sc --> net""",
        "scenario": "Envoy terminates mTLS and exports metrics per route",
        "pitfall": "sidecar CPU/memory larger than the app",
        "prev": "D19-T026",
        "next": "D19-T028",
    },
    "D19-T028": {
        "thesis": "Monolith-to-microservices migration sequences organizational readiness, boundary discovery, strangler routing, and operability before service count grows.",
        "pillars": ["team topology", "platform capabilities", "CI/CD per service", "SLOs", "incremental extraction"],
        "diagram": """flowchart TD
  assess[Assess monolith]
  slice[Identify slice]
  extract[Extract service]
  operate[Operate and iterate]
  assess --> slice --> extract --> operate
  operate --> slice""",
        "scenario": "extract notifications after observability and CI exist",
        "pitfall": "microservices day one without deployment automation",
        "prev": "D19-T027",
        "next": "D19-T029",
    },
    "D19-T029": {
        "thesis": "Microservices failure modes include cascading outages, data drift, contract skew, and operational entropy that a monolith hides in one process.",
        "pillars": ["cascading failure", "split brain data", "version skew", "thundering herd", "on-call fatigue"],
        "diagram": """flowchart TD
  slow[Slow dependency]
  retry[Retry storm]
  exhaust[Thread pool exhausted]
  outage[User-visible outage]
  slow --> retry --> exhaust --> outage""",
        "scenario": "one bad deploy plus aggressive retries takes down gateway",
        "pitfall": "blaming network without checking retry policy",
        "prev": "D19-T028",
        "next": "D19-T030",
    },
    "D19-T030": {
        "thesis": "Microservices are a trade-off, not a default: small teams, unclear domains, or weak ops maturity often ship faster and safer as a modular monolith.",
        "pillars": ["team size", "domain clarity", "operational cost", "latency budget", "modular monolith"],
        "diagram": """flowchart LR
  q{Clear boundaries and ops?}
  q -->|no| mono[Modular monolith]
  q -->|yes| ms[Microservices]""",
        "scenario": "startup keeps monolith until two teams block each other on deploy",
        "pitfall": "microservices for resume-driven architecture",
        "prev": "D19-T029",
        "next": None,
    },
}

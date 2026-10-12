# ruff: noqa: E501
"""Per-topic metadata for D16-T001..D16-T033."""

from __future__ import annotations

from textwrap import dedent

from d16_data.shared import A

TOPIC_ROWS: list[dict] = [
    {
        "id": "D16-T001",
        "focus": "what the system must do for users and operators",
        "mermaid": "flowchart TD\n  stakeholder[StakeholderNeeds]\n  useCase[UseCasesAndFlows]\n  apiSurface[APISurface]\n  dataOps[DataCreateReadUpdate]\n  stakeholder --> useCase\n  useCase --> apiSurface\n  useCase --> dataOps",
        "code_file": "d16_t001_functional_req.py",
        "capacity_extra": "Functional scope drives A (actions/day). If each use case maps to k API calls, multiply: Q_avg ≈ (DAU × A × k) / 86,400.",
        "confused": "feature list versus testable requirements",
        "combo": "`D16-T003` requirement clarification, `D06-T002` resource modeling",
    },
    {
        "id": "D16-T002",
        "focus": "latency, availability, durability, security, and cost targets",
        "mermaid": "flowchart LR\n  users[Users]\n  nfr[NFRTargets]\n  design[DesignChoices]\n  verify[Verification]\n  users --> nfr\n  nfr --> design\n  design --> verify",
        "code_file": "d16_t002_nfr.py",
        "capacity_extra": "NFR p99 latency L_target constrains fan-out: if each hop costs l_i, sum(l_i) ≤ L_target. Availability target A_target implies allowed downtime ≈ (1 - A_target) × year_seconds.",
        "confused": "SLI versus SLO versus SLA",
        "combo": "`D16-T008` SLOs, `D16-T007` latency budgets",
    },
    {
        "id": "D16-T003",
        "focus": "structured questions that narrow the design space",
        "mermaid": "flowchart TD\n  prompt[VaguePrompt]\n  clarify[ClarifyingQuestions]\n  scope[ScopedRequirements]\n  design[DesignPhase]\n  prompt --> clarify\n  clarify --> scope\n  scope --> design",
        "code_file": "d16_t003_clarify.py",
        "capacity_extra": "Clarification should pin U, p, A, and read/write ratio before using Q_avg = (DAU × A) / 86,400.",
        "confused": "assumptions versus requirements",
        "combo": "`D16-T001` functional requirements, `D16-T004` capacity estimation",
    },
    {
        "id": "D16-T004",
        "focus": "back-of-the-envelope sizing with explicit assumptions",
        "mermaid": "flowchart TD\n  assume[StateAssumptions]\n  dau[ComputeDAU]\n  qps[DeriveQavgQpeak]\n  resources[SizeDBCacheBW]\n  assume --> dau\n  dau --> qps\n  qps --> resources",
        "code_file": "d16_t004_capacity.py",
        "capacity_extra": "Servers_needed ≈ Q_peak / (per_instance_QPS × utilization). utilization is often 0.5–0.7 for stateless APIs.",
        "confused": "average QPS versus peak QPS",
        "combo": "`D16-T005` peak traffic, `D16-T006` bandwidth and storage",
    },
    {
        "id": "D16-T005",
        "focus": "peak multipliers, burstiness, and seasonality",
        "mermaid": "flowchart LR\n  qavg[Qavg]\n  kpeak[KpeakMultiplier]\n  qpeak[Qpeak]\n  provision[ProvisionForQpeak]\n  qavg --> kpeak\n  kpeak --> qpeak\n  qpeak --> provision",
        "code_file": "d16_t005_qps_peak.py",
        "capacity_extra": "If traffic is spiky within the day, Q_peak_hour ≈ Q_avg × (24 / active_hours) × burst_factor. State active_hours and burst_factor.",
        "confused": "peak RPS versus sustained RPS",
        "combo": "`D16-T023` load balancing, `D16-T022` scaling",
    },
    {
        "id": "D16-T006",
        "focus": "egress, ingress, and durable storage growth",
        "mermaid": "flowchart TD\n  qps[Qpeak]\n  payload[BytesPerRequest]\n  bw[BandwidthEgress]\n  rows[RowsPerDay]\n  disk[DiskGrowth]\n  qps --> bw\n  payload --> bw\n  rows --> disk",
        "code_file": "d16_t006_bw_storage.py",
        "capacity_extra": "Replication_factor R multiplies storage: Storage_total ≈ Storage_day × retention_days × R. CDN offload reduces origin BW by hit_rate × static_bytes.",
        "confused": "bandwidth versus storage IOPS",
        "combo": "`D16-T024` caching, `D07-T020` indexing",
    },
    {
        "id": "D16-T007",
        "focus": "end-to-end latency decomposition",
        "mermaid": "flowchart LR\n  client[Client]\n  edge[EdgeLB]\n  svc[Service]\n  db[Database]\n  client -->|t1| edge\n  edge -->|t2| svc\n  svc -->|t3| db",
        "code_file": "d16_t007_latency.py",
        "capacity_extra": "Parallel calls: L_parallel ≈ max(l_i). Serial: L_serial = sum(l_i). Budget slack = L_target - L_serial.",
        "confused": "p50 versus p99 latency budgets",
        "combo": "`D16-T027` sync vs async, `D04-T023` latency",
    },
    {
        "id": "D16-T008",
        "focus": "SLIs, SLOs, error budgets, and nines of availability",
        "mermaid": "flowchart TD\n  sli[SLI]\n  slo[SLOTarget]\n  budget[ErrorBudget]\n  policy[ReleasePolicy]\n  sli --> slo\n  slo --> budget\n  budget --> policy",
        "code_file": "d16_t008_slo.py",
        "capacity_extra": "Three nines (99.9%) allows ≈ 8.76 h downtime/year. Error budget burn rate = failed_requests / total_requests over window.",
        "confused": "availability SLO versus durability",
        "combo": "`D16-T029` failure recovery, `D13-T018` monitoring",
    },
    {
        "id": "D16-T009",
        "focus": "resources, relationships, and API contracts",
        "mermaid": "flowchart TD\n  entity[Entities]\n  relation[Relationships]\n  rest[RESTResources]\n  schema[StorageSchema]\n  entity --> relation\n  relation --> rest\n  relation --> schema",
        "code_file": "d16_t009_api_model.py",
        "capacity_extra": "Hot entity size affects B_row and index size: index_bytes ≈ row_count × key_bytes × fanout_factor.",
        "confused": "REST resources versus database tables",
        "combo": "`D06-T002` URL design, `D07-T009` relationships",
    },
    {
        "id": "D16-T010",
        "focus": "boxes, arrows, trust boundaries, and data flows",
        "mermaid": "flowchart TD\n  client[Clients]\n  lb[LoadBalancer]\n  api[APIService]\n  cache[Cache]\n  db[(PrimaryDB)]\n  client --> lb\n  lb --> api\n  api --> cache\n  api --> db",
        "code_file": "d16_t010_hld.py",
        "capacity_extra": "Diagram each synchronous hop when summing latency budget. Mark async edges for workers and queues.",
        "confused": "deployment diagram versus logical architecture",
        "combo": "`D16-T011` low-level design, `D16-T028` SPOF",
    },
    {
        "id": "D16-T011",
        "focus": "classes, modules, and interaction protocols inside a service",
        "mermaid": "flowchart TD\n  handler[HTTPHandler]\n  service[DomainService]\n  repo[Repository]\n  handler --> service\n  service --> repo",
        "code_file": "d16_t011_lld.py",
        "capacity_extra": "LLD thread pools: max_in_flight ≈ Q_peak × L_avg if each request holds a thread for L_avg seconds (Little's law).",
        "confused": "LLD versus code layout folders",
        "combo": "`D16-T013` layered architecture, `D05-T004` services",
    },
    {
        "id": "D16-T012",
        "focus": "deployment unit boundaries and team ownership",
        "mermaid": "flowchart LR\n  mono[Monolith]\n  mod[ModularMonolith]\n  micro[Microservices]\n  mono -->|extract modules| mod\n  mod -->|split deploy| micro",
        "code_file": "d16_t012_deployment_style.py",
        "capacity_extra": "Microservices multiply Q_peak on internal calls: Q_internal ≈ Q_external × fanout. Size network and service mesh accordingly.",
        "confused": "microservices versus SOA buzzword",
        "combo": "`D16-T017` bounded contexts, `D15-T001` distributed basics",
    },
    {
        "id": "D16-T013",
        "focus": "presentation, application, domain, and infrastructure layers",
        "mermaid": "flowchart TD\n  ui[Presentation]\n  app[Application]\n  domain[Domain]\n  infra[Infrastructure]\n  ui --> app\n  app --> domain\n  domain --> infra",
        "code_file": "d16_t013_layers.py",
        "capacity_extra": "Layer violations (UI calling SQL) hide N+1 query costs; estimate DB QPS as Q_peak × queries_per_request.",
        "confused": "layers versus microservice tiers",
        "combo": "`D16-T014` hexagonal, `D16-T015` clean architecture",
    },
    {
        "id": "D16-T014",
        "focus": "ports, adapters, and technology isolation",
        "mermaid": "flowchart TD\n  core[ApplicationCore]\n  port[Ports]\n  adapter[Adapters]\n  db[(DBAdapter)]\n  http[HTTPAdapter]\n  core --> port\n  port --> adapter\n  adapter --> db\n  adapter --> http",
        "code_file": "d16_t014_hexagonal.py",
        "capacity_extra": "Adapter swap should not change Q_avg; performance tests belong on adapter implementations (e.g., ORM vs raw SQL).",
        "confused": "hexagonal versus layered only",
        "combo": "`D16-T015` clean architecture, `D05-T005` DI",
    },
    {
        "id": "D16-T015",
        "focus": "dependency rule pointing inward to domain",
        "mermaid": "flowchart TD\n  entities[Entities]\n  usecases[UseCases]\n  interface[InterfaceAdapters]\n  frameworks[FrameworksDrivers]\n  frameworks --> interface\n  interface --> usecases\n  usecases --> entities",
        "code_file": "d16_t015_clean.py",
        "capacity_extra": "Keep hot paths in use cases measurable; p99 per use case ≤ allocated slice of L_target.",
        "confused": "clean architecture versus DDD only",
        "combo": "`D16-T016` DDD, `D16-T018` SOLID",
    },
    {
        "id": "D16-T016",
        "focus": "ubiquitous language, aggregates, and domain events",
        "mermaid": "flowchart TD\n  domain[DomainModel]\n  aggregate[AggregateRoot]\n  event[DomainEvents]\n  domain --> aggregate\n  aggregate --> event",
        "code_file": "d16_t016_ddd.py",
        "capacity_extra": "Aggregate size caps B_row and transaction time; large aggregates inflate lock hold time under Q_peak.",
        "confused": "DDD tactical patterns versus strategic design",
        "combo": "`D16-T017` bounded contexts, `D16-T009` data model",
    },
    {
        "id": "D16-T017",
        "focus": "context boundaries and consistency per aggregate",
        "mermaid": "flowchart LR\n  ctxA[ContextA]\n  ctxB[ContextB]\n  acl[AntiCorruptionLayer]\n  ctxA --> acl\n  acl --> ctxB",
        "code_file": "d16_t017_bounded.py",
        "capacity_extra": "Cross-context calls add sync latency; prefer events: ingest Q_events ≈ Q_peak × events_per_request.",
        "confused": "bounded context versus microservice",
        "combo": "`D16-T012` microservices, `D15-T010` messaging",
    },
    {
        "id": "D16-T018",
        "focus": "single responsibility, open/closed, and dependency inversion",
        "mermaid": "flowchart TD\n  client[Client]\n  abstraction[Abstraction]\n  impl[Implementation]\n  client --> abstraction\n  abstraction --> impl",
        "code_file": "d16_t018_solid.py",
        "capacity_extra": "SRP reduces blast radius of deploys; smaller services can scale independently: scale factor per service from its Q_peak slice.",
        "confused": "SOLID in interviews versus pattern names",
        "combo": "`D16-T019` design patterns, `D16-T020` separation of concerns",
    },
    {
        "id": "D16-T019",
        "focus": "recurring solutions such as factory, strategy, and observer",
        "mermaid": "flowchart TD\n  problem[DesignProblem]\n  pattern[PatternTemplate]\n  tradeoff[Tradeoffs]\n  problem --> pattern\n  pattern --> tradeoff",
        "code_file": "d16_t019_patterns.py",
        "capacity_extra": "Patterns adding indirection may add latency Δl; ensure sum(l_i) still meets L_target.",
        "confused": "pattern name dropping versus problem fit",
        "combo": "`D16-T011` LLD, `D01-T007` OOP",
    },
    {
        "id": "D16-T020",
        "focus": "isolating reasons to change",
        "mermaid": "flowchart LR\n  auth[AuthConcern]\n  billing[BillingConcern]\n  notify[NotificationConcern]\n  auth -.->|no direct| billing",
        "code_file": "d16_t020_soc.py",
        "capacity_extra": "Separate read and write paths (CQRS-lite) when read QPS ≫ write QPS: Q_read ≈ Q_peak × read_ratio.",
        "confused": "SoC versus microservices mandatory split",
        "combo": "`D16-T021` stateless services, `D16-T013` layers",
    },
    {
        "id": "D16-T021",
        "focus": "session stickiness versus externalized state",
        "mermaid": "flowchart TD\n  req[Request]\n  stateless[StatelessInstance]\n  store[(SessionStore)]\n  req --> stateless\n  stateless --> store",
        "code_file": "d16_t021_state.py",
        "capacity_extra": "Session RAM ≈ concurrent_sessions × session_bytes. concurrent_sessions ≈ Q_peak × session_duration.",
        "confused": "stateless service versus stateless protocol",
        "combo": "`D16-T023` load balancing, `D16-T024` caching",
    },
    {
        "id": "D16-T022",
        "focus": "scale up versus scale out",
        "mermaid": "flowchart LR\n  vertical[VerticalScale]\n  horizontal[HorizontalScale]\n  limit[HardwareLimit]\n  vertical --> limit\n  horizontal --> limit",
        "code_file": "d16_t022_scaling.py",
        "capacity_extra": "Horizontal shards: per_shard_Q ≈ Q_peak / shard_count. Choose shard_count so per_shard_Q fits single-node headroom.",
        "confused": "auto-scaling versus capacity planning",
        "combo": "`D16-T026` partitioning, `D16-T023` load balancing",
    },
    {
        "id": "D16-T023",
        "focus": "L4/L7 balancers, algorithms, and health checks",
        "mermaid": "flowchart TD\n  clients[Clients]\n  lb[LoadBalancer]\n  n1[Instance1]\n  n2[Instance2]\n  clients --> lb\n  lb --> n1\n  lb --> n2",
        "code_file": "d16_t023_lb.py",
        "capacity_extra": "Healthy instances needed N ≥ Q_peak / (instance_QPS × u). Round-robin assumes uniform capacity; use weighted if not.",
        "confused": "client-side versus server-side LB",
        "combo": "`D04-T019` reverse proxies, `D16-T028` SPOF",
    },
    {
        "id": "D16-T024",
        "focus": "client, CDN, app, and database caches",
        "mermaid": "flowchart TD\n  client[ClientCache]\n  cdn[CDN]\n  app[AppCache]\n  db[(Database)]\n  client --> cdn\n  cdn --> app\n  app --> db",
        "code_file": "d16_t024_cache.py",
        "capacity_extra": "Hit rate h reduces DB QPS: Q_db ≈ Q_peak × (1 - h). RAM ≈ working_set × value_bytes.",
        "confused": "cache aside versus read-through",
        "combo": "`D16-T006` bandwidth, `D07-T019` indexes",
    },
    {
        "id": "D16-T025",
        "focus": "SQL, document, wide-column, and graph fit",
        "mermaid": "flowchart TD\n  workload[WorkloadShape]\n  sql[(Relational)]\n  nosql[(SpecializedStore)]\n  workload -->|ACID joins| sql\n  workload -->|flex schema scale| nosql",
        "code_file": "d16_t025_db_pick.py",
        "capacity_extra": "Write-heavy logs: choose append-friendly store; rows/day from DAU×A drives partition count.",
        "confused": "polyglot persistence versus hype",
        "combo": "`D16-T026` replication, `D08-T001` SQL depth",
    },
    {
        "id": "D16-T026",
        "focus": "replicas, leaders, and partition keys",
        "mermaid": "flowchart TD\n  leader[(LeaderShard)]\n  replica[(ReadReplica)]\n  partkey[PartitionKey]\n  partkey --> leader\n  leader --> replica",
        "code_file": "d16_t026_repl_part.py",
        "capacity_extra": "Hot key problem: one partition receives λ_hot ≈ Q_peak; mitigate with key splitting or caching.",
        "confused": "replication versus partitioning",
        "combo": "`D15-T005` consistency models, `D16-T030` CAP trade-offs",
    },
    {
        "id": "D16-T027",
        "focus": "request/response versus queues and callbacks",
        "mermaid": "flowchart LR\n  sync[SynchronousPath]\n  async[MessageQueue]\n  worker[Worker]\n  sync -->|immediate| client[Client]\n  async --> worker",
        "code_file": "d16_t027_async.py",
        "capacity_extra": "Queue depth ≈ (produce_rate - consume_rate) × time. Size consumers so consume_rate ≥ peak produce_rate.",
        "confused": "async IO versus async workflow",
        "combo": "`D15-T002` queues, `D16-T007` latency",
    },
    {
        "id": "D16-T028",
        "focus": "identifying and eliminating single points of failure",
        "mermaid": "flowchart TD\n  path[CriticalPath]\n  spof[SPOFComponent]\n  mitigate[RedundancyOrFailover]\n  path --> spof\n  spof --> mitigate",
        "code_file": "d16_t028_spof.py",
        "capacity_extra": "Active-active doubles capacity need but removes failover RTO; state cost ≈ 2× RAM for hot state.",
        "confused": "SPOF versus bottleneck",
        "combo": "`D16-T029` failure scenarios, `D16-T008` availability",
    },
    {
        "id": "D16-T029",
        "focus": "blast radius, runbooks, and recovery objectives",
        "mermaid": "flowchart TD\n  fail[FailureEvent]\n  detect[Detection]\n  contain[Containment]\n  recover[Recovery]\n  fail --> detect\n  detect --> contain\n  contain --> recover",
        "code_file": "d16_t029_recovery.py",
        "capacity_extra": "RPO sets max data loss window; RTO sets max downtime. Backup storage ≈ daily_change_rate × retention.",
        "confused": "disaster recovery versus backup only",
        "combo": "`D16-T028` SPOF, `D13-T020` incident response",
    },
    {
        "id": "D16-T030",
        "focus": "CAP, PACELC, and product-appropriate consistency",
        "mermaid": "flowchart TD\n  partition[NetworkPartition]\n  choose[ChooseCOrA]\n  product[ProductTolerance]\n  partition --> choose\n  choose --> product",
        "code_file": "d16_t030_cap.py",
        "capacity_extra": "Strong consistency may add quorum round-trips: L_write ≈ 2× RTT + storage. Eventual paths shorten L_read.",
        "confused": "CAP theorem as a pick-one menu",
        "combo": "`D15-T005` consistency, `D16-T026` replication",
    },
    {
        "id": "D16-T031",
        "focus": "unit economics, reserved capacity, and architectural cost drivers",
        "mermaid": "flowchart LR\n  arch[Architecture]\n  cost[CostDrivers]\n  optimize[OptimizeLever]\n  arch --> cost\n  cost --> optimize",
        "code_file": "d16_t031_cost.py",
        "capacity_extra": "Monthly_egress_cost ≈ (BW_GB_month) × price_per_GB. Right-size instances when CPU < 30% sustained.",
        "confused": "cloud bill versus engineering time cost",
        "combo": "`D16-T022` scaling, `D16-T024` caching for hit rate savings",
    },
    {
        "id": "D16-T032",
        "focus": "threat modeling, authn/z, logs, metrics, and traces",
        "mermaid": "flowchart TD\n  req[Request]\n  auth[AuthNAuthZ]\n  app[AppLogic]\n  obs[LogsMetricsTraces]\n  req --> auth\n  auth --> app\n  app --> obs",
        "code_file": "d16_t032_sec_obs.py",
        "capacity_extra": "Observability overhead ≈ sampling_rate × Q_peak × bytes_per_span. Budget 1–5% CPU for telemetry.",
        "confused": "security at design time versus audit checkbox",
        "combo": "`D12-T001` security basics, `D13-T018` monitoring",
    },
    {
        "id": "D16-T033",
        "focus": "recording decisions, context, and consequences",
        "mermaid": "flowchart TD\n  context[Context]\n  decision[Decision]\n  consequences[Consequences]\n  context --> decision\n  decision --> consequences",
        "code_file": "d16_t033_adr.py",
        "capacity_extra": "ADRs should capture assumed Q_peak and SLO when the decision depends on scale; revisit when assumptions 10×.",
        "confused": "ADR versus design doc encyclopedia",
        "combo": "`D16-T012` monolith vs microservices decision, `D16-T025` database selection",
    },
]


def _code_template(tid: str, focus: str) -> str:
    num = tid.split("-T")[1]
    return dedent(
        f'''
        """Hypothetical sizing helper for {tid} — interview practice only."""

        SECONDS_PER_DAY = 86_400


        def qps_from_assumptions(
            registered_users: int,
            dau_fraction: float,
            actions_per_dau_per_day: float,
            peak_multiplier: float,
        ) -> tuple[float, float]:
            """Return (q_avg, q_peak) using stated assumptions."""
            dau = registered_users * dau_fraction
            q_avg = (dau * actions_per_dau_per_day) / SECONDS_PER_DAY
            q_peak = q_avg * peak_multiplier
            return q_avg, q_peak


        def storage_per_day(dau: float, actions_per_dau: float, bytes_per_row: int) -> int:
            return int(dau * actions_per_dau * bytes_per_row)


        def describe(focus: str) -> str:
            return f"Topic focus: {{focus}}"


        if __name__ == "__main__":
            # Assumptions (hypothetical product — not a real company)
            U = 2_000_000
            p = 0.15
            A = 12.0
            K = 5.0
            B_row = 512
            q_avg, q_peak = qps_from_assumptions(U, p, A, K)
            dau = U * p
            day_bytes = storage_per_day(dau, A, B_row)
            assert q_avg > 0 and q_peak > q_avg
            print(describe("{focus}"))
            print(f"q_avg={{q_avg:.2f}} q_peak={{q_peak:.2f}} storage_day_mb={{day_bytes/1_000_000:.2f}}")
            print("ok")
        '''
    ).strip()


def _principles(name: str, focus: str) -> list[str]:
    return [
        f"{name} is the practice of making {focus} explicit before choosing databases, queues, or instance counts.",
        "Start from user-visible behavior and measurable outcomes, then derive components. Components exist to satisfy requirements, not the reverse.",
        "In interviews, write assumptions in the corner of the whiteboard and update them when the interviewer gives new facts.",
    ]


def _internal(name: str) -> list[str]:
    return [
        f"Inputs: stakeholder goals, constraints, and existing systems. Output for {name}: a decision or artifact the team can implement and test.",
        "Process: enumerate options, compare against requirements, pick the smallest design that meets NFRs with known risks documented.",
        "Feedback loop: production metrics and incidents should refine the original decision; architecture is iterative, not a one-shot diagram.",
    ]


def _examples(name: str, focus: str) -> list[str]:
    return [
        f"Analogy: {name} is like agreeing on the recipe before buying kitchen equipment. The oven size matters, but only after you know you are baking bread versus steaming dumplings.",
        f"Worked example: for a hypothetical URL shortener, {focus} might force you to prioritize low-latency redirects and global uniqueness before debating SQL versus NoSQL.",
    ]


def _practical(name: str) -> list[str]:
    return [
        f"In sprint planning, translate {name.lower()} into acceptance criteria and non-functional checks on each story.",
        "During design reviews, block merges that add components without tracing them to a requirement or an explicit risk acceptance.",
    ]


def _debugging(name: str) -> list[str]:
    return [
        f"Symptom: architecture debates never converge. Often the team skipped {name.lower()} and is arguing about favorite technologies.",
        "Mitigation: time-box clarification, write assumptions, assign an owner to validate the riskiest assumption with a spike or load test.",
    ]


def _exercises(tid: str, name: str, focus: str) -> list[tuple[str, str, str]]:
    return [
        (
            f"Write a one-page requirements snippet for a hypothetical ride-hailing dispatch API emphasizing {name.lower()}. Include at least five functional bullets and three measurable NFRs.",
            "Functional items are testable; NFRs include numbers or targets; no technology names in the first draft.",
            "Sample: functional covers match driver, accept trip, cancel, fare estimate, trip history; NFRs p99 dispatch < 200 ms (assumed), 99.9% availability, encrypt PII at rest.",
        ),
        (
            f"Given U=500k, p=0.2, A=8, K_peak=4, compute Q_avg and Q_peak and identify which part of {name.lower()} would break first if DB write QPS max is 2000.",
            "Show arithmetic; state bottleneck; propose one mitigation tied to the topic.",
            "DAU=100k; total actions/day=800k; Q_avg≈9.26; Q_peak≈37. If each action is one write, peak writes exceed 2000 — mitigate with async write buffer, batching, or shard writes.",
        ),
        (
            f"Trade-off: stay monolithic versus split a service for {focus}. List two benefits and two costs and pick one side for an MVP.",
            "Mentions operational complexity, data consistency, and team size; choice matches stated constraints.",
            "MVP with small team: modular monolith — lower ops burden, single deploy, clear modules; defer microservices until Q_peak or org boundaries force split.",
        ),
    ]


def _iv(name: str, focus: str) -> dict:
    n = name
    f = focus
    return {
        "beginner": [
            (
                f"What is {n} in a system design interview?",
                A(
                    f"{n} is how you make {f} explicit so the design can be judged against measurable goals.",
                    "Without it, you risk building the wrong system that is fast but incorrect, or correct but unusably slow.",
                    "Interviewers listen for whether you write user stories, constraints, and success metrics before naming AWS services.",
                    "Treat it as the contract between product, engineering, and operations for what 'done' means.",
                ),
                f"Define {n}",
            ),
            (
                f"Why should {n} come before drawing boxes?",
                A(
                    "Boxes represent components chosen to satisfy requirements; unnamed requirements make every component optional.",
                    "Early diagrams cement premature decisions that are painful to undo when load or compliance appears.",
                    "Ordering shows structured thinking: clarify, estimate, architect, deepen.",
                    "It also saves time because you avoid deep-diving the wrong subsystem.",
                ),
                "Order requirements before architecture",
            ),
            (
                f"Give one example of {f}.",
                A(
                    "For a hypothetical chat app, message delivery latency and offline sync behavior are part of the design conversation.",
                    "You might require read receipts for 1:1 chats but not for large channels to control fan-out write load.",
                    "Each example should map to an API, a data structure, or a failure behavior you can test.",
                    "Examples grounded in user journeys beat abstract buzzwords.",
                ),
                "Example tied to user journey",
            ),
            (
                f"How do engineers validate that {n} were met?",
                A(
                    "Functional requirements become automated tests, contract tests, and manual QA scenarios.",
                    "Non-functional requirements become load tests, chaos experiments, and SLO dashboards.",
                    "Validation is continuous: CI for correctness, staging for performance, production for real traffic.",
                    "Document the mapping from requirement to test so gaps are visible during review.",
                ),
                "Validation strategy",
            ),
            (
                f"What is a common beginner mistake about {n}?",
                A(
                    "Copying a famous company's architecture slide without matching their requirements or scale.",
                    "Another mistake is listing features without priorities, which makes trade-offs impossible.",
                    "Interviewers want you to say what you would cut under a one-hour MVP constraint.",
                    "Mistakes are fixed by writing assumptions and asking clarifying questions.",
                ),
                "Anti-pattern: clone FAANG diagram",
            ),
        ],
        "intermediate": [
            (
                f"How does {n} interact with capacity estimation?",
                A(
                    f"{n} defines what to measure: actions per user, payload sizes, retention, and peak behavior.",
                    "Estimation turns those into Q_avg, Q_peak, storage, and bandwidth using explicit symbols.",
                    "If requirements change (e.g., add media uploads), every formula input changes — revisit the estimate.",
                    "Always state that numbers are hypothetical unless the interviewer supplies them.",
                ),
                "Link requirements to formulas",
            ),
            (
                f"How do you prioritize conflicting requirements for {f}?",
                A(
                    "Rank by business impact and regulatory cost: legal and safety beat convenience features.",
                    "Make trade-offs explicit: choose AP versus CP, or strong consistency on money only.",
                    "Use MoSCoW or a simple P0/P1 list when time-boxed.",
                    "Document rejected alternatives so the team does not relitigate every sprint.",
                ),
                "Prioritization method",
            ),
            (
                f"Where should {n} live in documentation?",
                A(
                    "Product requirements and engineering design docs cross-link: user stories link to API specs and SLOs.",
                    "ADRs capture contentious decisions with context and consequences.",
                    "Runbooks and on-call playbooks reference the NFRs they protect (latency, error rate).",
                    "Keep a single source of truth per fact to avoid wiki drift.",
                ),
                "Documentation placement",
            ),
            (
                f"How does {n} affect API design?",
                A(
                    "Each user journey becomes resources, methods, idempotency rules, and pagination contracts.",
                    "Error models and rate limits encode operational NFRs directly in the HTTP surface.",
                    "Versioning strategy reflects how strictly clients depend on stable behavior.",
                    "Skipping this step yields REST endpoints that mirror database tables without product meaning.",
                ),
                "API linkage",
            ),
            (
                f"When is it acceptable to defer part of {n}?",
                A(
                    "Defer only with explicit risk acceptance: document what might break and the trigger to revisit.",
                    "Security, privacy, and money correctness are poor candidates for deferral.",
                    "Cosmetic UX or secondary reports can wait if core journeys work.",
                    "In interviews, say what you defer for MVP and what you still stub (auth, observability hooks).",
                ),
                "MVP deferral rules",
            ),
        ],
        "advanced": [
            (
                f"How would you evolve {n} as scale grows 10×?",
                A(
                    "Re-baseline assumptions: U, p, A, and K_peak; identify the first saturated resource.",
                    "Split bottlenecks by concern: read scaling (cache, replicas), write scaling (sharding, queues).",
                    "Update SLOs and error budgets if product accepts different UX (eventual consistency).",
                    "Use ADRs to record why the architecture changed and what was rejected.",
                ),
                "10× growth evolution",
            ),
            (
                f"What metrics prove success for {f}?",
                A(
                    "Pick SLIs aligned to user pain: success rate, latency percentiles, freshness, cost per transaction.",
                    "Define SLO targets and measure error budget burn.",
                    "Supplement with business metrics (conversion, retention) tied to technical changes.",
                    "Avoid vanity metrics that improve while users suffer (average latency hiding tail).",
                ),
                "SLI selection",
            ),
            (
                f"How do organizational constraints shape {n}?",
                A(
                    "Team topology affects service boundaries: Conway's law means interfaces follow communication lines.",
                    "Compliance regimes (PCI, HIPAA) harden certain NFRs regardless of traffic.",
                    "Skill mix may favor managed services versus self-hosted databases.",
                    "State constraints explicitly instead of pretending a textbook ideal design.",
                ),
                "Conway and compliance",
            ),
            (
                f"Describe a failure mode when {n} are vague.",
                A(
                    "Ambiguous durability requirements cause data loss incidents that look like bugs but are specification gaps.",
                    "Vague latency goals lead to over-built caches or under-provisioned databases discovered only at launch.",
                    "On-call pays the cost as repeated Sev2s without a clear definition of fixed.",
                    "Prevention is writing testable statements and reviewing them in architecture sign-off.",
                ),
                "Failure from vague reqs",
            ),
            (
                f"How do you reconcile {n} across multiple teams?",
                A(
                    "Use bounded contexts and published API contracts with versioning policy.",
                    "Shared platform teams provide paved roads (auth, logging) so product teams do not reinvent.",
                    "Governance light-weight: architecture review for cross-cutting changes only.",
                    "Escalate conflicts with data: prototype cost, incident history, projected Q_peak.",
                ),
                "Multi-team alignment",
            ),
        ],
        "scenarios": [
            (
                f"You have 25 minutes left in an interview after clarification. How do you cover {n} quickly?",
                A(
                    "Spend five minutes confirming top three functional flows and two NFRs with numbers.",
                    "Spend ten minutes on diagram and estimation using stated U, p, A, K_peak.",
                    "Spend ten minutes on deep dive the interviewer chooses (storage, cache, or scaling).",
                    "Keep talking aloud; trade depth for breadth if prompted.",
                ),
                "Time-boxed interview plan",
            ),
            (
                "Interviewer doubles traffic and halves latency budget. What do you revisit first?",
                A(
                    "Recompute Q_peak and check synchronous chain against the new L_target.",
                    "Identify parallelization, caching, and read replicas before sharding.",
                    "Question whether functional scope can shrink (drop noncritical features).",
                    "Update risk list: hot keys, DB connection pools, thundering herd on cache miss.",
                ),
                "Changed constraints response",
            ),
            (
                f"Product adds a feature that conflicts with an earlier {n} decision. What process do you follow?",
                A(
                    "Write a new ADR or amend the old one with context, decision, and consequences.",
                    "Quantify impact on Q_peak, storage, and SLO error budget.",
                    "Ship behind a flag if possible; measure before full rollout.",
                    "Communicate to support and on-call what behavior changed.",
                ),
                "Changing requirements process",
            ),
            (
                "Stakeholders want 'five nines' on a budget for 'three nines'. How do you respond?",
                A(
                    "Translate nines to downtime minutes per year and required redundancy cost.",
                    "Propose tiered availability: critical path higher than analytics.",
                    "Offer error budget policy instead of impossible SLA promises.",
                    "Use hypothetical cost model, not a real vendor quote, unless provided.",
                ),
                "Availability negotiation",
            ),
            (
                f"Design review finds no traceability from tests to {n}. What do you add?",
                A(
                    "Requirement IDs in test case titles and CI reporting.",
                    "Contract tests for APIs and performance tests for SLO-critical endpoints.",
                    "Checklist in PR template linking story to NFR validation.",
                    "Quarterly audit sampling requirements to tests mapping.",
                ),
                "Traceability fix",
            ),
        ],
        "follow_ups": [
            (
                f"How does {n} connect to database schema choices?",
                A(
                    "Schema encodes invariants implied by requirements: uniqueness, relationships, retention.",
                    "Migration strategy is a non-functional requirement for zero-downtime deploys.",
                    "Indexing follows query patterns derived from user journeys.",
                    "See domain 7 for normalization and indexing depth.",
                ),
                "Link to D07 schema",
            ),
            (
                f"How does {n} connect to distributed systems concerns?",
                A(
                    "Once Q_peak exceeds one node, you need partitioning, replication, and consistency choices.",
                    "Distributed tracing and idempotency become functional requirements for async flows.",
                    "Failure handling must be specified, not assumed.",
                    "Domain 15 expands algorithms and trade-offs beyond this fundamentals track.",
                ),
                "Link to D15 distributed",
            ),
            (
                f"What should you study next after mastering {n}?",
                A(
                    "Follow the D16 topic sequence: estimation, architecture styles, scaling, caching, and CAP.",
                    "Practice full mock designs end-to-end with a timer.",
                    "Read postmortems to see requirements gaps that caused outages.",
                    "Build a personal checklist you reuse in every interview.",
                ),
                "Next study steps",
            ),
        ],
    }


def _revision(name: str) -> str:
    return dedent(
        f"""
        - {name} must be explicit, testable, and prioritized before technology choices.
        - State U, p, A, K_peak aloud for every estimation question.
        - Tie components on diagrams back to a requirement or risk.
        - Document trade-offs and rejected options briefly.
        """
    ).strip()


META_BY_ID: dict[str, dict] = {}

for row in TOPIC_ROWS:
    tid = row["id"]
    num = tid.split("-T")[1]
    # Name filled at assemble time from inventory; use placeholder for iv/exercise strings
    name = row.get("name", tid)
    focus = row["focus"]
    META_BY_ID[tid] = {
        "definition": f"**{tid}** covers **{focus}** as part of system design fundamentals.",
        "why": f"Production systems fail when teams skip {focus} and optimize the wrong layer.",
        "interview_angle": f"you narrate {focus} clearly while sizing with hypothetical assumptions",
        "principles": _principles(name, focus),
        "internal": _internal(name),
        "examples": _examples(name, focus),
        "practical": _practical(name),
        "debugging": _debugging(name),
        "mermaid": row["mermaid"],
        "code_file": row["code_file"],
        "code": _code_template(tid, focus),
        "capacity_extra": row["capacity_extra"],
        "confused": row["confused"],
        "combo": row["combo"],
        "exercises": _exercises(tid, name, focus),
        "revision_bullets": _revision(name),
        "iv": _iv(name, focus),
        "_focus": focus,
    }


def enrich_names_from_inventory(inv_name: str, tid: str) -> None:
    """Patch display name into meta for prose quality."""
    meta = META_BY_ID[tid]
    focus = meta["_focus"]
    meta["definition"] = (
        f"**{inv_name}** is the discipline of addressing **{focus}** when designing backend systems."
    )
    meta["why"] = (
        f"Teams that treat {inv_name.lower()} as optional rework architecture under fire during incidents and launch weeks."
    )
    meta["interview_angle"] = f"you connect {inv_name.lower()} to diagrams, formulas, and trade-offs"
    meta["principles"] = _principles(inv_name, focus)
    meta["internal"] = _internal(inv_name)
    meta["examples"] = _examples(inv_name, focus)
    meta["practical"] = _practical(inv_name)
    meta["debugging"] = _debugging(inv_name)
    meta["exercises"] = _exercises(tid, inv_name, focus)
    meta["revision_bullets"] = _revision(inv_name)
    meta["iv"] = _iv(inv_name, focus)

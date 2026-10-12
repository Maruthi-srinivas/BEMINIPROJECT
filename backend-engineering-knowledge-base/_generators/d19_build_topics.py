# ruff: noqa: E501
"""Build full D19 topic packages from inventory rows and TOPIC_SPECS."""

from __future__ import annotations

from d19_topic_specs import TOPIC_SPECS


def sent(*parts: str) -> str:
    return " ".join(p.strip() for p in parts if p.strip())


def qa(q: str, a1: str, a2: str, a3: str, a4: str) -> dict:
    return {"q": q, "a": sent(a1, a2, a3, a4), "bank": q}


def mistakes_md(name: str, pitfall: str, pillars: list[str]) -> str:
    items = [
        f"Adopting {name.lower()} patterns before the organization can operate them (CI/CD, tracing, on-call).",
        f"The classic pitfall: {pitfall}.",
        f"Treating {pillars[0]} as a slide title instead of an enforced design rule in code review.",
        "Sharing databases or libraries that hide coupling while labels say microservices.",
        "Optimizing for number of services instead of deploy independence and clear ownership.",
        "Skipping contract tests between teams and discovering breaks only in production.",
    ]
    return "\n".join(f"- {x}" for x in items)


def tradeoffs_table(name: str) -> str:
    return f"""| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Apply {name} fully | Clear ownership and evolvability | Higher moving parts | Multiple teams, stable domain seams | One team, unclear boundaries |
| Defer / simplify | Faster delivery early | Rework later | Product still searching for model | You already feel deploy pain |
| Sync communication | Simple mental model | Tail latency stacks | Need immediate answer | Many side effects |
| Async messaging | Decouples peaks | Eventual consistency | Notifications, analytics | Interactive checkout guardrails |
| Strong consistency | Easier reasoning | Coupling and locks | Single service DB | Cross-service money movement |
| Eventual consistency | Independent scaling | Reconciliation work | Read models, replicas | Invariants spanning services without saga |"""


def default_code(name: str, scenario: str) -> tuple[str, str, str]:
    intro = (
        f"File: conceptual illustration for {name}. "
        "Dependencies: Python 3 standard library only (no broker or cluster required)."
    )
    code = f'''"""Illustrates control flow for: {scenario}."""

from dataclasses import dataclass
from enum import Enum
import time
import uuid


class StepResult(Enum):
    OK = "ok"
    FAIL = "fail"


@dataclass
class Correlation:
    trace_id: str
    idempotency_key: str


def with_correlation() -> Correlation:
    return Correlation(trace_id=str(uuid.uuid4()), idempotency_key=str(uuid.uuid4()))


def simulate_remote(name: str, fail: bool = False) -> StepResult:
    time.sleep(0.001)
    return StepResult.FAIL if fail else StepResult.OK


def run_flow(corr: Correlation) -> str:
    print("trace", corr.trace_id, "idem", corr.idempotency_key)
    if simulate_remote("primary") == StepResult.FAIL:
        return "aborted"
    if simulate_remote("secondary", fail=False) == StepResult.FAIL:
        simulate_remote("compensate")
        return "compensated"
    return "completed"


if __name__ == "__main__":
    assert run_flow(with_correlation()) == "completed"
    print("ok")'''
    footer = (
        "How to run: `python` this file from any directory. "
        "Expected output includes `ok`. "
        "Important lines: correlation ids model production tracing and idempotency. "
        "Replace `simulate_remote` with real HTTP or message clients in a service codebase."
    )
    return intro, code, footer


def build_interview(meta: dict, spec: dict) -> dict:
    name = meta["name"]
    thesis = spec["thesis"]
    pitfall = spec["pitfall"]
    scenario = spec["scenario"]
    prev_t = spec.get("prev")
    next_t = spec.get("next")

    beginner = [
        qa(
            f"What is {name} in a microservices system?",
            f"{name} is about {thesis.split('.')[0].lower()}.",
            "It shows up when multiple teams deploy services that must cooperate without sharing one database.",
            "Interviewers want a concrete example, not a glossary recitation.",
            f"A strong answer mentions {scenario}.",
        ),
        qa(
            f"Why does {name} matter for backend engineers?",
            "Distributed systems move failure and consistency problems from hidden in-process calls to explicit network boundaries.",
            f"Without {name.lower()}, teams rediscover the same outages and data bugs on every new service.",
            "Production work includes designing APIs, operability, and rollback paths—not only coding features.",
            "Tie the concept to deploy independence or customer-visible reliability.",
        ),
        qa(
            f"Name one component involved in {name}.",
            f"Typical building blocks include {', '.join(spec['pillars'][:3])}.",
            "Each component has an owner: application code, platform, or security.",
            "You should say what the component does in one sentence, not only its product name.",
            "Follow up with how you would observe it in metrics or traces.",
        ),
        qa(
            f"What is a common misconception about {name}?",
            f"People assume the pattern is free; in practice {pitfall}.",
            "Another misconception is that tools alone implement the idea—policy and code review enforce it.",
            "Microservices amplify both good and bad architecture decisions.",
            "Interviewers listen for humility about operational cost.",
        ),
        qa(
            f"How does {name} relate to the API gateway or service mesh?",
            "Edge gateways handle north-south client traffic; meshes often handle east-west policy between services.",
            f"{name} may appear in gateway routes, sidecar config, or pure application logic depending on topic.",
            "Do not dump every platform component—pick the one that actually enforces this concern.",
            "Mention correlation ids or auth when the topic touches cross-cutting security or observability.",
        ),
    ]

    intermediate = [
        qa(
            f"How would you implement {name} on a greenfield checkout platform?",
            f"Start from {scenario} and list services, data owners, and sync vs async steps.",
            "Publish API contracts and add contract tests before splitting repositories.",
            "Introduce observability (trace id propagation) before scaling service count.",
            "Roll out with feature flags or strangler routing if replacing legacy.",
        ),
        qa(
            f"What trade-off does {name} introduce versus a modular monolith?",
            thesis,
            "You gain team autonomy and independent scaling at the cost of network calls, versioning, and operations.",
            "Measure whether deploy frequency or incident rate actually improved after the split.",
            "If metrics did not improve, boundaries may be wrong—not the idea of distribution itself.",
        ),
        qa(
            f"Which failures should you design for when applying {name}?",
            "Timeouts, partial responses, duplicate deliveries, and skewed versions during rolling deploys.",
            "Plan compensations or reconciliation when work spans services.",
            "Use bulkheads so one slow dependency does not exhaust shared pools.",
            "Document staleness SLAs wherever consistency is eventual.",
        ),
        qa(
            f"How do you test {name} end to end?",
            "Contract tests between consumer and provider teams catch schema drift early.",
            "Integration tests with testcontainers or dedicated environments exercise real wire protocols.",
            "Chaos or fault injection validates breakers, retries, and saga compensations.",
            "Load tests reveal retry storms and fan-out tail latency.",
        ),
        qa(
            f"What metrics and logs prove {name} is healthy?",
            "Golden signals per dependency: latency, traffic, errors, saturation.",
            "Business KPIs tied to the flow—checkout success rate, saga completion, outbox lag.",
            "Traces should show one root span with child spans across services.",
            "Alert on SLO burn rate, not only raw error counts.",
        ),
    ]

    advanced = [
        qa(
            f"Design a migration path that adopts {name} without a big-bang rewrite.",
            "Use strangler facades to route slices of traffic to new services.",
            "Keep backward-compatible schemas during expand-contract database changes.",
            "Run old and new paths in parallel with shadow traffic or dual writes when needed.",
            "Decommission legacy only after parity checklist and error budgets allow.",
        ),
        qa(
            f"How does {name} interact with sagas, outbox, or CQRS?",
            "Sagas coordinate multi-step business processes; outbox makes emission reliable; CQRS separates read/write paths.",
            f"For {scenario}, pick the minimum pattern—do not stack all three by default.",
            "Compensations must be idempotent because messages arrive more than once.",
            "Projections may lag; document what users see during lag.",
        ),
        qa(
            f"Explain security implications of {name}.",
            "Service-to-service auth should use short-lived tokens or mTLS, not long-lived shared secrets in repos.",
            "Authorize per route and scope, especially on admin or payment operations.",
            "Gateways terminate TLS but must not become a shadow database of PII.",
            "Audit who can change routing, config, or mesh policy.",
        ),
        qa(
            f"When would you deliberately not apply {name} yet?",
            "When domain boundaries are unstable, team size is small, or platform automation is immature.",
            "A modular monolith with clear modules often outperforms premature distribution.",
            "Revisit the decision when deploy coupling or scaling limits hurt the business.",
            "This is engineering judgment, not dogma.",
        ),
        qa(
            f"How do you prevent {pitfall}?",
            "Encode rules in architecture reviews: no shared tables, no domain logic in gateways.",
            "Use context maps and event storming before carving services.",
            "Automate checks—lint imports across service repos, contract tests in CI.",
            "Leaders reward outcomes (deploy speed, reliability), not service count.",
        ),
    ]

    scenarios = [
        qa(
            f"Checkout latency doubles after introducing {name.lower()}; databases look fine. What next?",
            "Pull traces with the same trace id across gateway, services, and dependencies.",
            "Compare p95 per hop; look for fan-out, missing timeouts, or retry storms.",
            "Check for version skew between consumer and provider during a rolling deploy.",
            "Roll back or flip a feature flag while keeping observability on.",
        ),
        qa(
            f"Two services disagree on customer balance after {scenario}. How do you reconcile?",
            "Identify the system of record for the balance and which service is a replica.",
            "Compare event logs or outbox tables for missing or duplicate deliveries.",
            "Run a reconciliation job with idempotent corrections and audit trail.",
            "Add monitors on lag between writer and reader.",
        ),
        qa(
            f"On-call sees cascading 503s from the edge. How could {name} contribute to the blast radius?",
            "A breaker opening upstream may be correct—find the root slow dependency.",
            "Unbounded retries from many pods multiply load on a sick service.",
            "Shared thread pools without bulkheads let one client exhaust workers.",
            "Mitigate with backoff, jitter, concurrency limits, and cached fallbacks where safe.",
        ),
        qa(
            f"Product wants a cross-service report joining five databases. What do you propose?",
            "Reject distributed joins in request path; build a read model or data product fed by events.",
            "Use API composition with deadlines and partial results for interactive UI if needed.",
            "For analytics, stream events to a warehouse rather than live query micro-DBs.",
            "Document staleness acceptable to finance or support.",
        ),
        qa(
            f"A team ships a breaking API change during {name} rollout. How do you recover?",
            "Roll forward compatible provider or roll back consumer if faster.",
            "Use versioned endpoints or additive schemas per expand-contract rules.",
            "Post-incident: add consumer-driven contract tests and deployment ordering policy.",
            "Track which clients still call deprecated fields before removal.",
        ),
    ]

    followups = [
        qa(
            f"How does {name} connect to {prev_t or 'D19-T001'}?",
            f"{prev_t or 'D19-T001'} sets context; {name} specializes the next concern in the microservices curriculum.",
            "Real systems combine several patterns—state how they compose without contradictions.",
            "Point to the note section that lists related topics for deeper reading.",
            "Interviewers like explicit sequencing: principles, boundaries, then platform mechanics.",
        ),
        qa(
            f"How does {name} connect to {next_t or 'operational maturity'}?",
            f"{next_t or 'Later topics'} build on the decisions you make here.",
            "If you skip fundamentals, later patterns (mesh, sagas) become cargo cult.",
            "Name one hand-off artifact: ADR, context map, or SLO document.",
            "Show you think in roadmaps, not single tickets.",
        ),
        qa(
            "What would you put in an architecture decision record for this choice?",
            "Context: team topology, traffic, consistency needs.",
            f"Decision: how {name} will be applied, including rejected alternatives.",
            "Consequences: operability cost, failure modes, migration steps.",
            "Review date to revisit when team size or domain clarity changes.",
        ),
    ]

    return {
        "beginner": beginner,
        "intermediate": intermediate,
        "advanced": advanced,
        "scenarios": scenarios,
        "follow_ups": followups,
    }


def build_topic(inv: dict) -> dict:
    tid = inv["id"]
    spec = TOPIC_SPECS[tid]
    name = inv["name"]
    subdomain = inv["subdomain"]
    pillars = spec["pillars"]
    deps_display = ", ".join(f"`{d}`" for d in inv["dependencies"])

    meta = {
        "id": tid,
        "name": name,
        "subdomain": subdomain,
        "importance": inv["importance"],
        "complexity": inv["complexity"],
        "deps_display": deps_display,
        "note_path": inv["note_path"],
    }

    overview = [
        spec["thesis"],
        f"This note covers {name.lower()} as part of microservices architecture: {', '.join(pillars[:3])}, and related ideas.",
        f"In production the pattern appears when {spec['scenario']}.",
        "Interviewers use the topic to test whether you can reason about distributed systems without hand-waving.",
        f"Prerequisites include inventory dependencies; prior topic in the chain is `{spec.get('prev') or 'foundational system design'}`.",
    ]

    first_principles = [
        "A monolith colocates calls, transactions, and failures in one process. Microservices move those boundaries to the network.",
        f"{name} exists to make one aspect of that distribution explicit: who owns what, how messages flow, or how failure is contained.",
        "Networks add latency, partial failure, and duplicate delivery. Designs must state assumptions about consistency and idempotency.",
        "What happens internally: a request or message enters at an edge or peer, policy is applied (auth, routing, limits), application logic runs against owned data, and side effects are emitted synchronously or asynchronously.",
        f"Why it works when done well: teams ship independently, blast radius shrinks, and technology choices can fit each workload. Limitations: {spec['pitfall']}.",
    ]

    internal = [
        "Components typically include the service runtime, its datastore, integration adapters (HTTP/gRPC clients, message publishers), and platform hooks (health checks, metrics, tracing).",
        f"For {name}, emphasize {pillars[0]} and {pillars[1]} as first-class design artifacts, not afterthoughts.",
        "Execution path: validate incoming contract, authorize caller, perform domain operation in a single-writer store, emit events or replies, and record observability fields (trace id, idempotency key).",
        f"State is owned locally; other services see snapshots, caches, or events—not live foreign keys. Cross-cutting flows like {spec['scenario']} should be diagrammed before coding.",
        "Memory and CPU matter at scale, but operational state—queues, breaker positions, outbox backlog—often dominates incident response.",
    ]

    examples = [
        f"Analogy: {name} is like airport security for distributed traffic—helpful when volume and rules are clear, costly when every passenger needs a unique manual process.",
        f"Backend example: {spec['scenario']}. Identify sync steps that need user-visible errors versus async steps that can retry.",
        f"Anti-pattern: {spec['pitfall']}. The fix is usually clearer boundaries, contracts, or platform policy—not more services.",
        "Do not confuse the marketing term with the operational requirement: every pattern here needs observability and rollback.",
    ]

    code_intro, code, code_footer = default_code(name, spec["scenario"])

    practical = [
        f"When rolling out {name.lower()}, start with one vertical slice that matches {spec['scenario']}.",
        "Add trace propagation and structured logs before optimizing payload formats.",
        "Document SLOs, on-call runbooks, and feature flags for the new path.",
        "Security: authenticate service callers, authorize per operation, and minimize PII fan-out.",
        "Scaling: watch fan-out multiplier, connection pools, and broker lag—not only CPU per pod.",
    ]

    debugging = [
        f"Symptoms: elevated 5xx at the gateway, growing outbox or queue lag, or inconsistent reads after {spec['scenario']}.",
        "Root causes often include missing timeouts, incompatible schema deploys, or shared datastore coupling.",
        "Diagnosis: find a failing trace id, compare dependency dashboards, verify deploy versions, replay idempotent messages in a sandbox.",
        "Mitigation: disable noncritical consumers, open breakers, extend deadlines only with product approval, fix forward with compatible contracts.",
        "Long-term: contract tests, chaos exercises, and ADRs so the team does not repeat the same coupling.",
    ]

    interview = build_interview(meta, spec)

    exercises = [
        {
            "prompt": f"Draw a context map for {spec['scenario']}. Label sync calls, async events, and each datastore owner. Acceptance: no shared databases; every arrow has a contract name.",
        },
        {
            "prompt": f"Given {spec['pitfall']}, write an ADR fragment (context, decision, consequences) explaining the fix for {name}. Acceptance: mentions observability and rollout, not only rename services.",
        },
        {
            "prompt": f"Design metrics and alerts for {spec['scenario']} under {name}. List three metrics, two alerts, and one runbook step. Acceptance: includes trace or correlation id usage.",
        },
    ]

    scenario = spec["scenario"]
    solutions = [
        f"Context map: place Order, Payment, Inventory (or analogs for {scenario}) in separate boxes with private databases. Sync: Order→Payment authorize. Async: OrderPlaced→Inventory reservation consumer. Contracts: `AuthorizePayment`, `OrderPlaced` v1. No shared tables.",
        f"ADR: Context—teams coupled via shared schema. Decision—enforce database-per-service and expose {pillars[0]} via API/events. Consequences—need saga/outbox for cross-service invariants; migrate via strangler; add contract tests in CI.",
        f"Metrics: checkout p95 latency; payment error rate; outbox lag seconds. Alerts: SLO burn on checkout; outbox lag > 60s. Runbook: fetch trace id from support ticket, inspect payment span, pause consumer if poison message, replay with idempotency key.",
    ]

    exercises_section = "\n".join(
        [
            f"### Exercise {i} — {ex['prompt'].split('.')[0].lower()}\n\n{ex['prompt']}"
            for i, ex in enumerate(exercises, 1)
        ]
    )

    revision = "\n".join(
        [
            f"- {spec['thesis']}",
            f"- Watch for: {spec['pitfall']}",
            f"- Pillars: {', '.join(pillars)}.",
            "- Propagate trace and idempotency keys on every cross-service call.",
            "- Prefer owned data and explicit contracts over shared libraries hiding coupling.",
        ]
    )

    related = f"""Understand this before: {', '.join(f'`{d}`' for d in inv['dependencies'][:4])}.

This topic supports: `{spec.get('next') or 'D20-T001'}` and neighboring microservices notes in domain 19.

Often confused with: platform products (Kubernetes, Kafka) versus the architectural rule itself.

Interviewers combine this with `D19-T004` gateway, `D19-T015` sagas, `D19-T016` outbox, and `D19-T030` when not to split."""

    completion = "\n".join(
        [
            f"- Explain {name} with a concrete scenario (`{spec['scenario']}`) without reading the note.",
            "- Sketch the mermaid flow for your system variant.",
            "- List one sync and one async step and justify each.",
            f"- Name the pitfall `{spec['pitfall']}` and how you would detect it in code review.",
            "- Answer five beginner and five scenario interview questions aloud.",
            "- Complete the three exercises and compare with the solution file.",
        ]
    )

    return {
        "meta": meta,
        "overview": overview,
        "first_principles": first_principles,
        "internal": internal,
        "mermaid": spec["diagram"],
        "diagram_caption": f"Diagram for {name}: {spec['scenario']}.",
        "examples": examples,
        "code_intro": code_intro,
        "code": code,
        "code_footer": code_footer,
        "practical": practical,
        "tradeoffs_table": tradeoffs_table(name),
        "mistakes": mistakes_md(name, spec["pitfall"], pillars),
        "debugging": debugging,
        "interview": interview,
        "exercises": exercises,
        "solutions": solutions,
        "exercises_section": exercises_section,
        "revision": revision,
        "related": related,
        "completion": completion,
    }

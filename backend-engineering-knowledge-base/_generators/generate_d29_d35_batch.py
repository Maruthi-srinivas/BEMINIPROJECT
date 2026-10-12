#!/usr/bin/env python3
"""Generate D29–D35 knowledge-base artifacts from inventory.json."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "00_INDEX" / "inventory.json"
EXERCISES = ROOT / "EXERCISES"
SOLUTIONS = EXERCISES / "solutions"
INTERVIEW = ROOT / "INTERVIEW_BANK" / "items"
MARKER = "## O. Completion Criteria"

try:
    from d29_d35_enrichments import ENRICHMENTS
except ImportError:
    try:
        from _generators.d29_d35_enrichments import ENRICHMENTS  # type: ignore
    except ImportError:
        ENRICHMENTS = {}


def load_topics(domains: tuple[int, ...]) -> list[dict]:
    data = json.loads(INV.read_text(encoding="utf-8"))
    out = [t for t in data["topics"] if t["domain_number"] in domains]
    out.sort(key=lambda t: (t["domain_number"], int(t["id"].split("-T")[1])))
    return out


def is_complete(note_path: Path) -> bool:
    if not note_path.is_file():
        return False
    return MARKER in note_path.read_text(encoding="utf-8")


def para4(s1: str, s2: str, s3: str, s4: str) -> str:
    return " ".join([s1.strip(), s2.strip(), s3.strip(), s4.strip()])


def interview_block(
    beginner: list[tuple[str, str]],
    intermediate: list[tuple[str, str]],
    advanced: list[tuple[str, str]],
    scenarios: list[tuple[str, str]],
    followups: list[tuple[str, str]],
) -> str:
    assert len(beginner) == len(intermediate) == len(advanced) == len(scenarios) == 5
    assert len(followups) == 3

    def section(title: str, items: list[tuple[str, str]]) -> str:
        lines = [f"### {title}", ""]
        for i, (q, a) in enumerate(items, 1):
            lines.append(f"#### Q{i}. {q}")
            lines.append("")
            lines.append(f"**Answer:** {a}")
            lines.append("")
        return "\n".join(lines)

    return "\n".join(
        [
            section("Beginner", beginner),
            section("Intermediate", intermediate),
            section("Advanced", advanced),
            section("Scenarios", scenarios),
            section("Follow-ups", followups),
        ]
    )


def slug_from_path(note_path: str) -> str:
    return Path(note_path).stem


def topic_num(tid: str) -> int:
    return int(tid.split("-T")[1])


def prev_next(t: dict) -> tuple[str, str]:
    d, n = t["domain_number"], topic_num(t["id"])
    prev_id = f"D{d:02d}-T{n-1:03d}" if n > 1 else None
    next_id = f"D{d:02d}-T{n+1:03d}"
    return (f"`{prev_id}`" if prev_id else "`D28-T002`", f"`{next_id}`")


def classify(t: dict) -> str:
    d = t["domain_number"]
    sub = t["subdomain"].lower()
    if d == 29:
        if "vector" in sub:
            return "vector"
        if "object storage" in sub or "pre-signed" in sub or "multipart" in sub:
            return "object"
        if "lifecycle" in sub or "metadata" in sub or "hash" in sub:
            return "object_meta"
        return "search"
    if d == 30:
        if "rag" in sub or "retrieval" in sub or "embedding" in sub or "chunk" in sub:
            return "rag"
        if "tool" in sub or "mcp" in sub or "agent" in sub:
            return "tools"
        if "injection" in sub or "security" in sub:
            return "llm_security"
        return "llm"
    if d == 33:
        return "incident"
    if d == 31:
        return "framework"
    if d == 32:
        return "communication"
    if d == 34:
        return "project"
    if d == 35:
        return "advanced_ds"
    return "generic"


def mermaid_for(t: dict, kind: str) -> str:
    if kind == "incident":
        return """flowchart TD
  alert[AlertOrReport]
  triage[TriageAndScope]
  checks[DiagnosticChecks]
  mitigate[Mitigation]
  prevent[Prevention]
  alert --> triage
  triage --> checks
  checks --> mitigate
  mitigate --> prevent"""
    if kind == "rag":
        return """flowchart LR
  query[UserQuery]
  embed[EmbedQuery]
  retrieve[VectorOrKeywordRetrieve]
  context[AssembleContext]
  model[LLMGenerate]
  query --> embed
  embed --> retrieve
  retrieve --> context
  context --> model"""
    if kind == "tools":
        return """flowchart TD
  userMsg[UserMessage]
  policy[PolicyAndAuthZ]
  planner[ToolSelection]
  executor[SandboxedExecutor]
  audit[AuditLog]
  userMsg --> policy
  policy --> planner
  planner --> executor
  executor --> audit"""
    if kind == "object":
        return """flowchart LR
  client[Client]
  api[ObjectAPI]
  bucket[Bucket]
  storage[DurabilityLayer]
  client --> api
  api --> bucket
  bucket --> storage"""
    if kind == "vector":
        return """flowchart TD
  doc[Document]
  chunk[ChunkAndEmbed]
  index[VectorIndex]
  query[QueryVector]
  hits[TopKNeighbors]
  doc --> chunk
  chunk --> index
  query --> index
  index --> hits"""
    if kind == "framework":
        return """flowchart TD
  request[HTTPRequest]
  middleware[MiddlewareStack]
  handler[RouteHandler]
  service[DomainService]
  data[DataAccess]
  request --> middleware
  middleware --> handler
  handler --> service
  service --> data"""
    if kind == "communication":
        return """flowchart LR
  prompt[InterviewPrompt]
  clarify[ClarifyAndAssume]
  structure[StructuredAnswer]
  tradeoff[TradeOffs]
  prompt --> clarify
  clarify --> structure
  structure --> tradeoff"""
    if kind == "project":
        return """flowchart TD
  req[Requirements]
  design[Architecture]
  build[Implementation]
  test[TestAndObserve]
  ship[DeployAndDocument]
  req --> design
  design --> build
  build --> test
  test --> ship"""
    if kind == "advanced_ds":
        return """flowchart TD
  client[ClientWrite]
  leader[LeaderNode]
  followers[FollowerReplicas]
  quorum[QuorumAck]
  client --> leader
  leader --> followers
  followers --> quorum"""
    return """flowchart TD
  write[WritePath]
  shard[ShardPrimary]
  replica[ReplicaCopy]
  search[SearchScatterGather]
  write --> shard
  shard --> replica
  search --> shard"""


def facts_for(t: dict, kind: str) -> list[str]:
    name = t["name"]
    sub = t["subdomain"]
    tid = t["id"]
    base = [
        f"{name} is a recurring backend concern when systems grow beyond a single database and single region.",
        f"Teams document `{tid}` so on-call engineers and interview candidates share vocabulary for {sub.lower()}.",
        "Production behavior is defined by configuration, capacity, and failure modes—not only API syntax.",
        "Measure before optimizing: latency, error rate, saturation, and cost per request.",
    ]
    if kind == "incident":
        return [
            f"Symptom: user-visible impact tied to {sub.lower()} (latency, errors, stale data, or missing features).",
            f"Common causes include recent deploys, dependency outages, resource exhaustion, and misconfiguration.",
            "Checks should be read-only first: metrics dashboards, logs with correlation ids, and dependency health.",
            "Mitigation prioritizes stopping bleeding (rollback, throttle, failover) before root-cause refactors.",
            "Prevention adds guardrails: alerts, limits, runbooks, chaos drills, and architectural fixes.",
        ]
    if kind == "llm_security":
        return [
            "Treat all retrieved text and user input as untrusted data, never as instructions to the runtime.",
            "Separate system policy from user content with clear delimiters and server-side enforcement.",
            "Tool calls require allowlists, argument validation, and least-privilege credentials.",
            "Log prompts and tool invocations with redaction; never train on production secrets.",
        ]
    if kind == "rag":
        return [
            "Retrieval quality dominates answer quality when models are already capable.",
            "Chunking and metadata filters reduce irrelevant context that confuses the model.",
            "Hybrid keyword plus vector retrieval improves recall for proper nouns and SKUs.",
            "Evaluate retrieval with labeled question–document pairs, not only end-to-end vibes.",
        ]
    return base


def code_section(t: dict, kind: str) -> str:
    tid = t["id"]
    slug = slug_from_path(t["note_path"]).replace("-", "_")
    if kind == "incident":
        return f"""File: `examples/{slug}.py`

Dependencies: Python 3 standard library only.

```python
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    SEV2 = "user_visible_degradation"
    SEV1 = "major_outage"


@dataclass
class IncidentStep:
    name: str
    read_only: bool


RUNBOOK = [
    IncidentStep("Confirm symptom in dashboards", True),
    IncidentStep("Identify last change window", True),
    IncidentStep("Apply mitigation (rollback/throttle)", False),
    IncidentStep("Document timeline", True),
]


def next_step(completed: int) -> IncidentStep | None:
    if completed >= len(RUNBOOK):
        return None
    return RUNBOOK[completed]


if __name__ == "__main__":
    assert RUNBOOK[0].read_only
    print("ok", next_step(0).name)
```

How to run: `python examples/{slug}.py` from the topic folder.

Expected output: `ok Confirm symptom in dashboards`

This illustrates ordered incident response for `{t['name']}`, not a live integration."""
    if kind in ("rag", "tools", "llm", "llm_security"):
        return f"""File: `examples/{slug}.py`

Dependencies: Python 3 standard library only.

```python
MAX_CONTEXT_CHARS = 12_000
ALLOWED_TOOLS = frozenset({{"search_docs", "get_order_status"}})


def trim_context(chunks: list[str]) -> str:
    joined = []
    total = 0
    for c in chunks:
        if total + len(c) > MAX_CONTEXT_CHARS:
            break
        joined.append(c)
        total += len(c)
    return "\\n---\\n".join(joined)


def invoke_tool(name: str, args: dict) -> dict:
    if name not in ALLOWED_TOOLS:
        raise PermissionError("tool not allowed")
    if not isinstance(args, dict):
        raise TypeError("args must be a dict")
    return {{"tool": name, "status": "ok"}}


if __name__ == "__main__":
    ctx = trim_context(["a" * 100, "b" * 100])
    assert "a" in ctx
    assert invoke_tool("search_docs", {{}})["status"] == "ok"
    print("ok", len(ctx))
```

How to run: `python examples/{slug}.py`.

Expected output: `ok` plus context length.

Defensive pattern: cap context size and allowlist tools before execution."""
    return f"""File: `examples/{slug}.py`

Dependencies: Python 3 standard library only.

```python
def bounded_page(page: int, size: int, max_size: int = 100) -> tuple[int, int]:
    if page < 1:
        raise ValueError("page must be >= 1")
    if size < 1 or size > max_size:
        raise ValueError("size out of range")
    return page, size


if __name__ == "__main__":
    assert bounded_page(1, 20) == (1, 20)
    print("ok", bounded_page(2, 50))
```

How to run: `python examples/{slug}.py`.

Expected output: `ok (2, 50)`

Illustrates validation at the boundary for `{t['name']}`."""


def interview_data(t: dict, kind: str) -> tuple[
    list[tuple[str, str]],
    list[tuple[str, str]],
    list[tuple[str, str]],
    list[tuple[str, str]],
    list[tuple[str, str]],
]:
    name = t["name"]
    sub = t["subdomain"]

    def b(i: int) -> tuple[str, str]:
        qs = [
            (f"What is {name}?", para4(
                f"It describes {sub.lower()} as backend engineers encounter it in production and interviews.",
                "Strong answers connect the concept to a user-visible outcome or a measurable signal.",
                "Weak answers only name a vendor or framework without explaining when to use it.",
                f"Inventory topic `{t['id']}` situates this inside {t['domain']}.",
            )),
            (f"Why does {name} matter?", para4(
                "At scale, small design choices become outages, cost overruns, or security incidents.",
                f"{name} is how teams make those choices deliberately instead of by accident.",
                "Interviewers listen for trade-offs, not buzzwords.",
                "Reliability and correctness beat feature velocity when trust is on the line.",
            )),
            (f"Name one signal you would monitor for {name}.", para4(
                "Pick latency, error rate, saturation, or a domain metric (lag, hit ratio, token usage).",
                "Explain what good looks like and what threshold would page you.",
                "Correlate the signal with deploy markers and dependency health.",
                "Avoid alerting on metrics nobody acts on.",
            )),
            (f"What is a common mistake with {name}?", para4(
                "Copying a tutorial config into production without capacity or security review.",
                "Treating a cache or search index as the system of record.",
                "Skipping validation at API boundaries.",
                "Debugging without a timeline of changes.",
            )),
            (f"What should you read before {name}?", para4(
                "Follow inventory dependencies for databases, APIs, caching, and observability.",
                "Skim the previous topic in the same domain for continuity.",
                "If this is an incident scenario, recall your last real postmortem structure.",
                "Hands-on beats passive reading for frameworks and tools.",
            )),
        ]
        return qs[i - 1]

    def m(i: int) -> tuple[str, str]:
        qs = [
            (f"How would you design a service touchpoint for {name}?", para4(
                "Start from the API contract and failure modes, then pick storage and async boundaries.",
                "Keep authoritative state in a transactional store; use specialized stores for search or cache.",
                "Add idempotency and timeouts on external calls.",
                "Document rollback and degradation behavior.",
            )),
            (f"How do you test {name} before production?", para4(
                "Use contract tests at boundaries and integration tests with realistic data volume.",
                "Load-test hot paths and failure injection for dependencies.",
                "For LLM features, keep golden-set regression tests offline.",
                "Staging should mirror auth, networking, and quotas—not only code version.",
            )),
            (f"Compare two approaches related to {name}.", para4(
                "State benefits, costs, and the decision context (team size, traffic, compliance).",
                "Pick a default and say what would make you revisit it.",
                "Interviewers want a decision with reasoning, not endless neutrality.",
                "Mention operational cost, not only development speed.",
            )),
            (f"How does {name} affect cost?", para4(
                "Count storage, egress, compute, and managed service fees.",
                "Autoscaling without caps can surprise finance after a traffic spike.",
                "Batch and cache where correctness allows.",
                "Measure cost per successful request, not only monthly bills.",
            )),
            (f"How do you document {name} for on-call?", para4(
                "Runbooks need symptoms, checks, mitigations, and escalation paths.",
                "Link dashboards and log queries with example filters.",
                "Record known false positives.",
                "Update the doc after every real incident.",
            )),
        ]
        return qs[i - 1]

    def a(i: int) -> tuple[str, str]:
        extra = ""
        if kind == "llm_security":
            extra = "Never execute tool arguments that contain secrets or out-of-scope resource ids."
        if kind == "incident":
            extra = "Blameless postmortems focus on systems and processes, not individuals."
        qs = [
            (f"Advanced failure mode #{i} for {name}?", para4(
                "Cascading retries amplify partial outages into full ones.",
                "Thundering herds after cache expiry or deploy warm-up crush databases.",
                "Skewed keys create hot partitions in search, cache, and queues.",
                extra or "Mitigate with backoff, jitter, limits, and bulkheads.",
            )),
            (f"How does {name} behave under multi-tenant load?", para4(
                "Noisy neighbors require per-tenant quotas and fair scheduling.",
                "Authorization must be enforced server-side on every path, including search filters.",
                "Noisy aggregation queries can starve interactive traffic.",
                "Isolate large tenants when contracts require it.",
            )),
            (f"Migration strategy involving {name}?", para4(
                "Dual-write or CDC with verification beats big-bang cutovers.",
                "Use aliases, feature flags, and reversible steps.",
                "Measure error budgets during migration windows.",
                "Keep rollback artifacts for the full retention period.",
            )),
            (f"Security considerations for {name}?", para4(
                "Least privilege credentials and short-lived tokens.",
                "Validate and encode all external input at boundaries.",
                "Audit sensitive reads and admin actions.",
                "For AI features, treat retrieved content as data, not instructions.",
            )),
            (f"How would you coach a junior on {name}?", para4(
                "Pair on a staged drill with read-only checks first.",
                "Have them narrate symptom versus cause.",
                "Review one prevention item they would add this sprint.",
                "Depth on one path beats shallow tool lists.",
            )),
        ]
        return qs[i - 1]

    def s(i: int) -> tuple[str, str]:
        if kind == "incident":
            qs = [
                (f"Users report {sub.lower()}. First five minutes?", para4(
                    "Confirm the symptom in dashboards and customer support volume.",
                    "Identify scope: one region, one tenant, or global.",
                    "Check the change log for deploys, flag flips, and config pushes.",
                    "Communicate status to stakeholders with what you know and do not know.",
                )),
                (f"Metrics look green but {sub.lower()} persists. Next?", para4(
                    "Segment by tenant, route, or dependency—averages hide outliers.",
                    "Compare canary versus stable pools.",
                    "Trace exemplars for slow requests.",
                    "Validate synthetic checks versus real user paths.",
                )),
                (f"Mitigation stopped impact. What before closing?", para4(
                    "Verify recovery across regions and edge caches.",
                    "Capture timelines and attach graphs to the incident record.",
                    "Open follow-up tickets for prevention with owners.",
                    "Schedule a postmortem if severity warrants.",
                )),
                (f"Same class of incident repeated in a month. Response?", para4(
                    "Escalate to an architecture review—mitigations are band-aids.",
                    "Add automated detection earlier in the chain.",
                    "Budget engineering time for structural fixes.",
                    "Track repeat rate as a leadership metric.",
                )),
                (f"Dependency vendor blames your stack during {sub.lower()}. How respond?", para4(
                    "Bring evidence: packet captures, request ids, and reproducible minimal cases.",
                    "Engage vendor support with timestamps aligned to UTC.",
                    "Run parallel tests from a neutral environment.",
                    "Meanwhile protect users with degradation modes.",
                )),
            ]
            return qs[i - 1]
        qs = [
            (f"Production issue tied to {name}. First commands or API calls?", para4(
                "Start read-only: health endpoints, cluster state, or framework metrics.",
                "Pull logs for error class and correlation id.",
                "Check recent deploy and configuration diffs.",
                "Only then mutate state (rollback, scale, failover).",
            )),
            (f"Latency regression after enabling {name}. What changed?", para4(
                "Diff feature flags and config.",
                "Profile hot paths—ORM N+1, new network hop, or larger payloads.",
                "Compare p50 versus p95 to see tail effects.",
                "Roll back if SLO burn is steep.",
            )),
            (f"Tests pass but staging misses a {name} bug. Why?", para4(
                "Data volume and shape differ from production.",
                "Missing integration with real auth, TLS, or quotas.",
                "Flaky tests masked the failure.",
                "Add contract tests and canary metrics.",
            )),
            (f"Cost doubled after adopting {name}. Investigation?", para4(
                "Attribute spend by service tag and query type.",
                "Look for scan-heavy queries or unbounded fan-out.",
                "Check autoscaling max and replica counts.",
                "Right-size before optimizing code microscopically.",
            )),
            (f"Security review flags {name}. Typical fix?", para4(
                "Tighten IAM, secrets handling, and input validation.",
                "Remove public admin interfaces.",
                "Add audit logs for sensitive operations.",
                "Threat-model data flows end to end.",
            )),
        ]
        return qs[i - 1]

    def f(i: int) -> tuple[str, str]:
        qs = [
            (f"How does {name} relate to observability?", para4(
                "Instrument the code path with metrics, structured logs, and traces.",
                "Tie dashboards to SLOs and runbooks.",
                "Use exemplars to jump from graphs to traces.",
                "See observability domains for deeper patterns.",
            )),
            (f"How does {name} relate to data stores?", para4(
                "Choose authoritative versus derived data deliberately.",
                "Use outbox or CDC for sync to search and cache.",
                "Plan schema evolution and backfills.",
                "See SQL and NoSQL topics for consistency models.",
            )),
            (f"What topic should you study next after {name}?", para4(
                "Follow the next inventory id in the same domain.",
                "Practice explaining one scenario aloud.",
                "Add a runbook bullet to your team wiki.",
                "Teaching solidifies interview answers.",
            )),
        ]
        return qs[i - 1]

    return (
        [b(i) for i in range(1, 6)],
        [m(i) for i in range(1, 6)],
        [a(i) for i in range(1, 6)],
        [s(i) for i in range(1, 6)],
        [f(i) for i in range(1, 4)],
    )


def make_interview(t: dict, kind: str) -> str:
    b, m, a, s, f = interview_data(t, kind)
    return interview_block(b, m, a, s, f)


def interview_question_lists(t: dict, kind: str) -> list[tuple[str, list[str]]]:
    b, m, a, s, f = interview_data(t, kind)
    return [
        ("Beginner", [q for q, _ in b]),
        ("Intermediate", [q for q, _ in m]),
        ("Advanced", [q for q, _ in a]),
        ("Scenario", [q for q, _ in s]),
        ("Follow-up", [q for q, _ in f]),
    ]


def build_body(t: dict) -> dict:
    kind = classify(t)
    facts = facts_for(t, kind)
    prev, nxt = prev_next(t)
    deps = ", ".join(f"`{d}`" for d in t.get("dependencies", [])[:6])
    name = t["name"]
    sub = t["subdomain"]
    tid = t["id"]
    enrich = ENRICHMENTS.get(tid, {})
    deep = enrich.get("deep", "")

    if kind == "incident":
        overview = (
            f"This scenario covers **{sub}**—a common production incident pattern for backend teams.\n\n"
            f"Interviewers use `{tid}` to see whether you can move from symptom to cause to mitigation without guessing.\n\n"
            "Use the workflow: symptom → likely causes → ordered checks → mitigation → prevention.\n\n"
            f"Prerequisites: {deps or 'observability and data-store basics'}."
        )
        first_principles = (
            f"**Symptom:** {sub}—what users, support, or SLO dashboards report.\n\n"
            f"**Likely causes:** deploys, dependency failure, capacity limits, misconfiguration, or traffic shifts.\n\n"
            f"**Checks:** confirm scope, inspect golden signals, trace exemplars, and validate dependencies read-only.\n\n"
            f"**Mitigation:** stop bleeding via rollback, throttle, failover, or feature degradation.\n\n"
            f"**Prevention:** alerts, limits, architecture fixes, game days, and runbooks.\n\n"
            + (deep + "\n\n" if deep else "")
            + "\n\n".join(facts)
        )
        internal = (
            "Incident workflow components:\n\n"
            "- **Detection** — alerts, synthetic checks, support tickets.\n"
            "- **Triage** — severity, blast radius, incident commander.\n"
            "- **Diagnostics** — metrics, logs, traces, change log.\n"
            "- **Mitigation** — reversible actions with communication.\n"
            "- **Follow-up** — postmortem, tickets, verified prevention.\n\n"
            f"For {sub}, map each component to concrete dashboards and commands your stack exposes."
        )
        debugging = (
            f"**Symptom:** {sub}.\n\n"
            "**Checks:** timeline of deploys; dependency health; saturation (CPU, memory, disk, connections); "
            "error budget burn; compare canary vs stable.\n\n"
            "**Mitigation:** rollback or scale; enable cached responses; shed non-critical traffic.\n\n"
            "**Prevention:** SLO-based alerts; autoscaling with sane max; load tests; chaos drills."
        )
    else:
        overview = (
            f"{name} covers {sub.lower()} for backend and platform engineers.\n\n"
            f"The topic exists because production systems need more than happy-path APIs: capacity, security, and operability.\n\n"
            f"In interviews, `{tid}` tests depth on trade-offs and failure modes in {t['domain']}.\n\n"
            f"Prerequisites: {deps or 'see inventory dependencies'}. Continue with {nxt}."
        )
        first_principles = (
            f"At a high level, {name} is about how applications interact with infrastructure and specialized services.\n\n"
            + (deep + "\n\n" if deep else "")
            + "\n\n".join(facts)
        )
        internal = (
            f"Components for {sub}:\n\n"
            "- **API or SDK boundary** — authentication, timeouts, retries with caps.\n"
            "- **Data path** — authoritative store versus derived indices or caches.\n"
            "- **Control plane** — configuration, versioning, and rollout.\n"
            "- **Observability** — metrics, logs, and traces on the critical path.\n\n"
            "Execution flows should be traceable end to end for debugging."
        )
        debugging = (
            f"Symptoms involving {name} often show up as elevated latency, errors, or inconsistent reads.\n\n"
            "Diagnosis: segment metrics, inspect logs with correlation ids, verify config and dependency health.\n\n"
            "Mitigate with rollback, throttling, or failover; then add prevention guardrails."
        )

    examples = enrich.get(
        "examples",
        f"Analogy: {name} is like a specialized tool in a workshop—you reach for it when the job matches, not for every nail.\n\n"
        f"Backend example: expose a narrow API, validate inputs, and keep authoritative state in your primary database.\n\n"
        "Anti-pattern: skipping observability until after an outage.\n\n"
        "Do measure; do document; do not copy production credentials into notebooks.",
    )

    practical = enrich.get(
        "practical",
        f"Ship {name} behind feature flags when risk is high. "
        "Run load tests on the integration path, not only unit tests. "
        "Security: least privilege and audit logs. "
        "Observability: SLO dashboards tied to this path.",
    )

    tradeoffs = enrich.get(
        "tradeoffs",
        "| Choice | Benefit | Cost | Choose when | Avoid when |\n"
        "| --- | --- | --- | --- | --- |\n"
        "| Managed service | Less ops | Vendor limits | Standard needs | Extreme tuning |\n"
        "| Self-hosted | Control | You operate it | Compliance, cost at scale | Small team without SRE |\n"
        "| Sync API | Simple mental model | Tail latency | Low QPS | Burst traffic |\n"
        "| Async jobs | Smooth spikes | Complexity | Heavy work | Need instant read-after-write |\n"
        "| Cache layer | Fast reads | Staleness | Read-heavy | Strong consistency required |",
    )

    mistakes = enrich.get(
        "mistakes",
        "- Ignoring backpressure and timeouts on external calls.\n"
        "- Using derived stores as system of record.\n"
        "- Missing validation at trust boundaries.\n"
        "- Alerting without runbooks.\n"
        "- Optimizing before measuring.",
    )

    exercises = (
        f"### Exercise 1 — implementation\n\n"
        f"Implement or sketch the section F example for `{tid}` and state expected output.\n\n"
        f"### Exercise 2 — debugging\n\n"
        f"For {sub}, list five read-only checks in order and what bad output means.\n\n"
        f"### Exercise 3 — trade-off\n\n"
        f"Choose between two designs relevant to {name}. Defend your choice in one paragraph."
    )

    ex_solutions = enrich.get(
        "ex_solutions",
        [
            "Run the section F script; asserts should pass and print `ok`.",
            "Example checks: health endpoint, error rate by route, dependency latency, recent deploy tag, saturation metric—interpret each.",
            "Trade-off paragraph should name blast radius, cost, operability, and rollback.",
        ],
    )

    revision = enrich.get(
        "revision",
        f"- {name}: know purpose, one failure mode, one mitigation.\n"
        "- Measure latency, errors, saturation, and cost.\n"
        "- Validate at boundaries; fail closed.\n"
        "- Document runbooks after incidents.",
    )

    completion = enrich.get(
        "completion",
        f"- Explain {name} without reading this note.\n"
        f"- Walk the section D diagram for {sub}.\n"
        "- Run or explain the section F example.\n"
        "- Answer two scenario questions from section K aloud.\n"
        "- Name one prevention item you would add in production.",
    )

    return {
        "overview": overview,
        "first_principles": first_principles,
        "internal": internal,
        "mermaid": mermaid_for(t, kind),
        "examples": examples,
        "code_section": code_section(t, kind),
        "practical": practical,
        "tradeoffs": tradeoffs,
        "mistakes": mistakes,
        "debugging": debugging,
        "interview": make_interview(t, kind),
        "exercises": exercises,
        "ex_solutions": ex_solutions,
        "revision": revision,
        "completion": completion,
        "prev": prev,
        "nxt": nxt,
        "deps": deps,
    }


def build_note(t: dict, body: dict) -> str:
    tid = t["id"]
    return f"""# {tid} — {t['name']}

Topic ID: `{tid}`
Domain: {t['domain']}
Subdomain: {t['subdomain']}
Importance: {t['importance']}
Complexity: {t['complexity']}
Dependencies: {body['deps']}
Execution status of the code in section F: not executed (documentation example)

## A. Topic Overview

{body['overview']}

## B. First-Principles Explanation

{body['first_principles']}

## C. Internal Working and Architecture

{body['internal']}

## D. Diagrams and Visual Models

```mermaid
{body['mermaid']}
```

Read the diagram as an operational or data-flow view for {t['subdomain']}, not as a vendor-internal implementation map.

## E. Examples and Analogies

{body['examples']}

## F. Code Examples

{body['code_section']}

## G. Practical Backend Application

{body['practical']}

## H. Advantages, Limitations and Trade-offs

{body['tradeoffs']}

## I. Common Mistakes and Misconceptions

{body['mistakes']}

## J. Debugging and Troubleshooting

{body['debugging']}

## K. Interview Preparation

{body['interview']}

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`. Try these before opening that file.

{body['exercises']}

## M. Revision Notes

{body['revision']}

## N. Related Topics

Understand this before: {body['prev']} and inventory dependencies listed above.

This topic supports: {body['nxt']} and adjacent topics in {t['domain']}.

Often confused with: neighboring topics in the same domain—compare responsibilities before combining them in design.

Interviewers combine this with observability, API design, and data-store fundamentals from earlier domains.

## O. Completion Criteria

{body['completion']}
"""


def write_topic(t: dict) -> None:
    body = build_body(t)
    tid = t["id"]
    note_path = ROOT / t["note_path"]
    note_path.parent.mkdir(parents=True, exist_ok=True)
    note_path.write_text(build_note(t, body), encoding="utf-8")

    EXERCISES.mkdir(parents=True, exist_ok=True)
    (EXERCISES / f"{tid}.md").write_text(
        f"""# Exercises — {tid}

Problems only. Solutions: [{tid}](solutions/{tid}.md).

1. Implement or run the section F example for {t['name']}.
2. List ordered read-only checks for the debugging scenario in section L exercise 2.
3. Write the trade-off paragraph for exercise 3.
""",
        encoding="utf-8",
    )

    SOLUTIONS.mkdir(parents=True, exist_ok=True)
    sol = body["ex_solutions"]
    (SOLUTIONS / f"{tid}.md").write_text(
        f"""# Solutions for {tid}

Open this only after attempting the exercises in the topic note.

## Exercise 1

{sol[0]}

## Exercise 2

{sol[1]}

## Exercise 3

{sol[2]}
""",
        encoding="utf-8",
    )

    slug = slug_from_path(t["note_path"])
    rel = f"../../{t['folder']}/notes/{slug}.md"
    INTERVIEW.mkdir(parents=True, exist_ok=True)
    qs = []
    n = 1
    kind = classify(t)
    for level, questions in interview_question_lists(t, kind):
        for q in questions:
            qs.append(f"{n}. {level}. {q}")
            n += 1
    (INTERVIEW / f"{tid}.md").write_text(
        f"""# {tid} interview items

Domain: {t['domain']}
Topic: {t['name']}
Difficulty mix: beginner, intermediate, advanced, scenario, follow-up
Interview type: architecture, debugging, trade-off, incident response
Full reasoned answers are in the topic note, section K.

## Questions

{chr(10).join(qs)}

Answer key: [topic note section K]({rel}).
""",
        encoding="utf-8",
    )


def main() -> int:
    topics = load_topics((29, 30, 31, 32, 33, 34, 35))
    skipped: list[str] = []
    ok: list[str] = []
    fail: list[str] = []
    for t in topics:
        note_path = ROOT / t["note_path"]
        if is_complete(note_path):
            skipped.append(t["id"])
            continue
        try:
            write_topic(t)
            ok.append(t["id"])
        except Exception as exc:  # noqa: BLE001
            fail.append(f"{t['id']}: {exc}")
    print(f"SKIPPED {len(skipped)}")
    for i in skipped:
        print(f"  skip {i}")
    print(f"OK {len(ok)}")
    for i in ok:
        print(i)
    if fail:
        print(f"FAIL {len(fail)}", file=sys.stderr)
        for f in fail:
            print(f, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# ruff: noqa: E501
"""Helpers to build interview blocks and generic seeds for D21–D23."""
from __future__ import annotations


def A(*parts: str) -> str:
    return " ".join(p.strip() for p in parts if p.strip())


def std_exercises(name: str) -> list[str]:
    return [
        f"Implement or configure instrumentation for {name.lower()} on a sample HTTP handler. Acceptance: expose at least one metric or log field named in the topic note and document how to query it.",
        f"Given a production symptom related to {name.lower()}, write a five-step debugging checklist referencing section J. Acceptance: each step names a signal and a decision.",
        f"Choose between two design options that trade cost versus reliability for {name.lower()}. Acceptance: pick one, cite the table in section H, and state what you would measure for two weeks after the change.",
    ]


def std_solutions(name: str) -> list[str]:
    return [
        f"Wire a counter or histogram (or structured log line) on the request path, label it with `service` and `route`, and verify in your metrics backend that samples appear under load. Document the query you use in dashboards.",
        f"Start from the user-visible SLO window, then compare error rate and saturation metrics, then isolate canary versus stable, then inspect one slow trace or profile, then check the dependency named in the scenario. Roll back if the change correlates with the spike.",
        f"State the chosen option, the resource you save, and the risk you accept. List two metrics (for example tail latency and error rate) and one log field you will watch; define what would trigger a revert.",
    ]


def std_iv(name: str, focus: str, pitfall: str) -> dict:
    """23 interview Q&A pairs with 4+ sentences each."""
    n = name
    return {
        "beginner": [
            (
                f"What is {n}?",
                A(
                    f"{n} is {focus}.",
                    "It matters in backend engineering because production traffic is variable and shared resources queue.",
                    "You use it to decide whether a deploy is safe and whether users are within an SLO.",
                    "A strong answer names one signal and one action, not only a definition.",
                ),
            ),
            (
                f"Why is {n} not optional in microservices?",
                A(
                    "Each hop adds latency variance and failure modes that a monolith hid.",
                    f"{n} gives a common language between dev, SRE, and product.",
                    "Without it, teams debate anecdotes after incidents.",
                    "Start small: one dashboard panel and one alert tied to a runbook.",
                ),
            ),
            (
                f"Name one metric or artifact related to {n}.",
                A(
                    "Pick a rate, error, duration, utilization, or saturation signal defined in this topic.",
                    "Explain whether it is a counter, gauge, or histogram and why that type fits.",
                    "Say where you emit it (middleware, pool, driver, sidecar).",
                    "Mention cardinality risk if labels explode.",
                ),
            ),
            (
                f"What is a common beginner mistake with {n}?",
                A(
                    pitfall,
                    "Another mistake is measuring only averages while SLOs use percentiles or error budgets.",
                    "Fix it by writing the SLO first, then choosing instrumentation.",
                    "Validate in staging with load that resembles production shape.",
                ),
            ),
            (
                f"Where does {n} appear in the request lifecycle?",
                A(
                    "It can appear at ingress, in application middleware, at connection pools, and at dependencies.",
                    "The earliest point you can measure is rarely the only point you should measure.",
                    "End-to-end checks complement in-process metrics.",
                    "Correlate with trace IDs when available.",
                ),
            ),
        ],
        "intermediate": [
            (
                f"How do you roll out changes that affect {n} safely?",
                A(
                    "Use canaries or progressive delivery and watch the signals from this topic on the canary cohort.",
                    "Define rollback thresholds before merging, not during the incident.",
                    "Keep changes small so attribution stays possible.",
                    "Record the deploy marker on dashboards for correlation.",
                ),
            ),
            (
                f"How does {n} interact with autoscaling?",
                A(
                    "Autoscalers need lagging indicators; scaling too late leaves queues, too early wastes money.",
                    f"Pair {n} with utilization and saturation so you scale the bottleneck tier.",
                    "Cooldowns prevent flapping but can delay recovery—document the trade-off.",
                    "Load tests should validate the scaling policy, not only steady state.",
                ),
            ),
            (
                f"When would you *not* invest in more {n} tooling?",
                A(
                    "When traffic is tiny, errors are obvious, and MTTR is already low, heavy tooling may not pay off.",
                    "When compliance forbids certain telemetry, simplify rather than bypass policy.",
                    "When the real problem is missing indexes or N+1 queries, fix the code first.",
                    "Revisit the decision when traffic grows an order of magnitude.",
                ),
            ),
            (
                f"How do you keep cardinality under control for {n}?",
                A(
                    "Avoid high-cardinality labels such as raw user IDs on every metric.",
                    "Prefer bounded labels: route template, dependency name, region.",
                    "Use logs or traces for drill-down, metrics for aggregation.",
                    "Sample debug logs in production instead of exporting every event as a time series.",
                ),
            ),
            (
                f"How does {n} support blameless postmortems?",
                A(
                    "Shared dashboards and SLOs shift discussion from who to what broke.",
                    "Timelines built from metrics and logs reduce guesswork.",
                    "Action items target systems: alerts, tests, limits, runbooks.",
                    "Measure whether postmortem actions actually moved the SLO.",
                ),
            ),
        ],
        "advanced": [
            (
                f"What are failure modes of misapplied {n}?",
                A(
                    "False confidence: green dashboards while users fail due to untracked paths.",
                    "Alert fatigue if thresholds ignore seasonality.",
                    "Harmful auto-actions (restarts, scale) driven by flaky probes.",
                    "Mitigate with SLO-based alerting and multi-window burn rates.",
                ),
            ),
            (
                f"How do multi-region deployments change {n}?",
                A(
                    "Clock skew and replication lag distort latency percentiles if you merge incorrectly.",
                    "Aggregate per region first, then compare; do not average percentiles across hosts.",
                    "Failover tests must exercise observability paths, not only traffic routing.",
                    "Document which SLIs are global versus regional.",
                ),
            ),
            (
                f"How do you test {n} before production?",
                A(
                    "Chaos or fault injection on dependencies validates alerts and dashboards.",
                    "Load tests should include ramp-up, steady state, and spike phases.",
                    "Verify that synthetic checks match real user journeys.",
                    "Game days prove runbooks, not only monitoring config.",
                ),
            ),
            (
                f"Relate {n} to error budgets.",
                A(
                    "Error budgets translate SLO misses into allowed change velocity.",
                    "When budget is exhausted, prioritize reliability work over features.",
                    f"{n} should show burn rate, not only static thresholds.",
                    "Product agrees on the budget policy in advance.",
                ),
            ),
            (
                f"How do you avoid optimizing the wrong layer for {n}?",
                A(
                    "Profile end-to-end latency and check queue depths before micro-optimizing code.",
                    "Compare time in app versus database versus network using traces.",
                    "Amdahl and Little's Law arguments help explain why local wins stall.",
                    "Re-measure after each change with the same load profile.",
                ),
            ),
        ],
        "scenarios": [
            (
                f"Dashboards look healthy but support tickets about slowness spike. How does {n} help?",
                A(
                    "Check tail latency and saturation metrics omitted from the executive dashboard.",
                    "Compare canary and stable, and verify whether probes hit the same code path as users.",
                    "Inspect dependency latency and pool wait times.",
                    "Communicate findings with the SLO window that matches user complaints.",
                ),
            ),
            (
                f"A deploy correlates with doubled errors. What do you check first for {n}?",
                A(
                    "Mark the deploy on graphs and split metrics by version label.",
                    "Determine whether errors are client (4xx) or server (5xx) and whether retries amplify load.",
                    "Roll back if user impact exceeds the error budget policy.",
                    "Capture exemplar traces for the new error class before rollback removes signal.",
                ),
            ),
            (
                f"Cost team asks to cut observability spend. Defend {n}.",
                A(
                    "Quantify MTTR reduction and prevented outages tied to existing signals.",
                    "Propose sampling and cardinality limits instead of blind cuts.",
                    "Show which alerts map directly to SLOs and which are noisy candidates to drop.",
                    "Offer a staged reduction with a rollback plan if MTTR rises.",
                ),
            ),
            (
                f"Black Friday is approaching. What {n} prep do you do?",
                A(
                    "Run a capacity test at expected peak and record bottleneck metrics.",
                    "Freeze risky changes and pre-scale critical tiers with documented limits.",
                    "Validate runbooks and on-call routing.",
                    "Define an incident commander role and comms channel before the event.",
                ),
            ),
            (
                f"A junior engineer adds high-cardinality labels everywhere. How do you remediate?",
                A(
                    "Identify the top cardinality offenders in the metrics backend.",
                    "Replace raw IDs with bounded buckets or move detail to traces.",
                    "Add linting or review checklist for instrumentation changes.",
                    "Teach why cardinality affects cost and query performance.",
                ),
            ),
        ],
        "followups": [
            (
                f"How does {n} connect to `D21-T001` latency percentiles?",
                A(
                    "Percentiles express user-visible latency for many SLOs.",
                    f"{n} should be interpreted alongside p95/p99, not only averages.",
                    "Histogram buckets must be chosen consistently when comparing releases.",
                    "See the percentile note for aggregation pitfalls.",
                ),
            ),
            (
                f"How does {n} connect to Kubernetes probes in `D22-T012`?",
                A(
                    "Orchestrators use probes to decide restarts and routing.",
                    "Misconfigured probes cause flapping or hidden unhealthy pods.",
                    "Align probe endpoints with real readiness conditions such as DB connectivity.",
                    "Differentiate liveness from readiness in interviews and in config.",
                ),
            ),
            (
                f"How does {n} connect to Docker images in `D23-T002`?",
                A(
                    "Smaller, reproducible images speed deploys and reduce attack surface.",
                    "Observability agents and exporters are part of the image supply chain.",
                    "Scan images and pin bases as you would pin dependencies.",
                    "Multi-stage builds keep tooling out of runtime layers.",
                ),
            ),
        ],
    }


def base_seed(name: str, focus: str, pitfall: str, mermaid: str, **overrides) -> dict:
    seed = {
        "mermaid": mermaid,
        "interview": std_iv(name, focus, pitfall),
        "exercises": std_exercises(name),
        "solutions": std_solutions(name),
    }
    seed.update(overrides)
    return seed

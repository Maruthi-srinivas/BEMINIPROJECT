#!/usr/bin/env python3
"""Generate D24–D27 knowledge-base artifacts from inventory.json."""
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

try:
    from d24_d27_enrichments import ENRICHMENTS
except ImportError:
    try:
        from _generators.d24_d27_enrichments import ENRICHMENTS  # type: ignore
    except ImportError:
        ENRICHMENTS = {}


def load_topics(domains: tuple[int, ...]) -> list[dict]:
    data = json.loads(INV.read_text(encoding="utf-8"))
    out = [t for t in data["topics"] if t["domain_number"] in domains]
    out.sort(key=lambda t: (t["domain_number"], int(t["id"].split("-T")[1])))
    return out


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
    # verify next exists in same domain
    return (f"`{prev_id}`" if prev_id else "`D23-T002`", f"`{next_id}`")


def classify(t: dict) -> str:
    sid = t["id"]
    sub = t["subdomain"].lower()
    if t["domain_number"] == 26:
        return "linux"
    if t["domain_number"] == 27:
        return "swe"
    if t["domain_number"] == 25:
        return "cicd"
    if "liveness" in sub or "readiness" in sub:
        return "k8s_probes"
    if "resource request" in sub:
        return "k8s_resources"
    if any(k in sub for k in ("vpc", "iam", "cloud", "object storage", "load balancer", "cdn", "terraform", "cost", "disaster", "rto", "availability zone", "autoscaling", "managed database")):
        return "cloud"
    return "k8s"


def mermaid_for(t: dict, kind: str) -> str:
    name = re.sub(r"[^a-zA-Z0-9]", "", t["name"])[:20] or "Topic"
    if kind == "k8s_probes":
        return """flowchart TD
  kubelet[Kubelet]
  liveness[LivenessProbe]
  readiness[ReadinessProbe]
  endpoints[ServiceEndpoints]
  restart[RestartContainer]
  traffic[SendTraffic]
  kubelet --> liveness
  kubelet --> readiness
  liveness -->|fails| restart
  readiness -->|passes| endpoints
  endpoints --> traffic"""
    if kind == "k8s_resources":
        return """flowchart LR
  spec[PodResourceSpec]
  request[Requests]
  limit[Limits]
  scheduler[SchedulerFit]
  cgroup[CgroupEnforcement]
  spec --> request
  spec --> limit
  request --> scheduler
  limit --> cgroup"""
    if kind == "linux":
        return f"""flowchart TD
  symptom[SymptomOnHost]
  cmd[DiagnosticCommand]
  interpret[InterpretOutput]
  fix[MitigationOrFix]
  symptom --> cmd
  cmd --> interpret
  interpret --> fix"""
    if kind == "cicd":
        return """flowchart LR
  commit[GitCommit]
  ci[CIBuildAndTest]
  artifact[VersionedArtifact]
  cd[CDDeploy]
  verify[ReleaseVerification]
  commit --> ci
  ci --> artifact
  artifact --> cd
  cd --> verify"""
    if kind == "swe":
        return """flowchart TD
  requirement[Requirement]
  design[DesignChoice]
  code[Implementation]
  review[CodeReview]
  operate[OperateAndLearn]
  requirement --> design
  design --> code
  code --> review
  review --> operate"""
    if kind == "cloud":
        return """flowchart TD
  user[ClientOrOperator]
  edge[EdgeOrLB]
  network[CloudNetwork]
  workload[ComputeOrData]
  user --> edge
  edge --> network
  network --> workload"""
    return f"""flowchart TD
  user[UserOrClient]
  api[KubernetesAPI]
  controller[Controller]
  node[NodeKubelet]
  pod[PodWorkload]
  user --> api
  api --> controller
  controller --> node
  node --> pod"""


def code_section(t: dict, kind: str, facts: list[str]) -> str:
    tid = t["id"]
    if kind == "k8s_probes":
        return f"""File: illustrative manifest for `{tid}`.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: api-with-probes
spec:
  containers:
    - name: api
      image: your-registry/api:1.2.3
      ports:
        - containerPort: 8080
      livenessProbe:
        httpGet:
          path: /healthz
          port: 8080
        periodSeconds: 10
        failureThreshold: 3
      readinessProbe:
        httpGet:
          path: /ready
          port: 8080
        periodSeconds: 5
        failureThreshold: 2
      startupProbe:
        httpGet:
          path: /healthz
          port: 8080
        periodSeconds: 5
        failureThreshold: 30
```

**Liveness** answers whether the process should be restarted. A failing liveness probe kills the container and lets the kubelet start a new one. **Readiness** answers whether this instance should receive traffic. A failing readiness probe removes the pod IP from Service endpoints without necessarily restarting the container. **Startup** protects slow-boot apps so liveness does not fire during initialization.

How to apply: `kubectl apply -f pod.yaml` then `kubectl describe pod api-with-probes` to see probe events. Expected: `READY 1/1` only after `/ready` succeeds."""
    if kind == "k8s_resources":
        return f"""File: illustrative manifest for `{tid}`.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: sized-api
spec:
  containers:
    - name: api
      image: your-registry/api:1.2.3
      resources:
        requests:
          cpu: "250m"
          memory: "256Mi"
        limits:
          cpu: "1000m"
          memory: "512Mi"
```

**Requests** are what the scheduler uses to place the pod and what the kubelet reserves on the node. They drive bin-packing and fair sharing. **Limits** cap usage; exceeding the memory limit triggers OOM kill; CPU is throttled when over the limit. Setting requests without limits risks noisy neighbors; limits without requests make scheduling blind.

Check usage: `kubectl top pod sized-api` (metrics-server required). Check events: `kubectl describe pod sized-api` for `FailedScheduling` or OOMKilled."""
    if kind == "linux":
        cmd_block = facts[0] if facts else "`ps aux`, `ss -tlnp`, `dig +short api.example.com`"
        return f"""Representative commands for `{t['name']}` on Linux.

{cmd_block}

Run these on the host or in a debug container with matching network namespace. Capture output before changing state. Redact secrets from pasted logs."""
    if kind == "cicd":
        return f"""File: illustrative GitHub Actions workflow for `{tid}`.

```yaml
name: ci
on:
  push:
    branches: [main]
  pull_request:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: "21"
      - run: mvn -B verify
      - run: mvn -B package -DskipTests
```

CD should promote the same immutable artifact (image digest or jar hash) through environments. Tag `latest` alone is not a version pin."""
    if kind == "swe":
        return f"""Illustrative Java sketch for `{t['name']}` (pattern only).

```java
// Depend on abstractions, not concretions (dependency inversion).
public interface PaymentGateway {{
  Result charge(Money amount, CustomerId customer);
}}

public final class CheckoutService {{
  private final PaymentGateway gateway;
  public CheckoutService(PaymentGateway gateway) {{ this.gateway = gateway; }}
  public Result checkout(Order order) {{
    return gateway.charge(order.total(), order.customerId());
  }}
}}
```

Keep domain rules in `CheckoutService`; swap gateways in tests with a fake implementation."""
    if kind == "cloud":
        return f"""Illustrative Terraform-style snippet for `{tid}` (illustrative only, not executed).

```hcl
resource "aws_s3_bucket" "app_assets" {{
  bucket = "my-app-assets-${{var.environment}}"
}}

resource "aws_s3_bucket_versioning" "app_assets" {{
  bucket = aws_s3_bucket.app_assets.id
  versioning_configuration {{ status = "Enabled" }}
}}
```

Treat cloud resources as cattle: name with environment, enable versioning on stateful buckets, and restrict IAM to least privilege. Do not embed access keys in manifests."""
    return f"""kubectl examples for `{tid}`.

```bash
kubectl get pods -A
kubectl describe deployment your-api -n production
kubectl logs deployment/your-api -n production --tail=200
kubectl get events -n production --sort-by=.lastTimestamp
```

Use `describe` for scheduling and probe failures; use `logs` for application errors; use `events` for cluster-level timing."""


def facts_for(t: dict, kind: str) -> list[str]:
    name = t["name"]
    sub = t["subdomain"]
    tid = t["id"]
    # Topic-specific command blocks and deep bullets
    LINUX_CMDS: dict[str, str] = {
        "D26-T003": (
            "```bash\n"
            "ps aux --sort=-%cpu | head -20\n"
            "```\n"
            "Shows every process with user, PID, CPU%, MEM%, and command. "
            "High `%CPU` rows are hot threads or runaway loops.\n\n"
            "```bash\n"
            "ps -eo pid,ppid,cmd --forest\n"
            "```\n"
            "Prints a process tree so you can see which parent spawned workers.\n\n"
            "```bash\n"
            "top -b -n 1 | head -25\n"
            "```\n"
            "One-shot batch `top` summary: load averages, running tasks, and top consumers."
        ),
        "D26-T008": (
            "```bash\n"
            "ss -tlnp\n"
            "```\n"
            "Lists TCP listening sockets with process names (`-p` needs root). "
            "Confirm which PID owns port 8080 before blaming the app.\n\n"
            "```bash\n"
            "ss -tan state established '( dport = :5432 or sport = :5432 )'\n"
            "```\n"
            "Shows established PostgreSQL connections for saturation checks.\n\n"
            "```bash\n"
            "lsof -iTCP:8080 -sTCP:LISTEN\n"
            "```\n"
            "Alternative listener view; useful when `ss` output is crowded."
        ),
        "D26-T009": (
            "```bash\n"
            "dig +short api.example.com A\n"
            "```\n"
            "Returns A records only; fast check that DNS resolves from this host.\n\n"
            "```bash\n"
            "dig api.example.com +trace\n"
            "```\n"
            "Walks delegation from root to authoritative server; exposes broken NS glue.\n\n"
            "```bash\n"
            "ping -c 4 api.example.com\n"
            "```\n"
            "ICMP reachability (may be blocked); use with `traceroute` for path issues."
        ),
    }
    if tid in LINUX_CMDS:
        return [LINUX_CMDS[tid]]
    enrich = ENRICHMENTS.get(tid, {})
    if enrich.get("linux_cmds"):
        return [enrich["linux_cmds"]]

    probes = (
        "Liveness tells the kubelet whether the container is dead enough to restart. "
        "Readiness tells the Service whether the pod should receive traffic. "
        "They must not check the same dependency blindly: liveness on a downstream DB outage causes restart storms; readiness on the same outage correctly drains traffic."
    )
    resources = (
        "Requests influence scheduling and guaranteed share; limits enforce caps and OOM behavior. "
        "HPA reads actual usage against requests for CPU/memory scaling. "
        "Under-provisioned requests cause throttling; missing limits allow memory spikes to evict neighbors."
    )

    base = [
        f"{name} is a core operational topic for backend engineers shipping on Linux, Kubernetes, or cloud platforms.",
        f"In `{sub}`, the failure modes are usually misconfiguration, capacity, or observability gaps rather than algorithm bugs.",
        "Production debugging starts from symptoms (latency, 5xx, CrashLoopBackOff) and narrows with commands and control-plane state.",
        f"This note (`{tid}`) ties the concept to commands, manifests, or workflow steps you can run in staging first.",
    ]
    if kind == "k8s_probes":
        base.append(probes)
    if kind == "k8s_resources":
        base.append(resources)
    if kind == "cloud" and "cost" in sub.lower():
        base.append(
            "Cost optimization uses billing dimensions (service, tag, environment), rightsizing, autoscaling bounds, and storage lifecycle rules—use your provider's cost explorer rather than invented benchmark prices."
        )
    return base


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
            (f"What is {name} in one sentence?", para4(
                f"It is the practice and tooling around {sub.lower()} in production systems.",
                "Backend interviews use it to see whether you can operate what you build, not only write features.",
                "Strong answers name one command, one manifest field, or one pipeline stage.",
                "Weak answers stay abstract without a failure story.",
            )),
            (f"Why does {name} matter for reliability?", para4(
                "Reliability is the sum of deployability, observability, and recovery time.",
                f"{name} directly affects how fast you detect and fix incidents.",
                "SLOs are meaningless if you cannot inspect or change the running system safely.",
                "Teams that skip this topic ship faster until the first outage.",
            )),
            (f"Name one tool or command for {name}.", para4(
                "Pick something you have actually run: kubectl, git, ss, dig, terraform, or a CI workflow.",
                "Say what output you expect and what would worry you.",
                "Interviewers follow up with 'what if that command lies?'—mention corroboration.",
                "Do not list ten tools without depth on one.",
            )),
            (f"What is a common beginner mistake with {name}?", para4(
                "Copying snippets without understanding probes, permissions, or pipeline gates.",
                "Treating staging and production as identical when data and traffic shape differ.",
                "Restarting or redeploying before collecting logs and events.",
                "Confusing symptoms (502) with causes (readiness failing on DB migration).",
            )),
            (f"How does {name} connect to security?", para4(
                "Least privilege applies to IAM, RBAC, CI secrets, and shell access.",
                "Misconfigured network paths and exposed secrets dominate cloud incidents.",
                "Supply-chain checks in CI reduce compromised dependency risk.",
                "Operational access should be audited and time-bound.",
            )),
        ]
        return qs[i - 1]

    def m(i: int) -> tuple[str, str]:
        qs = [
            (f"How would you debug a production issue involving {name}?", para4(
                "Reproduce or narrow scope: one pod, one region, one deploy window.",
                "Collect evidence: metrics, logs, events, traces, and the last change.",
                "Form a hypothesis and test it with a read-only command before mutating state.",
                "Document timeline and fix forward with a guardrail (alert, probe, limit).",
            )),
            (f"What signals would you alert on for {name}?", para4(
                "Alert on user-visible SLO burn or imminent capacity, not only CPU graphs.",
                "Use multi-window burn rates for error budgets where applicable.",
                "Page humans for actionable states; ticket for trends.",
                "Every alert should link to a runbook section tied to this topic.",
            )),
            (f"Compare two design choices relevant to {name}.", para4(
                "State the trade-off: speed vs safety, cost vs redundancy, coupling vs autonomy.",
                "Pick a default for your context (traffic, team size, compliance).",
                "Mention how you would revisit the decision with metrics.",
                "Interviewers want a decision, not endless neutrality.",
            )),
            (f"How do you test changes for {name} before production?", para4(
                "Use staging that exercises real integrations with sanitized data.",
                "Automate smoke tests in CI and post-deploy verification in CD.",
                "Practice game days or chaos in non-prod for failover paths.",
                "Roll out with canaries or flags when blast radius is large.",
            )),
            (f"What documentation do you leave after touching {name}?", para4(
                "Update runbooks, ADRs, or README ops sections with commands and dashboards.",
                "Record rollback steps and known sharp edges.",
                "Link monitors and on-call playbooks.",
                "Future you is also on-call.",
            )),
        ]
        return qs[i - 1]

    def a(i: int) -> tuple[str, str]:
        extra = ""
        if kind == "k8s_probes":
            extra = "Never point liveness at the same dependency as readiness without tuning thresholds."
        if kind == "k8s_resources":
            extra = "Vertical pod autoscaler and limit ranges interact with manually set requests."
        qs = [
            (f"Explain advanced failure mode #{i} for {name}.", para4(
                "Cascading failure happens when retries, restarts, or autoscaling amplify a small fault.",
                "Control plane degradation can make kubectl succeed while data plane starves.",
                "Split-brain and partial partitions look like flaky networks in metrics.",
                extra or "Mitigate with budgets, backoff, and idempotent handlers.",
            )),
            (f"How does {name} behave at multi-region scale?", para4(
                "Latency and consistency constraints dominate; health checks must be region-local.",
                "Global load balancing shifts traffic only when backends are actually ready.",
                "Configuration drift across regions causes subtle version skew bugs.",
                "Disaster recovery objectives (RTO/RPO) dictate how much automation you need.",
            )),
            (f"How do GitOps and imperative changes interact with {name}?", para4(
                "Git becomes desired state; controllers reconcile clusters continuously.",
                "Manual kubectl edits get reverted unless escaped via break-glass process.",
                "Drift detection should alert when live state diverges from declared state.",
                "Pipelines should commit manifest changes, not only mutate clusters.",
            )),
            (f"What capacity planning inputs feed {name}?", para4(
                "Traffic forecasts, payload growth, retention, and dependency limits (DB connections).",
                "Load tests with realistic think times beat guessing from CPU averages.",
                "Headroom for deploys and failures should be explicit in autoscaling max.",
                "Review quarterly or after major product launches.",
            )),
            (f"How would you coach a junior on {name}?", para4(
                "Pair on a staged incident drill with read-only commands first.",
                "Have them write the timeline from symptoms to root cause.",
                "Review one change they would make to prevent recurrence.",
                "Depth beats breadth in the first month on-call.",
            )),
        ]
        return qs[i - 1]

    def s(i: int) -> tuple[str, str]:
        qs = [
            (f"Pods CrashLoop after a deploy touching {name}. First three commands?", para4(
                "`kubectl describe pod` for probe and image pull errors.",
                "`kubectl logs --previous` for the crashed instance stack trace.",
                "`kubectl get events --sort-by=.lastTimestamp` for scheduling or quota issues.",
                "Only then roll back or patch if the blast radius is wide.",
            )),
            (f"Latency spikes after a config change related to {name}. What do you check?", para4(
                "Diff the change against last known good in git or the config store.",
                "Check saturation: connections, thread pools, disk, and GC if JVM.",
                "Validate dependencies with curl from inside the network namespace.",
                "Roll forward with a fix if rollback is slower than a targeted patch.",
            )),
            (f"CI is green but production breaks {name}. Why?", para4(
                "Tests may not cover integration, data shape, or feature-flag combinations.",
                "Environment variables or secrets differ between CI and prod.",
                "Migrations may be backward-incompatible despite passing unit tests.",
                "Add release verification and canaries tied to business metrics.",
            )),
            (f"On-call sees flapping alerts for {name}. Response?", para4(
                "Stabilize paging: widen thresholds temporarily only with a ticket and owner.",
                "Find whether flapping is probe noise, metric cardinality, or real oscillation.",
                "Fix the root cause—often too aggressive autoscaling or retry storms.",
                "Post-incident, delete noisy alerts or fix the underlying signal.",
            )),
            (f"Security audit flags {name}. Typical findings?", para4(
                "Overbroad IAM or cluster-admin bindings.",
                "Secrets in logs, images, or plain ConfigMaps.",
                "Missing network policies between tiers.",
                "Remediate with least privilege, sealed secrets, and policy-as-code.",
            )),
        ]
        return qs[i - 1]

    def f(i: int) -> tuple[str, str]:
        qs = [
            (f"How does {name} relate to observability (metrics, logs, traces)?", para4(
                "Metrics show rates and saturation; logs explain discrete failures; traces show cross-service latency.",
                "Instrument the code path this topic protects, not only the infrastructure.",
                "Correlate deploy markers with SLO dashboards.",
                "See domain 13 for deeper telemetry patterns.",
            )),
            (f"How does {name} relate to containers and images?", para4(
                "Images package dependencies; orchestrators schedule and health-check them.",
                "Image digest pinning and scanning belong in CI before CD.",
                "Debug containers attach tools without rebuilding the app image.",
                "See domain 23 for Dockerfile and compose details.",
            )),
            (f"What should you read next after {name}?", para4(
                "Follow the inventory dependency chain for this domain.",
                "Practice one staged drill that combines this topic with networking and data stores.",
                "Write a one-page runbook section for your current service.",
                "Teaching the topic once solidifies it for interviews.",
            )),
        ]
        return qs[i - 1]

    beginner = [b(i) for i in range(1, 6)]
    intermediate = [m(i) for i in range(1, 6)]
    advanced = [a(i) for i in range(1, 6)]
    scenarios = [s(i) for i in range(1, 6)]
    followups = [f(i) for i in range(1, 4)]
    return beginner, intermediate, advanced, scenarios, followups


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
    deps = ", ".join(f"`{d}`" for d in t.get("dependencies", [])[:5])
    name = t["name"]
    sub = t["subdomain"]
    domain = t["domain"]
    tid = t["id"]

    overview = (
        f"{name} covers {sub.lower()} for teams running backend services in production.\n\n"
        f"The concept exists because distributed systems fail in operational ways: bad deploys, exhausted disks, "
        f"DNS drift, RBAC gaps, and pipelines that pass tests but miss integration risk.\n\n"
        f"In interviews, `{tid}` checks whether you can reason about failure, mitigation, and trade-offs—not only happy-path APIs.\n\n"
        f"Prerequisites from inventory: {deps or 'see domain prerequisites'}. Continue with {nxt} in this domain track."
    )

    enrich = ENRICHMENTS.get(tid, {})
    deep = enrich.get("deep", "")
    first_principles = (
        f"At the bottom, {name} is about maintaining desired state under change and load. "
        f"Humans declare intent (manifests, terraform, git branches); controllers and schedulers reconcile reality.\n\n"
        + (deep + "\n\n" if deep else "")
        + "\n\n".join(facts[:3])
        + "\n\n"
        + (facts[3] if len(facts) > 3 else "")
    )

    internal = (
        f"Components involved in {sub}:\n\n"
        "- **Declarative config** — YAML, HCL, workflow files, or systemd units describing desired state.\n"
        "- **Reconciliation loop** — control plane or CI job that compares desired vs actual and acts.\n"
        "- **Data plane** — processes, packets, and bytes users depend on.\n"
        "- **Observability** — metrics, logs, events, and traces proving which layer failed.\n\n"
        f"Execution flow: change lands in git or kubectl apply → admission/validation → scheduler/placement → "
        f"runtime start → health signals → traffic shift → verification. Rollback reverses artifact or manifest revision.\n\n"
        f"State is stored in etcd (Kubernetes), remote state buckets (Terraform), or git tags (releases). "
        f"Treat those stores as sensitive configuration history."
    )

    examples = (
        f"Analogy: {name} is the flight checklist—not the airplane. The checklist prevents skipping steps when tired.\n\n"
        f"Backend example: after deploying an API, you confirm readiness before shifting the Service, watch error rate for ten minutes, "
        f"and keep the previous image digest tagged for instant rollback.\n\n"
        f"Anti-pattern: restarting pods randomly without reading events—masks a failing migration or probe misconfiguration.\n\n"
        f"Do run commands read-only first; do pin versions; do not share production kubeconfig broadly."
    )

    practical = (
        f"On-call uses {name} when alerts tie to deploy windows or infrastructure change. "
        f"Correlate `kubectl`/`git`/`ss` output with application logs and trace IDs.\n\n"
        f"Security: least privilege for CI tokens, RBAC, and SSH. Rotate secrets without printing them in job logs.\n\n"
        f"Scaling: autoscaling and queues only help when bottlenecks are identified—CPU without I/O checks misleads.\n\n"
        f"Observability: every runbook step should name a dashboard or log query."
    )

    tradeoffs = (
        "| Choice | Benefit | Cost | Choose when | Avoid when |\n"
        "| --- | --- | --- | --- | --- |\n"
        "| Manual kubectl | Fast for one-off debug | Drift, no audit trail | Break-glass incident | Routine config |\n"
        "| GitOps | Auditable desired state | Learning curve, sync delays | Multi-team clusters | Solo dev sandbox |\n"
        "| Rolling deploy | Simple, native | Mixed versions during roll | Stateless APIs | Breaking schema change |\n"
        "| Blue-green | Instant switch | Double capacity cost | Critical cutovers | Tight cost budget |\n"
        "| Managed service | Less ops toil | Vendor lock-in, limits | Standard databases | Exotic tuning needs |"
    )

    mistakes = (
        "- Using liveness probes that fail when dependencies blip, causing restart loops.\n"
        "- Setting memory limits below working set, causing OOMKilled pods under normal load.\n"
        "- Pushing `:latest` images without recording digest in the deployment manifest.\n"
        "- Running `kill -9` before capturing heap or thread dump for a JVM outage.\n"
        "- Assuming `ping` failure means HTTP failure—ICMP is often blocked.\n"
        "- Granting cluster-admin to CI service accounts."
    )

    debugging = (
        f"Symptoms map to layers: `ImagePullBackOff` (registry/auth), `CrashLoopBackOff` (app exit), "
        f"`Pending` (scheduling/resources), elevated 502 (readiness/endpoints), slow CI (cache/test flakiness).\n\n"
        f"Diagnosis loop: timestamp the change → collect events/logs → reproduce in staging → patch or rollback → add guardrail.\n\n"
        f"For Linux hosts: combine `ps`/`top` for CPU, `free`/`vmstat` for memory pressure, `df`/`du` for disk, "
        f"`ss`/`lsof` for ports, `dig` for DNS.\n\n"
        f"Document findings in the incident channel before closing."
    )

    exercises = (
        f"### Exercise 1 — implementation\n\n"
        f"Apply one safe change for {name} in a staging cluster or VM: write the manifest/config, apply it, and capture `describe` or command output proving success.\n\n"
        f"### Exercise 2 — debugging\n\n"
        f"Given a fictional incident tied to {sub}, list five read-only commands you would run in order and what bad output looks like.\n\n"
        f"### Exercise 3 — trade-off\n\n"
        f"Choose between two operational strategies for {name} (for example GitOps vs imperative, rolling vs blue-green). "
        f"Write one paragraph defending your choice for a high-traffic API."
    )

    ex_solutions = [
        f"Staging change should include revision metadata (git sha, image digest) and show healthy probes or command output. "
        f"If `{tid}` is probe-related, show separate liveness and readiness paths.",
        "Ordered read-only commands with interpreted failure signals—for Linux topics include at least one of ps, ss, or dig with explanation.",
        "Trade-off answer names blast radius, cost, rollback time, and team skill—not only buzzwords.",
    ]

    revision = (
        f"- {name}: know one command, one failure mode, one mitigation.\n"
        "- Kubernetes: requests schedule; limits cap; liveness restarts; readiness routes traffic.\n"
        "- CI/CD: immutable artifacts, verified promotions, secret hygiene.\n"
        "- Linux: correlate process, network, DNS, disk, memory layers.\n"
        "- SWE principles: cohesion, coupling, compatibility, deliberate debt."
    )

    completion = (
        f"- Explain {name} without reading this note.\n"
        f"- Draw or narrate the mermaid flow for {sub}.\n"
        "- Run or write the section F example and interpret output.\n"
        "- Answer two scenario questions from section K aloud.\n"
        "- Add a runbook bullet to your team's doc."
    )

    return {
        "overview": overview,
        "first_principles": first_principles,
        "internal": internal,
        "mermaid": mermaid_for(t, kind),
        "examples": examples,
        "code_section": code_section(t, kind, facts),
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
Execution status of the code in section F: illustrative (commands/manifests not executed in CI for this topic)

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

Read the diagram as an operational flow for {t['subdomain']}, not as a vendor-specific internal implementation.

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

Understand this before: {body['prev']}.

This topic supports: {body['nxt']} and adjacent inventory dependencies.

Often confused with: neighboring topics in the same domain—compare probes vs metrics, and CI vs CD.

Interviewers combine this with `D05-T019` health checks, `D13-T003` observability, and `D23-T007` containers.

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

1. Apply or draft the staging change described in section L exercise 1 for {t['name']}.
2. List read-only diagnostic commands for the fictional incident in exercise 2.
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
Interview type: operations, debugging, trade-off, system design
Full reasoned answers are in the topic note, section K.

## Questions

{chr(10).join(qs)}

Answer key: [topic note section K]({rel}).
""",
        encoding="utf-8",
    )


def main() -> int:
    topics = load_topics((24, 25, 26, 27))
    ok: list[str] = []
    fail: list[str] = []
    for t in topics:
        try:
            write_topic(t)
            ok.append(t["id"])
        except Exception as exc:  # noqa: BLE001
            fail.append(f"{t['id']}: {exc}")
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

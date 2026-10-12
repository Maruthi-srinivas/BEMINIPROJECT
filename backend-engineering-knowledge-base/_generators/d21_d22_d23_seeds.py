# ruff: noqa: E501
"""Content seeds for D21–D23 generators."""
from __future__ import annotations

from d21_d22_d23_seed_lib import A, base_seed, std_exercises, std_iv, std_solutions

SEEDS: dict[str, dict] = {}

# --- Rich overrides (accuracy-critical topics) ---

SEEDS["D21-T001"] = {
    "overview_1": "A latency percentile (for example p50, p90, p95, p99) is the threshold below which that fraction of observed request durations fall, when computed over a defined population and time window.",
    "overview_2": "Means hide tail behavior: most users can be fast while a minority waits on GC pauses, lock contention, or slow dependencies. SLOs and capacity discussions therefore use percentiles, not averages alone.",
    "overview_3": "Interviewers test whether you know how percentiles are computed (sorted samples, histogram buckets, or t-digest), and why you must not average p99 across machines without merging histograms.",
    "overview_4": "This topic underpins load testing (`D21-T020`), tail latency (`D21-T024`), and observability SLIs (`D22-T013`).",
    "define": "Given n sorted latencies, the nearest-rank p99 is the value at rank ceil(0.99 × n). Histogram-based systems estimate percentiles from bucket counts; bucket boundaries change the estimate.",
    "mechanism": "Clients or servers record each request duration, aggregate into rolling windows, and export histograms or sketches. Dashboards query `histogram_quantile(0.99, rate(...))` in Prometheus or equivalent.",
    "example": "If p50 is 40 ms and p99 is 800 ms, half of requests are faster than 40 ms and 99% are faster than 800 ms—one percent are at or above 800 ms depending on estimator definition.",
    "mermaid": """flowchart TD
  requests[IncomingRequests]
  timer[RecordDurationPerRequest]
  hist[HistogramOrSketch]
  window[RollingTimeWindow]
  query[PercentileQuery]
  slo[SLOCompare]
  requests --> timer
  timer --> hist
  hist --> window
  window --> query
  query --> slo""",
    "code": """File: `examples/d21_t001_percentiles.py`

Dependencies: Python 3 standard library only.

```python
from statistics import median


def nearest_rank_percentile(sorted_values: list[float], p: float) -> float:
    if not sorted_values:
        raise ValueError("empty sample")
    if not 0 < p <= 1:
        raise ValueError("p must be in (0, 1]")
    rank = int(__import__("math").ceil(p * len(sorted_values)))
    return sorted_values[rank - 1]


def summarize(latencies_ms: list[float]) -> dict[str, float]:
    s = sorted(latencies_ms)
    return {
        "p50": median(s),
        "p90": nearest_rank_percentile(s, 0.90),
        "p95": nearest_rank_percentile(s, 0.95),
        "p99": nearest_rank_percentile(s, 0.99),
    }


if __name__ == "__main__":
    sample = [10, 12, 15, 18, 20, 25, 30, 40, 200, 500]
    print(summarize(sample))
```

How to run: `python examples/d21_t001_percentiles.py` from `EXERCISES/examples/`.

Expected output: a dict with p50 near the median and p99 pulled upward by the 200 and 500 ms tail (exact numbers depend on the ten-point sample).

Important lines: sorting before rank selection; p99 uses the tail of the distribution, not the mean.""",
    "mistakes": [
        "Averaging per-host p99 values—merge histograms or raw samples instead.",
        "Using too-coarse histogram buckets, which flatten the tail.",
        "Reporting percentiles on a five-minute window while the SLO is monthly.",
        "Ignoring warmup: cold JVM or empty caches distort the first minutes after deploy.",
        "Treating p99 as a maximum; it is a threshold exceeded by about 1% of requests (definition-dependent).",
    ],
    "interview": {
        "beginner": [
            (
                "What is p50 latency?",
                A(
                    "p50 is the median latency: half of requests complete faster and half slower, for the chosen window and population.",
                    "It describes typical user experience better than a mean when the distribution is skewed.",
                    "It is still blind to the slowest users, which is why p95 and p99 exist.",
                    "Always state the window (for example last 5 minutes) when quoting a percentile.",
                ),
            ),
            (
                "What is p99 latency?",
                A(
                    "p99 is the latency threshold below which about 99% of requests fall, depending on the estimator.",
                    "Roughly one in a hundred requests is at or above p99 in a large steady sample.",
                    "Product and SRE teams care because that minority can be high-value users or retries amplifying load.",
                    "Do not confuse p99 with the maximum unless you explicitly track max.",
                ),
            ),
            (
                "Why not use average latency?",
                A(
                    "A few very slow requests pull the mean up, but most users may still be fast.",
                    "Averages also hide bimodal distributions (fast cache hits vs slow misses).",
                    "SLOs and autoscaling policies increasingly specify percentiles or error rates.",
                    "Use mean only when the distribution is tight and symmetric, which HTTP latency rarely is.",
                ),
            ),
            (
                "What population should percentiles cover?",
                A(
                    "Define whether you measure server-side handling time, end-to-end user time, or per-dependency calls.",
                    "Include only successful requests or also failures, matching the SLI definition.",
                    "Exclude health checks if they skew the distribution.",
                    "Document exclusions so dashboards match the SLO.",
                ),
            ),
            (
                "Name p90 versus p95 in one sentence each.",
                A(
                    "p90: 90% of requests are faster than this value.",
                    "p95: 95% are faster—stricter than p90 and closer to tail-focused SLOs.",
                    "Higher percentiles widen the gap between typical and worst-case batches.",
                    "Pick the percentile your SLO names; do not cargo-cult p99 if the SLO says p95.",
                ),
            ),
        ],
        "intermediate": [
            (
                "How do Prometheus histograms estimate percentiles?",
                A(
                    "Observations increment bucket counters labeled `le` (less than or equal).",
                    "`histogram_quantile` interpolates within buckets using bucket counts and rates.",
                    "Finer buckets near your SLO line improve tail accuracy at the cost of cardinality.",
                    "You must use consistent bucket boundaries across services you compare.",
                ),
            ),
            (
                "Can you average p99 across three replicas?",
                A(
                    "Averaging per-instance p99 is statistically wrong for the global tail.",
                    "Merge histograms or combine raw samples, then compute the percentile once.",
                    "If you only have per-pod summaries, treat comparisons as approximate and prefer a centralized sink.",
                    "Exemplars help link histogram buckets to traces for investigation.",
                ),
            ),
            (
                "How does sample size affect percentile stability?",
                A(
                    "With few requests, p99 jumps when a single slow request arrives.",
                    "Low-traffic endpoints need longer windows or Bayesian smoothing.",
                    "High-traffic services stabilize quickly but still move after deploys.",
                    "Use min traffic thresholds before paging on p99.",
                ),
            ),
            (
                "What is the difference between server and client measured latency?",
                A(
                    "Server time excludes DNS, TLS, and network last mile; client time includes them.",
                    "Mobile clients add radio variability missing from datacenter metrics.",
                    "Align SLIs with what users feel, often via RUM or synthetic checks plus server metrics.",
                    "Disagreement between layers localizes the bottleneck.",
                ),
            ),
            (
                "How do retries change percentile interpretation?",
                A(
                    "Retries inflate server-side request counts and can make user-visible latency worse.",
                    "Measure attempts separately from user-perceived success if retries are hidden.",
                    "Idempotent retry policies belong in SLO discussions.",
                    "Tail latency often spikes when a dependency degrades and retry storms follow.",
                ),
            ),
        ],
        "advanced": [
            (
                "Compare nearest-rank versus linear interpolation percentiles.",
                A(
                    "Nearest-rank picks an actual sample at a computed rank; simple but coarse on small n.",
                    "Linear interpolation between ranks smooths estimates between data points.",
                    "Different tools use different methods; document yours when comparing vendors.",
                    "SLO compliance should use the same estimator in alert and dashboard.",
                ),
            ),
            (
                "How do coordinated omission problems affect load test percentiles?",
                A(
                    "If the load generator waits for responses before sending the next request, it omits slow periods from offered load.",
                    "Reported percentiles look optimistic compared to open-loop offered load.",
                    "Use tools that maintain target arrival rate independent of latency.",
                    "Always pair percentile charts with achieved throughput and error rate.",
                ),
            ),
            (
                "Relate percentiles to multi-tenant noisy neighbor effects.",
                A(
                    "Shared CPU or disk can create tail spikes for one tenant without moving p50 much.",
                    "Per-tenant percentiles expose fairness issues aggregate metrics hide.",
                    "Isolation (quotas, dedicated pools) is a product decision informed by tail metrics.",
                    "Watch steal time and IO wait alongside HTTP percentiles.",
                ),
            ),
            (
                "When is p99 the wrong SLO line?",
                A(
                    "When traffic is too low for stable p99, or when batch jobs dominate.",
                    "When user experience is dominated by errors, prioritize availability SLIs.",
                    "When p99 ignores the slowest 1% that includes paying customers on large carts.",
                    "Sometimes p99.9 or joint SLIs (latency given success) fit better—negotiate with product.",
                ),
            ),
            (
                "How do you regression-test percentiles in CI?",
                A(
                    "Micro-benchmarks are noisy; prefer controlled load tests on release candidates.",
                    "Store historical distributions, not single numbers, to detect shape changes.",
                    "Gate on error rate first; latency gates need generous bands to avoid flakes.",
                    "Compare canary vs baseline with the same load profile.",
                ),
            ),
        ],
        "scenarios": [
            (
                "p50 is flat but p99 doubled after a deploy. What hypotheses?",
                A(
                    "A new code path, lock, or dependency call adds rare slow work.",
                    "GC or pool exhaustion affects only saturated periods.",
                    "Check version-labeled histograms and traces at high percentiles.",
                    "Roll back if error budget burn exceeds policy while investigating.",
                ),
            ),
            (
                "Two regions show different p99 for the same service. Why?",
                A(
                    "Different traffic mix, replica count, or cross-region dependency latency.",
                    "Clock skew is rare for latency but replication lag affects read paths.",
                    "Compare per-region histogram merges, not averaged percentiles.",
                    "Route users to healthier regions if failover policy allows.",
                ),
            ),
            (
                "Marketing expects a latency SLO; engineering only tracks CPU. What do you propose?",
                A(
                    "Define an SLI on server or edge latency with a percentile and window.",
                    "Instrument middleware histograms and validate bucket layout.",
                    "Tie releases to error budget policy instead of CPU targets.",
                    "Educate that CPU can be low while queues grow.",
                ),
            ),
            (
                "Histogram buckets stop at 1s but p99 SLO is 300 ms. Problem?",
                A(
                    "All times above 1s land in the +Inf bucket, losing tail shape inside the bucket.",
                    "Add buckets between 300 ms and 1s for meaningful quantile error near the SLO.",
                    "Revisit buckets when latency improves after optimization.",
                    "Alerts on quantile error can fire if buckets are misaligned.",
                ),
            ),
            (
                "Synthetic monitoring shows good p99 but users complain. Next steps?",
                A(
                    "Compare synthetic path to real user monitoring and geography.",
                    "Check auth-specific or checkout-specific routes omitted from synthetics.",
                    "Inspect dependency and database percentiles on those routes.",
                    "Expand probes to include mobile networks if that is the cohort complaining.",
                ),
            ),
        ],
        "followups": [
            (
                "How does this connect to Little's Law (`D21-T021`)?",
                A(
                    "Higher concurrency at fixed service time increases queueing, which widens latency tails.",
                    "Little's Law relates average concurrency, throughput, and residence time in steady state.",
                    "Percentiles show the tail; Little's Law explains average queue depth trends.",
                    "Use both when sizing pools and thread counts.",
                ),
            ),
            (
                "How do golden signals use percentiles?",
                A(
                    "Latency is a golden signal, often tracked as a percentile for user-facing services.",
                    "Pair with rate and errors before optimizing duration.",
                    "RED method names duration explicitly for services.",
                    "See `D22-T004` and `D22-T005`.",
                ),
            ),
            (
                "How does load testing report percentiles fairly?",
                A(
                    "Maintain offered load independent of response time to avoid coordinated omission.",
                    "Report warmup separately and align test duration with SLO windows.",
                    "Include error rate and throughput alongside percentiles.",
                    "See `D21-T020`.",
                ),
            ),
        ],
    },
    "exercises": std_exercises("Latency percentiles"),
    "solutions": std_solutions("Latency percentiles"),
}

SEEDS["D21-T021"] = {
    **base_seed(
        "Little's Law",
        "the steady-state relationship L = λW linking average number in system L, arrival rate λ, and average time in system W",
        "Applying Little's Law during transients right after a traffic spike or before queues drain",
        """flowchart LR
  arrivals[ArrivalRateLambda]
  queue[SystemWithQueue]
  departures[CompletionRate]
  arrivals --> queue
  queue --> departures""",
    ),
    "overview_1": "Little's Law states that in a stable system with well-defined boundaries, the average number of items in the system L equals the average arrival rate λ multiplied by the average time each item spends in the system W: L = λW.",
    "overview_2": "It is not an approximation for open systems in steady state—it follows from conservation of flow when averages exist and the system is not drifting unbounded.",
    "principles_1": "If you know any two of average concurrency (in-flight requests), throughput, and average latency, you can infer the third, which is invaluable for capacity planning and pool sizing.",
    "principles_3": "For a single-server M/M/1 queue in steady state, the same intuition holds: higher utilization increases queue length and therefore waiting time; Little's Law relates the averages regardless of distribution details (with standard caveats on stability).",
    "example": "If a service averages 1000 requests per second (λ) and each request spends 50 ms in the system (W = 0.05 s), average concurrency L ≈ 1000 × 0.05 = 50 in-flight requests.",
    "mistakes": [
        "Using Little's Law immediately after a step change in traffic before averages stabilize.",
        "Mixing units (milliseconds vs seconds) for W.",
        "Applying it inside a subsystem whose boundaries leak work (unbounded internal queues).",
        "Confusing service time with time in system when queueing exists.",
    ],
    "interview": std_iv(
        "Little's Law",
        "L = λW for averages in a stable system",
        "Dividing peak RPS by average latency without checking whether the system is in steady state",
    ),
}

SEEDS["D21-T022"] = {
    **base_seed(
        "Amdahl's Law",
        "an upper bound on speedup when only part of work parallelizes: Speedup = 1 / (S + P/N)",
        "Expecting linear speedup when a serial fraction S remains",
        """flowchart TD
  work[TotalWork]
  serial[SerialFractionS]
  parallel[ParallelFractionP]
  cores[NWorkers]
  work --> serial
  work --> parallel
  parallel --> cores""",
    ),
    "overview_1": "Amdahl's Law models speedup when improving only the parallelizable fraction P of work on N processors, with serial fraction S (where S + P = 1).",
    "overview_2": "Speedup = 1 / (S + P/N). As N grows, speedup approaches 1/S, so a small serial segment caps global wins—optimize the serial path first if it dominates.",
    "example": "If S = 0.1 (10% serial), even infinite cores yield at most 10× speedup.",
    "mistakes": [
        "Ignoring coordination, locking, and IO in the 'parallel' section.",
        "Measuring lab micro-benchmarks instead of end-to-end request time.",
        "Assuming N equals CPU count when work is IO-bound.",
    ],
    "interview": std_iv(
        "Amdahl's Law",
        "speedup limited by serial fraction S in 1/(S+P/N)",
        "Throwing more instances at a service whose latency is dominated by one serial database row lock",
    ),
}

SEEDS["D22-T005"] = {
    **base_seed(
        "RED and USE methods",
        "RED (Rate, Errors, Duration) for services and USE (Utilization, Saturation, Errors) for resources",
        "Dashboarding CPU only while user-facing errors climb",
        """flowchart TD
  service[ServiceRED]
  rate[Rate]
  errors[Errors]
  duration[Duration]
  resource[ResourceUSE]
  util[Utilization]
  sat[Saturation]
  err[Errors]
  service --> rate
  service --> errors
  service --> duration
  resource --> util
  resource --> sat
  resource --> err""",
    ),
    "overview_1": "RED applies to request-driven services: monitor request Rate, Error rate, and Duration (often percentiles). USE applies to resources like CPU, memory, disks, and pools: Utilization, Saturation, and Errors.",
    "overview_2": "Utilization is percent busy; saturation is extra work waiting (queue length, pool wait); errors are clear fault signals at both layers.",
    "example": "A pod can show moderate CPU utilization while saturation is high because threads block on a full connection pool—USE catches that; RED shows rising duration and errors at the API.",
    "interview": std_iv(
        "RED and USE",
        "Rate/Errors/Duration for services and Utilization/Saturation/Errors for resources",
        "Using RED metrics on a batch worker without defining what a 'request' means",
    ),
}

SEEDS["D22-T013"] = {
    **base_seed(
        "SLIs, SLOs and SLAs",
        "SLI = measured indicator, SLO = internal target for that SLI, SLA = external contract often with remedies",
        "Publishing an SLA without an SLO and error budget process internally",
        """flowchart TD
  sli[SLIMeasurement]
  slo[SLOTarget]
  budget[ErrorBudget]
  sla[SLAContract]
  sli --> slo
  slo --> budget
  slo --> sla""",
    ),
    "overview_1": "An SLI is a quantifiable measure of service behavior (for example proportion of successful requests faster than 300 ms). An SLO sets a target (for example 99.9% monthly). An SLA is a business agreement that may reference SLO-like thresholds with consequences.",
    "overview_2": "Good SLIs are user-centric, measurable, and resistant to gaming; SLOs should be slightly stricter than SLAs to provide buffer.",
    "interview": std_iv(
        "SLI/SLO/SLA",
        "indicator, internal objective, and external agreement",
        "Choosing an SLI engineers can game (synthetic-only) that misses real users",
    ),
}

SEEDS["D22-T012"] = {
    **base_seed(
        "Health, liveness and readiness probes",
        "Kubernetes-style probes: liveness restarts unhealthy containers, readiness removes them from service endpoints, startup protects slow boots",
        "A liveness probe that hits a dependency and restarts pods during database outages",
        """flowchart TD
  kube[Orchestrator]
  live[LivenessProbe]
  ready[ReadinessProbe]
  start[StartupProbe]
  pod[ApplicationPod]
  kube --> live
  kube --> ready
  kube --> start
  live --> pod
  ready --> pod
  start --> pod""",
    ),
    "overview_1": "Liveness probes decide whether the container should be restarted. Readiness probes decide whether the pod should receive traffic. Startup probes disable other probes until the app finishes slow initialization.",
    "overview_2": "Readiness should fail when the instance cannot serve correct traffic (for example DB down). Liveness should fail only when the process is wedged and restart helps—not when dependencies are external.",
    "interview": std_iv(
        "Liveness and readiness probes",
        "orchestrator health checks with different actions on failure",
        "Using the same deep health check for liveness and readiness",
    ),
}

SEEDS["D23-T002"] = {
    **base_seed(
        "Images and layers",
        "Docker images as ordered read-only layers stacked with a union filesystem; each Dockerfile instruction can create a layer",
        "Assuming `docker save` size equals sum of logical file sizes without understanding layer sharing",
        """flowchart TD
  dockerfile[DockerfileInstructions]
  layer1[Layer1Base]
  layer2[Layer2Deps]
  layer3[Layer3App]
  image[ImageManifest]
  dockerfile --> layer1
  layer1 --> layer2
  layer2 --> layer3
  layer3 --> image""",
    ),
    "overview_1": "A container image is a manifest pointing to ordered layers. Each layer is a tarball of filesystem diffs. Containers add a thin writable layer on top (copy-on-write).",
    "overview_2": "Layer caching speeds rebuilds: if an instruction's inputs are unchanged, Docker reuses the cached layer. Changing an early instruction invalidates later layers.",
    "interview": std_iv(
        "Docker image layers",
        "stacked read-only filesystem diffs with copy-on-write container layer",
        "Running `apt upgrade` in every build on top of a moving tag, destroying cache reproducibility",
    ),
}

SEEDS["D23-T004"] = {
    **base_seed(
        "Multi-stage builds",
        "Dockerfiles with multiple FROM stages to compile in a builder image and copy only artifacts into a minimal runtime image",
        "Copying entire build contexts including `.git` and build tools into the final stage",
        """flowchart TD
  buildStage[BuildStage]
  compile[CompileOrBundle]
  runtimeStage[RuntimeStage]
  artifact[CopiedArtifacts]
  final[FinalImage]
  buildStage --> compile
  compile --> artifact
  artifact --> runtimeStage
  runtimeStage --> final""",
    ),
    "overview_1": "Multi-stage builds use `AS` named stages. The final image can `COPY --from=builder` only binaries and runtime assets, omitting compilers and headers.",
    "overview_2": "Benefits: smaller attack surface, faster deploys, fewer vulnerable packages in production. Costs: more complex Dockerfile maintenance and need to keep stage contracts explicit.",
    "interview": std_iv(
        "Multi-stage Docker builds",
        "separate build and runtime images linked by COPY --from",
        "Leaving package managers and source code in the runtime stage",
    ),
}

# --- Catalog: (id, display name, focus phrase, pitfall phrase, mermaid) ---

_CATALOG: list[tuple[str, str, str, str, str]] = [
    ("D21-T002", "Throughput and concurrency", "completed work per unit time versus simultaneous in-flight work", "Raising concurrency without measuring queue depth", "flowchart LR\n  clients[Clients] --> svc[Service]\n  svc --> pool[WorkerPool]\n  pool --> db[Database]"),
    ("D21-T003", "Profiling CPU and memory", "sampling or instrumenting where time and bytes go in a process", "Profiling only in dev with unrepresentative data", "flowchart TD\n  app[AppProcess] --> prof[Profiler]\n  prof --> flame[FlameGraph]"),
    ("D21-T004", "Flame graphs", "icicle charts of stack samples showing hot code paths", "Reading width as time per single call instead of aggregate sample share", "flowchart TD\n  samples[StackSamples] --> merge[MergeStacks]\n  merge --> flame[FlameGraph]"),
    ("D21-T005", "Memory leaks and allocation pressure", "unreleased retained objects and churn causing GC pressure", "Chasing leaks when the issue is simply oversized caches", "flowchart TD\n  alloc[Allocations] --> heap[Heap]\n  heap --> gc[GC]\n  gc --> pause[PauseTimes]"),
    ("D21-T006", "Garbage collection tuning", "JVM/runtime GC flags and heap sizing to trade throughput for pause times", "Tuning GC before fixing allocation hotspots", "flowchart LR\n  heap[Heap] --> gc[Collector]\n  gc --> mutator[ApplicationThreads]"),
    ("D21-T007", "Database query optimization", "plans, indexes, and SQL shape to reduce work per request", "Adding indexes without measuring write amplification", "flowchart TD\n  sql[Query] --> planner[Planner]\n  planner --> index[IndexScan]\n  planner --> seq[SeqScan]"),
    ("D21-T008", "Index tuning", "choosing and maintaining indexes for read paths", "Indexing every column leading to slow writes", "flowchart TD\n  table[Table] --> idx[BTreeIndex]\n  idx --> seek[SeekRows]"),
    ("D21-T009", "N+1 queries", "one query per row instead of batched loads", "Fixing only in logs without ORM fetch joins or batch loaders", "flowchart TD\n  api[Handler] --> loop[PerItemQuery]\n  loop --> db[Database]"),
    ("D21-T010", "Connection pool tuning", "sizing pools to match DB capacity and app concurrency", "Pools larger than database max connections", "flowchart TD\n  app[AppThreads] --> pool[Pool]\n  pool --> db[DBConnections]"),
    ("D21-T011", "Caching and cache hit rates", "serving reads from a fast tier with measured hit ratio", "Caching without TTL and invalidation strategy", "flowchart TD\n  req[Request] --> cache[Cache]\n  cache -->|miss| origin[Origin]"),
    ("D21-T012", "Async I/O", "non-blocking waits to improve throughput on I/O bound work", "Async style with blocking calls inside", "flowchart LR\n  loop[EventLoop] --> io[AsyncIO]\n  io --> net[Network]"),
    ("D21-T013", "Batching and bulk operations", "amortizing round trips via batches", "Batches so large they cause timeouts", "flowchart TD\n  items[Items] --> batch[BatchBuffer]\n  batch --> bulk[BulkAPI]"),
    ("D21-T014", "Compression", "CPU traded for smaller payloads on wire or disk", "Compressing already compressed media", "flowchart LR\n  payload[Payload] --> enc[Compressor]\n  enc --> wire[Network]"),
    ("D21-T015", "Payload size optimization", "smaller JSON/protobuf and fewer fields", "Stripping fields without versioning APIs", "flowchart TD\n  dto[ResponseDTO] --> trim[FieldSelection]\n  trim --> client[Client]"),
    ("D21-T016", "Network overhead", "RTT, TLS, and chatter dominating latency", "Chatty protocols across regions", "flowchart LR\n  client[Client] --> tls[TLS]\n  tls --> rtt[RTT]"),
    ("D21-T017", "Thread pool sizing", "matching worker count to workload and CPU cores", "CPU-bound work on huge thread pools", "flowchart TD\n  tasks[Tasks] --> queue[Queue]\n  queue --> workers[ThreadPool]"),
    ("D21-T018", "Backpressure", "signaling producers to slow when consumers saturate", "Unbounded queues that hide overload until OOM", "flowchart TD\n  prod[Producer] -->|pressure| slow[SlowDown]\n  slow --> cons[Consumer]"),
    ("D21-T019", "Queue depth and consumer lag", "messages waiting versus processing rate", "Scaling consumers without fixing poison messages", "flowchart LR\n  topic[Queue] --> lag[LagMetric]\n  lag --> consumer[Consumers]"),
    ("D21-T020", "Load testing and benchmarking", "controlled offered load to measure throughput and percentiles", "Coordinated omission and missing warmup", "flowchart TD\n  gen[LoadGenerator] --> sut[SystemUnderTest]\n  sut --> metrics[Metrics]"),
    ("D21-T023", "Bottleneck identification", "finding the limiting resource along the critical path", "Optimizing CPU when DB waits dominate", "flowchart TD\n  trace[Trace] --> span[Spans]\n  span --> bottleneck[SlowestSpan]"),
    ("D21-T024", "Tail latency", "slowest requests and coordination effects at high percentiles", "Chasing p50 while SLO is p99", "flowchart TD\n  hist[LatencyHist] --> tail[TailPercentiles]\n  tail --> slo[SLO]"),
    ("D21-T025", "Capacity planning", "forecasting resources from growth and headroom targets", "Planning on peak marketing day without error budget", "flowchart LR\n  forecast[Forecast] --> headroom[Headroom]\n  headroom --> purchase[ScalePlan]"),
    ("D22-T001", "Structured logging", "machine-parseable logs with stable field names", "Logging unstructured strings only", "flowchart TD\n  app[App] --> json[JSONLog]\n  json --> ship[LogShipper]"),
    ("D22-T002", "Log levels and log sampling", "severity taxonomy and reducing volume via sampling", "DEBUG in production at full rate", "flowchart TD\n  event[Event] --> level[Level]\n  level --> sample[Sampler]"),
    ("D22-T003", "Metrics, logs and traces", "three pillars with different cardinality and query models", "Using logs where metrics suffice", "flowchart TD\n  app[App] --> m[Metrics]\n  app --> l[Logs]\n  app --> t[Traces]"),
    ("D22-T004", "Golden signals", "latency, traffic, errors, and saturation per Google SRE practice", "Tracking only CPU golden signal", "flowchart TD\n  svc[Service] --> lat[Latency]\n  svc --> traf[Traffic]\n  svc --> err[Errors]\n  svc --> sat[Saturation]"),
    ("D22-T006", "Prometheus", "pull-based metrics with PromQL and histograms", "High-cardinality labels on user IDs", "flowchart TD\n  prom[Prometheus] --> scrape[ScrapeTargets]\n  scrape --> tsdb[TSDB]"),
    ("D22-T007", "Grafana", "dashboards and alerts on top of metric sources", "Dashboards without owners", "flowchart LR\n  metrics[Metrics] --> grafana[Grafana]\n  grafana --> dash[Dashboard]"),
    ("D22-T008", "OpenTelemetry", "vendor-neutral traces, metrics, and logs APIs", "Duplicating instrumentation for every vendor", "flowchart TD\n  otel[OTelSDK] --> col[Collector]\n  col --> backend[Backends]"),
    ("D22-T009", "Distributed tracing", "spans linked across services for critical path analysis", "Broken parent span context", "flowchart LR\n  a[ServiceA] --> b[ServiceB]\n  b --> c[ServiceC]"),
    ("D22-T010", "Correlation and trace IDs", "propagating IDs across logs and traces", "Generating new trace ID per internal call", "flowchart TD\n  req[Request] --> id[TraceID]\n  id --> logs[Logs]\n  id --> spans[Spans]"),
    ("D22-T011", "Loki / Elasticsearch-based logging", "log aggregation and search backends", "Indexing every log line at full text cost", "flowchart TD\n  logs[Logs] --> agg[Aggregator]\n  agg --> search[SearchUI]"),
    ("D22-T014", "Error budgets", "allowed unreliability derived from SLO targets", "Feature launches ignoring exhausted budget", "flowchart TD\n  slo[SLO] --> budget[ErrorBudget]\n  budget --> policy[ReleasePolicy]"),
    ("D22-T015", "Alert design and noise reduction", "actionable pages with SLO burn rates", "Paging on non-user-facing metrics", "flowchart TD\n  metric[Metric] --> rule[AlertRule]\n  rule --> page[PageOnCall]"),
    ("D22-T016", "Dashboards", "curated views for roles and incidents", "Wall of graphs without hierarchy", "flowchart LR\n  metrics[Metrics] --> board[Dashboard]"),
    ("D22-T017", "Incident response", "coordination roles and comms during outages", "Hero debugging without incident commander", "flowchart TD\n  detect[Detect] --> triage[Triage]\n  triage --> mitigate[Mitigate]"),
    ("D22-T018", "Root cause analysis (RCA)", "evidence-based causal analysis", "Stopping at proximate cause", "flowchart TD\n  timeline[Timeline] --> fivewhys[FiveWhys]\n  fivewhys --> root[RootCause]"),
    ("D22-T019", "Postmortems and corrective actions", "blameless writeups with tracked follow-ups", "Postmortems without owners or dates", "flowchart TD\n  incident[Incident] --> pm[Postmortem]\n  pm --> actions[Actions]"),
    ("D22-T020", "On-call fundamentals", "rotation, escalation, and fatigue management", "Single-human bus factor on-call", "flowchart LR\n  alert[Alert] --> primary[Primary]\n  primary --> esc[Escalation]"),
    ("D22-T021", "Runbooks and playbooks", "documented operational procedures", "Runbooks that mirror dashboards only", "flowchart TD\n  alert[Alert] --> runbook[Runbook]\n  runbook --> steps[Steps]"),
    ("D22-T022", "Production debugging", "safe techniques to debug live systems", "Attaching debuggers in prod casually", "flowchart TD\n  sym[Symptom] --> signals[Signals]\n  signals --> fix[Fix]"),
    ("D22-T023", "Memory, CPU and connection saturation", "resource exhaustion signals", "Watching CPU only during IO wait", "flowchart TD\n  host[Host] --> cpu[CPU]\n  host --> mem[Memory]\n  host --> conn[Connections]"),
    ("D22-T024", "Queue lag and database saturation", "consumer lag and DB thread/connection limits", "Scaling app while DB is maxed", "flowchart TD\n  q[Queue] --> lag[Lag]\n  db[Database] --> threads[ThreadsRunning]"),
    ("D22-T025", "Dependency failures", "cascades and graceful degradation when upstreams fail", "Retry storms without budgets", "flowchart TD\n  svc[Service] --> dep[Dependency]\n  dep -->|fail| fallback[Fallback]"),
    ("D22-T026", "Service-level and end-to-end monitoring", "synthetic and RUM checks for user journeys", "Monitoring only internal health endpoints", "flowchart TD\n  user[User] --> edge[Edge]\n  edge --> e2e[E2ECheck]"),
    ("D23-T001", "Containers vs virtual machines", "shared-kernel containers versus hardware-virtualized VMs", "Treating containers as security boundaries equal to VMs", "flowchart TD\n  vm[VMWithGuestOS] --> hw[Hardware]\n  ctr[Container] --> kernel[SharedKernel]"),
    ("D23-T003", "Dockerfile instructions", "FROM, RUN, COPY, ENTRYPOINT semantics and layer effects", "Using `latest` tags in production Dockerfiles", "flowchart TD\n  instr[Instructions] --> layer[NewLayer]\n  layer --> cache[BuildCache]"),
    ("D23-T005", "Image size optimization", "slimmer bases, fewer layers, and `.dockerignore`", "Installing debug tools in prod images", "flowchart TD\n  fat[FatImage] --> diet[Optimize]\n  diet --> slim[SlimImage]"),
    ("D23-T006", "Build cache", "Docker layer cache and BuildKit cache mounts", "Busting cache by copying source before deps install", "flowchart TD\n  ctx[BuildContext] --> cache[LayerCache]\n  cache --> rebuild[Rebuild]"),
    ("D23-T007", "Docker Compose", "multi-container local stacks with networks and volumes", "Compose files that only work on one laptop path", "flowchart TD\n  compose[ComposeFile] --> svcA[ServiceA]\n  compose --> svcB[ServiceB]"),
    ("D23-T008", "Container networking", "bridge networks, DNS, and published ports", "Publishing databases on host 0.0.0.0 in prod", "flowchart LR\n  c1[Container] --> net[BridgeNetwork]\n  c2[Container] --> net"),
    ("D23-T009", "Volumes and bind mounts", "persistent data versus host path mounts", "Bind-mounting prod data directories read-write by mistake", "flowchart TD\n  container[Container] --> vol[Volume]\n  vol --> disk[HostOrDriver]"),
    ("D23-T010", "Environment variables and secrets", "twelve-factor config injected at runtime", "Secrets baked into image layers", "flowchart TD\n  env[EnvVars] --> container[Container]\n  secret[SecretStore] --> env"),
    ("D23-T011", "Health checks", "Docker HEALTHCHECK and orchestrator probes", "Healthcheck curling external SaaS", "flowchart TD\n  engine[DockerEngine] --> hc[Healthcheck]\n  hc --> status[ContainerHealth]"),
    ("D23-T012", "Resource limits", "cgroups CPU/memory limits on containers", "No limits leading to noisy neighbor", "flowchart TD\n  cgroup[Cgroups] --> cpu[CPULimit]\n  cgroup --> mem[MemLimit]"),
    ("D23-T013", "Container logs", "stdout/stderr collection drivers", "Apps logging only to files inside ephemeral FS", "flowchart LR\n  app[App] --> stdout[Stdout]\n  stdout --> driver[LogDriver]"),
    ("D23-T014", "Non-root containers", "USER directive and filesystem permissions", "Running as root in production", "flowchart TD\n  image[ImageUSER] --> runtime[RuntimeUID]\n  runtime --> perms[FilePerms]"),
    ("D23-T015", "Image scanning", "CVE scanning in CI and registries", "Ignoring scan results because base is official", "flowchart TD\n  image[Image] --> scan[Scanner]\n  scan --> report[CVE report]"),
    ("D23-T016", "Container registries", "OCI distribution, tags, and immutability", "Mutable `latest` in prod deploys", "flowchart TD\n  build[Build] --> push[Registry]\n  push --> pull[DeployPull]"),
    ("D23-T017", "Container startup and shutdown", "PID 1, signals, and graceful drain", "SIGKILL before connections drain", "flowchart TD\n  start[Start] --> init[PID1]\n  stop[Stop] --> drain[GracefulDrain]"),
    ("D23-T018", "Service dependency management", "depends_on, health-aware startup in Compose/K8s", "Starting app before migrations finish", "flowchart TD\n  db[Database] --> ready[Ready]\n  ready --> app[AppStart]"),
    ("D23-T019", "Docker debugging", "exec, logs, inspect, and ephemeral debug containers", "Changing running prod containers manually", "flowchart TD\n  bug[Issue] --> logs[DockerLogs]\n  logs --> exec[DockerExec]"),
    ("D23-T020", "Persistent storage", "named volumes and cloud volume plugins", "Data in container writable layer", "flowchart TD\n  pod[Container] --> pv[PersistentVolume]\n  pv --> backend[StorageBackend]"),
    ("D23-T021", "Development vs production images", "dev bind mounts versus immutable prod images", "Shipping dev Dockerfile to prod", "flowchart TD\n  dev[DevImage] -->|local| mount[BindMount]\n  prod[ProdImage] -->|immutable| deploy[Deploy]"),
    ("D23-T022", "Reproducible builds", "pinned bases, lockfiles, and digest-pinned FROM", "Non-reproducible `apt-get upgrade` in build", "flowchart TD\n  pin[PinnedDigest] --> build[Build]\n  build --> same[SameArtifact]"),
]

for tid, name, focus, pitfall, mermaid in _CATALOG:
    if tid not in SEEDS:
        SEEDS[tid] = base_seed(name, focus, pitfall, mermaid)

# Ensure all expected IDs exist
_EXPECTED = [f"D21-T{i:03d}" for i in range(1, 26)] + [f"D22-T{i:03d}" for i in range(1, 27)] + [
    f"D23-T{i:03d}" for i in range(1, 23)
]
_missing = [t for t in _EXPECTED if t not in SEEDS]
if _missing:
    raise RuntimeError(f"Missing seeds: {_missing}")

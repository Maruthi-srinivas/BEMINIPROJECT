# D34-T009 — Unit, integration and API tests

Topic ID: `D34-T009`
Domain: Practical Project Validation Checklist
Subdomain: Unit, integration and API tests
Importance: common
Complexity: intermediate
Dependencies: `D34-T008`, `D34-T001`, `D05-T001`, `D05-T002`, `D06-T001`, `D06-T002`
Execution status of the code in section F: not executed (documentation example)

## A. Topic Overview

Unit, integration and API tests is a backend engineering concern because production systems must handle real traffic, failures, and evolving requirements—not only happy-path demos. In interviews, strong candidates explain how Unit, integration and API tests affects latency, consistency, cost, and operability instead of naming a tool without context. This topic sits in domain 34 (Practical Project Validation Checklist) and connects to dependencies such as `D34-T008`.

## B. First-Principles Explanation

At the root, Unit, integration and API tests answers a constraint: limited CPU, network partitions, untrusted input, or business rules that must hold under retries. First-principles thinking lists the actors, the data they exchange, and the invariant that must remain true after crashes or duplicate requests. Alternatives exist because no single pattern optimizes for simplicity, scale, and correctness at once; you choose based on measurable requirements. Internal details matter when they change failure modes—for example whether state is centralized, replicated, or cached—and who must reconcile conflicts.

For Unit, integration and API tests, draw the write path and the read path separately; many bugs appear when they assume different sources of truth. State transitions should be explicit: what is persisted, what is ephemeral, and what happens if a worker dies mid-step. Boundaries (API, queue, database, external SaaS) are where typing, authorization, and idempotency belong.

## C. Internal Working and Architecture

Typical components for Unit, integration and API tests: an edge entrypoint, application services, a primary datastore, optional cache or search index, and asynchronous workers. Control plane configuration (feature flags, quotas, routing rules) should be versioned separately from data plane request handling so rollbacks are fast. Under load, the bottleneck for Unit, integration and API tests is often IO to the datastore or an external dependency; CPU profiling alone can mislead.

Observability hooks belong at each hop: trace id propagation, structured logs with tenant id, and RED/USE metrics per dependency. Security checks are not optional extras—they must run before expensive work and before side-effecting tools or transactions.

## D. Diagrams and Visual Models

```mermaid
flowchart TD
  client[ClientOrCaller]
  edge[EdgeGateway]
  service[AppService]
  store[DataStore]
  client --> edge
  edge --> service
  service --> store
  service -->|async| queue[MessageBus]
  queue --> worker[BackgroundWorker]
  worker --> store
```

This diagram highlights the main data flow for Unit, integration and API tests. Node ids are alphanumeric only for Mermaid compatibility.

## E. Examples and Analogies

Analogy: treating Unit, integration and API tests like a traffic intersection—rules only work if everyone sees the same lights; hidden shortcuts become incidents. Backend example: a checkout service applying Unit, integration and API tests must still charge exactly once when the client retries POST after a timeout. Do not skip explicit limits at the edge; unbounded queues turn latency problems into data loss problems.

## F. Code Examples

File: `examples/d34_t009.py`

Dependencies: Python 3 standard library unless noted.

```python
"""Sketch related to Unit, integration and API tests (illustrative)."""
from typing import Any, Dict

def handle_request(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """Validate, authorize, then execute domain logic."""
    if "tenant_id" not in ctx:
        raise ValueError("tenant_id required")
    # Domain-specific logic for Unit, integration and API tests belongs here.
    return {"status": "ok", "topic": "D34-T009"}

if __name__ == "__main__":
    print(handle_request({"tenant_id": "t1"}))
```

How to run: `python examples/d34_t009.py` from `EXERCISES/examples/` after copying the snippet.

Expected output: `{"status": "ok", "topic": "D34-T009"}`

The snippet is illustrative; wire real persistence and auth before production.
Keep side effects behind interfaces so tests can use fakes.

## G. Practical Backend Application

Roll out Unit, integration and API tests behind a feature flag when behavior changes are risky; measure p95 latency and error rate per tenant during canary. Document SLO impact: which user journeys degrade if this component fails and what fallback UX is acceptable. Run game days or table-top exercises for the highest-risk dependencies before peak traffic seasons.

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Minimal Unit, integration and API tests | Fast to ship, easy to reason about | Breaks under scale or abuse | Early product, low risk | Regulated or multi-tenant production |
| Managed Unit, integration and API tests | Ops burden shifts to vendor | Cost, less control | Small team, standard needs | Hard latency or compliance constraints |
| Custom Unit, integration and API tests | Fits exact policy | Build and test cost | Differentiating requirement | Commodity problem with mature libs |
| No Unit, integration and API tests | Fewer moving parts | Pain appears suddenly at scale | Prototypes | Known hot path or compliance gap |

Under abuse or viral traffic, Unit, integration and API tests must fail closed or shed load rather than retry infinitely into dependencies.

## I. Common Mistakes and Misconceptions

- Treating Unit, integration and API tests as purely infrastructure with no product-visible failure modes.
- Omitting idempotency when clients or brokers retry.
- Sharing mutable state across requests without clear ownership.

## J. Debugging and Troubleshooting

Symptoms involving Unit, integration and API tests often show up as elevated p95 latency, rising error budgets, or skewed saturation on one dependency. Separate client-side retries from server overload by checking retry headers and comparing 5xx rates with upstream latency. Capture exemplar traces for slow requests and verify whether the database, cache, or external API dominates span time. After mitigation, add a regression test or alert on the earliest signal that preceded the incident.

## K. Interview Preparation

### Beginner

#### Q1. What problem does Unit, integration and API tests solve in a backend system?

**Answer:** Question: What problem does Unit, integration and API tests solve in a backend system? — in the context of Unit, integration and API tests, interviewers at the beginner level want foundations and vocabulary tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 1 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

#### Q2. What are the main components involved in Unit, integration and API tests?

**Answer:** Question: What are the main components involved in Unit, integration and API tests? — in the context of Unit, integration and API tests, interviewers at the beginner level want foundations and vocabulary tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 2 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

#### Q3. How does Unit, integration and API tests show up at an API boundary?

**Answer:** Question: How does Unit, integration and API tests show up at an API boundary? — in the context of Unit, integration and API tests, interviewers at the beginner level want foundations and vocabulary tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 3 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

#### Q4. What is a common misconception about Unit, integration and API tests?

**Answer:** Question: What is a common misconception about Unit, integration and API tests? — in the context of Unit, integration and API tests, interviewers at the beginner level want foundations and vocabulary tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 4 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

#### Q5. Which metric would you watch first after enabling Unit, integration and API tests?

**Answer:** Question: Which metric would you watch first after enabling Unit, integration and API tests? — in the context of Unit, integration and API tests, interviewers at the beginner level want foundations and vocabulary tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 5 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

### Intermediate

#### Q1. Walk through the request path for Unit, integration and API tests under normal load.

**Answer:** Question: Walk through the request path for Unit, integration and API tests under normal load. — in the context of Unit, integration and API tests, interviewers at the intermediate level want request paths and operational limits tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 1 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

#### Q2. How would you test Unit, integration and API tests before a production rollout?

**Answer:** Question: How would you test Unit, integration and API tests before a production rollout? — in the context of Unit, integration and API tests, interviewers at the intermediate level want request paths and operational limits tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 2 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

#### Q3. What consistency or durability guarantees matter for Unit, integration and API tests?

**Answer:** Question: What consistency or durability guarantees matter for Unit, integration and API tests? — in the context of Unit, integration and API tests, interviewers at the intermediate level want request paths and operational limits tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 3 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

#### Q4. How does Unit, integration and API tests interact with retries and timeouts?

**Answer:** Question: How does Unit, integration and API tests interact with retries and timeouts? — in the context of Unit, integration and API tests, interviewers at the intermediate level want request paths and operational limits tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 4 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

#### Q5. Where would you place authorization checks relative to Unit, integration and API tests?

**Answer:** Question: Where would you place authorization checks relative to Unit, integration and API tests? — in the context of Unit, integration and API tests, interviewers at the intermediate level want request paths and operational limits tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 5 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

### Advanced

#### Q1. What failure modes are unique to Unit, integration and API tests at scale?

**Answer:** Question: What failure modes are unique to Unit, integration and API tests at scale? — in the context of Unit, integration and API tests, interviewers at the advanced level want edge cases and distributed failure tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 1 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

#### Q2. How would you design Unit, integration and API tests for multi-region or multi-tenant isolation?

**Answer:** Question: How would you design Unit, integration and API tests for multi-region or multi-tenant isolation? — in the context of Unit, integration and API tests, interviewers at the advanced level want edge cases and distributed failure tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 2 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

#### Q3. Compare two implementation options for Unit, integration and API tests and pick one with reasons.

**Answer:** Question: Compare two implementation options for Unit, integration and API tests and pick one with reasons. — in the context of Unit, integration and API tests, interviewers at the advanced level want edge cases and distributed failure tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 3 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

#### Q4. How do you prevent Unit, integration and API tests from becoming a single point of failure?

**Answer:** Question: How do you prevent Unit, integration and API tests from becoming a single point of failure? — in the context of Unit, integration and API tests, interviewers at the advanced level want edge cases and distributed failure tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 4 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

#### Q5. What load or chaos tests would you run for Unit, integration and API tests?

**Answer:** Question: What load or chaos tests would you run for Unit, integration and API tests? — in the context of Unit, integration and API tests, interviewers at the advanced level want edge cases and distributed failure tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 5 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

### Scenarios

#### Q1. Latency spikes right after a deploy touching Unit, integration and API tests. What do you check first?

**Answer:** Question: Latency spikes right after a deploy touching Unit, integration and API tests. What do you check first? — in the context of Unit, integration and API tests, interviewers at the scenario level want on-call triage and mitigation order tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 1 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

#### Q2. One tenant reports errors while others are healthy. How does Unit, integration and API tests factor in?

**Answer:** Question: One tenant reports errors while others are healthy. How does Unit, integration and API tests factor in? — in the context of Unit, integration and API tests, interviewers at the scenario level want on-call triage and mitigation order tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 2 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

#### Q3. Costs doubled after enabling Unit, integration and API tests. How do you investigate?

**Answer:** Question: Costs doubled after enabling Unit, integration and API tests. How do you investigate? — in the context of Unit, integration and API tests, interviewers at the scenario level want on-call triage and mitigation order tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 3 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

#### Q4. A dependency used by Unit, integration and API tests is slow but not down. What mitigations apply?

**Answer:** Question: A dependency used by Unit, integration and API tests is slow but not down. What mitigations apply? — in the context of Unit, integration and API tests, interviewers at the scenario level want on-call triage and mitigation order tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 4 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

#### Q5. An audit asks for evidence that Unit, integration and API tests is enforced. What artifacts do you provide?

**Answer:** Question: An audit asks for evidence that Unit, integration and API tests is enforced. What artifacts do you provide? — in the context of Unit, integration and API tests, interviewers at the scenario level want on-call triage and mitigation order tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 5 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

### Follow-ups

#### Q1. How does Unit, integration and API tests relate to observability and SLOs?

**Answer:** Question: How does Unit, integration and API tests relate to observability and SLOs? — in the context of Unit, integration and API tests, interviewers at the follow-up level want dependencies on neighboring curriculum topics tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 1 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

#### Q2. Which earlier database or networking topics does Unit, integration and API tests assume?

**Answer:** Question: Which earlier database or networking topics does Unit, integration and API tests assume? — in the context of Unit, integration and API tests, interviewers at the follow-up level want dependencies on neighboring curriculum topics tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 2 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

#### Q3. What would you study next after mastering Unit, integration and API tests?

**Answer:** Question: What would you study next after mastering Unit, integration and API tests? — in the context of Unit, integration and API tests, interviewers at the follow-up level want dependencies on neighboring curriculum topics tied to this exact point. Start with the user-visible behavior or SLA, then walk inward through the request path until you name the component that enforces the rule or holds the state. For item 3 in this tier, add one concrete production detail: a metric name, a timeout value order-of-magnitude, or a consistency choice (strong vs eventual) with a product reason. Close by stating a failure mode and mitigation so the answer sounds like on-call experience, not a glossary entry.

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/D34-T009.md`. Try these before opening that file.

### Exercise 1 — implementation

Implement a minimal service module that enforces the core invariant for `Unit, integration and API tests`: validate inputs, apply authorization, and return structured errors. Acceptance: unit tests cover happy path, missing tenant, and duplicate request id.

### Exercise 2 — debugging

Given logs where p95 latency doubled after a deploy touching `Unit, integration and API tests`, list the top five checks in order and which metric proves each hypothesis.

### Exercise 3 — trade-off

Choose between a managed platform feature and a custom implementation for `Unit, integration and API tests`. Write one page comparing cost, operability, and blast radius; pick one with explicit trade-offs.

## M. Revision Notes

- Unit, integration and API tests: know the invariant, the failure modes, and the metrics.
- Draw write and read paths before proposing tools.
- Retries require idempotency; caches require invalidation strategy.

Flashcards:

- What is the core risk if Unit, integration and API tests is misconfigured? Data loss, inconsistency, or unbounded cost.
- Symptom vs root cause? Symptom is what users see; root cause is the broken invariant.
## N. Related Topics

Understand this before: `D34-T008`

This topic supports: the next topic in domain 34

Often confused with: adjacent topics in domain 34 with similar names

Interviewers combine this with: `D22-T001` observability, `D12-T001` API design, `D15-T001` distributed systems fundamentals

## O. Completion Criteria

- Explain Unit, integration and API tests with a diagram and name one failure mode.
- List three metrics you would alert on.
- Describe a safe mitigation and a long-term prevention item.

# D15-T021 — Retries, timeouts and exponential backoff

Topic ID: `D15-T021`
Domain: Distributed Systems
Subdomain: Retries, timeouts and exponential backoff
Importance: core
Complexity: advanced
Dependencies: `D15-T020`, `D15-T001`, `D03-T001`, `D03-T002`, `D04-T001`, `D04-T002`
Execution status of the code in section F: unexecuted

## A. Topic Overview

Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed.

## B. First-Principles Explanation

Retry only idempotent or keyed operations; classify errors as retryable vs fatal. Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed.

## C. Internal Working and Architecture

Client-side retry budgets; server-side rate limits. Components interact through RPC, replication logs, and coordination services.

## D. Diagrams and Visual Models

```mermaid
flowchart TD
  call[RPC]
  timeout{Timeout?}
  retry[BackoffRetry]
  call --> timeout
  timeout -->|yes retryable| retry
  retry --> call
```

Read the diagram as a causal flow from client action to stored or observed outcome, including failure branches.

## E. Examples and Analogies

AWS SDK default backoff with max attempts.

## F. Code Examples

File: `examples/d15_t021_backoff.py`

Dependencies: Python 3 standard library only.

```python
def backoff(attempt: int, base: float, cap: float) -> float:
    return min(cap, base * (2 ** attempt))
```

The snippet models control flow you would embed in a service or test harness. It is not a production client library.

## G. Practical Backend Application

Set deadline per request tree; subtract child latency from parent budget.

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Aggressive retry | Higher success | Retry storm | Idempotent reads | Overloaded payment API | | | | |

Under load, the cheap choice on paper becomes the choice that amplifies retries, stale reads, or operator toil. Measure p99 latency and error budgets, not only happy-path throughput.

## I. Common Mistakes and Misconceptions

- Retrying 500 on POST without idempotency.
- Infinite retries on overload.

A weak interview answer names a buzzword without a failure story. A strong answer names what breaks, what users see, and what invariant you still enforce.

## J. Debugging and Troubleshooting

Metric: retry count per endpoint; correlate with saturation.

## K. Interview Preparation
### Beginner
#### Q1. What is Retries, timeouts and exponential backoff?

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. Interviewers want a precise definition tied to retry with backoff and budgets, not a slogan.
#### Q2. Why does Retries, timeouts and exponential backoff matter in backends?

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. Production systems fail one hop at a time; users still expect coherent behavior.
#### Q3. Give a one-line example of retry with backoff and budgets.

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. Name a concrete multi-service flow where the issue appears.
#### Q4. Is Retries, timeouts and exponential backoff about hardware or software policy?

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. Mostly policy and protocols on top of unreliable networks.
#### Q5. What is a common myth about Retries, timeouts and exponential backoff?

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. Buzzword definitions that ignore partitions, retries, or consistency definitions.
### Intermediate
#### Q1. How do timeouts interact with retry with backoff and budgets?

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. Timeouts create unknown outcomes; retries amplify load unless idempotent.
#### Q2. How do replicas interact with retry with backoff and budgets?

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. Replication lag makes stale reads a normal case unless you pay for stronger reads.
#### Q3. How do idempotency keys help retry with backoff and budgets?

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. They make at-least-once delivery safe for business side effects.
#### Q4. What metrics expose retry with backoff and budgets?

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. Error rate by dependency, lag histograms, reconciliation queue depth.
#### Q5. How does Retries, timeouts and exponential backoff relate to user-visible SLAs?

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. SLAs must state behavior during degradation, not only median latency.
### Advanced
#### Q1. How would you test retry with backoff and budgets?

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. Fault injection: delay, drop, partition links; assert invariants and recovery.
#### Q2. How does Retries, timeouts and exponential backoff differ from a single-machine failure?

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. Partial failure leaves other paths alive, producing ambiguous global state.
#### Q3. What documentation should teams publish about Retries, timeouts and exponential backoff?

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. Failure modes, consistency guarantees per endpoint, and runbooks for unknown outcomes.
#### Q4. When is strong consistency worth the latency for retry with backoff and budgets?

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. When invariants involve money, inventory, or safety; not for best-effort feeds.
#### Q5. How do circuit breakers relate to retry with backoff and budgets?

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. They stop retry storms but do not fix correctness; they protect capacity.
### Scenarios
#### Q1. Incident: errors spike after deploy touching Retries, timeouts and exponential backoff. First checks?

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. Roll forward/rollback decision, feature flag, canary metrics, dependency health.
#### Q2. Incident: customers report inconsistent reads around retry with backoff and budgets. Diagnosis?

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. Check replica lag, routing, cache TTL, and read-your-writes settings.
#### Q3. Incident: reconciliation backlog grows for retry with backoff and budgets. Why?

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. Downstream was slow; retries duplicated work; missing idempotency.
#### Q4. Design review challenges your Retries, timeouts and exponential backoff approach. What do you defend?

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. State invariants, failure model, and measured trade-offs with PACELC/CAP precision.
#### Q5. Finance audit questions retry with backoff and budgets after duplicate charges. Response?

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. Show idempotency keys, ledger reconciliation, and provider correlation IDs.
### Follow-ups
#### Q1. How does Retries, timeouts and exponential backoff connect to `D15-T001`?

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. Fundamentals frame partial failure and message passing assumptions.
#### Q2. How does Retries, timeouts and exponential backoff connect to databases (`D07-T012`)?

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. Transactions are local unless you add distributed protocols or sagas.
#### Q3. How does Retries, timeouts and exponential backoff connect to messaging (`D14-T031`)?

**Answer:** Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed. Brokers provide at-least-once unless you engineer exactly-once effects.

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/D15-T021.md`. Try these before opening that file.

### Exercise 1 — implementation

Compute backoff attempts 0-3 with base=0.1 cap=2.

### Exercise 2 — debugging

Latency SLO blown by retries—fix?

### Exercise 3 — trade-off

Retry on 429 vs 503.

## M. Revision Notes

- Retries, timeouts and exponential backoff
- Retries convert transient failures into success but amplify load.
- Measure lag, errors, and reconciliation—not only CPU.
- Document behavior during partition and during normal load.

Flashcards:

- What is Retries, timeouts and exponential backoff? See focus paragraph in overview.
- Common mistake: Retrying 500 on POST without idempotency.

## N. Related Topics

Understand this before: `D15-T020`, `D15-T001`, `D03-T001`, `D03-T002`, `D04-T001`, `D04-T002`.

This topic supports: `D15-T022`, `D15-T023`.

Often confused with: `D15-T022`, `D13-T024`.

Interviewers combine this with replication (`D15-T009`), partial failure (`D15-T002`), and API idempotency (`D06-T011`).

## O. Completion Criteria

- Define Retries, timeouts and exponential backoff without buzzwords.
- Draw the mermaid model for D15-T021.
- Explain one mistake and its safer alternative.

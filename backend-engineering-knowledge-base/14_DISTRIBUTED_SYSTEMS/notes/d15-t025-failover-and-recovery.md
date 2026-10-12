# D15-T025 — Failover and recovery

Topic ID: `D15-T025`
Domain: Distributed Systems
Subdomain: Failover and recovery
Importance: core
Complexity: advanced
Dependencies: `D15-T024`, `D15-T001`, `D03-T001`, `D03-T002`, `D04-T001`, `D04-T002`
Execution status of the code in section F: unexecuted

## A. Topic Overview

Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal.

## B. First-Principles Explanation

RTO/RPO drive automation vs manual steps. Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal.

## C. Internal Working and Architecture

DNS/load balancer health checks, controlled promotion, rehearsed runbooks. Components interact through RPC, replication logs, and coordination services.

## D. Diagrams and Visual Models

```mermaid
flowchart LR
  primary[Primary]
  standby[Standby]
  traffic[Traffic]
  traffic --> primary
  primary -. failure .-> standby
```

Read the diagram as a causal flow from client action to stored or observed outcome, including failure branches.

## E. Examples and Analogies

RDS Multi-AZ failover; Kubernetes pod reschedule.

## F. Code Examples

File: `examples/d15_t025_failover.py`

Dependencies: Python 3 standard library only.

```python
def should_failover(primary_healthy: bool, standby_ready: bool) -> bool:
    return not primary_healthy and standby_ready
```

The snippet models control flow you would embed in a service or test harness. It is not a production client library.

## G. Practical Backend Application

Test failover quarterly; verify app reconnects and schema compatible.

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Automatic failover | Low RTO | False positive risk | HA DB | Experimental shard | | | | |

Under load, the cheap choice on paper becomes the choice that amplifies retries, stale reads, or operator toil. Measure p99 latency and error budgets, not only happy-path throughput.

## I. Common Mistakes and Misconceptions

- Failover without checking replication lag.
- Clients cache dead primary DNS forever.

A weak interview answer names a buzzword without a failure story. A strong answer names what breaks, what users see, and what invariant you still enforce.

## J. Debugging and Troubleshooting

Timeline from detection to stable traffic on standby.

## K. Interview Preparation
### Beginner
#### Q1. What is Failover and recovery?

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. Interviewers want a precise definition tied to failover RTO RPO, not a slogan. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.
#### Q2. Why does Failover and recovery matter in backends?

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. Production systems fail one hop at a time; users still expect coherent behavior. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.
#### Q3. Give a one-line example of failover RTO RPO.

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. Name a concrete multi-service flow where the issue appears. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.
#### Q4. Is Failover and recovery about hardware or software policy?

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. Mostly policy and protocols on top of unreliable networks. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.
#### Q5. What is a common myth about Failover and recovery?

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. Buzzword definitions that ignore partitions, retries, or consistency definitions. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.
### Intermediate
#### Q1. How do timeouts interact with failover RTO RPO?

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. Timeouts create unknown outcomes; retries amplify load unless idempotent. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.
#### Q2. How do replicas interact with failover RTO RPO?

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. Replication lag makes stale reads a normal case unless you pay for stronger reads. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.
#### Q3. How do idempotency keys help failover RTO RPO?

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. They make at-least-once delivery safe for business side effects. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.
#### Q4. What metrics expose failover RTO RPO?

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. Error rate by dependency, lag histograms, reconciliation queue depth. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.
#### Q5. How does Failover and recovery relate to user-visible SLAs?

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. SLAs must state behavior during degradation, not only median latency. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.
### Advanced
#### Q1. How would you test failover RTO RPO?

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. Fault injection: delay, drop, partition links; assert invariants and recovery. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.
#### Q2. How does Failover and recovery differ from a single-machine failure?

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. Partial failure leaves other paths alive, producing ambiguous global state. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.
#### Q3. What documentation should teams publish about Failover and recovery?

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. Failure modes, consistency guarantees per endpoint, and runbooks for unknown outcomes. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.
#### Q4. When is strong consistency worth the latency for failover RTO RPO?

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. When invariants involve money, inventory, or safety; not for best-effort feeds. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.
#### Q5. How do circuit breakers relate to failover RTO RPO?

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. They stop retry storms but do not fix correctness; they protect capacity. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.
### Scenarios
#### Q1. Incident: errors spike after deploy touching Failover and recovery. First checks?

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. Roll forward/rollback decision, feature flag, canary metrics, dependency health. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.
#### Q2. Incident: customers report inconsistent reads around failover RTO RPO. Diagnosis?

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. Check replica lag, routing, cache TTL, and read-your-writes settings. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.
#### Q3. Incident: reconciliation backlog grows for failover RTO RPO. Why?

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. Downstream was slow; retries duplicated work; missing idempotency. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.
#### Q4. Design review challenges your Failover and recovery approach. What do you defend?

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. State invariants, failure model, and measured trade-offs with PACELC/CAP precision. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.
#### Q5. Finance audit questions failover RTO RPO after duplicate charges. Response?

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. Show idempotency keys, ledger reconciliation, and provider correlation IDs. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.
### Follow-ups
#### Q1. How does Failover and recovery connect to `D15-T001`?

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. Fundamentals frame partial failure and message passing assumptions. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.
#### Q2. How does Failover and recovery connect to databases (`D07-T012`)?

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. Transactions are local unless you add distributed protocols or sagas. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.
#### Q3. How does Failover and recovery connect to messaging (`D14-T031`)?

**Answer:** Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal. Brokers provide at-least-once unless you engineer exactly-once effects. In production, the failure mode matters more than the slogan: measure timeouts, error budgets, and client-visible symptoms before you rename the problem.

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/D15-T025.md`. Try these before opening that file.

### Exercise 1 — implementation

Implement should_failover guard.

### Exercise 2 — debugging

Failover succeeded but data old—what metric?

### Exercise 3 — trade-off

Blue/green vs active-passive.

## M. Revision Notes

- Failover and recovery
- Failover redirects traffic to standby when primary fails.
- Measure lag, errors, and reconciliation—not only CPU.
- Document behavior during partition and during normal load.

Flashcards:

- What is Failover and recovery? See focus paragraph in overview.
- Common mistake: Failover without checking replication lag.

## N. Related Topics

Understand this before: `D15-T024`, `D15-T001`, `D03-T001`, `D03-T002`, `D04-T001`, `D04-T002`.

This topic supports: `D15-T008`, `D15-T026`.

Often confused with: `D15-T013`, `D15-T033`.

Interviewers combine this with replication (`D15-T009`), partial failure (`D15-T002`), and API idempotency (`D06-T011`).

## O. Completion Criteria

- Define Failover and recovery without buzzwords.
- Draw the mermaid model for D15-T025.
- Explain one mistake and its safer alternative.

# D07-T014 — Dirty reads, non-repeatable reads, phantom reads

Topic ID: `D07-T014`
Domain: Database Fundamentals
Subdomain: Dirty reads, non-repeatable reads, phantom reads
Importance: core
Complexity: intermediate
Dependencies: `D07-T013`, `D07-T001`, `D01-T001`, `D01-T002`
SQL in section F: unexecuted (illustrative only)

## A. Topic Overview

Dirty, non-repeatable, and phantom reads are isolation anomalies defined by ANSI SQL concurrency.

Prerequisites: `D07-T013`. Next in the database track: `D07-T015`.

## B. First-Principles Explanation

They describe what concurrent schedules allow. MVCC and locks map levels to prevented anomalies.

## C. Internal Working and Architecture

Dirty read is uncommitted data. Non-repeatable is two reads, different committed value. Phantom is new rows in range.

## D. Diagrams and Visual Models

```mermaid
flowchart TD
  dirty[DirtyRead]
  nrr[NonRepeatableRead]
  phantom[PhantomRead]
  dirty -->|prevented_by| rc[ReadCommitted]
  nrr -->|prevented_by| rr[RepeatableRead]
  phantom -->|prevented_by| ser[Serializable]
```

Read the diagram as a logical model for this topic; engine details vary by product.

## E. Examples and Analogies

Double booking can be phantom if second transaction inserts overlapping reservation.

## F. Code Examples

Illustrative SQL (dirty, non-repeatable, and phantom reads). Not executed in this repository.

```sql
-- unexecuted
-- Session A
BEGIN; UPDATE accounts SET balance = balance - 50 WHERE id = 1; -- not committed
-- Session B (READ COMMITTED) should not see -50 until commit
```

Read the statements as teaching examples. Bind parameters in application code; do not concatenate user input into these patterns.

## G. Practical Backend Application

Match anomaly to business risk; choose isolation or explicit locks.

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Apply topic pattern | predictable behavior | design time | core domain data | quick hacks |
| Defer topic pattern | faster prototype | incident debt | throwaway demos | money and compliance |

## I. Common Mistakes and Misconceptions

- Calling all races dirty reads.
- Thinking RR stops all phantoms everywhere.
- No version column on optimistic path.
- SELECT FOR UPDATE forgotten.
- Read replica for just-written row.

## J. Debugging and Troubleshooting

- Reproduce with two sessions.
- Check isolation setting.
- Use version column mismatch.
- Route critical read to primary.

## K. Interview Preparation

### Beginner

#### Q1. What is the core idea behind dirty, non-repeatable, and phantom reads?

**Answer:** A dirty read sees uncommitted changes from another transaction. A non-repeatable read sees different values when reading the same row twice. A phantom read sees new rows matching a predicate on a re-scan. Lost update occurs when two writers overwrite without proper isolation or locking.

#### Q2. Why do backend teams care about dirty, non-repeatable, and phantom reads?

**Answer:** READ COMMITTED prevents dirty reads in Postgres. REPEATABLE READ prevents non-repeatable reads in Postgres. SERIALIZABLE or careful locking prevents phantoms for critical predicates. Optimistic schemes detect lost updates with version columns.

#### Q3. Name one mistake juniors make with dirty, non-repeatable, and phantom reads.

**Answer:** Teams forget that DDL can lock tables during careless migrations. Assuming default isolation is SERIALIZABLE causes surprise anomalies. Application retries must be idempotent when constraints fail. Caching without invalidation creates ghost reads for users.

#### Q4. How does dirty, non-repeatable, and phantom reads show up in production incidents?

**Answer:** Backups are worthless without tested restore procedures. Replication is not sharding; conflating them breaks capacity plans. Incidents show up as 500s, timeouts, or silent wrong balances. Compare primary versus replica lag during read inconsistency tickets.

#### Q5. What should you read in logs when debugging dirty, non-repeatable, and phantom reads?

**Answer:** EXPLAIN output tells you whether the planner chose a seq scan. Check max_connections and pool exhaustion before blaming CPU. Correlate deploy time with migration version and lock waits. Use statement timeouts to fail fast instead of wedging pools.

### Intermediate

#### Q1. How would you explain dirty, non-repeatable, and phantom reads to a product manager?

**Answer:** Product wants features; you translate them into constraints and indexes. Teach stakeholders that data rules live in the database when possible. Show how a constraint prevents an entire class of bugs. Estimate migration downtime using row counts and lock models.

#### Q2. What SQL or schema detail best teaches dirty, non-repeatable, and phantom reads?

**Answer:** Illustrative SQL in notes is unexecuted but should be valid dialect. Use parameterized queries in real services, not string concatenation. Foreign keys document relationships for the next engineer. CHECK constraints encode domain rules close to storage.

#### Q3. How does dirty, non-repeatable, and phantom reads interact with connection pooling?

**Answer:** Pools reuse TCP connections and amortize authentication. Pool size times pod count must stay below database max_connections. Long transactions hold connections and block pool recycling. Monitor hikaricp or pgBouncer wait metrics in production.

#### Q4. When does dirty, non-repeatable, and phantom reads block a release?

**Answer:** Backward-incompatible DDL needs expand-contract deploy steps. Blocking migrations should run in maintenance windows or online tools. Feature flags do not rollback applied DDL automatically. Document forward-only migrations with compensating application logic.

#### Q5. What metric proves you solved a dirty, non-repeatable, and phantom reads problem?

**Answer:** Success means p95 query latency within SLO after change. Deadlock rate should not spike after a concurrency change. Replication lag p99 within budget for stale-tolerant reads. Constraint violation rate should be near zero for happy paths.

### Advanced

#### Q1. How does dirty, non-repeatable, and phantom reads differ between PostgreSQL and MySQL?

**Answer:** PostgreSQL uses MVCC; MySQL InnoDB does with different DDL behavior. Isolation semantics differ slightly; read the manual per engine. Never assume Oracle locking on Postgres without testing. Session-level settings can change isolation for one transaction.

#### Q2. How does dirty, non-repeatable, and phantom reads change under replication lag?

**Answer:** Asynchronous replicas apply WAL after commit on primary. Read-your-writes fails if you read a lagging replica too soon. Critical reads after a write should target the primary. Lag-aware routers help dashboards but not payment confirmation.

#### Q3. How does dirty, non-repeatable, and phantom reads relate to MVCC?

**Answer:** MVCC keeps snapshot versions per transaction id or xmin xmax. UPDATE creates new row versions; old versions need vacuum. HOT updates avoid index churn when indexed columns unchanged. Serializable isolation uses SSI or predicate locks depending on engine.

#### Q4. What is a distributed-systems failure mode for dirty, non-repeatable, and phantom reads?

**Answer:** Network partitions can promote a replica while primary still writes. Split brain duplicates primary unless fencing stops old writer. Idempotent consumers heal duplicate messages after failover. Cross-shard transactions need two-phase commit or sagas.

#### Q5. How would you test dirty, non-repeatable, and phantom reads in CI?

**Answer:** Spin up test database in CI and apply migration chain. Run EXPLAIN on golden queries when indexes change. Assert migration checksum and rollback script presence. Concurrency integration tests catch lost updates early.

### Scenarios

#### Q1. On-call: p95 latency doubled after a deploy touching dirty, non-repeatable, and phantom reads. First three steps?

**Answer:** Load test with pool size matching production per instance. Inspect recent deploy, pool metrics, and slow query log. Capture pg_stat_activity for blocking queries. Roll back application if migration is forward-only broken.

#### Q2. Finance reports wrong totals linked to dirty, non-repeatable, and phantom reads. What do you verify?

**Answer:** Reconcile financial totals against ledger constraints. Halt batch jobs that double-apply partial migrations. Compare row counts before and after backfill scripts. Restore from PITR if DDL corrupted constraints mid-flight.

#### Q3. A migration failed mid-way affecting dirty, non-repeatable, and phantom reads. How do you recover?

**Answer:** Put cluster in read-only, fix schema, replay missed writes. Keep runbook steps in the incident channel for audit. Explain risk of data loss if shortcuts ship without review. Offer phased rollout with measurable rollback triggers.

#### Q4. Team wants to skip dirty, non-repeatable, and phantom reads to ship faster. Your response?

**Answer:** Pair extra QA time with any isolation level change. Send post-write reads to primary until lag under threshold. Stamp session with last_write_lsn for replica routing if available. Invalidate caches on write path before acknowledging client.

#### Q5. Read replica serves stale data involving dirty, non-repeatable, and phantom reads. Mitigation?

**Answer:** Page if replica lag exceeds minutes for user-facing reads. The next topic in domain seven builds on this foundation. API pagination should use indexed columns for stability. Map SQLSTATE or vendor codes to stable HTTP errors.

### Follow-ups

#### Q1. How does dirty, non-repeatable, and phantom reads connect to the next topic in domain 7?

**Answer:** Emit db.client.operation spans with sanitized statements. Dashboard pool usage, deadlocks, replication lag, and bloat. Shard keys should be chosen before volume makes resharding painful. Index-only scans may still hit the heap when the visibility map is stale.

#### Q2. How does dirty, non-repeatable, and phantom reads connect to API design?

**Answer:** Prepared statements conflict with transaction-level pool modes. Logical dumps differ from physical backups in restore time and PITR. Autovacuum tuning must match update-heavy table churn. Partial indexes shrink size when queries always filter status.

#### Q3. How does dirty, non-repeatable, and phantom reads connect to observability?

**Answer:** Covering indexes trade disk for fewer heap lookups on hot reads. SERIALIZABLE workloads need application retry on serialization failures. Retention documentation belongs in privacy policies and ops runbooks. Document expected query shapes beside every new index in code review.


## L. Practical Exercises

Solutions are in `EXERCISES/solutions/D07-T014.md`. Try these before opening that file.

### Exercise 1

Script two-session anomaly demo.

### Exercise 2

Add version optimistic lock.

### Exercise 3

Document read-after-write.

## M. Revision Notes

- Three anomaly definitions.
- Map to isolation.
- Lost update related.
- Postgres specifics.

## N. Related Topics

Understand this before: `D07-T013`.

This topic supports: `D07-T015`.

Often confused with: adjacent domain-7 topics—read section N of neighbors when unsure.

Interviewers combine this with `D05-T021` pooling and `D07-T023` EXPLAIN.

## O. Completion Criteria

- Demonstrate phantom.
- Fix lost update.
- Explain dirty read.
- Replica stale vs anomaly.

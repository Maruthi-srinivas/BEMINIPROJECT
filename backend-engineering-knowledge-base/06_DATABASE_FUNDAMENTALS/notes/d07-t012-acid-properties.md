# D07-T012 — ACID properties

Topic ID: `D07-T012`
Domain: Database Fundamentals
Subdomain: ACID properties
Importance: core
Complexity: intermediate
Dependencies: `D07-T011`, `D07-T001`, `D01-T001`, `D01-T002`
SQL in section F: unexecuted (illustrative only)

## A. Topic Overview

ACID: Atomicity, Consistency, Isolation, Durability—properties of transactional database processing.

Prerequisites: `D07-T011`. Next in the database track: `D07-T013`.

## B. First-Principles Explanation

Atomicity is undo on failure; consistency is valid state per constraints; isolation is concurrency control; durability is log replay.

## C. Internal Working and Architecture

WAL provides durability; lock/MVCC provides isolation; constraint checks provide consistency.

## D. Diagrams and Visual Models

```mermaid
flowchart TD
  A[Atomicity]
  C[Consistency]
  I[Isolation]
  D[Durability]
  A --> C --> I --> D
```

Read the diagram as a logical model for this topic; engine details vary by product.

## E. Examples and Analogies

Order header and lines commit together—atomicity. Negative balance rejected—consistency.

## F. Code Examples

Illustrative SQL (ACID properties). Not executed in this repository.

```sql
-- unexecuted
-- Atomicity + consistency example
BEGIN;
INSERT INTO orders (id, total_cents) VALUES (1, 5000);
INSERT INTO order_lines (order_id, line_no, amount_cents) VALUES (1, 1, 5000);
COMMIT;
```

Read the statements as teaching examples. Bind parameters in application code; do not concatenate user input into these patterns.

## G. Practical Backend Application

Tune isolation and synchronous_commit knowing which ACID letter you relax.

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Apply topic pattern | predictable behavior | design time | core domain data | quick hacks |
| Defer topic pattern | faster prototype | incident debt | throwaway demos | money and compliance |

## I. Common Mistakes and Misconceptions

- Confusing CAP C with ACID C.
- Assuming cross-db ACID.
- No constraints then claiming C.
- async commit for money.
- Long TX breaking I.

## J. Debugging and Troubleshooting

- Check synchronous_commit.
- Find partial commits across services.
- Verify constraints exist.
- Measure commit latency.

## K. Interview Preparation

### Beginner

#### Q1. What is the core idea behind ACID properties?

**Answer:** Atomicity means a transaction's changes all commit or all roll back. Consistency means constraints hold before and after each transaction. Isolation means concurrent transactions do not observe each other's partial work. Durability means committed data survives crashes after WAL fsync.

#### Q2. Why do backend teams care about ACID properties?

**Answer:** ACID is a bundle; weakening one letter changes application assumptions. Consistency in ACID is about constraints, not CAP consistency. Interviewers contrast ACID OLTP with BASE eventually consistent stores. Durability depends on synchronous_commit and replication settings.

#### Q3. Name one mistake juniors make with ACID properties.

**Answer:** Teams forget that DDL can lock tables during careless migrations. Assuming default isolation is SERIALIZABLE causes surprise anomalies. Application retries must be idempotent when constraints fail. Caching without invalidation creates ghost reads for users.

#### Q4. How does ACID properties show up in production incidents?

**Answer:** Backups are worthless without tested restore procedures. Replication is not sharding; conflating them breaks capacity plans. Incidents show up as 500s, timeouts, or silent wrong balances. Compare primary versus replica lag during read inconsistency tickets.

#### Q5. What should you read in logs when debugging ACID properties?

**Answer:** EXPLAIN output tells you whether the planner chose a seq scan. Check max_connections and pool exhaustion before blaming CPU. Correlate deploy time with migration version and lock waits. Use statement timeouts to fail fast instead of wedging pools.

### Intermediate

#### Q1. How would you explain ACID properties to a product manager?

**Answer:** Product wants features; you translate them into constraints and indexes. Teach stakeholders that data rules live in the database when possible. Show how a constraint prevents an entire class of bugs. Estimate migration downtime using row counts and lock models.

#### Q2. What SQL or schema detail best teaches ACID properties?

**Answer:** Illustrative SQL in notes is unexecuted but should be valid dialect. Use parameterized queries in real services, not string concatenation. Foreign keys document relationships for the next engineer. CHECK constraints encode domain rules close to storage.

#### Q3. How does ACID properties interact with connection pooling?

**Answer:** Pools reuse TCP connections and amortize authentication. Pool size times pod count must stay below database max_connections. Long transactions hold connections and block pool recycling. Monitor hikaricp or pgBouncer wait metrics in production.

#### Q4. When does ACID properties block a release?

**Answer:** Backward-incompatible DDL needs expand-contract deploy steps. Blocking migrations should run in maintenance windows or online tools. Feature flags do not rollback applied DDL automatically. Document forward-only migrations with compensating application logic.

#### Q5. What metric proves you solved a ACID properties problem?

**Answer:** Success means p95 query latency within SLO after change. Deadlock rate should not spike after a concurrency change. Replication lag p99 within budget for stale-tolerant reads. Constraint violation rate should be near zero for happy paths.

### Advanced

#### Q1. How does ACID properties differ between PostgreSQL and MySQL?

**Answer:** PostgreSQL uses MVCC; MySQL InnoDB does with different DDL behavior. Isolation semantics differ slightly; read the manual per engine. Never assume Oracle locking on Postgres without testing. Session-level settings can change isolation for one transaction.

#### Q2. How does ACID properties change under replication lag?

**Answer:** Asynchronous replicas apply WAL after commit on primary. Read-your-writes fails if you read a lagging replica too soon. Critical reads after a write should target the primary. Lag-aware routers help dashboards but not payment confirmation.

#### Q3. How does ACID properties relate to MVCC?

**Answer:** MVCC keeps snapshot versions per transaction id or xmin xmax. UPDATE creates new row versions; old versions need vacuum. HOT updates avoid index churn when indexed columns unchanged. Serializable isolation uses SSI or predicate locks depending on engine.

#### Q4. What is a distributed-systems failure mode for ACID properties?

**Answer:** Network partitions can promote a replica while primary still writes. Split brain duplicates primary unless fencing stops old writer. Idempotent consumers heal duplicate messages after failover. Cross-shard transactions need two-phase commit or sagas.

#### Q5. How would you test ACID properties in CI?

**Answer:** Spin up test database in CI and apply migration chain. Run EXPLAIN on golden queries when indexes change. Assert migration checksum and rollback script presence. Concurrency integration tests catch lost updates early.

### Scenarios

#### Q1. On-call: p95 latency doubled after a deploy touching ACID properties. First three steps?

**Answer:** Load test with pool size matching production per instance. Inspect recent deploy, pool metrics, and slow query log. Capture pg_stat_activity for blocking queries. Roll back application if migration is forward-only broken.

#### Q2. Finance reports wrong totals linked to ACID properties. What do you verify?

**Answer:** Reconcile financial totals against ledger constraints. Halt batch jobs that double-apply partial migrations. Compare row counts before and after backfill scripts. Restore from PITR if DDL corrupted constraints mid-flight.

#### Q3. A migration failed mid-way affecting ACID properties. How do you recover?

**Answer:** Put cluster in read-only, fix schema, replay missed writes. Keep runbook steps in the incident channel for audit. Explain risk of data loss if shortcuts ship without review. Offer phased rollout with measurable rollback triggers.

#### Q4. Team wants to skip ACID properties to ship faster. Your response?

**Answer:** Pair extra QA time with any isolation level change. Send post-write reads to primary until lag under threshold. Stamp session with last_write_lsn for replica routing if available. Invalidate caches on write path before acknowledging client.

#### Q5. Read replica serves stale data involving ACID properties. Mitigation?

**Answer:** Page if replica lag exceeds minutes for user-facing reads. The next topic in domain seven builds on this foundation. API pagination should use indexed columns for stability. Map SQLSTATE or vendor codes to stable HTTP errors.

### Follow-ups

#### Q1. How does ACID properties connect to the next topic in domain 7?

**Answer:** Emit db.client.operation spans with sanitized statements. Dashboard pool usage, deadlocks, replication lag, and bloat. Shard keys should be chosen before volume makes resharding painful. Index-only scans may still hit the heap when the visibility map is stale.

#### Q2. How does ACID properties connect to API design?

**Answer:** Prepared statements conflict with transaction-level pool modes. Logical dumps differ from physical backups in restore time and PITR. Autovacuum tuning must match update-heavy table churn. Partial indexes shrink size when queries always filter status.

#### Q3. How does ACID properties connect to observability?

**Answer:** Covering indexes trade disk for fewer heap lookups on hot reads. SERIALIZABLE workloads need application retry on serialization failures. Retention documentation belongs in privacy policies and ops runbooks. Document expected query shapes beside every new index in code review.


## L. Practical Exercises

Solutions are in `EXERCISES/solutions/D07-T012.md`. Try these before opening that file.

### Exercise 1

Document ACID boundaries for payment service.

### Exercise 2

Choose sync commit policy.

### Exercise 3

Add missing constraints.

## M. Revision Notes

- Four letters defined.
- C is constraints.
- Durability = WAL.
- Not same as CAP.

## N. Related Topics

Understand this before: `D07-T011`.

This topic supports: `D07-T013`.

Often confused with: adjacent domain-7 topics—read section N of neighbors when unsure.

Interviewers combine this with `D05-T021` pooling and `D07-T023` EXPLAIN.

## O. Completion Criteria

- Explain each letter with example.
- When async commit OK.
- Cross-service atomicity limits.
- Map to Postgres settings.

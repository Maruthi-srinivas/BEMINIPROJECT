# D07-T013 — Isolation levels

Topic ID: `D07-T013`
Domain: Database Fundamentals
Subdomain: Isolation levels
Importance: core
Complexity: intermediate
Dependencies: `D07-T012`, `D07-T001`, `D01-T001`, `D01-T002`
SQL in section F: unexecuted (illustrative only)

## A. Topic Overview

Isolation levels define which concurrency anomalies a transaction may see.

Prerequisites: `D07-T012`. Next in the database track: `D07-T014`.

## B. First-Principles Explanation

ANSI levels form a ladder of stricter behavior. Engines implement with locks or MVCC snapshots.

## C. Internal Working and Architecture

Postgres uses snapshots; RR prevents non-repeatable reads; serializable adds predicate checks.

## D. Diagrams and Visual Models

```mermaid
flowchart TD
  ru[ReadUncommitted]
  rc[ReadCommitted]
  rr[RepeatableRead]
  ser[Serializable]
  ru --> rc --> rr --> ser
```

Read the diagram as a logical model for this topic; engine details vary by product.

## E. Examples and Analogies

Inventory hold may need REPEATABLE READ or SERIALIZABLE to avoid double sell.

## F. Code Examples

Illustrative SQL (SQL isolation levels). Not executed in this repository.

```sql
-- unexecuted
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT balance FROM accounts WHERE id = 1;
-- same balance if re-selected in this transaction
COMMIT;
```

Read the statements as teaching examples. Bind parameters in application code; do not concatenate user input into these patterns.

## G. Practical Backend Application

Pick lowest isolation that preserves invariants; test under concurrency.

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Apply topic pattern | predictable behavior | design time | core domain data | quick hacks |
| Defer topic pattern | faster prototype | incident debt | throwaway demos | money and compliance |

## I. Common Mistakes and Misconceptions

- Always SERIALIZABLE for speed myth.
- Ignoring default per engine.
- Phantom under RR in some engines.
- No retry on serialization_failure.
- Long RR holding versions.

## J. Debugging and Troubleshooting

- Log isolation level per TX.
- Watch serialization_failure rate.
- Compare statement vs transaction snapshot.
- Load test concurrent updates.

## K. Interview Preparation

### Beginner

#### Q1. What is the core idea behind SQL isolation levels?

**Answer:** READ UNCOMMITTED allows dirty reads in theory; Postgres treats it as READ COMMITTED. READ COMMITTED sees only committed data per statement snapshot. REPEATABLE READ keeps one snapshot for the whole transaction. SERIALIZABLE prevents serializable anomalies using SSI or locking.

#### Q2. Why do backend teams care about SQL isolation levels?

**Answer:** Higher isolation reduces anomalies but increases retries and blocking. Default in Postgres is READ COMMITTED; in MySQL InnoDB REPEATABLE READ. Set isolation per transaction when needed, not globally without review. Anomalies map to isolation level: dirty, non-repeatable, phantom.

#### Q3. Name one mistake juniors make with SQL isolation levels.

**Answer:** Teams forget that DDL can lock tables during careless migrations. Assuming default isolation is SERIALIZABLE causes surprise anomalies. Application retries must be idempotent when constraints fail. Caching without invalidation creates ghost reads for users.

#### Q4. How does SQL isolation levels show up in production incidents?

**Answer:** Backups are worthless without tested restore procedures. Replication is not sharding; conflating them breaks capacity plans. Incidents show up as 500s, timeouts, or silent wrong balances. Compare primary versus replica lag during read inconsistency tickets.

#### Q5. What should you read in logs when debugging SQL isolation levels?

**Answer:** EXPLAIN output tells you whether the planner chose a seq scan. Check max_connections and pool exhaustion before blaming CPU. Correlate deploy time with migration version and lock waits. Use statement timeouts to fail fast instead of wedging pools.

### Intermediate

#### Q1. How would you explain SQL isolation levels to a product manager?

**Answer:** Product wants features; you translate them into constraints and indexes. Teach stakeholders that data rules live in the database when possible. Show how a constraint prevents an entire class of bugs. Estimate migration downtime using row counts and lock models.

#### Q2. What SQL or schema detail best teaches SQL isolation levels?

**Answer:** Illustrative SQL in notes is unexecuted but should be valid dialect. Use parameterized queries in real services, not string concatenation. Foreign keys document relationships for the next engineer. CHECK constraints encode domain rules close to storage.

#### Q3. How does SQL isolation levels interact with connection pooling?

**Answer:** Pools reuse TCP connections and amortize authentication. Pool size times pod count must stay below database max_connections. Long transactions hold connections and block pool recycling. Monitor hikaricp or pgBouncer wait metrics in production.

#### Q4. When does SQL isolation levels block a release?

**Answer:** Backward-incompatible DDL needs expand-contract deploy steps. Blocking migrations should run in maintenance windows or online tools. Feature flags do not rollback applied DDL automatically. Document forward-only migrations with compensating application logic.

#### Q5. What metric proves you solved a SQL isolation levels problem?

**Answer:** Success means p95 query latency within SLO after change. Deadlock rate should not spike after a concurrency change. Replication lag p99 within budget for stale-tolerant reads. Constraint violation rate should be near zero for happy paths.

### Advanced

#### Q1. How does SQL isolation levels differ between PostgreSQL and MySQL?

**Answer:** PostgreSQL uses MVCC; MySQL InnoDB does with different DDL behavior. Isolation semantics differ slightly; read the manual per engine. Never assume Oracle locking on Postgres without testing. Session-level settings can change isolation for one transaction.

#### Q2. How does SQL isolation levels change under replication lag?

**Answer:** Asynchronous replicas apply WAL after commit on primary. Read-your-writes fails if you read a lagging replica too soon. Critical reads after a write should target the primary. Lag-aware routers help dashboards but not payment confirmation.

#### Q3. How does SQL isolation levels relate to MVCC?

**Answer:** MVCC keeps snapshot versions per transaction id or xmin xmax. UPDATE creates new row versions; old versions need vacuum. HOT updates avoid index churn when indexed columns unchanged. Serializable isolation uses SSI or predicate locks depending on engine.

#### Q4. What is a distributed-systems failure mode for SQL isolation levels?

**Answer:** Network partitions can promote a replica while primary still writes. Split brain duplicates primary unless fencing stops old writer. Idempotent consumers heal duplicate messages after failover. Cross-shard transactions need two-phase commit or sagas.

#### Q5. How would you test SQL isolation levels in CI?

**Answer:** Spin up test database in CI and apply migration chain. Run EXPLAIN on golden queries when indexes change. Assert migration checksum and rollback script presence. Concurrency integration tests catch lost updates early.

### Scenarios

#### Q1. On-call: p95 latency doubled after a deploy touching SQL isolation levels. First three steps?

**Answer:** Load test with pool size matching production per instance. Inspect recent deploy, pool metrics, and slow query log. Capture pg_stat_activity for blocking queries. Roll back application if migration is forward-only broken.

#### Q2. Finance reports wrong totals linked to SQL isolation levels. What do you verify?

**Answer:** Reconcile financial totals against ledger constraints. Halt batch jobs that double-apply partial migrations. Compare row counts before and after backfill scripts. Restore from PITR if DDL corrupted constraints mid-flight.

#### Q3. A migration failed mid-way affecting SQL isolation levels. How do you recover?

**Answer:** Put cluster in read-only, fix schema, replay missed writes. Keep runbook steps in the incident channel for audit. Explain risk of data loss if shortcuts ship without review. Offer phased rollout with measurable rollback triggers.

#### Q4. Team wants to skip SQL isolation levels to ship faster. Your response?

**Answer:** Pair extra QA time with any isolation level change. Send post-write reads to primary until lag under threshold. Stamp session with last_write_lsn for replica routing if available. Invalidate caches on write path before acknowledging client.

#### Q5. Read replica serves stale data involving SQL isolation levels. Mitigation?

**Answer:** Page if replica lag exceeds minutes for user-facing reads. The next topic in domain seven builds on this foundation. API pagination should use indexed columns for stability. Map SQLSTATE or vendor codes to stable HTTP errors.

### Follow-ups

#### Q1. How does SQL isolation levels connect to the next topic in domain 7?

**Answer:** Emit db.client.operation spans with sanitized statements. Dashboard pool usage, deadlocks, replication lag, and bloat. Shard keys should be chosen before volume makes resharding painful. Index-only scans may still hit the heap when the visibility map is stale.

#### Q2. How does SQL isolation levels connect to API design?

**Answer:** Prepared statements conflict with transaction-level pool modes. Logical dumps differ from physical backups in restore time and PITR. Autovacuum tuning must match update-heavy table churn. Partial indexes shrink size when queries always filter status.

#### Q3. How does SQL isolation levels connect to observability?

**Answer:** Covering indexes trade disk for fewer heap lookups on hot reads. SERIALIZABLE workloads need application retry on serialization failures. Retention documentation belongs in privacy policies and ops runbooks. Document expected query shapes beside every new index in code review.


## L. Practical Exercises

Solutions are in `EXERCISES/solutions/D07-T013.md`. Try these before opening that file.

### Exercise 1

Set isolation for stock decrement.

### Exercise 2

Add retry on serialization failure.

### Exercise 3

Document default per service.

## M. Revision Notes

- Four ANSI levels.
- Postgres RC default.
- RR snapshot.
- Serializable strongest.

## N. Related Topics

Understand this before: `D07-T012`.

This topic supports: `D07-T014`.

Often confused with: adjacent domain-7 topics—read section N of neighbors when unsure.

Interviewers combine this with `D05-T021` pooling and `D07-T023` EXPLAIN.

## O. Completion Criteria

- Pick level for inventory.
- Explain RR vs RC.
- Handle 40001 retry.
- Engine differences.

"""Compact metadata for D15-T001..T034; expanded by d15_expand.py."""
from __future__ import annotations

from typing import TypedDict


class Meta(TypedDict):
    id: str
    slug: str
    name: str
    subdomain: str
    deps: list[str]
    related: list[str]
    confused_with: list[str]
    importance: str
    focus: str
    principles_extra: str
    arch_extra: str
    mermaid: str
    examples: str
    code_file: str
    code: str
    backend: str
    mistakes: list[str]
    debug: str
    trade_row: str
    interview_theme: str
    ex1: str
    ex2: str
    ex3: str
    sol1: str
    sol2: str
    sol3: str


def M(**kwargs) -> Meta:  # type: ignore[no-untyped-def]
    return Meta(**kwargs)  # type: ignore[typeddict-item]


METAS: list[Meta] = [
    M(
        id="D15-T002",
        slug="d15-t002-partial-failures",
        name="Partial failures",
        subdomain="Partial failures",
        deps=["D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002", "D13-T001"],
        related=["D15-T003", "D15-T021"],
        confused_with=["D15-T008", "D13-T007"],
        importance="core",
        focus=(
            "Partial failure means some components fail or slow down while others keep working. "
            "Unlike a total crash, the system enters ambiguous states: half-written workflows, duplicate retries, and clients that cannot tell success from timeout."
        ),
        principles_extra=(
            "Failure is a first-class outcome at every RPC boundary. "
            "A service can fail after doing work but before replying, or fail before work while the client already moved on. "
            "Healthy dependency graphs assume any node can disappear at any time."
        ),
        arch_extra="Instrument each outbound call with result class: success, error, timeout. Persist workflow state between steps.",
        mermaid="""flowchart TD
  req[Request]
  a[ServiceA_ok]
  b[ServiceB_timeout]
  c[ServiceC_ok]
  req --> a
  req --> b
  req --> c
  b --> unknown[UnknownOutcome]""",
        examples="Payment succeeds while notification times out; user sees failure banner but was charged.",
        code_file="d15_t002_partial_result.py",
        code="""
from dataclasses import dataclass
from typing import Literal

Outcome = Literal["ok", "error", "timeout"]


@dataclass
class StepResult:
    name: str
    outcome: Outcome


def aggregate(results: list[StepResult]) -> str:
    if any(r.outcome == "timeout" for r in results):
        return "needs_reconciliation"
    if any(r.outcome == "error" for r in results):
        return "failed"
    return "completed"
""",
        backend="Use sagas or outbox for multi-step flows; never infer global failure from one timeout.",
        mistakes=[
            "Rolling back a local DB transaction when a downstream call timed out (downstream may have committed).",
            "Returning 500 to trigger blind client retries on non-idempotent POST.",
            "Treating health check green as proof all dependencies are usable.",
        ],
        debug="Map each step to committed/unknown/failed; reconcile unknown before compensating.",
        trade_row="Fail fast vs complete partial work | Clear UX | Inconsistent interim state | Money movement | Best-effort analytics",
        interview_theme="partial failure and unknown outcomes",
        ex1="Implement aggregate() and tests for mixed ok/timeout/error.",
        ex2="Order shows failed but wallet debited—list reconciliation steps.",
        ex3="When is returning 202 better than 500 on partial failure?",
        sol1="needs_reconciliation if any timeout; failed if any error without timeout.",
        sol2="Query payment idempotency store, provider API, then fix order state; do not auto-refund on timeout alone.",
        sol3="202 when work continues async and client has poll URL; 500 causes dangerous retries.",
    ),
    M(
        id="D15-T003",
        slug="d15-t003-network-partitions",
        name="Network partitions",
        subdomain="Network partitions",
        deps=["D15-T002", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T004", "D15-T013"],
        confused_with=["D15-T002", "D04-T016"],
        importance="core",
        focus=(
            "A network partition splits nodes into groups that cannot communicate for a period. "
            "Partitions are indistinguishable from slow networks without extra evidence. "
            "Systems must choose whether to refuse writes, accept divergent writes, or elect a single writable side."
        ),
        principles_extra=(
            "TCP may keep a session alive while routing blackholes traffic. "
            "Detection uses timeouts and quorum communication, never a single ping. "
            "Partitions are not rare edge cases at scale; they are continuous at low intensity."
        ),
        arch_extra="Design explicit partition behavior: read-only mode, fence tokens, or majority quorum before writes.",
        mermaid="""flowchart LR
  subgraph sideA [PartitionA]
    n1[Node1]
    n2[Node2]
  end
  subgraph sideB [PartitionB]
    n3[Node3]
  end
  n1 ---x n3
  n2 ---x n3""",
        examples="Two DCs lose link; each thinks the other is down and may promote a primary.",
        code_file="d15_t003_quorum_gate.py",
        code="""
def can_write(reachable_peers: int, total: int) -> bool:
    \"\"\"Majority partition may accept writes; minority should not.\"\"\"
    return reachable_peers * 2 > total
""",
        backend="Multi-AZ clusters use odd member counts and fencing to avoid dual writers.",
        mistakes=[
            "Assuming split-brain cannot happen with 'good networking'.",
            "Using a single coordinator without quorum for write acceptance.",
            "Ignoring asymmetric partitions (A can reach B but not vice versa).",
        ],
        debug="Compare membership views from both sides; look for divergent epoch numbers.",
        trade_row="Availability during partition | Keep serving | Risk split brain | Read-heavy | Financial writes",
        interview_theme="network partition detection and write policy",
        ex1="Implement can_write for odd N and document minority behavior.",
        ex2="Both sites claim primary after link flap—what evidence do you collect?",
        ex3="CP vs AP during partition for a shopping cart—justify.",
        sol1="Majority: reachable*2>total; minority rejects writes.",
        sol2="Epoch/term, last committed log index, fencing tokens, who holds quorum.",
        sol3="Cart can be AP with merge; payment authorization should be CP or use external authority.",
    ),
    M(
        id="D15-T004",
        slug="d15-t004-cap-theorem",
        name="CAP theorem",
        subdomain="CAP theorem",
        deps=["D15-T003", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T005", "D15-T006"],
        confused_with=["D15-T005", "D07-T012"],
        importance="core",
        focus=(
            "The CAP theorem (Gilbert and Lynch, 2002) models asynchronous networks with crash failures. "
            "When a partition occurs, a linearizable read/write register cannot be both available (every request gets a response) and consistent (linearizable) at the same time. "
            "It is not a menu to 'pick two of three' for all time—when there is no partition, C and A can both hold. "
            "Interview precision: C here is linearizability (atomic consistency), not every informal use of 'consistent'."
        ),
        principles_extra=(
            "Availability in the proof means every non-failing node completes operations in bounded time during a partition. "
            "Consistency means responses reflect a single total order of operations as if on one register. "
            "Real systems slide along the trade-off with quorums, leases, and tunable consistency."
        ),
        arch_extra="Document behavior during partition: reject writes, serve stale reads, or route to majority partition only.",
        mermaid="""flowchart TD
  normal[NoPartition]
  part[PartitionEvent]
  cp[ChooseCP_RejectMinority]
  ap[ChooseAP_StaleOrDivergent]
  normal --> part
  part --> cp
  part --> ap""",
        examples="During partition, a CP store may return errors to preserve linearizability; an AP cache may serve old values.",
        code_file="d15_t004_cap_mode.py",
        code="""
def handle_write(partition: bool, has_quorum: bool, policy: str) -> str:
    if not partition:
        return "accept"
    if policy == "CP":
        return "accept" if has_quorum else "reject"
    if policy == "AP":
        return "accept"
    raise ValueError("unknown policy")
""",
        backend="Label services CP/AP per operation, not per entire product. Payments CP; feature flags may be AP.",
        mistakes=[
            "Claiming CAP proves databases cannot scale.",
            "Equating C with ACID C in isolation levels.",
            "Ignoring that partitions are about inability to communicate, not merely high latency.",
        ],
        debug="During incident, ask: are we partitioned or just slow? Check quorum reachability.",
        trade_row="CP during split | Strong correctness | Unavailable minority | Ledger | Social likes",
        interview_theme="CAP during partition only",
        ex1="Implement handle_write for CP/AP policies.",
        ex2="Interviewer says 'we chose AP so we are always consistent'—correct them.",
        ex3="Classify primary-replica DB failover as CP or AP during split.",
        sol1="CP rejects without quorum; AP accepts on all sides (divergence risk).",
        sol2="AP does not guarantee linearizability during partition; eventual consistency may apply.",
        sol3="Depends on fencing: unfenced dual primary is AP/dangerous; quorum+fencing trends CP.",
    ),
    M(
        id="D15-T005",
        slug="d15-t005-pacelc-theorem",
        name="PACELC theorem",
        subdomain="PACELC theorem",
        deps=["D15-T004", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T006", "D15-T009"],
        confused_with=["D15-T004", "D15-T007"],
        importance="advanced",
        focus=(
            "PACELC extends CAP: if Partition then choose Availability or Consistency (PA/ELC); Else (normal operation) choose Latency or Consistency. "
            "Most user-visible trade-offs happen without a partition—replication lag vs fast reads is an LC tension. "
            "It is a framework for describing systems, not a formal impossibility result like Gilbert-Lynch CAP."
        ),
        principles_extra=(
            "Many databases offer tunable consistency: stronger reads cost RTT to a quorum. "
            "PACELC reminds you to discuss both partition behavior and steady-state replication lag."
        ),
        arch_extra="Expose consistency knobs per query (R/W quorum, read concern) and measure lag.",
        mermaid="""flowchart TD
  op[ClientOperation]
  part{Partition?}
  pac[PA_or_PC]
  elc[Latency_or_Consistency]
  op --> part
  part -->|yes| pac
  part -->|no| elc""",
        examples="Cassandra: PA/EL by default; strong reads add latency via QUORUM.",
        code_file="d15_t005_read_policy.py",
        code="""
def read_replicas(policy: str, lag_ms: float, max_lag: float) -> str:
    if policy == "low_latency":
        return "any_replica"
    if policy == "consistent" and lag_ms <= max_lag:
        return "quorum"
    return "primary_only"
""",
        backend="SLAs should state both partition behavior and p99 read staleness bounds.",
        mistakes=[
            "Using PACELC to claim CAP is wrong—it refines the conversation.",
            "Ignoring EL when marketing 'strongly consistent' with async replication.",
        ],
        debug="Plot replication lag vs read policy errors.",
        trade_row="Low latency reads | Fast UX | Stale data | Dashboards | Bank balance",
        interview_theme="PACELC Else branch latency vs consistency",
        ex1="Implement read_replicas with lag guard.",
        ex2="p99 read latency improved but users see stale inventory—map to PACELC.",
        ex3="When is PA/EL appropriate for notifications?",
        sol1="consistent path waits for lag bound or primary.",
        sol2="Chose EL in normal case; tighten read concern or route to primary for hot SKUs.",
        sol3="Notifications tolerate lag; inventory for purchase needs LC toward consistency.",
    ),
    M(
        id="D15-T006",
        slug="d15-t006-strong-eventual-and-causal-consistency",
        name="Strong, eventual and causal consistency",
        subdomain="Strong, eventual and causal consistency",
        deps=["D15-T005", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T007", "D15-T009"],
        confused_with=["D15-T007", "D07-T013"],
        importance="core",
        focus=(
            "Consistency models describe what reads are allowed to return relative to writes. "
            "Strong (often linearizable) guarantees behave like a single copy in real time. "
            "Eventual consistency promises convergence if writes stop, not a bound on staleness. "
            "Causal consistency preserves cause-effect order (read-your-writes, related events) without full global linearization."
        ),
        principles_extra="Pick the weakest model that preserves product invariants; stronger models cost latency and availability during faults.",
        arch_extra="Tag operations with consistency level; route strong reads to leader or quorum.",
        mermaid="""flowchart LR
  w[Write]
  r1[ReadStrong]
  r2[ReadEventual]
  w --> r1
  w -. may lag .-> r2""",
        examples="Social feed eventual; bank balance strong; session cart causal.",
        code_file="d15_t006_consistency_level.py",
        code="""
def route_read(level: str, role: str) -> str:
    if level == "strong":
        return "primary"
    if level == "causal":
        return "primary_if_session_token else replica_with_token"
    return "any_replica"
""",
        backend="Document per-endpoint consistency; do not claim strong if replication is async.",
        mistakes=["Calling async replication 'strong'.", "Ignoring monotonic reads for UX."],
        debug="Measure staleness windows; compare primary vs replica read.",
        trade_row="Eventual reads | Low latency | Stale UI | Feeds | Inventory checkout",
        interview_theme="consistency model selection",
        ex1="Implement route_read for three levels.",
        ex2="Users never see their own post—what consistency broke?",
        ex3="Choose model for 'like count' vs 'password change'.",
        sol1="strong→primary; causal needs session stickiness.",
        sol2="Missing read-your-writes / causal session routing.",
        sol3="Likes eventual; password strong on primary with invalidation.",
    ),
    M(
        id="D15-T007",
        slug="d15-t007-linearizability-and-sequential-consistency",
        name="Linearizability and sequential consistency",
        subdomain="Linearizability and sequential consistency",
        deps=["D15-T006", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T012", "D15-T004"],
        confused_with=["D15-T006", "D07-T013"],
        importance="advanced",
        focus=(
            "Linearizability requires each operation to appear to take effect atomically at some point between its invocation and response, "
            "and the global history respects real-time ordering. "
            "Sequential consistency only requires a single sequential order agreed by all nodes, but that order need not respect real-time "
            "(a slow reader may see an old value even after a faster client finished a write). "
            "Linearizability is strictly stronger than sequential consistency for register histories."
        ),
        principles_extra="CAP 'C' in Gilbert-Lynch is linearizability. Do not equate either term with database isolation levels without mapping.",
        arch_extra="Leader-based replication with synchronous commit to a quorum approximates linearizable writes; reads may need quorum too.",
        mermaid="""sequenceDiagram
  participant C1 as Client1
  participant C2 as Client2
  participant S as Store
  C1->>S: write(x=1)
  C1-->>C1: ok
  C2->>S: read(x)
  Note over C2,S: Linearizable: must see 1""",
        examples="Compare-and-swap on a leader is often linearizable; multi-leader without coordination is not.",
        code_file="d15_t007_history.py",
        code="""
def is_sequential_order(ops: list[tuple[str, str]]) -> bool:
    \"\"\"ops: list of (op, value_seen) for single register; toy checker.\"\"\"
    return len(ops) >= 1
""",
        backend="Use linearizability language only when you can point to coordination (leader, quorum, fencing).",
        mistakes=["Saying 'sequential consistency is good enough for everything'.", "Confusing linearizability with serializability in SQL."],
        debug="Litmus-style tests: write by C1 then read by C2 should see write if linearizable.",
        trade_row="Linearizable ops | Simple mental model | Higher latency | Locks/inventory | Analytics replicas",
        interview_theme="linearizability vs sequential consistency",
        ex1="Explain litmus test w(x) r(x) for both models.",
        ex2="System is sequentially consistent but not linearizable—give a timeline.",
        ex3="Does Raft leader commit imply linearizable reads?",
        sol1="Linearizable: r must return 1 after w ack; sequential may reorder real-time.",
        sol2="C2 reads before C1 write visible despite real-time order.",
        sol3="Committed writes yes if reads go through leader/quorum; stale follower reads break linearizability.",
    ),
    M(
        id="D15-T008",
        slug="d15-t008-availability-and-fault-tolerance",
        name="Availability and fault tolerance",
        subdomain="Availability and fault tolerance",
        deps=["D15-T007", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T025", "D15-T010"],
        confused_with=["D15-T002", "D05-T023"],
        importance="core",
        focus="Availability is the fraction of time a system correctly serves requests; fault tolerance is the ability to continue despite faults. They require redundancy, failover, and graceful degradation—not infinite retries.",
        principles_extra="Define 'correctly' (degraded mode may exclude some features). SLOs use successful responses over window, not ping.",
        arch_extra="N+1 capacity, health checks, automated failover, chaos testing.",
        mermaid="""flowchart TD
  users[Users]
  active[ActiveRegion]
  standby[StandbyRegion]
  users --> active
  active -. failover .-> standby""",
        examples="99.9% allows ~43m downtime/month; plan maintenance within error budget.",
        code_file="d15_t008_slo.py",
        code="""
def within_budget(errors: int, total: int, budget: float) -> bool:
    return total > 0 and (errors / total) <= budget
""",
        backend="Pair HA with idempotency and data durability; uptime without correctness is worthless.",
        mistakes=["Equating load balancer up with app healthy.", "No error budget policy."],
        debug="Split availability by dependency; blame analysis per hop.",
        trade_row="Active-active | Max uptime | Split brain risk | Global read | Single-writer data",
        interview_theme="availability SLOs and redundancy",
        ex1="Compute if 15 errors in 100k requests meets 99.95% budget.",
        ex2="Site up but checkout down—availability metric?",
        ex3="When is active-active worth split-brain risk?",
        sol1="0.015% error < 0.05% budget → within.",
        sol2="Feature-level SLO failed though ping succeeds.",
        sol3="Read-heavy multi-region; not for unfenced dual writes.",
    ),
    M(
        id="D15-T009",
        slug="d15-t009-replication-strategies",
        name="Replication strategies",
        subdomain="Replication strategies",
        deps=["D15-T008", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T010", "D15-T012"],
        confused_with=["D15-T031", "D07-T019"],
        importance="core",
        focus="Replication copies data for durability and read scale. Sync replication waits for followers before ack; async acks early and risks loss on primary failure. Multi-leader increases write availability but complicates conflicts.",
        principles_extra="Replication is not backup unless you can restore independently; lag is a consistency knob.",
        arch_extra="Binlog/WAL shipping, chain replication, quorum replication.",
        mermaid="""flowchart LR
  primary[Primary]
  syncF[SyncReplica]
  asyncF[AsyncReplica]
  primary --> syncF
  primary -.-> asyncF""",
        examples="Postgres streaming replication async by default; sync replicas for RPO≈0.",
        code_file="d15_t009_ack.py",
        code="""
def client_visible_commit(sync_acks: int, required: int) -> bool:
    return sync_acks >= required
""",
        backend="State RPO/RTO; monitor replication lag alarms.",
        mistakes=["Assuming replica read is always fresh.", "No plan when lag unbounded."],
        debug="Compare LSN/offset on primary vs replica.",
        trade_row="Async replication | Fast writes | Data loss window | Most OLTP | Zero RPO needs",
        interview_theme="sync vs async replication",
        ex1="Implement client_visible_commit.",
        ex2="Failover loses last 30s writes—sync or async?",
        ex3="When add read replicas vs shards?",
        sol1="True when acks meet required sync count.",
        sol2="Async; sync would need quorum ack before commit.",
        sol3="Replicas for read scale; shard when single primary CPU/IO maxed.",
    ),
    M(
        id="D15-T010",
        slug="d15-t010-leader-follower-architecture",
        name="Leader-follower architecture",
        subdomain="Leader-follower architecture",
        deps=["D15-T009", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T011", "D15-T014"],
        confused_with=["D15-T011", "D15-T009"],
        importance="core",
        focus="A single leader orders writes; followers apply the log. Reads may hit followers for scale but risk staleness unless routed carefully. Failover promotes a follower when leader is deemed dead.",
        principles_extra="Leadership is a safety property: at most one leader epoch should accept writes if fencing works.",
        arch_extra="Log replication, commit index, snapshot shipping.",
        mermaid="""flowchart TD
  leader[Leader]
  f1[Follower1]
  f2[Follower2]
  leader --> f1
  leader --> f2""",
        examples="MySQL primary/replica; Kafka partition leader.",
        code_file="d15_t010_write_path.py",
        code="""
def accept_write(is_leader: bool, fenced: bool) -> bool:
    return is_leader and fenced
""",
        backend="Route writes to leader; use follower reads with lag bounds for dashboards only.",
        mistakes=["Writing to follower 'just once'.", "Failover without epoch bump."],
        debug="Check role, term, replication lag on write errors.",
        trade_row="Follower reads | Scale reads | Stale | Reports | Session cart after write",
        interview_theme="leader-follower write routing",
        ex1="Implement accept_write with fencing flag.",
        ex2="Split writes between leader and replica—symptoms?",
        ex3="Sticky sessions vs leader reads for read-your-writes.",
        sol1="Requires leader and valid fence token.",
        sol2="Divergent data, lost updates, replication conflicts.",
        sol3="Route session reads to leader or track commit index.",
    ),
    M(
        id="D15-T011",
        slug="d15-t011-leader-election",
        name="Leader election",
        subdomain="Leader election",
        deps=["D15-T010", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T014", "D15-T027"],
        confused_with=["D15-T010", "D15-T015"],
        importance="core",
        focus="Leader election picks one coordinator among peers. Practical systems use timeouts, epochs, and votes (Raft, ZooKeeper ephemeral nodes). Election must tolerate split votes and ensure safety via majority.",
        principles_extra="Election is liveness; fencing/epochs are safety during failover.",
        arch_extra="Campaign, vote, grant term, heartbeat to maintain leadership.",
        mermaid="""stateDiagram-v2
  [*] --> Follower
  Follower --> Candidate: election timeout
  Candidate --> Leader: majority votes
  Candidate --> Follower: discover higher term
  Leader --> Follower: discover higher term""",
        examples="etcd Raft election; old leader must step down on higher term.",
        code_file="d15_t011_vote.py",
        code="""
def grant_vote(candidate_term: int, my_term: int, voted: bool) -> bool:
    return candidate_term > my_term and not voted
""",
        backend="Run odd-sized voter sets; avoid manual 'force primary' without quorum.",
        mistakes=["Two leaders after network heal without fencing.", "Election storms from too-low timeouts."],
        debug="Graph terms over time; correlate with GC pauses.",
        trade_row="Fast election | Quick failover | Flapping | Small clusters | JVM with long GC",
        interview_theme="leader election safety and terms",
        ex1="Implement grant_vote rules.",
        ex2="Flapping leadership—causes?",
        ex3="Difference election vs distributed lock.",
        sol1="Vote once per term if candidate term higher.",
        sol2="Too-aggressive timeouts, asymmetric partition, clock not required but delay matters.",
        sol3="Election picks writer; lock serializes workers with lease.",
    ),
    M(
        id="D15-T012",
        slug="d15-t012-quorum-reads-and-writes",
        name="Quorum reads and writes",
        subdomain="Quorum reads and writes",
        deps=["D15-T011", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T009", "D15-T007"],
        confused_with=["D15-T010", "D15-T004"],
        importance="core",
        focus=(
            "Quorum systems use N replicas with write quorum W and read quorum R. "
            "If W + R > N, intersecting quorums overlap so a read sees latest write (classic Dynamo-style argument for versioned values). "
            "Sloppy quorums and hinted handoff relax strict quorums for availability. "
            "Tunable R/W trades latency versus staleness."
        ),
        principles_extra="Use version vectors or timestamps to resolve concurrent writes; quorum does not erase conflicts in multi-writer models.",
        arch_extra="Coordinator sends parallel requests; wait for W or R acks.",
        mermaid="""flowchart TD
  c[Coordinator]
  n1[Replica1]
  n2[Replica2]
  n3[Replica3]
  c --> n1
  c --> n2
  c --> n3""",
        examples="Cassandra ONE/QUORUM/ALL; W=2,R=2,N=3 strong for single writer per key if coordinated.",
        code_file="d15_t012_quorum.py",
        code="""
def strong_intersection(n: int, w: int, r: int) -> bool:
    return w + r > n
""",
        backend="Pick W/R per operation; document allowed staleness for reads at ONE.",
        mistakes=["Assuming quorum without version merge handles all conflicts.", "W+R≤N and expecting strong reads."],
        debug="Check per-replica versions on divergent read results.",
        trade_row="W=1 | Fast writes | Weak | Counters | Financial ledger",
        interview_theme="quorum W+R>N",
        ex1="Given N=5, find W,R for strong intersection.",
        ex2="Read returns two versions—next step?",
        ex3="When is sloppy quorum acceptable?",
        sol1="e.g. W=3,R=3 gives 6>5.",
        sol2="Read repair or application merge using version vector.",
        sol3="Degraded availability with eventual repair—not for strict invariants.",
    ),
    M(
        id="D15-T013",
        slug="d15-t013-split-brain-scenarios",
        name="Split-brain scenarios",
        subdomain="Split-brain scenarios",
        deps=["D15-T012", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T033", "D15-T003"],
        confused_with=["D15-T003", "D15-T011"],
        importance="core",
        focus="Split-brain is two or more nodes believing they are the active writer, causing divergent data. It follows partitions plus misconfigured failover or lack of fencing.",
        principles_extra="Prevention beats cure: quorum, STONITH/fencing, shared witness, or external coordinator.",
        arch_extra="Epoch numbers on storage; reject writes from old epoch.",
        mermaid="""flowchart LR
  a[SiteA_Primary]
  b[SiteB_Primary]
  a ---x b
  a --> dataA[(DataA)]
  b --> dataB[(DataB)]""",
        examples="DR drill promotes secondary while primary alive.",
        code_file="d15_t013_epoch.py",
        code="""
def allow_write(epoch: int, current_epoch: int) -> bool:
    return epoch == current_epoch
""",
        backend="Automate failover with quorum; ban manual dual-primary.",
        mistakes=["DNS flip without data reconciliation.", "Ignoring object store fencing."],
        debug="Compare write epochs and binlog positions both sides.",
        trade_row="Manual failover | Human judgment | Human error | Tiny teams | Regulated HA",
        interview_theme="split-brain divergence",
        ex1="Implement epoch gate.",
        ex2="Two primaries after partition—merge strategy?",
        ex3="Witness node role in 2-node DC pair.",
        sol1="Only latest epoch writes accepted.",
        sol2="Pick winner by epoch/data loss policy; reconcile divergent rows.",
        sol3="Break tie for quorum; not a data node.",
    ),
    M(
        id="D15-T014",
        slug="d15-t014-consensus-raft-and-paxos-concepts",
        name="Consensus: Raft and Paxos concepts",
        subdomain="Consensus: Raft and Paxos concepts",
        deps=["D15-T013", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T011", "D15-T010"],
        confused_with=["D15-T029", "D15-T011"],
        importance="advanced",
        focus=(
            "Consensus agrees on a single ordered log of values despite failures. "
            "Paxos is the classic family of protocols; Raft decomposes leader election, log replication, and safety with terms. "
            "At concept level: a leader appends entries; followers replicate; commits advance when majority persist. "
            "Raft ensures safety (no two leaders in same term) and eventual consistency of logs under partial connectivity."
        ),
        principles_extra="Consensus is for coordination metadata and replicated state machines, not a substitute for application sagas across heterogeneous DBs.",
        arch_extra="State machine apply at same index; snapshot + log compaction.",
        mermaid="""sequenceDiagram
  participant L as Leader
  participant F as Follower
  L->>F: AppendEntries term=5 index=10
  F-->>L: success
  Note over L: commit index 10 after majority""",
        examples="etcd/consul use Raft; Spanner uses Paxos variants at scale.",
        code_file="d15_t014_commit.py",
        code="""
def committed(acks: int, cluster_size: int) -> bool:
    return acks * 2 > cluster_size
""",
        backend="Use off-the-shelf consensus for locks/config; avoid homegrown Raft.",
        mistakes=["Claiming Raft gives cross-service transactions.", "Ignoring leader election on membership change."],
        debug="Dump raft log indices, term, commitIndex on incidents.",
        trade_row="Embedded Raft | Strong metadata | Ops complexity | Coordination | Simple CRUD app",
        interview_theme="Raft log replication at concept level",
        ex1="When is entry committed in Raft?",
        ex2="Leader partitioned with one follower—can it commit?",
        ex3="Raft vs 2PC use cases.",
        sol1="Majority replicated same index in current term.",
        sol2="Only if majority of cluster reachable; minority partition cannot commit new entries.",
        sol3="Raft replicates log on homogeneous cluster; 2PC coordinates external resources.",
    ),
    M(
        id="D15-T015",
        slug="d15-t015-distributed-locking",
        name="Distributed locking",
        subdomain="Distributed locking",
        deps=["D15-T014", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T011", "D15-T019"],
        confused_with=["D03-T005", "D15-T011"],
        importance="core",
        focus="Distributed locks serialize work across nodes using a coordination service with leases and fencing tokens. Locks must expire if holder dies; fencing prevents stale holders from writing after release.",
        principles_extra="A lock without fencing is unsafe under GC pause or long stop-the-world.",
        arch_extra="Acquire lease, store fence token in DB, reject lower tokens.",
        mermaid="""flowchart TD
  worker[Worker]
  zk[(Coordination)]
  db[(Database)]
  worker --> zk
  worker --> db""",
        examples="Redlock is debated; prefer consensus-backed locks with fencing for correctness-critical paths.",
        code_file="d15_t015_fence.py",
        code="""
def write_allowed(fence: int, max_fence: int) -> bool:
    return fence >= max_fence
""",
        backend="Prefer idempotent design over global locks; short lease + renew heartbeat.",
        mistakes=["Lock without TTL.", "Using wall clock only for lease."],
        debug="Log fence monotonicity violations.",
        trade_row="Coarse lock | Simple | Low throughput | Batch jobs | Hot key inventory",
        interview_theme="fencing tokens with locks",
        ex1="Implement write_allowed.",
        ex2="Holder paused by GC—what breaks without fencing?",
        ex3="Lock vs database row FOR UPDATE.",
        sol1="Reject writes with fence < stored max.",
        sol2="Stale holder may write after lease expired; fencing blocks it.",
        sol3="Row lock is local DB; dist lock crosses services.",
    ),
    M(
        id="D15-T016",
        slug="d15-t016-clock-skew-and-clock-synchronization",
        name="Clock skew and clock synchronization",
        subdomain="Clock skew and clock synchronization",
        deps=["D15-T015", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T017", "D15-T020"],
        confused_with=["D15-T017", "D13-T022"],
        importance="core",
        focus="Wall clocks drift and jump (NTP step). Never use unsynchronized time as causal order across nodes. Use logical clocks or centralized timestamps (TrueTime-style) when ordering matters.",
        principles_extra="Lease expiry based on local clock can disagree across machines.",
        arch_extra="Run chrony/NTP; monitor skew; prefer monotonic clocks for durations.",
        mermaid="""flowchart LR
  n1[Node1_clock]
  n2[Node2_clock]
  n1 -. skew .- n2""",
        examples="TTL token appears expired on server with fast clock.",
        code_file="d15_t016_skew.py",
        code="""
def lease_valid(now: float, expires: float, skew_margin: float) -> bool:
    return now + skew_margin < expires
""",
        backend="Add skew margin to lease checks; use DB time for expirations when possible.",
        mistakes=["Ordering events by created_at across regions.", "Ignoring leap seconds/smearing policies."],
        debug="Compare offset metrics across fleet.",
        trade_row="NTP sync | Comparable timestamps | Misconfig spikes | Logging | Distributed ordering",
        interview_theme="clock skew and leases",
        ex1="Implement lease_valid with margin.",
        ex2="Events out of order in logs—clock or logic?",
        ex3="Why Spanner uses TrueTime bounds.",
        sol1="Margin absorbs fast-clock client.",
        sol2="Check skew; may need logical clocks.",
        sol3="To assign global timestamps with uncertainty interval.",
    ),
    M(
        id="D15-T017",
        slug="d15-t017-logical-clocks-and-vector-clocks",
        name="Logical clocks and vector clocks",
        subdomain="Logical clocks and vector clocks",
        deps=["D15-T016", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T006", "D15-T012"],
        confused_with=["D15-T016", "D15-T006"],
        importance="advanced",
        focus="Lamport clocks give a partial order via counters; vector clocks track per-node counts to detect concurrency. They help version merges and causal metadata without trusting wall time.",
        principles_extra="Logical time does not measure latency; it captures happened-before.",
        arch_extra="Attach version vectors to records for read-repair and CRDT merges.",
        mermaid="""flowchart TD
  e1[EventA]
  e2[EventB]
  e3[EventC]
  e1 --> e3
  e2 --> e3""",
        examples="Dynamo-style version reconciliation on read.",
        code_file="d15_t017_lamport.py",
        code="""
def lamport_tick(local: int, received: int) -> int:
    return max(local, received) + 1
""",
        backend="Store versions on writes; merge on conflict with deterministic rule.",
        mistakes=["Thinking Lamport total-orders concurrent events.", "Huge vectors at planet scale without compaction."],
        debug="Dump conflicting versions on divergent reads.",
        trade_row="Vector metadata | Detect concurrency | Size | Quorum stores | Single-leader log",
        interview_theme="logical vs wall-clock ordering",
        ex1="Apply lamport_tick on message receive.",
        ex2="Two concurrent writes—vector clock result?",
        ex3="When Lamport enough vs vector needed.",
        sol1="max(local,received)+1.",
        sol2="Neither dominates; concurrent siblings.",
        sol3="Lamport for tie-break; vector to detect concurrency.",
    ),
    M(
        id="D15-T018",
        slug="d15-t018-at-most-once-and-at-least-once-execution",
        name="At-most-once and at-least-once execution",
        subdomain="At-most-once and at-least-once execution",
        deps=["D15-T017", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T019", "D15-T020"],
        confused_with=["D15-T020", "D14-T028"],
        importance="core",
        focus="At-most-once avoids duplicates by not retrying (may lose work). At-least-once retries until ack (may duplicate). Networks force most systems to at-least-once unless dropping on failure.",
        principles_extra="Ack boundaries define delivery semantics end-to-end.",
        arch_extra="Consumer offsets, visibility timeout, dedup store.",
        mermaid="""flowchart LR
  prod[Producer]
  broker[Broker]
  cons[Consumer]
  prod --> broker --> cons""",
        examples="Kafka consumers commit offset after processing → at-least-once if crash before commit.",
        code_file="d15_t018_delivery.py",
        code="""
def deliver(mode: str, retry: bool) -> str:
    if mode == "at_most_once":
        return "no_retry"
    if mode == "at_least_once" and retry:
        return "retry_until_ack"
    return "unknown"
""",
        backend="Pair at-least-once with idempotent handlers.",
        mistakes=["Assuming TCP gives message exactly-once.", "Committing offset before side effects."],
        debug="Count duplicate business keys in warehouse.",
        trade_row="At-most-once | No dupes | Loss | Metrics | Payments",
        interview_theme="delivery semantics",
        ex1="Map Kafka consumer settings to semantics.",
        ex2="Duplicate emails after crash—fix?",
        ex3="When accept message loss.",
        sol1="Process then commit offset; retry on failure → at-least-once.",
        sol2="Idempotent send keyed by message id; commit after persist.",
        sol3="Low-value telemetry, not money.",
    ),
    M(
        id="D15-T019",
        slug="d15-t019-idempotency",
        name="Idempotency",
        subdomain="Idempotency",
        deps=["D15-T018", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D06-T011", "D15-T020"],
        confused_with=["D06-T007", "D15-T018"],
        importance="core",
        focus="An idempotent operation can be applied multiple times without changing outcome beyond the first successful application. Idempotency keys let safe retries after timeouts.",
        principles_extra="Store key→result with TTL; return same response for duplicates.",
        arch_extra="DB unique constraint on idempotency key; outbox pattern.",
        mermaid="""flowchart TD
  client[Client]
  api[API]
  store[(IdempotencyStore)]
  client --> api --> store""",
        examples="Stripe idempotency-key header on POST /charges.",
        code_file="d15_t019_idem.py",
        code="""
def process(key: str, seen: dict[str, str], body: str) -> str:
    if key in seen:
        return seen[key]
    seen[key] = f"ok:{body}"
    return seen[key]
""",
        backend="Require keys on non-safe methods; scope per user/account.",
        mistakes=["Keys only in memory per instance.", "Reusing keys across different operations."],
        debug="Find duplicate keys with different payloads.",
        trade_row="DB dedup | Strong | Storage/latency | Payments | Read-only GET",
        interview_theme="idempotency keys",
        ex1="Implement process() with in-memory store.",
        ex2="Double charge same key different amounts—bug?",
        ex3="TTL for idempotency records.",
        sol1="Return cached result for key.",
        sol2="Yes—should reject payload mismatch.",
        sol3="Long enough for client retry window (24-72h).",
    ),
    M(
        id="D15-T020",
        slug="d15-t020-exactly-once-processing-limitations",
        name="Exactly-once processing limitations",
        subdomain="Exactly-once processing limitations",
        deps=["D15-T019", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T018", "D15-T030"],
        confused_with=["D15-T018", "D14-T030"],
        importance="advanced",
        focus=(
            "True exactly-once end-to-end across heterogeneous systems is not achievable with only asynchronous messaging under failures. "
            "Engineering achieves exactly-once *effects* via idempotent consumers, transactional outbox, and deduplication with atomic write of offset+effect. "
            "Kafka 'exactly-once' is scoped to broker transactions between producers/consumers, not your entire business workflow."
        ),
        principles_extra="Name the boundary where semantics are defined (broker vs application vs database).",
        arch_extra="Atomic: mark processed + apply business write in one transaction.",
        mermaid="""flowchart TD
  msg[Message]
  tx[DBTransaction]
  msg --> tx
  tx --> effect[BusinessEffect]
  tx --> offset[OffsetMark]""",
        examples="Flink checkpointing; still needs idempotent sinks.",
        code_file="d15_t020_atomic.py",
        code="""
def handle(msg_id: str, processed: set[str], apply) -> None:
    if msg_id in processed:
        return
    apply()
    processed.add(msg_id)
""",
        backend="Sell stakeholders 'effectively once' with provable dedup, not magic middleware.",
        mistakes=["Marketing exactly-once without defining failure model.", "Side effect outside transaction."],
        debug="Reprocess log segment; count duplicate side effects.",
        trade_row="Transactional outbox | Strong effects | Complexity | Billing | Fire-and-forget logs",
        interview_theme="exactly-once effect boundaries",
        ex1="Why two-phase commit alone ≠ exactly-once across services.",
        ex2="Kafka EOS still duplicates at sink—why?",
        ex3="Design idempotent payment sink.",
        sol1="2PC blocks and does not cover external systems without all participants transactional.",
        sol2="Sink not transactional with consumer offset.",
        sol3="Unique business key + ledger insert in one DB tx.",
    ),
    M(
        id="D15-T021",
        slug="d15-t021-retries-timeouts-and-exponential-backoff",
        name="Retries, timeouts and exponential backoff",
        subdomain="Retries, timeouts and exponential backoff",
        deps=["D15-T020", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T022", "D15-T023"],
        confused_with=["D15-T022", "D13-T024"],
        importance="core",
        focus="Retries convert transient failures into success but amplify load. Exponential backoff spaces attempts; caps prevent unbounded delay. Timeouts bound waiting and define when retry is allowed.",
        principles_extra="Retry only idempotent or keyed operations; classify errors as retryable vs fatal.",
        arch_extra="Client-side retry budgets; server-side rate limits.",
        mermaid="""flowchart TD
  call[RPC]
  timeout{Timeout?}
  retry[BackoffRetry]
  call --> timeout
  timeout -->|yes retryable| retry
  retry --> call""",
        examples="AWS SDK default backoff with max attempts.",
        code_file="d15_t021_backoff.py",
        code="""
def backoff(attempt: int, base: float, cap: float) -> float:
    return min(cap, base * (2 ** attempt))
""",
        backend="Set deadline per request tree; subtract child latency from parent budget.",
        mistakes=["Retrying 500 on POST without idempotency.", "Infinite retries on overload."],
        debug="Metric: retry count per endpoint; correlate with saturation.",
        trade_row="Aggressive retry | Higher success | Retry storm | Idempotent reads | Overloaded payment API",
        interview_theme="retry with backoff and budgets",
        ex1="Compute backoff attempts 0-3 with base=0.1 cap=2.",
        ex2="Latency SLO blown by retries—fix?",
        ex3="Retry on 429 vs 503.",
        sol1="0.1,0.2,0.4,0.8.",
        sol2="Reduce max attempts, add jitter, fix root capacity.",
        sol3="429 respect Retry-After; 503 maybe with backoff if idempotent.",
    ),
    M(
        id="D15-T022",
        slug="d15-t022-jitter-and-retry-storms",
        name="Jitter and retry storms",
        subdomain="Jitter and retry storms",
        deps=["D15-T021", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T023", "D15-T021"],
        confused_with=["D15-T021", "D13-T024"],
        importance="core",
        focus="Synchronized retries align in time and create thundering herds. Full jitter randomizes delay in [0, backoff] to spread load. Retry storms can take down a recovering service.",
        principles_extra="Decorate retry metrics; alert when retry fraction spikes.",
        arch_extra="Combine exponential backoff with equal or full jitter per AWS architecture guidance.",
        mermaid="""flowchart TD
  many[ManyClients]
  spike[AlignedRetrySpike]
  svc[RecoveringService]
  many --> spike --> svc""",
        examples="All clients retry at 1s after outage ends → second outage.",
        code_file="d15_t022_jitter.py",
        code="""
import random

def delay_with_full_jitter(attempt: int, base: float, cap: float) -> float:
    bound = min(cap, base * (2 ** attempt))
    return random.uniform(0, bound)
""",
        backend="Server shed load with 503 + Retry-After; client honors jitter.",
        mistakes=["Fixed retry interval for all instances.", "No max concurrency on client retries."],
        debug="Plot retry timestamps—look for periodic spikes.",
        trade_row="Full jitter | Spreads load | Less predictable latency | Large fleets | Tiny single client",
        interview_theme="jitter preventing retry storms",
        ex1="Compare aligned vs jittered retry timeline.",
        ex2="Service recovers then dies at T+1s—explain.",
        ex3="Equal vs full jitter trade-off.",
        sol1="Aligned peaks; jitter spreads attempts.",
        sol2="Classic retry storm on synchronized backoff.",
        sol3="Full jitter more spread; equal jitter tighter bound.",
    ),
    M(
        id="D15-T023",
        slug="d15-t023-circuit-breakers",
        name="Circuit breakers",
        subdomain="Circuit breakers",
        deps=["D15-T022", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T024", "D15-T021"],
        confused_with=["D15-T024", "D04-T014"],
        importance="core",
        focus="Circuit breakers stop calls to a failing dependency after error threshold, fail fast while open, then probe in half-open. They protect caller resources; they do not repair the downstream.",
        principles_extra="Breakers complement timeouts/retries; configure per dependency.",
        arch_extra="States: closed, open, half-open; sliding window error rate.",
        mermaid="""stateDiagram-v2
  [*] --> Closed
  Closed --> Open: error threshold
  Open --> HalfOpen: timeout elapsed
  HalfOpen --> Closed: probe success
  HalfOpen --> Open: probe fail""",
        examples="Hystrix / resilience4j patterns in JVM services.",
        code_file="d15_t023_breaker.py",
        code="""
class Breaker:
    def __init__(self):
        self.state = "closed"
        self.failures = 0

    def record_failure(self, threshold: int) -> None:
        self.failures += 1
        if self.failures >= threshold:
            self.state = "open"
""",
        backend="Return fallback or cached response when open; surface degradation clearly.",
        mistakes=["Breaker on wrong metric (latency vs errors).", "Shared breaker across unrelated deps."],
        debug="Log state transitions with dependency name.",
        trade_row="Open circuit | Saves threads | User impact | Cascading failure risk | Optional features",
        interview_theme="circuit breaker states",
        ex1="Implement state transitions on failures/success.",
        ex2="Breaker open but dependency healthy—causes?",
        ex3="Breaker vs bulkhead.",
        sol1="Open after threshold; half-open probe resets.",
        sol2="Stale metrics, too-low threshold, network partition to subset.",
        sol3="Breaker stops calls; bulkhead limits concurrent calls.",
    ),
    M(
        id="D15-T024",
        slug="d15-t024-bulkheads",
        name="Bulkheads",
        subdomain="Bulkheads",
        deps=["D15-T023", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T023", "D13-T024"],
        confused_with=["D15-T023", "D05-T023"],
        importance="core",
        focus="Bulkheads isolate resource pools (threads, connections) per dependency so one slow service cannot exhaust all workers.",
        principles_extra="Sized from traffic mix and SLO; monitor queue depth.",
        arch_extra="Separate executor per downstream; limit queue length.",
        mermaid="""flowchart TD
  api[API]
  poolA[PoolPayments]
  poolB[PoolSearch]
  api --> poolA
  api --> poolB""",
        examples="Tomcat connector threads vs dedicated async pool for reports.",
        code_file="d15_t024_bulkhead.py",
        code="""
def acquire(pool_free: int) -> bool:
    return pool_free > 0
""",
        backend="Reject fast when pool saturated instead of hanging all users.",
        mistakes=["One giant pool for all HTTP clients.", "Unbounded queues."],
        debug="Thread dump shows all blocked on same downstream.",
        trade_row="Dedicated pool | Isolation | Idle capacity | Mixed workloads | Uniform microservice",
        interview_theme="resource isolation bulkheads",
        ex1="Size pool given p99 latency and arrival rate.",
        ex2="All threads blocked on search—bulkhead fix?",
        ex3="Bulkhead vs rate limit.",
        sol1="Little's law rough: concurrency = RPS * latency.",
        sol2="Cap search concurrency; payments keep own pool.",
        sol3="Bulkhead isolates resources; rate limit caps RPS.",
    ),
    M(
        id="D15-T025",
        slug="d15-t025-failover-and-recovery",
        name="Failover and recovery",
        subdomain="Failover and recovery",
        deps=["D15-T024", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T008", "D15-T026"],
        confused_with=["D15-T013", "D15-T033"],
        importance="core",
        focus="Failover redirects traffic to standby when primary fails. Recovery includes restoring data consistency, rebuilding caches, and validating replication before returning to normal.",
        principles_extra="RTO/RPO drive automation vs manual steps.",
        arch_extra="DNS/load balancer health checks, controlled promotion, rehearsed runbooks.",
        mermaid="""flowchart LR
  primary[Primary]
  standby[Standby]
  traffic[Traffic]
  traffic --> primary
  primary -. failure .-> standby""",
        examples="RDS Multi-AZ failover; Kubernetes pod reschedule.",
        code_file="d15_t025_failover.py",
        code="""
def should_failover(primary_healthy: bool, standby_ready: bool) -> bool:
    return not primary_healthy and standby_ready
""",
        backend="Test failover quarterly; verify app reconnects and schema compatible.",
        mistakes=["Failover without checking replication lag.", "Clients cache dead primary DNS forever."],
        debug="Timeline from detection to stable traffic on standby.",
        trade_row="Automatic failover | Low RTO | False positive risk | HA DB | Experimental shard",
        interview_theme="failover RTO RPO",
        ex1="Implement should_failover guard.",
        ex2="Failover succeeded but data old—what metric?",
        ex3="Blue/green vs active-passive.",
        sol1="Only if standby ready.",
        sol2="Replication lag / LSN gap at promotion.",
        sol3="Blue/green for deploy; active-passive for DR.",
    ),
    M(
        id="D15-T026",
        slug="d15-t026-service-discovery",
        name="Service discovery",
        subdomain="Service discovery",
        deps=["D15-T025", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T027", "D04-T014"],
        confused_with=["D04-T014", "D16-T018"],
        importance="core",
        focus="Service discovery maps logical names to current instance endpoints. Client-side (smart client) vs server-side (proxy/LB) discovery trades agility vs central control.",
        principles_extra="Health-aware routing; cache TTL causes stale endpoints after crash.",
        arch_extra="Consul/etcd/Kubernetes DNS; sidecars push updates.",
        mermaid="""flowchart TD
  client[Client]
  registry[(Registry)]
  inst1[InstanceA]
  inst2[InstanceB]
  client --> registry
  registry --> inst1
  registry --> inst2""",
        examples="Kubernetes ClusterIP + Endpoints watch.",
        code_file="d15_t026_discover.py",
        code="""
def pick_instance(instances: list[str], healthy: set[str]) -> str | None:
    live = [i for i in instances if i in healthy]
    return live[0] if live else None
""",
        backend="Combine discovery with retries and breakers; drain instances before kill.",
        mistakes=["Hard-coded IPs in config.", "Ignoring zone affinity."],
        debug="Compare registry view vs actual listening ports.",
        trade_row="Client-side discovery | Low proxy hop | Library coupling | gRPC mesh | Simple public REST",
        interview_theme="service discovery patterns",
        ex1="Implement pick_instance skipping unhealthy.",
        ex2="Calls fail after deploy until TTL—why?",
        ex3="Service mesh vs DNS discovery.",
        sol1="First healthy instance.",
        sol2="Clients cache stale endpoints.",
        sol3="Mesh adds L7 policy; DNS simpler L4.",
    ),
    M(
        id="D15-T027",
        slug="d15-t027-heartbeats-and-failure-detection",
        name="Heartbeats and failure detection",
        subdomain="Heartbeats and failure detection",
        deps=["D15-T026", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T011", "D15-T025"],
        confused_with=["D05-T023", "D15-T026"],
        importance="core",
        focus="Heartbeats are periodic signals proving liveness. Failure detection declares a node dead after missed beats within timeout φ. False positives cause unnecessary failover.",
        principles_extra="Phi-accrual and adaptive timeouts reduce misdetection under GC.",
        arch_extra="Separate liveness (restart) from readiness (accept traffic).",
        mermaid="""sequenceDiagram
  participant A as NodeA
  participant B as Monitor
  loop every T
    A->>B: heartbeat
  end
  Note over B: missing > phi => suspect""",
        examples="Kubernetes liveness vs readiness probes.",
        code_file="d15_t027_heartbeat.py",
        code="""
def is_suspect(missed: int, allowed: int) -> bool:
    return missed > allowed
""",
        backend="Tune timeouts > p99 GC pause; use readiness for dependency failures.",
        mistakes=["Same probe for liveness and readiness.", "Too aggressive timeouts."],
        debug="Correlate suspect events with GC logs.",
        trade_row="Long timeout | Few false fails | Slow detection | Large nodes | Fast failover needs",
        interview_theme="heartbeat failure detection",
        ex1="Implement is_suspect.",
        ex2="Node killed by liveness but dependencies down—fix?",
        ex3="Gossip vs centralized failure detector.",
        sol1="True when missed beats exceed allowed.",
        sol2="Use readiness to pull from LB; liveness only for restart.",
        sol3="Gossip scales; centralized simpler small clusters.",
    ),
    M(
        id="D15-T028",
        slug="d15-t028-distributed-transactions",
        name="Distributed transactions",
        subdomain="Distributed transactions",
        deps=["D15-T027", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T029", "D15-T030"],
        confused_with=["D07-T012", "D15-T029"],
        importance="core",
        focus="A distributed transaction coordinates commits across multiple services or databases. Without a single log, you need protocols (2PC) or application-level sagas; latency and availability suffer under faults.",
        principles_extra="Prefer single-service transactions; split only when domain requires.",
        arch_extra="Orchestrator vs choreography; compensating actions.",
        mermaid="""flowchart TD
  s1[ServiceA]
  s2[ServiceB]
  coord[Coordinator]
  coord --> s1
  coord --> s2""",
        examples="Order + payment + inventory crossing three DBs.",
        code_file="d15_t028_steps.py",
        code="""
def workflow(done: list[str], required: list[str]) -> str:
    return "complete" if all(s in done for s in required) else "pending"
""",
        backend="Model business invariants; avoid XA unless you accept ops pain.",
        mistakes=["Distributed TX for every microservice call.", "No compensation path."],
        debug="Trace global transaction id across services.",
        trade_row="2PC | Atomic commit | Blocking | Homogeneous participants | Heterogeneous SaaS",
        interview_theme="distributed transaction alternatives",
        ex1="Track workflow state with required steps.",
        ex2="When local TX per service enough?",
        ex3="Saga vs 2PC availability.",
        sol1="complete when all required in done.",
        sol2="When single aggregate in one DB.",
        sol3="Saga accepts temporary inconsistency; 2PC blocks on coordinator failure.",
    ),
    M(
        id="D15-T029",
        slug="d15-t029-two-phase-commit",
        name="Two-phase commit",
        subdomain="Two-phase commit",
        deps=["D15-T028", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T030", "D15-T014"],
        confused_with=["D15-T030", "D15-T014"],
        importance="advanced",
        focus=(
            "Two-phase commit (2PC) has prepare then commit phases coordinated by a transaction manager. "
            "If all participants vote yes in prepare, coordinator sends commit; otherwise abort. "
            "2PC is blocking if coordinator fails after prepare—participants hold locks until decision. "
            "It does not magically provide exactly-once across arbitrary external systems."
        ),
        principles_extra="XA transactions use 2PC; cloud-native stacks often avoid it.",
        arch_extra="Write-ahead log at coordinator; presumed abort on timeout.",
        mermaid="""sequenceDiagram
  participant C as Coordinator
  participant P as Participant
  C->>P: prepare
  P-->>C: vote yes
  C->>P: commit""",
        examples="Classic DB XA; rare in modern microservices.",
        code_file="d15_t029_2pc.py",
        code="""
def decide(votes: list[str]) -> str:
    return "commit" if all(v == "yes" for v in votes) else "abort"
""",
        backend="Use only when all participants support prepare and ops accepts blocking risk.",
        mistakes=["2PC across HTTP microservices without prepare support.", "Ignoring coordinator SPOF."],
        debug="Find in-doubt transactions after coordinator crash.",
        trade_row="2PC | All-or-nothing | Block/avail | Single cluster | Multi-SaaS checkout",
        interview_theme="2PC prepare commit blocking",
        ex1="Implement decide on votes.",
        ex2="Coordinator dies after all yes—participant state?",
        ex3="Why Spanner/sagas instead of 2PC everywhere.",
        sol1="commit only if unanimous yes.",
        sol2="In-doubt blocked until recovery log replay.",
        sol3="2PC blocking/latency; sagas fit heterogeneous long flows.",
    ),
    M(
        id="D15-T030",
        slug="d15-t030-sagas",
        name="Sagas",
        subdomain="Sagas",
        deps=["D15-T029", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T019", "D15-T028"],
        confused_with=["D15-T029", "D15-T020"],
        importance="core",
        focus="Sagas are sequences of local transactions with compensating transactions to undo prior steps on failure. Choreography uses events; orchestration uses a central coordinator. They trade strong atomicity for availability and long-running workflows.",
        principles_extra="Compensations must be business-valid (cannot un-send email; send correction).",
        arch_extra="Persist saga state; idempotent forward and compensate handlers.",
        mermaid="""flowchart LR
  t1[ReserveInventory]
  t2[ChargePayment]
  t3[ConfirmOrder]
  t1 --> t2 --> t3
  t2 -. fail .-> c1[ReleaseInventory]""",
        examples="Temporal/Camunda orchestrated sagas; outbox events for choreography.",
        code_file="d15_t030_saga.py",
        code="""
def next_step(state: str, ok: bool) -> str:
    if state == "reserved" and ok:
        return "paid"
    if state == "reserved" and not ok:
        return "compensate_inventory"
    return state
""",
        backend="Design compensations first; test duplicate events.",
        mistakes=["Compensation that itself is not idempotent.", "No timeout on stuck saga."],
        debug="Saga table shows step stuck; replay with same idempotency key.",
        trade_row="Orchestrated saga | Clear flow | Coordinator SPOF | Complex checkout | Single DB TX enough",
        interview_theme="saga compensating transactions",
        ex1="Model states for reserve/pay/compensate.",
        ex2="Payment succeeded but order cancel—saga path?",
        ex3="Choreography vs orchestration pick.",
        sol1="Transitions on ok/fail flags.",
        sol2="Run compensate payment refund + release inventory.",
        sol3="Orchestration for visibility; choreography for loose coupling.",
    ),
    M(
        id="D15-T031",
        slug="d15-t031-data-partitioning-and-rebalancing",
        name="Data partitioning and rebalancing",
        subdomain="Data partitioning and rebalancing",
        deps=["D15-T030", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T032", "D16-T015"],
        confused_with=["D15-T009", "D07-T019"],
        importance="core",
        focus="Partitioning splits data by key range or hash across nodes for scale. Rebalancing moves shards when cluster grows; consistent hashing reduces moved keys.",
        principles_extra="Choose partition key for even spread and query locality.",
        arch_extra="Metadata service tracks shard map; double-write during migration.",
        mermaid="""flowchart TD
  key[PartitionKey]
  hash[HashFunction]
  shard1[Shard1]
  shard2[Shard2]
  key --> hash --> shard1
  hash --> shard2""",
        examples="Cassandra token ranges; Kafka partitions.",
        code_file="d15_t031_partition.py",
        code="""
def shard_for(key: str, num_shards: int) -> int:
    return hash(key) % num_shards
""",
        backend="Plan rebalance windows; throttle copy; verify checksums.",
        mistakes=["Hot partition key (all users in one shard).", "Rebalance without dual-read phase."],
        debug="Per-shard QPS and size metrics.",
        trade_row="Hash partition | Even spread | Scatter-gather queries | Huge tables | Small single-tenant DB",
        interview_theme="partitioning and rebalance",
        ex1="Implement shard_for.",
        ex2="Adding node causes latency spike—why?",
        ex3="Range vs hash partitioning.",
        sol1="Modulo hash into num_shards.",
        sol2="Rebalancing data movement competes with prod IO.",
        sol3="Range good range scans; hash better even load.",
    ),
    M(
        id="D15-T032",
        slug="d15-t032-hotspots-and-load-skew",
        name="Hotspots and load skew",
        subdomain="Hotspots and load skew",
        deps=["D15-T031", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T031", "D16-T017"],
        confused_with=["D15-T031", "D13-T024"],
        importance="core",
        focus="Hotspots concentrate traffic on one shard, partition, or leader. Skew breaks horizontal scale assumptions. Mitigations: salting keys, caching, split hot ranges, async aggregation.",
        principles_extra="Measure per-key QPS; celebrity accounts are classic hotspots.",
        arch_extra="Write sharding with random suffix; read merge.",
        mermaid="""flowchart TD
  traffic[Traffic]
  hot[HotShard]
  cold[ColdShard]
  traffic --> hot
  traffic --> cold""",
        examples="Viral post likes hammer one Redis key.",
        code_file="d15_t032_salt.py",
        code="""
def spread_keys(entity_id: str, salts: int) -> list[str]:
    return [f"{entity_id}:{i}" for i in range(salts)]
""",
        backend="Autoscale cannot fix wrong partition key; redesign or cache hot path.",
        mistakes=["Partitioning by country with one huge country.", "Ignoring leader hotspot in Kafka single partition."],
        debug="Top keys by QPS; shard heatmap.",
        trade_row="Key salting | Spread writes | Complex reads | Counter shards | Low traffic uniform",
        interview_theme="hotspot mitigation",
        ex1="Generate spread_keys for counter shards.",
        ex2="One Kafka partition lagging—cause?",
        ex3="Cache vs shard split for hot key.",
        sol1="List salted key names.",
        sol2="All events keyed same → single partition.",
        sol3="Cache helps reads; writes need split or aggregation tree.",
    ),
    M(
        id="D15-T033",
        slug="d15-t033-split-brain-prevention",
        name="Split-brain prevention",
        subdomain="Split-brain prevention",
        deps=["D15-T032", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D15-T013", "D15-T012"],
        confused_with=["D15-T013", "D15-T011"],
        importance="core",
        focus="Split-brain prevention enforces a single writable authority via quorum, fencing tokens, STONITH, or external lease (cloud API). Detection alone is insufficient without denying old leaders.",
        principles_extra="Combine membership changes with joint consensus (Raft) to avoid unsafe config updates.",
        arch_extra="Witness/quorum in DR; integrate with load balancer drain.",
        mermaid="""flowchart TD
  old[OldLeader]
  new[NewLeader]
  fence[FencingStore]
  old -->|rejected| fence
  new -->|allowed| fence""",
        examples="etcd lease + compare-and-swap on revision.",
        code_file="d15_t033_prevent.py",
        code="""
def may_serve_writes(holder: str, elected: str) -> bool:
    return holder == elected
""",
        backend="Automate promotion; manual break-glass with audit only.",
        mistakes=["Promote without demoting old primary.", "Split DNS to both primaries."],
        debug="Audit epoch/term at each write rejection.",
        trade_row="Fencing | Strong safety | Extra round trip | Shared storage | Best-effort cache",
        interview_theme="split-brain prevention controls",
        ex1="Implement may_serve_writes.",
        ex2="List three prevention mechanisms.",
        ex3="Why witness beats ping between two DCs.",
        sol1="Only elected holder serves.",
        sol2="Quorum, fencing/STONITH, lease with external authority.",
        sol3="Two DCs ping cannot prove which is majority; witness breaks tie.",
    ),
    M(
        id="D15-T034",
        slug="d15-t034-graceful-degradation",
        name="Graceful degradation",
        subdomain="Graceful degradation",
        deps=["D15-T033", "D15-T001", "D03-T001", "D03-T002", "D04-T001", "D04-T002"],
        related=["D05-T024", "D15-T023"],
        confused_with=["D05-T024", "D15-T008"],
        importance="core",
        focus="Graceful degradation reduces optional features while keeping core path alive under stress. It pairs with timeouts, breakers, and cached fallbacks. Users should see honest partial functionality, not opaque failures.",
        principles_extra="Define feature tiers before incident; automate toggles on SLO burn.",
        arch_extra="Feature flags, static fallbacks, read-only mode.",
        mermaid="""flowchart TD
  req[Request]
  core[CorePath]
  optional[OptionalFeatures]
  req --> core
  req -. degrade .-> optional""",
        examples="Show cached recommendations when personalization service down.",
        code_file="d15_t034_degrade.py",
        code="""
def respond(core_ok: bool, optional_ok: bool) -> dict:
    body = {"items": []}
    if core_ok:
        body["items"] = ["product"]
    if optional_ok:
        body["recommendations"] = ["a", "b"]
    return body
""",
        backend="Monitor degraded mode rate; exit when dependencies healthy.",
        mistakes=["Degrading security checks.", "Silent wrong prices in fallback cache."],
        debug="Flag in response or header when degraded.",
        trade_row="Cached fallback | Keeps UX | Stale/wrong risk | Recommendations | Payment authorization",
        interview_theme="graceful degradation tiers",
        ex1="Return partial JSON when optional fails.",
        ex2="What must never degrade?",
        ex3="Degradation vs circuit breaker interaction.",
        sol1="core items without recommendations.",
        sol2="AuthZ, payment correctness, legal consent.",
        sol3="Breaker opens optional path; core may still call if healthy.",
    ),
]

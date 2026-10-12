"""Topic-specific deep sections for selected D28–D35 notes."""
from __future__ import annotations

from d28_d35_core import ans

# Keys are topic IDs. Values are partial overrides merged into generated meta.

DEEP: dict[str, dict] = {}

DEEP["D35-T001"] = {
    "first_principles": [
        ans(
            "Raft is a consensus protocol: a replicated log where a single leader orders client commands and followers acknowledge before the leader considers an entry committed.",
            "The problem is that independent nodes can disagree after partitions; without agreement, two writers could pick conflicting orders for the same key.",
            "Raft decomposes consensus into leader election, log replication, and safety rules so operators can reason about behavior during crashes and network splits.",
            "Engineering depth here means knowing which RPCs fire on a write, what 'committed' means for reads, and how election timeouts interact with clock skew—not memorizing a proof.",
        ),
        ans(
            "Each server is follower, candidate, or leader. Followers accept entries only from the current leader for a given term.",
            "The leader appends to its log, replicates to a quorum of followers, then advances the commit index when a majority has stored the entry.",
            "If the leader dies, followers increment term, become candidates, and request votes; a candidate wins if it has at least as up-to-date a log as voters require.",
            "After election, the new leader may overwrite uncommitted tail entries on followers to match its log, which is why clients must retry ambiguous failures.",
        ),
    ],
    "internal": [
        ans(
            "Components: persistent state (currentTerm, votedFor, log[]), volatile leader state (nextIndex[], matchIndex[]), and RPC handlers AppendEntries and RequestVote.",
            "A client write hits the leader, which assigns a log index and term, persists locally, then streams AppendEntries to followers with prevLogIndex/prevLogTerm checks for consistency.",
            "Followers reject mismatched prefixes; the leader decrements nextIndex until a match is found—this backtracking heals forks without a separate merge phase.",
            "Committed entries are applied to the state machine in order; snapshots compact old log segments while retaining the last included index/term for new followers.",
        ),
    ],
    "mermaid": """stateDiagram-v2
  [*] --> Follower
  Follower --> Candidate: electionTimeout
  Candidate --> Leader: majorityVotes
  Candidate --> Follower: discoverLeader
  Leader --> Follower: higherTermSeen
  Follower --> Leader: discoverLeader""",
    "code": '''"""Illustrative Raft term and log entry checks (not a full implementation)."""
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class LogEntry:
    term: int
    command: str

@dataclass
class Server:
    current_term: int = 0
    voted_for: Optional[int] = None
    log: List[LogEntry] = field(default_factory=list)

    def last_log_index(self) -> int:
        return len(self.log)

    def last_log_term(self) -> int:
        return self.log[-1].term if self.log else 0

    def can_vote_for(self, candidate_id: int, candidate_term: int, candidate_last_index: int, candidate_last_term: int) -> bool:
        if candidate_term < self.current_term:
            return False
        if self.voted_for not in (None, candidate_id):
            return False
        # Up-to-date: higher term in last entry, or same term with longer log.
        up_to_date = (candidate_last_term, candidate_last_index) >= (self.last_log_term(), self.last_log_index())
        return up_to_date

if __name__ == "__main__":
    s = Server(log=[LogEntry(1, "set x=1")])
    assert s.can_vote_for(2, 2, 1, 1)
    print("ok", s.last_log_index())''',
}

DEEP["D35-T003"] = {
    "first_principles": [
        ans(
            "A CRDT (conflict-free replicated data type) is a data structure whose merge function is commutative, associative, and idempotent, so replicas converge without centralized locking.",
            "They exist because offline-first editors, edge caches, and gossiping services need concurrent updates without a single serializing database transaction.",
            "State-based CRDTs ship whole state and merge with a join; operation-based CRDTs ship operations applied in any order at each replica using a reliable causal broadcast.",
            "Engineering focus: pick a type (G-Counter, PN-Counter, OR-Set, LWW-Register) that matches your invariants—counters cannot go negative unless you choose a PN-Counter, not a G-Counter.",
        ),
    ],
    "mermaid": """flowchart LR
  replicaA[ReplicaA]
  replicaB[ReplicaB]
  replicaC[ReplicaC]
  replicaA -->|merge| replicaB
  replicaB -->|merge| replicaC
  replicaC -->|merge| replicaA""",
}

DEEP["D35-T004"] = {
    "first_principles": [
        ans(
            "An LSM (log-structured merge) tree optimizes write throughput by appending sorted runs to disk instead of random in-place B-tree page updates.",
            "Writes go to an in-memory memtable, flush to immutable SSTable files, and reads consult memtable plus SSTables newest-first with bloom filters to skip absent keys.",
            "Compaction merges overlapping SSTables to bound read amplification and reclaim tombstoned keys; tuning level sizes trades write amplification against read cost.",
            "Operators care about stall during compaction, disk bandwidth, and whether deletes are visible promptly—those are the production levers, not proving merge correctness on paper.",
        ),
    ],
    "mermaid": """flowchart TD
  write[WriteRequest]
  mem[MemTable]
  wal[WAL]
  l0[SSTableL0]
  l1[SSTableL1]
  read[ReadRequest]
  write --> wal
  write --> mem
  mem -->|flush| l0
  l0 -->|compaction| l1
  read --> mem
  read --> l0
  read --> l1""",
}

DEEP["D35-T008"] = {
    "first_principles": [
        ans(
            "Consistent hashing maps both keys and servers onto a ring so adding or removing a node moves only neighboring key ranges, unlike modulo hashing that reshuffles almost everything.",
            "Virtual nodes (vnodes) place many logical points per physical machine so load spreads evenly and a failure affects multiple small slices instead of one huge arc.",
            "Lookup walks the ring clockwise from the key hash to the first server token; replication walks additional successors for N copies.",
            "In production you still need health checks, handoff when a node dies, and rebalancing bandwidth limits—consistent hashing solves assignment, not operations.",
        ),
    ],
    "mermaid": """flowchart LR
  keyHash[KeyHash]
  ring[HashRing]
  vnode1[VnodeOnNodeA]
  vnode2[VnodeOnNodeB]
  vnode3[VnodeOnNodeC]
  keyHash --> ring
  ring --> vnode1
  ring --> vnode2
  ring --> vnode3""",
}

DEEP["D30-T012"] = {
    "overview_extra": ans(
        "RAG (retrieval-augmented generation) grounds an LLM answer with chunks retrieved from a knowledge base instead of relying on parametric memory alone.",
        "The backend owns ingestion, chunking, embedding, vector search, prompt assembly, and citation of sources so product can audit what the model saw.",
        "Latency is dominated by retrieval and reranking; quality is dominated by chunk boundaries and metadata filters, not only the choice of foundation model.",
    ),
    "mermaid": """flowchart TD
  query[UserQuery]
  embed[EmbedQuery]
  vectorDB[VectorIndex]
  chunks[TopKChunks]
  prompt[AssemblePrompt]
  llm[LLMCompletion]
  query --> embed
  embed --> vectorDB
  vectorDB --> chunks
  chunks --> prompt
  prompt --> llm""",
}

DEEP["D30-T008"] = {
    "overview_extra": ans(
        "Tool calling lets a model emit structured function invocations that your backend executes, then feeds results back into the conversation state.",
        "The server must validate tool names, arguments against JSON Schema, enforce authorization per tool, and cap side effects because the model is not a trusted caller.",
        "Design the orchestration loop with max steps, timeouts per tool, and idempotency keys for mutating tools to survive retries.",
    ),
}

DEEP["D30-T022"] = {
    "overview_extra": ans(
        "Prompt injection is untrusted text influencing model behavior—often via retrieved documents or user messages—so defenses treat model output and tool calls as untrusted until validated.",
        "Defensive patterns include separating system and user channels, allowlisting tools, human confirmation for sensitive actions, and never executing model-produced SQL or shell without static checks.",
        "This note documents mitigation architecture only; it does not include attack payloads or jailbreak recipes.",
    ),
    "mistakes_extra": [
        "Granting tools broad database access because the model 'usually' behaves.",
        "Inlining retrieved HTML into the system prompt without sanitization or source labels.",
    ],
}


def d33_runbook_sections(scenario: str) -> dict[str, str]:
    """Incident runbook content for D33 topics."""
    return {
        "overview": ans(
            f"This note is an incident runbook for: {scenario}.",
            "On-call engineers use it to separate observable symptoms from underlying root causes, then apply mitigations in a safe order before chasing optimizations.",
            "Symptoms are what dashboards and users report; root causes are the broken invariant in code, config, capacity, or dependencies.",
            "Every section below maps to checklists you can paste into a post-incident template after the fire is out.",
        ),
        "debugging": ans(
            "**Symptoms versus root cause.** Symptoms for this scenario often include elevated error rates, saturation graphs, or customer tickets that sound like total outage when only one path is failing.",
            f"Root causes for '{scenario}' frequently cluster around a recent deploy, a dependency limit, missing backpressure, or a data shape change—not generic 'the cloud is slow'.",
            "**What to check first.** Confirm scope (one region, tenant, endpoint, or job type), correlate deploy and config changes, and open the golden signals: latency, traffic, errors, saturation for each hop.",
            "**Mitigation (stop the bleeding).** Roll back or disable the risky change, shed load (rate limits, queue pauses), fail over read paths, or scale the bottlenecked tier while keeping data safety constraints in mind.",
            "**Prevention.** Add alerting on the symptom that fired earliest, integration tests for the failure class, capacity headroom, idempotency for retries, and runbooks linked from the service dashboard.",
        ),
    }

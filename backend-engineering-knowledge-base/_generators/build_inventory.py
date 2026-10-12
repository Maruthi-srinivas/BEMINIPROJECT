"""Parse interview/syllabus.md into the Phase 1 knowledge-base indexes.

Run from the repository root:

    python backend-engineering-knowledge-base/_generators/build_inventory.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SYLLABUS = ROOT / "interview" / "syllabus.md"
KB = ROOT / "backend-engineering-knowledge-base"
INDEX = KB / "00_INDEX"

# Checklist section -> knowledge-base directory. Sections 1 and 2 share a folder.
FOLDERS = {
    1: "01_PROGRAMMING_AND_ALGORITHMS",
    2: "01_PROGRAMMING_AND_ALGORITHMS",
    3: "02_OPERATING_SYSTEMS",
    4: "03_COMPUTER_NETWORKS",
    5: "04_BACKEND_FUNDAMENTALS",
    6: "05_API_DESIGN",
    7: "06_DATABASE_FUNDAMENTALS",
    8: "07_ADVANCED_SQL",
    9: "08_POSTGRESQL_INTERNALS",
    10: "09_NOSQL_DATABASES",
    11: "10_REDIS_AND_CACHING",
    12: "11_SECURITY",
    13: "12_CONCURRENCY",
    14: "13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE",
    15: "14_DISTRIBUTED_SYSTEMS",
    16: "15_SYSTEM_DESIGN_FUNDAMENTALS",
    17: "16_SYSTEM_DESIGN_PROBLEMS",
    18: "17_LOW_LEVEL_DESIGN",
    19: "18_MICROSERVICES",
    20: "19_TESTING",
    21: "20_PERFORMANCE_ENGINEERING",
    22: "21_OBSERVABILITY_AND_SRE",
    23: "22_DOCKER",
    24: "23_KUBERNETES_AND_CLOUD",
    25: "24_CI_CD",
    26: "25_LINUX_TROUBLESHOOTING",
    27: "26_SOFTWARE_ENGINEERING_PRINCIPLES",
    28: "27_ADVANCED_BACKEND",
    29: "28_SEARCH_AND_STORAGE",
    30: "29_AI_LLM_BACKEND",
    31: "30_BACKEND_FRAMEWORKS",
    32: "31_INTERVIEW_COMMUNICATION",
    33: "32_PRODUCTION_SCENARIOS",
    34: "33_PRACTICAL_PROJECTS",
    35: "34_ADVANCED_SPECIALIZED_TOPICS",
}

OWNERS = {
    1: "Programming and Algorithms",
    2: "Programming and Algorithms",
    3: "Programming and Algorithms",
    4: "Networking and API",
    5: "Networking and API",
    6: "Networking and API",
    7: "Database",
    8: "Database",
    9: "Database",
    10: "Database",
    11: "Database",
    12: "Security",
    13: "Programming and Algorithms",
    14: "Messaging and Distributed Systems",
    15: "Messaging and Distributed Systems",
    16: "Architecture and System Design",
    17: "Architecture and System Design",
    18: "Architecture and System Design",
    19: "Architecture and System Design",
    20: "Testing and Performance",
    21: "Testing and Performance",
    22: "DevOps, Cloud and SRE",
    23: "DevOps, Cloud and SRE",
    24: "DevOps, Cloud and SRE",
    25: "DevOps, Cloud and SRE",
    26: "DevOps, Cloud and SRE",
    27: "Architecture and System Design",
    28: "Architecture and System Design",
    29: "Database",
    30: "Framework and AI Backend",
    31: "Framework and AI Backend",
    32: "Interview and Validation",
    33: "Interview and Validation",
    34: "Architecture and System Design",
    35: "Messaging and Distributed Systems",
}

# Prerequisite domains. Topic-level edges are derived from these plus earlier topics.
DOMAIN_PREREQS = {
    1: [],
    2: [1],
    3: [1],
    4: [1, 3],
    5: [1, 4],
    6: [4, 5],
    7: [1, 5],
    8: [7],
    9: [7, 8],
    10: [7],
    11: [7, 5],
    12: [4, 5, 6],
    13: [1, 3],
    14: [4, 5, 13],
    15: [3, 4, 13, 14],
    16: [5, 6, 7, 15],
    17: [16, 7, 11],
    18: [1],
    19: [15, 16, 14],
    20: [5, 7],
    21: [2, 7, 13],
    22: [5, 21],
    23: [3, 5],
    24: [23, 22],
    25: [23, 20],
    26: [3, 23],
    27: [1],
    28: [15, 19, 12],
    29: [7, 10],
    30: [5, 12, 29],
    31: [1, 5, 7],
    32: [16, 17],
    33: [15, 22, 7],
    34: [5, 6, 7, 11, 20, 23],
    35: [15, 9, 2],
}

DEFAULTS = {
    1: ("core", "fundamentals"),
    2: ("core", "intermediate"),
    3: ("core", "intermediate"),
    4: ("core", "intermediate"),
    5: ("core", "intermediate"),
    6: ("core", "intermediate"),
    7: ("core", "intermediate"),
    8: ("common", "advanced"),
    9: ("advanced", "advanced"),
    10: ("common", "intermediate"),
    11: ("core", "intermediate"),
    12: ("core", "intermediate"),
    13: ("core", "advanced"),
    14: ("common", "advanced"),
    15: ("core", "advanced"),
    16: ("core", "intermediate"),
    17: ("common", "intermediate"),
    18: ("core", "intermediate"),
    19: ("common", "advanced"),
    20: ("common", "intermediate"),
    21: ("common", "advanced"),
    22: ("core", "intermediate"),
    23: ("common", "intermediate"),
    24: ("common", "advanced"),
    25: ("common", "intermediate"),
    26: ("core", "intermediate"),
    27: ("core", "fundamentals"),
    28: ("advanced", "advanced"),
    29: ("common", "advanced"),
    30: ("common", "advanced"),
    31: ("common", "intermediate"),
    32: ("core", "fundamentals"),
    33: ("core", "intermediate"),
    34: ("common", "intermediate"),
    35: ("advanced", "advanced"),
}

ADVANCED_WORDS = (
    "internals",
    "raft",
    "paxos",
    "crdt",
    "ebpf",
    "lsm",
    "mvcc",
    "wal",
    "consensus",
    "jvm",
    "gil",
    "kernel",
    "write amplification",
    "merkle",
    "gossip",
    "linearizability",
    "two-phase",
    "exactly-once",
    "vector clock",
    "pacelc",
    "bloom",
    "compaction",
    "toast",
    "brin",
    "logical replication",
    "service mesh",
    "chaos",
    "queueing theory",
    "hedged",
    "adaptive concurrency",
)

CORE_WORDS = (
    "acid",
    "transaction",
    "index",
    "tcp",
    "http",
    "rest",
    "jwt",
    "oauth",
    "cache",
    "deadlock",
    "race",
    "big-o",
    "normalization",
    "docker",
    "process",
    "thread",
    "sql injection",
    "authentication",
    "idempoten",
)

HEADING = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$")
BULLET = re.compile(r"^- \[ \]\s+(.+?)\s*$")


def slug(text: str) -> str:
    value = text.lower()
    value = value.replace("+", " plus ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value[:80].rstrip("-")


def classify(domain: int, name: str) -> tuple[str, str]:
    importance, complexity = DEFAULTS[domain]
    lowered = name.lower()
    if any(word in lowered for word in ADVANCED_WORDS):
        return "advanced", "advanced"
    if any(word in lowered for word in CORE_WORDS):
        importance = "core"
    return importance, complexity


def parse_syllabus(text: str) -> tuple[list[dict], dict[int, list[str]]]:
    domains: list[dict] = []
    current = None
    narratives: dict[int, list[str]] = {}
    for raw in text.splitlines():
        heading = HEADING.match(raw)
        if heading:
            if current:
                domains.append(current)
            number = int(heading.group(1))
            current = {"number": number, "name": heading.group(2).strip(), "topics": []}
            narratives[number] = []
            continue
        if current is None:
            continue
        bullet = BULLET.match(raw)
        if bullet:
            current["topics"].append(bullet.group(1).strip())
            continue
        stripped = raw.strip()
        if stripped and not stripped.startswith("Notes:") and not stripped.startswith("#"):
            narratives[current["number"]].append(stripped)
    if current:
        domains.append(current)
    return domains, narratives


def topic_id(domain: int, index: int) -> str:
    return f"D{domain:02d}-T{index:03d}"


def assign(domains: list[dict]) -> list[dict]:
    by_domain: dict[int, list[dict]] = {}
    topics: list[dict] = []
    for domain in domains:
        number = domain["number"]
        rows = []
        for index, name in enumerate(domain["topics"], start=1):
            importance, complexity = classify(number, name)
            tid = topic_id(number, index)
            filename = f"{tid.lower()}-{slug(name)}.md"
            row = {
                "id": tid,
                "domain_number": number,
                "domain": domain["name"],
                "subdomain": name,
                "name": name,
                "folder": FOLDERS[number],
                "note_path": f"{FOLDERS[number]}/notes/{filename}",
                "owner": OWNERS[number],
                "importance": importance,
                "complexity": complexity,
                "doc_status": "NOT_STARTED",
                "validation_status": "NOT_STARTED",
                "dependencies": [],
            }
            rows.append(row)
            topics.append(row)
        by_domain[number] = rows

    for row in topics:
        number = row["domain_number"]
        siblings = by_domain[number]
        position = siblings.index(row)
        deps: list[str] = []
        if position >= 1:
            deps.append(siblings[position - 1]["id"])
        if position >= 2:
            deps.append(siblings[0]["id"])
        for pred in DOMAIN_PREREQS[number]:
            anchor = by_domain[pred][0]["id"]
            if anchor not in deps:
                deps.append(anchor)
            if len(by_domain[pred]) > 1 and len(deps) < 6:
                second = by_domain[pred][1]["id"]
                if second not in deps:
                    deps.append(second)
        row["dependencies"] = deps[:6]
    return topics


def esc(text: str) -> str:
    return text.replace("|", "\\|")


def write_inventory(topics: list[dict], domains: list[dict]) -> None:
    lines = [
        "# Master topic inventory",
        "",
        "Canonical list of every checklist bullet in `interview/syllabus.md`.",
        "This checklist has no level below the bullet, so subdomain and exact topic name are the same string.",
        "A topic is complete only when validation status is `VALIDATED`.",
        "",
        f"Domains: {len(domains)}",
        f"Topics: {len(topics)}",
        "",
        "Status values: `NOT_STARTED`, `IN_PROGRESS`, `GENERATED`, `VALIDATION_FAILED`, `VALIDATED`, `BLOCKED`.",
        "",
        "Machine-readable copy: [inventory.json](./inventory.json).",
        "",
    ]
    by_domain: dict[int, list[dict]] = {}
    for topic in topics:
        by_domain.setdefault(topic["domain_number"], []).append(topic)
    for domain in domains:
        rows = by_domain[domain["number"]]
        lines.append(f"## D{domain['number']:02d} — {domain['name']}")
        lines.append("")
        lines.append(f"Folder: `{FOLDERS[domain['number']]}`. Owner: {OWNERS[domain['number']]}. Topics: {len(rows)}.")
        lines.append("")
        lines.append("| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
        for row in rows:
            deps = ", ".join(row["dependencies"]) if row["dependencies"] else "—"
            lines.append(
                f"| {row['id']} | {esc(row['name'])} | {deps} | {row['importance']} | {row['complexity']} | {row['doc_status']} | {row['validation_status']} | `{row['note_path']}` |"
            )
        lines.append("")
    (INDEX / "MASTER_TOPIC_INVENTORY.md").write_text("\n".join(lines), encoding="utf-8")


def write_checklist(topics: list[dict], domains: list[dict], narratives: dict[int, list[str]]) -> None:
    by_domain: dict[int, list[dict]] = {}
    for topic in topics:
        by_domain.setdefault(topic["domain_number"], []).append(topic)
    lines = [
        "# Backend master checklist",
        "",
        "Same scope as [interview/syllabus.md](../interview/syllabus.md), with a topic ID on every bullet.",
        "",
    ]
    for domain in domains:
        lines.append(f"## {domain['number']}. {domain['name']}")
        lines.append("")
        lines.append(f"Folder: `{FOLDERS[domain['number']]}`.")
        lines.append("")
        for row in by_domain[domain["number"]]:
            lines.append(f"- [ ] `{row['id']}` {row['name']}")
        for paragraph in narratives.get(domain["number"], []):
            lines.append("")
            lines.append(paragraph)
        lines.append("")
    (KB / "BACKEND_MASTER_CHECKLIST.md").write_text("\n".join(lines), encoding="utf-8")


def write_domain_index(topics: list[dict], domains: list[dict]) -> None:
    counts: dict[int, int] = {}
    for topic in topics:
        counts[topic["domain_number"]] = counts.get(topic["domain_number"], 0) + 1
    lines = [
        "# Domain index",
        "",
        "Thirty-five checklist domains. Sections 1 and 2 share `01_PROGRAMMING_AND_ALGORITHMS` and are still tracked separately.",
        "",
        "| Domain | Name | Folder | Topics | ID range | Owner |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for domain in domains:
        number = domain["number"]
        count = counts[number]
        lines.append(
            f"| D{number:02d} | {esc(domain['name'])} | `{FOLDERS[number]}` | {count} | `D{number:02d}-T001`–`D{number:02d}-T{count:03d}` | {OWNERS[number]} |"
        )
    lines.append("")
    lines.append(f"Total topics: {len(topics)}.")
    lines.append("")
    (INDEX / "DOMAIN_INDEX.md").write_text("\n".join(lines), encoding="utf-8")


def write_dependency_map(topics: list[dict], domains: list[dict]) -> None:
    lines = [
        "# Dependency map",
        "",
        "Learn in this order. Later domains assume the anchor topics of the domains they depend on.",
        "Each topic also depends on the previous topic in its own domain, and on that domain's first topic once you are past the second bullet.",
        "Per-topic edges are listed below and in the inventory. Root topics have no dependencies.",
        "",
        "## Domain order",
        "",
        "```mermaid",
        "flowchart TD",
        "  D01[D01_Language]",
        "  D02[D02_Algorithms]",
        "  D03[D03_OperatingSystems]",
        "  D13[D13_Concurrency]",
        "  D04[D04_Networks]",
        "  D05[D05_Backend]",
        "  D06[D06_API]",
        "  D07[D07_Databases]",
        "  D08[D08_SQL]",
        "  D09[D09_PostgreSQL]",
        "  D10[D10_NoSQL]",
        "  D11[D11_Redis]",
        "  D12[D12_Security]",
        "  D14[D14_Messaging]",
        "  D15[D15_DistributedSystems]",
        "  D16[D16_SystemDesign]",
        "  D18[D18_LowLevelDesign]",
        "  D19[D19_Microservices]",
        "  D27[D27_Principles]",
        "  D20[D20_Testing]",
        "  D21[D21_Performance]",
        "  D22[D22_Observability]",
        "  D23[D23_Docker]",
        "  D24[D24_Kubernetes]",
        "  D35[D35_Specialized]",
        "  D01 --> D02",
        "  D01 --> D03",
        "  D03 --> D13",
        "  D01 --> D04",
        "  D04 --> D05",
        "  D05 --> D06",
        "  D05 --> D07",
        "  D07 --> D08",
        "  D08 --> D09",
        "  D07 --> D10",
        "  D07 --> D11",
        "  D06 --> D12",
        "  D13 --> D14",
        "  D14 --> D15",
        "  D15 --> D16",
        "  D01 --> D18",
        "  D16 --> D19",
        "  D01 --> D27",
        "  D07 --> D20",
        "  D13 --> D21",
        "  D21 --> D22",
        "  D05 --> D23",
        "  D23 --> D24",
        "  D15 --> D35",
        "```",
        "",
        "How to read the diagram: an arrow means the source domain should be understood before the destination. It is a study order, not a runtime call graph.",
        "",
        "## Domain prerequisites",
        "",
        "| Domain | Depends on |",
        "| --- | --- |",
    ]
    names = {domain["number"]: domain["name"] for domain in domains}
    for number in range(1, 36):
        preds = DOMAIN_PREREQS[number]
        rendered = ", ".join(f"D{pred:02d} {names[pred]}" for pred in preds) if preds else "—"
        lines.append(f"| D{number:02d} {names[number]} | {rendered} |")
    lines.extend(["", "## Topic edges", ""])
    for topic in topics:
        if topic["dependencies"]:
            lines.append(f"- `{topic['id']}` {topic['name']} depends on {', '.join(f'`{dep}`' for dep in topic['dependencies'])}")
        else:
            lines.append(f"- `{topic['id']}` {topic['name']} is a root topic")
    lines.append("")
    (INDEX / "DEPENDENCY_MAP.md").write_text("\n".join(lines), encoding="utf-8")


def write_progress(topics: list[dict], domains: list[dict]) -> None:
    lines = [
        "# Progress tracker",
        "",
        "Only `VALIDATED` topics count toward completion. Phase 1 records the inventory. No note has been validated.",
        "",
        f"Inventoried topics: {len(topics)}",
        "",
        "| Domain | Topics | NOT_STARTED | IN_PROGRESS | GENERATED | VALIDATION_FAILED | VALIDATED | BLOCKED |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for domain in domains:
        count = sum(1 for topic in topics if topic["domain_number"] == domain["number"])
        lines.append(f"| D{domain['number']:02d} {esc(domain['name'])} | {count} | {count} | 0 | 0 | 0 | 0 | 0 |")
    lines.extend(
        [
            "",
            f"| Total | {len(topics)} | {len(topics)} | 0 | 0 | 0 | 0 | 0 |",
            "",
            "Completion: 0 validated / "
            + str(len(topics))
            + f" inventoried (0%).",
            "",
        ]
    )
    (INDEX / "PROGRESS_TRACKER.md").write_text("\n".join(lines), encoding="utf-8")


def write_execution_state(topics: list[dict]) -> None:
    first_batch = [topic["id"] for topic in topics if topic["domain_number"] == 1][:8]
    text = f"""# Execution state

Read this file first when resuming.

## Current phase

Phase 1 inventory is written. Detailed notes have not been generated.

## Counts

- Domains inventoried: 35
- Topics inventoried: {len(topics)}
- Validation status of every topic: NOT_STARTED
- Notes generated: 0
- Topics validated: 0

## Next action

Generate full notes for the first batch, in order:

{chr(10).join(f"- `{tid}`" for tid in first_batch)}

Batch size is 5–10 topics. After the batch, set those IDs to GENERATED in the inventory and in this file, then continue with the next D01 topics. Do not mark a topic VALIDATED until the audit passes.

## Resume steps

1. Read this file.
2. Read [MASTER_TOPIC_INVENTORY.md](./MASTER_TOPIC_INVENTORY.md) and [inventory.json](./inventory.json).
3. Confirm the note files named there exist before treating a topic as generated.
4. Continue from the first ID whose validation status is not VALIDATED and whose note does not already satisfy the template.
5. Do not regenerate a VALIDATED note unless an audit records a concrete defect.

## Files created in Phase 1

- `BACKEND_MASTER_CHECKLIST.md`
- `README.md`
- `00_INDEX/MASTER_TOPIC_INVENTORY.md`
- `00_INDEX/inventory.json`
- `00_INDEX/DOMAIN_INDEX.md`
- `00_INDEX/DEPENDENCY_MAP.md`
- `00_INDEX/PROGRESS_TRACKER.md`
- `00_INDEX/EXECUTION_STATE.md`
- `00_INDEX/GLOSSARY.md`
- `00_INDEX/LEARNING_PATH.md`
- `00_INDEX/COMPLETENESS_REPORT.md`

## Blockers

None.

## Unresolved questions

None. Web verification of version-sensitive claims is still outstanding and must be recorded per note when those notes are written.
"""
    (INDEX / "EXECUTION_STATE.md").write_text(text, encoding="utf-8")


def write_glossary() -> None:
    text = """# Glossary

Acronyms that appear in the checklist. Definitions here are short anchors. The topic note is the full explanation, and this file grows as notes are validated.

| Term | Meaning |
| --- | --- |
| ABAC | Attribute-based access control. Allow or deny using attributes of the user, resource, and context. |
| ACID | Atomicity, consistency, isolation, durability. The transactional guarantees of a typical relational database. |
| AOF | Append-only file. A Redis persistence log of write commands. |
| API | Application programming interface. The contract a client uses to call a service. |
| ARP | Address Resolution Protocol. Maps an IPv4 address to a MAC address on a local network. |
| BCNF | Boyce-Codd normal form. A stricter relational normal form than third normal form. |
| BFS | Breadth-first search. Graph traversal that visits neighbors before going deeper. |
| BOLA | Broken object-level authorization. An API lets a caller access an object they do not own. Also called IDOR. |
| CAP | Consistency, availability, partition tolerance. A partition forces a choice between linearizable consistency and availability. |
| CDC | Change data capture. Streaming row changes out of a database log. |
| CDN | Content delivery network. Caches responses at edges close to users. |
| CIDR | Classless Inter-Domain Routing. An IP prefix written as address plus prefix length. |
| CQRS | Command Query Responsibility Segregation. Separate models for writes and reads. |
| CRDT | Conflict-free replicated data type. A structure that merges concurrent updates without a coordinator. |
| CSRF | Cross-site request forgery. A browser sends the user's credentials to a site the user did not intend to call. |
| CTE | Common table expression. A named subquery introduced with `WITH`. |
| DFS | Depth-first search. Graph traversal that follows one path before backtracking. |
| DLQ | Dead-letter queue. A place for messages that could not be processed. |
| DNS | Domain Name System. Resolves names to records such as IP addresses. |
| DRY | Don't repeat yourself. One rule should have one representation. |
| eBPF | Extended Berkeley Packet Filter. A way to run sandboxed programs in the Linux kernel. |
| GC | Garbage collection. Reclaiming memory that is no longer reachable. |
| GIL | Global interpreter lock. In CPython, a lock that allows one thread to execute bytecode at a time. |
| HATEOAS | Hypermedia as the engine of application state. Clients follow links in responses. |
| HTTP | Hypertext Transfer Protocol. The request-response protocol of the web. |
| IAM | Identity and access management. Who can do what in a cloud account. |
| IDOR | Insecure direct object reference. Access control that trusts a client-supplied identifier. |
| ISR | In-sync replicas. Kafka replicas that are caught up enough to be eligible for the high watermark. |
| JIT | Just-in-time compilation. Translating hot code to native code at runtime. |
| JWT | JSON Web Token. A signed (and sometimes encrypted) set of claims. |
| KISS | Keep it simple. Prefer the smallest design that meets the requirement. |
| LLD | Low-level design. Classes, interfaces, and interactions inside a component. |
| LSM | Log-structured merge tree. A storage structure that batches writes and compacts them later. |
| MAC | Media access control address. A link-layer identifier. |
| MCP | Model Context Protocol. A protocol for connecting tools and context to a model. |
| MVCC | Multi-version concurrency control. Readers see a snapshot instead of blocking on writers. |
| NAT | Network address translation. Rewriting IP addresses, usually between private and public networks. |
| OAuth | An authorization framework for delegated access. It is not itself a login protocol. |
| OOP | Object-oriented programming. |
| OSI | Open Systems Interconnection model. A seven-layer teaching model for networks. |
| OWASP | Open Worldwide Application Security Project. Publisher of the commonly cited web risk list. |
| PACELC | An extension of CAP: if there is a partition choose availability or consistency; else choose latency or consistency. |
| PII | Personally identifiable information. |
| QPS | Queries per second. A throughput unit. |
| RAG | Retrieval-augmented generation. Fetch relevant documents and pass them to a model. |
| RBAC | Role-based access control. Permissions come from roles. |
| RCA | Root cause analysis. |
| RDB | Redis database file. A point-in-time snapshot of Redis data. |
| RED | Rate, errors, duration. A service-level metrics method. |
| REST | Representational State Transfer. An architectural style for HTTP APIs. |
| RPO | Recovery point objective. How much data loss is acceptable. |
| RTO | Recovery time objective. How long a recovery may take. |
| SLA | Service level agreement. The contractual commitment. |
| SLI | Service level indicator. A measured signal. |
| SLO | Service level objective. The internal target for an SLI. |
| SOLID | Five object-design principles: single responsibility, open-closed, Liskov substitution, interface segregation, dependency inversion. |
| SQL | Structured Query Language. |
| SRE | Site reliability engineering. |
| SSRF | Server-side request forgery. The server is tricked into requesting an internal URL. |
| SSO | Single sign-on. |
| TLS | Transport Layer Security. Cryptographic protection for a byte stream, commonly under HTTPS. |
| TTL | Time to live. How long a cache entry or DNS record remains valid. |
| USE | Utilization, saturation, errors. A resource-level metrics method. |
| WAL | Write-ahead log. A database log that is flushed before a commit is acknowledged. |
| XSS | Cross-site scripting. Untrusted content executed as script in a victim's browser. |
| YAGNI | You aren't gonna need it. Do not build for a requirement you do not have. |

Unverified against external standards in this stub. Topic notes must cite a source when a claim depends on a specific version.
"""
    (INDEX / "GLOSSARY.md").write_text(text, encoding="utf-8")


def write_learning_path() -> None:
    text = """# Learning path

Study order for the 35 domains. Stay on a domain until you can explain its topics without reading the note. The dependency map is the detailed edge list.

1. D01 Programming language fundamentals, then D02 data structures and algorithms.
2. D03 Operating systems, then D13 concurrency.
3. D04 Computer networks, D05 backend fundamentals, D06 API design.
4. D07 Database fundamentals, D08 advanced SQL, D09 PostgreSQL internals.
5. D10 NoSQL, D11 Redis and caching, D29 search and specialized storage.
6. D12 Authentication, authorization, and security.
7. D14 Messaging, D15 distributed systems, then the D35 topics those notes depend on.
8. D27 Software engineering principles and D18 low-level design.
9. D16 System design fundamentals, then D17 design problems.
10. D19 Microservices and D28 advanced backend topics.
11. D20 Testing, D21 performance, D22 observability.
12. D23 Docker, D24 Kubernetes and cloud, D25 CI/CD, D26 Linux troubleshooting.
13. D30 AI/LLM backends and D31 frameworks.
14. D32 Interview communication, D33 production scenarios, D34 project checklist.

D34 is a portfolio gate, not a concept to memorize. Use it after the project notes exist.

Notes for each topic are linked from [MASTER_TOPIC_INVENTORY.md](./MASTER_TOPIC_INVENTORY.md) once they are generated. Until then the note path is the planned file, and the status is `NOT_STARTED`.
"""
    (INDEX / "LEARNING_PATH.md").write_text(text, encoding="utf-8")


def write_completeness(topics: list[dict]) -> None:
    text = f"""# Completeness report

Status: not audited. Phase 1 inventoried the checklist. Phase 4 fills the validated counts.

This report must not be read as completion of the knowledge base.

| Measure | Count |
| --- | --- |
| Original domains | 35 |
| Topics inventoried | {len(topics)} |
| Topics validated | 0 |
| Topics incomplete | {len(topics)} |
| Topics blocked | 0 |
| Notes generated | 0 |
| Interview questions with answers | 0 |
| Exercises | 0 |
| Runnable examples tested | 0 |
| Diagrams | 0 |
| Unresolved technical issues | 0 |
| Source links verified | 0 |

Completion against the canonical inventory: 0 / {len(topics)} (0%).

Phase 4 checks, still open:

- Every inventory ID has a note.
- Every note has the required sections.
- No empty placeholders.
- Links and Mermaid fences parse.
- Code that is marked executed was actually run.
- Interview questions and exercises exist, or an exception is recorded.
"""
    (INDEX / "COMPLETENESS_REPORT.md").write_text(text, encoding="utf-8")


def write_readme(topics: list[dict]) -> None:
    text = f"""# Backend engineering knowledge base

Interview and implementation notes for the 35-domain backend checklist.

Start here:

1. [Learning path](./00_INDEX/LEARNING_PATH.md)
2. [Domain index](./00_INDEX/DOMAIN_INDEX.md)
3. [Master topic inventory](./00_INDEX/MASTER_TOPIC_INVENTORY.md)
4. [Checklist with topic IDs](./BACKEND_MASTER_CHECKLIST.md)

{len(topics)} topics are inventoried. Detailed notes are generated by topic ID and are not marked complete until validation status is `VALIDATED`. Progress: [progress tracker](./00_INDEX/PROGRESS_TRACKER.md). Resume point: [execution state](./00_INDEX/EXECUTION_STATE.md).

The checkbox copy used as input is [interview/syllabus.md](../interview/syllabus.md).

Reading these files needs a Markdown reader only. Examples that need PostgreSQL, Redis, Kafka, Java, or Go say so and use Docker Compose when Docker is available. They are labeled unexecuted until they have been run.
"""
    (KB / "README.md").write_text(text, encoding="utf-8")


def update_interview_readme() -> None:
    path = ROOT / "interview" / "README.md"
    original = path.read_text(encoding="utf-8")
    pointer = (
        "The canonical topic inventory and, as they are written, the detailed notes live in "
        "[backend-engineering-knowledge-base](../backend-engineering-knowledge-base/README.md). "
        "This folder keeps the checkbox syllabus.\n\n"
    )
    if "backend-engineering-knowledge-base" not in original:
        original = original.replace(
            "The full checklist is in [syllabus.md](./syllabus.md).",
            "The full checklist is in [syllabus.md](./syllabus.md).\n\n" + pointer,
        )
        path.write_text(original, encoding="utf-8")


def verify(domains: list[dict], topics: list[dict], syllabus_text: str) -> None:
    if len(domains) != 35:
        raise SystemExit(f"expected 35 domains, found {len(domains)}")
    numbers = [domain["number"] for domain in domains]
    if numbers != list(range(1, 36)):
        raise SystemExit(f"domain numbers are not 1..35: {numbers}")
    bullet_count = len(re.findall(r"^- \[ \] .+$", syllabus_text, flags=re.MULTILINE))
    for domain in domains:
        print(f"D{domain['number']:02d} {len(domain['topics']):3d} {domain['name']}")
    if bullet_count != len(topics):
        raise SystemExit(f"bullet count {bullet_count} != topic count {len(topics)}")
    ids = [topic["id"] for topic in topics]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate topic IDs")
    missing = [topic["id"] for topic in topics if not topic["name"]]
    if missing:
        raise SystemExit(f"blank names: {missing}")
    print(f"verified domains=35 topics={len(topics)}")


def main() -> None:
    syllabus_text = SYLLABUS.read_text(encoding="utf-8")
    domains, narratives = parse_syllabus(syllabus_text)
    topics = assign(domains)
    verify(domains, topics, syllabus_text)
    INDEX.mkdir(parents=True, exist_ok=True)
    write_inventory(topics, domains)
    write_checklist(topics, domains, narratives)
    write_domain_index(topics, domains)
    write_dependency_map(topics, domains)
    write_progress(topics, domains)
    write_execution_state(topics)
    write_glossary()
    write_learning_path()
    write_completeness(topics)
    write_readme(topics)
    update_interview_readme()
    (INDEX / "inventory.json").write_text(json.dumps({"domains": domains, "topics": topics}, indent=2), encoding="utf-8")
    print(f"wrote indexes under {INDEX}")


if __name__ == "__main__":
    main()

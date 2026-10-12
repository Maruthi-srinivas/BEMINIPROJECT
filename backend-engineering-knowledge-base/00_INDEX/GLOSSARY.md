# Glossary

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

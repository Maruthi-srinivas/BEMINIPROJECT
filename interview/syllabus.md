# Backend Interview Syllabus

Master checklist. Study notes for each numbered topic live in the matching file in this folder. Check items off here as you can explain them out loud without notes.

## 1. Programming Language Fundamentals

Notes: [01-programming-language-fundamentals.md](./01-programming-language-fundamentals.md)

- [ ] Data types, variables, operators, type conversion
- [ ] Control flow, loops, functions, recursion
- [ ] Pointers, references, memory management
- [ ] Stack vs heap memory
- [ ] Value vs reference semantics
- [ ] Object-oriented programming (OOP)
- [ ] Encapsulation, abstraction, inheritance, polymorphism
- [ ] Composition vs inheritance
- [ ] Interfaces, abstract classes, generics
- [ ] Exception handling and custom exceptions
- [ ] Immutability and mutability
- [ ] Collections and data structures
- [ ] Iterators, generators, streams
- [ ] Functional programming concepts
- [ ] Lambdas, closures, higher-order functions
- [ ] Concurrency and parallelism
- [ ] Memory leaks and garbage collection
- [ ] Runtime, compilation, interpretation
- [ ] Language-specific internals (Java/Python/Go/Node.js)
- [ ] Clean code, naming, readability, maintainability

## 2. Data Structures and Algorithms

Notes: [02-data-structures-and-algorithms.md](./02-data-structures-and-algorithms.md)

- [ ] Time and space complexity
- [ ] Big-O, Big-Theta, Big-Omega
- [ ] Arrays and strings
- [ ] Linked lists
- [ ] Stacks and queues
- [ ] Hash maps and hash sets
- [ ] Trees and binary search trees
- [ ] Heaps and priority queues
- [ ] Tries
- [ ] Graphs and graph representations
- [ ] BFS and DFS
- [ ] Topological sorting
- [ ] Shortest-path algorithms
- [ ] Union-Find / Disjoint Set Union
- [ ] Sorting and searching
- [ ] Binary search patterns
- [ ] Two pointers and sliding window
- [ ] Prefix sums and difference arrays
- [ ] Monotonic stacks and queues
- [ ] Greedy algorithms
- [ ] Backtracking
- [ ] Dynamic programming
- [ ] Bit manipulation
- [ ] Intervals and sweep-line algorithms
- [ ] Randomized algorithms
- [ ] Amortized analysis
- [ ] Problem-solving patterns and edge cases

## 3. Operating Systems

Notes: [03-operating-systems.md](./03-operating-systems.md)

- [ ] Processes vs threads
- [ ] Process lifecycle and context switching
- [ ] User mode vs kernel mode
- [ ] System calls
- [ ] CPU scheduling
- [ ] Threads and thread pools
- [ ] Concurrency vs parallelism
- [ ] Race conditions
- [ ] Critical sections and synchronization
- [ ] Mutexes, semaphores, read-write locks
- [ ] Deadlocks: prevention, detection, recovery
- [ ] Starvation and livelocks
- [ ] Atomic operations and compare-and-swap
- [ ] Memory management and virtual memory
- [ ] Paging and segmentation
- [ ] Page faults
- [ ] File descriptors and file systems
- [ ] I/O buffering
- [ ] Blocking vs non-blocking I/O
- [ ] Synchronous vs asynchronous execution
- [ ] Event loops
- [ ] Signals and inter-process communication
- [ ] Linux process and networking commands
- [ ] Resource limits and process isolation

## 4. Computer Networks

Notes: [04-computer-networks.md](./04-computer-networks.md)

- [ ] OSI and TCP/IP models
- [ ] IP addressing, subnetting, CIDR
- [ ] MAC addresses, ARP
- [ ] TCP vs UDP
- [ ] TCP handshake and connection termination
- [ ] Sequence numbers, ACKs, retransmission
- [ ] Flow control and congestion control
- [ ] TCP connection states and TIME_WAIT
- [ ] HTTP/1.1, HTTP/2, HTTP/3
- [ ] HTTP methods, headers, status codes
- [ ] HTTP caching semantics
- [ ] DNS resolution and record types
- [ ] TLS/SSL handshake
- [ ] Certificates, CAs, public/private keys
- [ ] Symmetric vs asymmetric encryption
- [ ] WebSockets and Server-Sent Events
- [ ] Long polling
- [ ] REST vs gRPC
- [ ] Proxies, reverse proxies and load balancers
- [ ] NAT, firewalls and ports
- [ ] CDN and edge networking
- [ ] Connection pooling and keep-alive
- [ ] Latency, bandwidth, throughput and packet loss

## 5. Backend Development Fundamentals

Notes: [05-backend-development-fundamentals.md](./05-backend-development-fundamentals.md)

- [ ] Client-server architecture
- [ ] Request-response lifecycle
- [ ] Routing and middleware
- [ ] Controllers, services and repositories
- [ ] Dependency injection
- [ ] Configuration and environment variables
- [ ] Input validation and sanitization
- [ ] Serialization and deserialization
- [ ] Error handling and exception mapping
- [ ] Centralized logging
- [ ] Authentication and authorization
- [ ] Pagination: offset vs cursor
- [ ] Filtering, sorting and searching
- [ ] File uploads and downloads
- [ ] Background jobs
- [ ] Email, SMS and push notifications
- [ ] Scheduled jobs and cron
- [ ] Graceful startup and shutdown
- [ ] Health checks and readiness checks
- [ ] API versioning
- [ ] Database connection pooling
- [ ] Configuration and secret management
- [ ] Request context and correlation IDs
- [ ] Graceful degradation

## 6. API Design and REST

Notes: [06-api-design-and-rest.md](./06-api-design-and-rest.md)

- [ ] REST architectural constraints
- [ ] Resource-oriented URL design
- [ ] HTTP methods and idempotency
- [ ] HTTP status codes
- [ ] Request and response schemas
- [ ] API contracts and schema evolution
- [ ] Path vs query vs header parameters
- [ ] Validation and consistent error responses
- [ ] Pagination, filtering and sorting
- [ ] Versioning strategies
- [ ] Idempotency keys
- [ ] Rate limiting and quotas
- [ ] Conditional requests: ETag, If-Match
- [ ] Caching: Cache-Control, ETag, Last-Modified
- [ ] HATEOAS and when it is useful
- [ ] OpenAPI and Swagger
- [ ] API gateways
- [ ] Webhooks and signature verification
- [ ] API deprecation strategies
- [ ] REST vs GraphQL vs gRPC vs RPC
- [ ] API compatibility and backward compatibility

## 7. Database Fundamentals

Notes: [07-database-fundamentals.md](./07-database-fundamentals.md)

- [ ] Relational vs non-relational databases
- [ ] Tables, rows, columns and schemas
- [ ] Primary and foreign keys
- [ ] Candidate, composite and surrogate keys
- [ ] Constraints and data integrity
- [ ] Normalization: 1NF, 2NF, 3NF, BCNF
- [ ] Denormalization
- [ ] One-to-one, one-to-many, many-to-many relationships
- [ ] Joins and subqueries
- [ ] Aggregations and grouping
- [ ] Transactions
- [ ] ACID properties
- [ ] Isolation levels
- [ ] Dirty reads, non-repeatable reads, phantom reads
- [ ] Locks and deadlocks
- [ ] Optimistic vs pessimistic concurrency control
- [ ] MVCC
- [ ] Database indexes
- [ ] Composite and covering indexes
- [ ] Clustered vs non-clustered indexes
- [ ] B-tree and hash indexes
- [ ] Query execution plans
- [ ] EXPLAIN and EXPLAIN ANALYZE
- [ ] Slow query optimization
- [ ] Connection pooling
- [ ] Migrations and schema evolution
- [ ] Backup, restore and point-in-time recovery
- [ ] Replication and failover
- [ ] Partitioning and sharding
- [ ] Read replicas and read/write splitting
- [ ] Data archival and retention

## 8. SQL — Advanced Topics

Notes: [08-sql-advanced-topics.md](./08-sql-advanced-topics.md)

- [ ] Advanced joins
- [ ] Correlated subqueries
- [ ] Common Table Expressions (CTEs)
- [ ] Recursive CTEs
- [ ] Window functions
- [ ] Ranking functions
- [ ] Running totals and moving averages
- [ ] CASE, COALESCE, NULLIF
- [ ] NULL semantics and three-valued logic
- [ ] Upserts and conflict handling
- [ ] Transactions and savepoints
- [ ] Locking reads
- [ ] Advisory locks
- [ ] Generated and computed columns
- [ ] Views and materialized views
- [ ] Stored procedures and triggers
- [ ] JSON and JSONB querying
- [ ] Full-text search
- [ ] Geospatial queries
- [ ] Index selectivity and cardinality
- [ ] N+1 query problem
- [ ] Keyset pagination
- [ ] Database performance troubleshooting

## 9. PostgreSQL Internals

Notes: [09-postgresql-internals.md](./09-postgresql-internals.md)

- [ ] PostgreSQL architecture
- [ ] MVCC and tuple visibility
- [ ] WAL (Write-Ahead Logging)
- [ ] Checkpoints and crash recovery
- [ ] Vacuum and autovacuum
- [ ] Dead tuples and table bloat
- [ ] Heap storage and TOAST
- [ ] B-tree, GIN, GiST and BRIN indexes
- [ ] Query planner and optimizer
- [ ] Statistics and ANALYZE
- [ ] Isolation and row-level locking
- [ ] Advisory locks
- [ ] Streaming and logical replication
- [ ] Table partitioning
- [ ] Connection poolers
- [ ] Replication lag
- [ ] Backup and recovery
- [ ] High availability and failover

## 10. NoSQL Databases

Notes: [10-nosql-databases.md](./10-nosql-databases.md)

- [ ] SQL vs NoSQL trade-offs
- [ ] Key-value stores
- [ ] Document databases
- [ ] Wide-column databases
- [ ] Graph databases
- [ ] Data modeling for access patterns
- [ ] Denormalization and embedding vs referencing
- [ ] Secondary indexes
- [ ] TTL and expiration
- [ ] Consistency models
- [ ] Partition keys and hot partitions
- [ ] Replication and sharding
- [ ] Quorums
- [ ] Eventual consistency
- [ ] MongoDB indexes and aggregation pipelines
- [ ] MongoDB transactions
- [ ] DynamoDB partition and sort keys
- [ ] Cassandra data modeling
- [ ] Choosing the right database for a workload

## 11. Redis and Caching

Notes: [11-redis-and-caching.md](./11-redis-and-caching.md)

- [ ] Why caching works
- [ ] Cache hit ratio and cache efficiency
- [ ] Cache-aside
- [ ] Read-through and write-through
- [ ] Write-behind and write-around
- [ ] TTL and expiration
- [ ] Cache invalidation
- [ ] Cache stampede
- [ ] Cache penetration
- [ ] Cache avalanche
- [ ] Hot keys and key design
- [ ] Redis strings, hashes, lists, sets, sorted sets
- [ ] Redis Streams
- [ ] Pub/Sub
- [ ] Persistence: RDB and AOF
- [ ] Eviction policies
- [ ] Redis transactions and Lua scripts
- [ ] Distributed locks and their limitations
- [ ] Rate limiting with Redis
- [ ] Sliding-window counters
- [ ] Leaderboards and ranking
- [ ] Redis replication and Sentinel
- [ ] Redis Cluster
- [ ] Cache consistency with a primary database
- [ ] When not to use caching

## 12. Authentication, Authorization and Security

Notes: [12-authentication-authorization-and-security.md](./12-authentication-authorization-and-security.md)

- [ ] Authentication vs authorization
- [ ] Sessions and cookies
- [ ] JWT structure and validation
- [ ] Access and refresh tokens
- [ ] OAuth 2.0
- [ ] OpenID Connect
- [ ] SSO and identity providers
- [ ] RBAC and ABAC
- [ ] Multi-factor authentication
- [ ] Password hashing: Argon2, bcrypt
- [ ] Password reset and account recovery
- [ ] API keys and service credentials
- [ ] TLS and certificate validation
- [ ] CORS and preflight requests
- [ ] CSRF
- [ ] XSS
- [ ] SQL and NoSQL injection
- [ ] SSRF
- [ ] Path traversal
- [ ] Broken access control and IDOR/BOLA
- [ ] Request smuggling
- [ ] Replay attacks
- [ ] Rate limiting and brute-force protection
- [ ] Input validation and output encoding
- [ ] Secrets management and rotation
- [ ] Encryption at rest and in transit
- [ ] Audit logging
- [ ] OWASP Top 10
- [ ] Least privilege and zero-trust principles
- [ ] Dependency and supply-chain security
- [ ] Threat modeling and security testing

## 13. Concurrency and Parallel Processing

Notes: [13-concurrency-and-parallel-processing.md](./13-concurrency-and-parallel-processing.md)

- [ ] Threads vs processes
- [ ] Async/await
- [ ] Event-driven concurrency
- [ ] Thread pools and worker pools
- [ ] Futures and promises
- [ ] Race conditions and atomicity
- [ ] Mutexes and semaphores
- [ ] Read-write locks
- [ ] Lock-free programming basics
- [ ] Producer-consumer pattern
- [ ] Bounded queues and backpressure
- [ ] Concurrent collections
- [ ] Deadlock prevention
- [ ] Task scheduling
- [ ] CPU-bound vs I/O-bound workloads
- [ ] Python GIL and multiprocessing
- [ ] Java memory model
- [ ] Go goroutines and channels
- [ ] Node.js event loop and worker threads
- [ ] Concurrency limits and bulkheads
- [ ] Cancellation and timeouts
- [ ] Structured concurrency concepts

## 14. Messaging and Event-Driven Architecture

Notes: [14-messaging-and-event-driven-architecture.md](./14-messaging-and-event-driven-architecture.md)

- [ ] Message queues vs event streams
- [ ] Synchronous vs asynchronous communication
- [ ] Kafka architecture
- [ ] Topics, partitions and offsets
- [ ] Producers and consumers
- [ ] Consumer groups and rebalancing
- [ ] Partition keys and ordering
- [ ] Replication and ISR
- [ ] Delivery semantics: at-most-once, at-least-once, exactly-once
- [ ] Idempotent producers
- [ ] Idempotent consumers
- [ ] Retries and retry topics
- [ ] Dead-letter queues (DLQs)
- [ ] Delayed messages
- [ ] Backpressure and consumer lag
- [ ] Offset commits
- [ ] Message schemas and schema registry
- [ ] Schema evolution and compatibility
- [ ] Event sourcing
- [ ] CQRS
- [ ] Transactional outbox
- [ ] CDC (Change Data Capture)
- [ ] Sagas and compensating actions
- [ ] RabbitMQ exchanges, queues and bindings
- [ ] Acknowledgments and redelivery
- [ ] RabbitMQ vs Kafka
- [ ] Pub/Sub systems
- [ ] Ordering guarantees
- [ ] Poison messages
- [ ] Message deduplication
- [ ] Replay and reprocessing
- [ ] Workflow orchestration vs choreography

## 15. Distributed Systems

Notes: [15-distributed-systems.md](./15-distributed-systems.md)

- [ ] Distributed system fundamentals
- [ ] Partial failures
- [ ] Network partitions
- [ ] CAP theorem
- [ ] PACELC theorem
- [ ] Strong, eventual and causal consistency
- [ ] Linearizability and sequential consistency
- [ ] Availability and fault tolerance
- [ ] Replication strategies
- [ ] Leader-follower architecture
- [ ] Leader election
- [ ] Quorum reads and writes
- [ ] Split-brain scenarios
- [ ] Consensus: Raft and Paxos concepts
- [ ] Distributed locking
- [ ] Clock skew and clock synchronization
- [ ] Logical clocks and vector clocks
- [ ] At-most-once and at-least-once execution
- [ ] Idempotency
- [ ] Exactly-once processing limitations
- [ ] Retries, timeouts and exponential backoff
- [ ] Jitter and retry storms
- [ ] Circuit breakers
- [ ] Bulkheads
- [ ] Failover and recovery
- [ ] Service discovery
- [ ] Heartbeats and failure detection
- [ ] Distributed transactions
- [ ] Two-phase commit
- [ ] Sagas
- [ ] Data partitioning and rebalancing
- [ ] Hotspots and load skew
- [ ] Split-brain prevention
- [ ] Graceful degradation

## 16. System Design Fundamentals

Notes: [16-system-design-fundamentals.md](./16-system-design-fundamentals.md)

- [ ] Functional requirements
- [ ] Non-functional requirements
- [ ] Requirement clarification
- [ ] Capacity estimation
- [ ] QPS and peak traffic estimation
- [ ] Bandwidth and storage estimation
- [ ] Latency budgets
- [ ] SLOs and availability targets
- [ ] API and data model design
- [ ] High-level architecture diagrams
- [ ] Low-level design
- [ ] Monolith vs modular monolith vs microservices
- [ ] Layered architecture
- [ ] Hexagonal / ports-and-adapters architecture
- [ ] Clean architecture
- [ ] Domain-driven design (DDD)
- [ ] Bounded contexts and aggregates
- [ ] SOLID principles
- [ ] Design patterns
- [ ] Separation of concerns
- [ ] Stateless vs stateful services
- [ ] Horizontal vs vertical scaling
- [ ] Load balancing
- [ ] Caching layers
- [ ] Database selection
- [ ] Replication and partitioning
- [ ] Synchronous vs asynchronous workflows
- [ ] Single points of failure
- [ ] Failure scenarios and recovery
- [ ] Consistency vs availability trade-offs
- [ ] Cost optimization
- [ ] Security and observability
- [ ] Architecture decision records (ADRs)

## 17. Common System Design Problems

Notes: [17-common-system-design-problems.md](./17-common-system-design-problems.md)

- [ ] URL shortener
- [ ] Rate limiter
- [ ] API gateway
- [ ] Notification service
- [ ] Email delivery system
- [ ] Chat application
- [ ] WhatsApp/Telegram-like messaging
- [ ] Slack-like multi-tenant application
- [ ] Social media news feed
- [ ] File storage / Google Drive
- [ ] S3-style object storage
- [ ] Video streaming platform
- [ ] Search autocomplete
- [ ] Web crawler
- [ ] E-commerce platform
- [ ] Amazon-like order management
- [ ] Inventory management
- [ ] Payment processing system
- [ ] Ticket booking system
- [ ] Ride-hailing service
- [ ] Food delivery platform
- [ ] Hotel reservation system
- [ ] Job scheduler
- [ ] Distributed task queue
- [ ] Logging and metrics platform
- [ ] Metrics monitoring system
- [ ] Feature flag service
- [ ] Distributed cache
- [ ] Recommendation system
- [ ] Multi-tenant SaaS platform
- [ ] Real-time location tracking
- [ ] Leaderboard service
- [ ] Webhook delivery platform
- [ ] Audit log service
- [ ] Search engine
- [ ] AI/RAG inference service

## 18. Low-Level Design (LLD) and Object-Oriented Design

Notes: [18-low-level-design-and-ood.md](./18-low-level-design-and-ood.md)

- [ ] SOLID principles
- [ ] DRY, KISS and YAGNI
- [ ] Encapsulation and composition
- [ ] Interfaces and abstractions
- [ ] Dependency inversion and injection
- [ ] UML class and sequence diagrams
- [ ] Class responsibility and collaboration
- [ ] Object lifecycle and ownership
- [ ] Factory and Abstract Factory
- [ ] Builder
- [ ] Singleton and its pitfalls
- [ ] Prototype
- [ ] Strategy
- [ ] Observer
- [ ] Adapter
- [ ] Decorator
- [ ] Facade
- [ ] Proxy
- [ ] Command
- [ ] State
- [ ] Template Method
- [ ] Chain of Responsibility
- [ ] Repository and Unit of Work
- [ ] Dependency injection containers
- [ ] Extensibility and testability
- [ ] Concurrency-safe object design
- [ ] Domain modeling and invariants
- [ ] Refactoring and avoiding overengineering

## 19. Microservices Architecture

Notes: [19-microservices-architecture.md](./19-microservices-architecture.md)

- [ ] Microservices principles
- [ ] Service boundaries
- [ ] Domain-driven decomposition
- [ ] API gateway patterns
- [ ] Service discovery
- [ ] Inter-service communication
- [ ] REST vs gRPC between services
- [ ] Synchronous vs asynchronous calls
- [ ] Centralized configuration
- [ ] Distributed tracing
- [ ] Service authentication
- [ ] Resilience patterns
- [ ] Circuit breakers and bulkheads
- [ ] Timeouts and retries
- [ ] Saga pattern
- [ ] Transactional outbox
- [ ] CQRS and event sourcing
- [ ] Distributed data ownership
- [ ] Database-per-service
- [ ] Cross-service consistency
- [ ] API composition
- [ ] Aggregation and fan-out
- [ ] Service versioning
- [ ] Backward-compatible deployments
- [ ] Strangler pattern
- [ ] Service mesh basics
- [ ] Sidecars and proxies
- [ ] Monolith-to-microservices migration
- [ ] Microservices failure modes
- [ ] When not to use microservices

## 20. Software Testing

Notes: [20-software-testing.md](./20-software-testing.md)

- [ ] Unit testing
- [ ] Integration testing
- [ ] Component testing
- [ ] API testing
- [ ] End-to-end testing
- [ ] Contract testing
- [ ] Consumer-driven contracts
- [ ] Regression testing
- [ ] Smoke and sanity testing
- [ ] Acceptance testing
- [ ] Test doubles, mocks, stubs and fakes
- [ ] Fixtures and test data management
- [ ] Database integration tests
- [ ] Testing transactions and rollbacks
- [ ] Testing asynchronous workflows
- [ ] Testing Kafka consumers and producers
- [ ] Concurrency and race testing
- [ ] Property-based testing
- [ ] Fuzz testing
- [ ] Mutation testing
- [ ] Performance testing
- [ ] Load, stress, spike and soak testing
- [ ] Fault injection and chaos testing
- [ ] Test coverage vs test quality
- [ ] CI test pipelines
- [ ] Testcontainers and ephemeral dependencies

## 21. Performance Engineering

Notes: [21-performance-engineering.md](./21-performance-engineering.md)

- [ ] Latency percentiles: p50, p90, p95, p99
- [ ] Throughput and concurrency
- [ ] Profiling CPU and memory
- [ ] Flame graphs
- [ ] Memory leaks and allocation pressure
- [ ] Garbage collection tuning
- [ ] Database query optimization
- [ ] Index tuning
- [ ] N+1 queries
- [ ] Connection pool tuning
- [ ] Caching and cache hit rates
- [ ] Async I/O
- [ ] Batching and bulk operations
- [ ] Compression
- [ ] Payload size optimization
- [ ] Network overhead
- [ ] Thread pool sizing
- [ ] Backpressure
- [ ] Queue depth and consumer lag
- [ ] Load testing and benchmarking
- [ ] Little's Law
- [ ] Amdahl's Law
- [ ] Bottleneck identification
- [ ] Tail latency
- [ ] Capacity planning

## 22. Observability and Production Operations

Notes: [22-observability-and-production-operations.md](./22-observability-and-production-operations.md)

- [ ] Structured logging
- [ ] Log levels and log sampling
- [ ] Metrics, logs and traces
- [ ] Golden signals
- [ ] RED and USE methods
- [ ] Prometheus
- [ ] Grafana
- [ ] OpenTelemetry
- [ ] Distributed tracing
- [ ] Correlation and trace IDs
- [ ] Loki / Elasticsearch-based logging
- [ ] Health, liveness and readiness probes
- [ ] SLIs, SLOs and SLAs
- [ ] Error budgets
- [ ] Alert design and noise reduction
- [ ] Dashboards
- [ ] Incident response
- [ ] Root cause analysis (RCA)
- [ ] Postmortems and corrective actions
- [ ] On-call fundamentals
- [ ] Runbooks and playbooks
- [ ] Production debugging
- [ ] Memory, CPU and connection saturation
- [ ] Queue lag and database saturation
- [ ] Dependency failures
- [ ] Service-level and end-to-end monitoring

## 23. Docker and Containerization

Notes: [23-docker-and-containerization.md](./23-docker-and-containerization.md)

- [ ] Containers vs virtual machines
- [ ] Images and layers
- [ ] Dockerfile instructions
- [ ] Multi-stage builds
- [ ] Image size optimization
- [ ] Build cache
- [ ] Docker Compose
- [ ] Container networking
- [ ] Volumes and bind mounts
- [ ] Environment variables and secrets
- [ ] Health checks
- [ ] Resource limits
- [ ] Container logs
- [ ] Non-root containers
- [ ] Image scanning
- [ ] Container registries
- [ ] Container startup and shutdown
- [ ] Service dependency management
- [ ] Docker debugging
- [ ] Persistent storage
- [ ] Development vs production images
- [ ] Reproducible builds

## 24. Kubernetes and Cloud Infrastructure

Notes: [24-kubernetes-and-cloud-infrastructure.md](./24-kubernetes-and-cloud-infrastructure.md)

- [ ] Kubernetes architecture
- [ ] Pods and Deployments
- [ ] ReplicaSets
- [ ] Services and service discovery
- [ ] Ingress and Gateway API
- [ ] ConfigMaps and Secrets
- [ ] Namespaces
- [ ] Liveness, readiness and startup probes
- [ ] Resource requests and limits
- [ ] Horizontal Pod Autoscaler
- [ ] Persistent Volumes and Claims
- [ ] StatefulSets and DaemonSets
- [ ] Jobs and CronJobs
- [ ] Rolling updates and rollbacks
- [ ] Pod disruption budgets
- [ ] RBAC and service accounts
- [ ] Network policies
- [ ] Helm
- [ ] Kubernetes troubleshooting
- [ ] Cloud networking fundamentals
- [ ] VPCs, subnets, routing and firewalls
- [ ] IAM and least privilege
- [ ] Compute, storage and managed databases
- [ ] Object storage
- [ ] Load balancers and CDNs
- [ ] Autoscaling
- [ ] Availability zones and regions
- [ ] Disaster recovery
- [ ] RTO and RPO
- [ ] Infrastructure as Code: Terraform
- [ ] Cost monitoring and optimization

## 25. CI/CD and Release Engineering

Notes: [25-cicd-and-release-engineering.md](./25-cicd-and-release-engineering.md)

- [ ] Git fundamentals and branching strategies
- [ ] Pull requests and code reviews
- [ ] Merge vs rebase
- [ ] CI pipelines
- [ ] Automated testing
- [ ] Build artifacts and versioning
- [ ] Container image publishing
- [ ] CD pipelines
- [ ] Jenkins / GitHub Actions / GitLab CI
- [ ] Environment promotion
- [ ] Deployment strategies
- [ ] Rolling deployments
- [ ] Blue-green deployments
- [ ] Canary releases
- [ ] Feature flags
- [ ] Database migration safety
- [ ] Backward-compatible changes
- [ ] Rollbacks and roll-forwards
- [ ] Release automation
- [ ] GitOps and Argo CD
- [ ] Artifact and dependency security
- [ ] Supply-chain security
- [ ] Secrets in CI/CD
- [ ] Release verification

## 26. Linux and Backend Troubleshooting

Notes: [26-linux-and-backend-troubleshooting.md](./26-linux-and-backend-troubleshooting.md)

- [ ] Filesystem and permissions
- [ ] Users, groups and ownership
- [ ] Processes: ps, top, htop
- [ ] Signals and process termination
- [ ] grep, sed, awk, find
- [ ] Pipes and redirection
- [ ] curl and wget
- [ ] ss, netstat, lsof
- [ ] dig, nslookup, ping, traceroute
- [ ] Disk and memory diagnostics
- [ ] df, du, free, vmstat
- [ ] CPU profiling and system load
- [ ] strace basics
- [ ] Environment variables
- [ ] Shell scripting
- [ ] Log inspection and rotation
- [ ] File descriptor limits
- [ ] Port conflicts
- [ ] TLS certificate debugging
- [ ] DNS and connectivity debugging
- [ ] Out-of-memory failures
- [ ] Disk exhaustion
- [ ] Process crashes and restarts

## 27. Software Engineering Principles

Notes: [27-software-engineering-principles.md](./27-software-engineering-principles.md)

- [ ] SOLID
- [ ] DRY, KISS, YAGNI
- [ ] Separation of concerns
- [ ] High cohesion and low coupling
- [ ] Dependency inversion
- [ ] Encapsulation and information hiding
- [ ] Clean code and refactoring
- [ ] Technical debt management
- [ ] Code review practices
- [ ] Design documentation
- [ ] Architecture Decision Records
- [ ] API and schema compatibility
- [ ] Backward and forward compatibility
- [ ] Semantic versioning
- [ ] Feature flags
- [ ] Configuration management
- [ ] Secure coding
- [ ] Maintainability and extensibility
- [ ] Debugging methodology
- [ ] Root cause analysis
- [ ] Engineering trade-offs
- [ ] Documentation and knowledge sharing

## 28. Advanced Backend Topics That Make You Stand Out

Notes: [28-advanced-backend-topics.md](./28-advanced-backend-topics.md)

- [ ] Multi-tenancy: shared DB vs schema vs database per tenant
- [ ] Tenant isolation and tenant-aware authorization
- [ ] Fairness and noisy-neighbor protection
- [ ] API quotas and tenant-level rate limiting
- [ ] Distributed rate limiting
- [ ] Idempotent payment and order workflows
- [ ] Double-entry ledger fundamentals
- [ ] Exactly-once business effects
- [ ] Transactional outbox and inbox patterns
- [ ] CDC-based integrations
- [ ] Distributed scheduling
- [ ] Leader election and leases
- [ ] Workflow engines and durable execution
- [ ] Long-running transactions and compensations
- [ ] Data consistency across services
- [ ] Hot-key mitigation
- [ ] Multi-region architecture
- [ ] Disaster recovery and failover
- [ ] Data retention and deletion workflows
- [ ] Auditability and compliance
- [ ] Tenant migration
- [ ] Zero-downtime schema migrations
- [ ] Backpressure and load shedding
- [ ] Admission control
- [ ] Graceful degradation
- [ ] Cost-aware architecture
- [ ] Feature flags and progressive delivery
- [ ] Production readiness reviews
- [ ] Chaos engineering
- [ ] Capacity planning and load forecasting

## 29. Search and Specialized Storage

Notes: [29-search-and-specialized-storage.md](./29-search-and-specialized-storage.md)

- [ ] Elasticsearch / OpenSearch architecture
- [ ] Inverted indexes
- [ ] Full-text search and analyzers
- [ ] Tokenization and relevance scoring
- [ ] Filtering, sorting and aggregations
- [ ] Index mappings and schema evolution
- [ ] Reindexing and alias swaps
- [ ] Search pagination and deep pagination
- [ ] Geo-spatial queries
- [ ] Vector databases
- [ ] Object storage and multipart uploads
- [ ] Pre-signed URLs
- [ ] Content hashing and deduplication
- [ ] Metadata storage vs blob storage
- [ ] Lifecycle and archival policies

## 30. AI/LLM Backend Engineering

Notes: [30-ai-llm-backend-engineering.md](./30-ai-llm-backend-engineering.md)

- [ ] LLM API integration
- [ ] Streaming responses
- [ ] Token budgets and context windows
- [ ] Rate limits and quotas
- [ ] Retries and timeouts for model APIs
- [ ] Prompt templates and versioning
- [ ] Structured outputs and schema validation
- [ ] Tool calling
- [ ] MCP (Model Context Protocol)
- [ ] Agent orchestration
- [ ] LangChain and LangGraph
- [ ] RAG architecture
- [ ] Document ingestion and chunking
- [ ] Embeddings and vector search
- [ ] Hybrid retrieval and reranking
- [ ] Retrieval evaluation
- [ ] Hallucination and grounding controls
- [ ] Conversation state and memory
- [ ] Background ingestion pipelines
- [ ] Async inference jobs
- [ ] LLM caching and semantic caching
- [ ] Prompt injection and tool security
- [ ] PII handling and data isolation
- [ ] Model fallback and provider routing
- [ ] Cost, latency and token observability
- [ ] LLM evaluation and regression tests
- [ ] Queue-based inference scaling
- [ ] Human-in-the-loop workflows
- [ ] AI service reliability and graceful degradation

## 31. Backend Frameworks — Choose One Deeply

Notes: [31-backend-frameworks.md](./31-backend-frameworks.md)

- [ ] Spring Boot: IoC, beans, DI, auto-configuration
- [ ] Spring MVC and request lifecycle
- [ ] Spring Security
- [ ] Spring Data JPA and Hibernate
- [ ] Transactions and propagation
- [ ] Entity lifecycle and persistence context
- [ ] Lazy vs eager loading
- [ ] N+1 queries
- [ ] Bean scopes and lifecycle
- [ ] Filters, interceptors and AOP
- [ ] FastAPI routing and dependency injection
- [ ] Pydantic validation and serialization
- [ ] ASGI and Uvicorn
- [ ] SQLAlchemy sessions and transactions
- [ ] FastAPI background tasks
- [ ] Node.js event loop and asynchronous I/O
- [ ] Express middleware and error handling
- [ ] Go net/http, contexts and goroutines
- [ ] Framework testing and dependency overrides
- [ ] Framework security and performance
- [ ] Production deployment and configuration

## 32. Backend Interview Communication

Notes: [32-backend-interview-communication.md](./32-backend-interview-communication.md)

- [ ] Clarifying ambiguous requirements
- [ ] Explaining assumptions explicitly
- [ ] Breaking down a problem systematically
- [ ] Writing readable code under time pressure
- [ ] Explaining time and space complexity
- [ ] Discussing edge cases
- [ ] Comparing alternative designs
- [ ] Justifying technology choices
- [ ] Explaining trade-offs rather than naming tools
- [ ] Debugging unfamiliar code
- [ ] Discussing failures and recovery
- [ ] Explaining your own projects end-to-end
- [ ] Presenting measurable project outcomes
- [ ] Handling follow-up questions
- [ ] Communicating uncertainty honestly
- [ ] Explaining a production incident using root cause and remediation
- [ ] Describing ownership, collaboration and technical decisions

## 33. Real-World Engineering Scenarios

Notes: [33-real-world-engineering-scenarios.md](./33-real-world-engineering-scenarios.md)

- [ ] API latency suddenly increases
- [ ] Database CPU reaches 100%
- [ ] Connection pool is exhausted
- [ ] Redis becomes unavailable
- [ ] Kafka consumer lag grows continuously
- [ ] Duplicate events create duplicate orders
- [ ] An external payment provider times out
- [ ] A service returns intermittent 5xx errors
- [ ] A deployment causes elevated errors
- [ ] Database migration fails halfway
- [ ] A cache stampede overloads the database
- [ ] A tenant monopolizes shared resources
- [ ] A distributed lock expires during work
- [ ] A retry storm overloads dependencies
- [ ] A message is permanently failing
- [ ] A region becomes unavailable
- [ ] Data is accidentally deleted
- [ ] A secret or credential is exposed
- [ ] A queue grows faster than consumers process it
- [ ] A service must handle 10× traffic
- [ ] An API change breaks old clients
- [ ] A background job runs twice
- [ ] Two requests update the same resource concurrently
- [ ] A downstream service is slow but not fully down

## 34. Practical Project Validation Checklist

Notes: [34-practical-project-validation-checklist.md](./34-practical-project-validation-checklist.md)

For each serious backend project, be able to demonstrate:

- [ ] Clear requirements and architecture diagrams
- [ ] REST APIs with documented contracts
- [ ] Authentication and authorization
- [ ] PostgreSQL schema and optimized queries
- [ ] Redis caching where justified
- [ ] Background processing or message queues where justified
- [ ] Idempotency and duplicate-request protection
- [ ] Retries, timeouts and failure handling
- [ ] Unit, integration and API tests
- [ ] Load testing and performance measurements
- [ ] Structured logs, metrics and distributed tracing
- [ ] Dockerized services and reproducible startup
- [ ] CI/CD pipeline
- [ ] Database migrations and recovery plan
- [ ] Security review
- [ ] Failure scenarios documented
- [ ] README, API docs and architecture diagrams
- [ ] Measurable benchmarks and documented trade-offs

For a strong backend portfolio, build at least one production-style project that brings together PostgreSQL, Redis, Kafka, authentication, observability, automated testing and Docker. A multi-tenant SaaS backend or event-driven order-processing platform is particularly suitable for demonstrating these concepts.

## 35. Advanced and Specialized Topics

Notes: [35-advanced-and-specialized-topics.md](./35-advanced-and-specialized-topics.md)

- [ ] Raft consensus in depth
- [ ] Distributed transactions and isolation
- [ ] CRDTs and conflict-free replication
- [ ] LSM trees and storage-engine internals
- [ ] B-trees and database storage internals
- [ ] Write amplification and compaction
- [ ] Bloom filters
- [ ] Consistent hashing and virtual nodes
- [ ] Gossip protocols
- [ ] Merkle trees and anti-entropy
- [ ] Distributed snapshots
- [ ] Eventual consistency repair
- [ ] Tail-tolerant systems
- [ ] Hedged requests
- [ ] Adaptive concurrency limits
- [ ] Queueing theory
- [ ] Load shedding and overload control
- [ ] Multi-region replication
- [ ] Data locality and placement
- [ ] eBPF and advanced Linux observability
- [ ] Kernel networking and socket internals
- [ ] Advanced JVM / Python / Go runtime profiling
- [ ] Storage and network cost optimization

# Master topic inventory

Canonical list of every checklist bullet in `interview/syllabus.md`.
This checklist has no level below the bullet, so subdomain and exact topic name are the same string.
A topic is complete only when validation status is `VALIDATED`.

Domains: 35
Topics: 877

Status values: `NOT_STARTED`, `IN_PROGRESS`, `GENERATED`, `VALIDATION_FAILED`, `VALIDATED`, `BLOCKED`.

Machine-readable copy: [inventory.json](./inventory.json).

## D01 — Programming Language Fundamentals

Folder: `01_PROGRAMMING_AND_ALGORITHMS`. Owner: Programming and Algorithms. Topics: 20.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D01-T001 | Data types, variables, operators, type conversion | — | core | fundamentals | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d01-t001-data-types-variables-operators-type-conversion.md` |
| D01-T002 | Control flow, loops, functions, recursion | D01-T001 | core | fundamentals | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d01-t002-control-flow-loops-functions-recursion.md` |
| D01-T003 | Pointers, references, memory management | D01-T002, D01-T001 | core | fundamentals | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d01-t003-pointers-references-memory-management.md` |
| D01-T004 | Stack vs heap memory | D01-T003, D01-T001 | core | fundamentals | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d01-t004-stack-vs-heap-memory.md` |
| D01-T005 | Value vs reference semantics | D01-T004, D01-T001 | core | fundamentals | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d01-t005-value-vs-reference-semantics.md` |
| D01-T006 | Object-oriented programming (OOP) | D01-T005, D01-T001 | core | fundamentals | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d01-t006-object-oriented-programming-oop.md` |
| D01-T007 | Encapsulation, abstraction, inheritance, polymorphism | D01-T006, D01-T001 | core | fundamentals | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d01-t007-encapsulation-abstraction-inheritance-polymorphism.md` |
| D01-T008 | Composition vs inheritance | D01-T007, D01-T001 | core | fundamentals | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d01-t008-composition-vs-inheritance.md` |
| D01-T009 | Interfaces, abstract classes, generics | D01-T008, D01-T001 | core | fundamentals | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d01-t009-interfaces-abstract-classes-generics.md` |
| D01-T010 | Exception handling and custom exceptions | D01-T009, D01-T001 | core | fundamentals | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d01-t010-exception-handling-and-custom-exceptions.md` |
| D01-T011 | Immutability and mutability | D01-T010, D01-T001 | core | fundamentals | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d01-t011-immutability-and-mutability.md` |
| D01-T012 | Collections and data structures | D01-T011, D01-T001 | core | fundamentals | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d01-t012-collections-and-data-structures.md` |
| D01-T013 | Iterators, generators, streams | D01-T012, D01-T001 | core | fundamentals | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d01-t013-iterators-generators-streams.md` |
| D01-T014 | Functional programming concepts | D01-T013, D01-T001 | core | fundamentals | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d01-t014-functional-programming-concepts.md` |
| D01-T015 | Lambdas, closures, higher-order functions | D01-T014, D01-T001 | core | fundamentals | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d01-t015-lambdas-closures-higher-order-functions.md` |
| D01-T016 | Concurrency and parallelism | D01-T015, D01-T001 | core | fundamentals | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d01-t016-concurrency-and-parallelism.md` |
| D01-T017 | Memory leaks and garbage collection | D01-T016, D01-T001 | core | fundamentals | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d01-t017-memory-leaks-and-garbage-collection.md` |
| D01-T018 | Runtime, compilation, interpretation | D01-T017, D01-T001 | core | fundamentals | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d01-t018-runtime-compilation-interpretation.md` |
| D01-T019 | Language-specific internals (Java/Python/Go/Node.js) | D01-T018, D01-T001 | advanced | advanced | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d01-t019-language-specific-internals-java-python-go-node-js.md` |
| D01-T020 | Clean code, naming, readability, maintainability | D01-T019, D01-T001 | core | fundamentals | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d01-t020-clean-code-naming-readability-maintainability.md` |

## D02 — Data Structures and Algorithms

Folder: `01_PROGRAMMING_AND_ALGORITHMS`. Owner: Programming and Algorithms. Topics: 27.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D02-T001 | Time and space complexity | D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t001-time-and-space-complexity.md` |
| D02-T002 | Big-O, Big-Theta, Big-Omega | D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t002-big-o-big-theta-big-omega.md` |
| D02-T003 | Arrays and strings | D02-T002, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t003-arrays-and-strings.md` |
| D02-T004 | Linked lists | D02-T003, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t004-linked-lists.md` |
| D02-T005 | Stacks and queues | D02-T004, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t005-stacks-and-queues.md` |
| D02-T006 | Hash maps and hash sets | D02-T005, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t006-hash-maps-and-hash-sets.md` |
| D02-T007 | Trees and binary search trees | D02-T006, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t007-trees-and-binary-search-trees.md` |
| D02-T008 | Heaps and priority queues | D02-T007, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t008-heaps-and-priority-queues.md` |
| D02-T009 | Tries | D02-T008, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t009-tries.md` |
| D02-T010 | Graphs and graph representations | D02-T009, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t010-graphs-and-graph-representations.md` |
| D02-T011 | BFS and DFS | D02-T010, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t011-bfs-and-dfs.md` |
| D02-T012 | Topological sorting | D02-T011, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t012-topological-sorting.md` |
| D02-T013 | Shortest-path algorithms | D02-T012, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t013-shortest-path-algorithms.md` |
| D02-T014 | Union-Find / Disjoint Set Union | D02-T013, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t014-union-find-disjoint-set-union.md` |
| D02-T015 | Sorting and searching | D02-T014, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t015-sorting-and-searching.md` |
| D02-T016 | Binary search patterns | D02-T015, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t016-binary-search-patterns.md` |
| D02-T017 | Two pointers and sliding window | D02-T016, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t017-two-pointers-and-sliding-window.md` |
| D02-T018 | Prefix sums and difference arrays | D02-T017, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t018-prefix-sums-and-difference-arrays.md` |
| D02-T019 | Monotonic stacks and queues | D02-T018, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t019-monotonic-stacks-and-queues.md` |
| D02-T020 | Greedy algorithms | D02-T019, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t020-greedy-algorithms.md` |
| D02-T021 | Backtracking | D02-T020, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t021-backtracking.md` |
| D02-T022 | Dynamic programming | D02-T021, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t022-dynamic-programming.md` |
| D02-T023 | Bit manipulation | D02-T022, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t023-bit-manipulation.md` |
| D02-T024 | Intervals and sweep-line algorithms | D02-T023, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t024-intervals-and-sweep-line-algorithms.md` |
| D02-T025 | Randomized algorithms | D02-T024, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t025-randomized-algorithms.md` |
| D02-T026 | Amortized analysis | D02-T025, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t026-amortized-analysis.md` |
| D02-T027 | Problem-solving patterns and edge cases | D02-T026, D02-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `01_PROGRAMMING_AND_ALGORITHMS/notes/d02-t027-problem-solving-patterns-and-edge-cases.md` |

## D03 — Operating Systems

Folder: `02_OPERATING_SYSTEMS`. Owner: Programming and Algorithms. Topics: 24.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D03-T001 | Processes vs threads | D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t001-processes-vs-threads.md` |
| D03-T002 | Process lifecycle and context switching | D03-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t002-process-lifecycle-and-context-switching.md` |
| D03-T003 | User mode vs kernel mode | D03-T002, D03-T001, D01-T001, D01-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t003-user-mode-vs-kernel-mode.md` |
| D03-T004 | System calls | D03-T003, D03-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t004-system-calls.md` |
| D03-T005 | CPU scheduling | D03-T004, D03-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t005-cpu-scheduling.md` |
| D03-T006 | Threads and thread pools | D03-T005, D03-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t006-threads-and-thread-pools.md` |
| D03-T007 | Concurrency vs parallelism | D03-T006, D03-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t007-concurrency-vs-parallelism.md` |
| D03-T008 | Race conditions | D03-T007, D03-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t008-race-conditions.md` |
| D03-T009 | Critical sections and synchronization | D03-T008, D03-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t009-critical-sections-and-synchronization.md` |
| D03-T010 | Mutexes, semaphores, read-write locks | D03-T009, D03-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t010-mutexes-semaphores-read-write-locks.md` |
| D03-T011 | Deadlocks: prevention, detection, recovery | D03-T010, D03-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t011-deadlocks-prevention-detection-recovery.md` |
| D03-T012 | Starvation and livelocks | D03-T011, D03-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t012-starvation-and-livelocks.md` |
| D03-T013 | Atomic operations and compare-and-swap | D03-T012, D03-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t013-atomic-operations-and-compare-and-swap.md` |
| D03-T014 | Memory management and virtual memory | D03-T013, D03-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t014-memory-management-and-virtual-memory.md` |
| D03-T015 | Paging and segmentation | D03-T014, D03-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t015-paging-and-segmentation.md` |
| D03-T016 | Page faults | D03-T015, D03-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t016-page-faults.md` |
| D03-T017 | File descriptors and file systems | D03-T016, D03-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t017-file-descriptors-and-file-systems.md` |
| D03-T018 | I/O buffering | D03-T017, D03-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t018-i-o-buffering.md` |
| D03-T019 | Blocking vs non-blocking I/O | D03-T018, D03-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t019-blocking-vs-non-blocking-i-o.md` |
| D03-T020 | Synchronous vs asynchronous execution | D03-T019, D03-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t020-synchronous-vs-asynchronous-execution.md` |
| D03-T021 | Event loops | D03-T020, D03-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t021-event-loops.md` |
| D03-T022 | Signals and inter-process communication | D03-T021, D03-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t022-signals-and-inter-process-communication.md` |
| D03-T023 | Linux process and networking commands | D03-T022, D03-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t023-linux-process-and-networking-commands.md` |
| D03-T024 | Resource limits and process isolation | D03-T023, D03-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `02_OPERATING_SYSTEMS/notes/d03-t024-resource-limits-and-process-isolation.md` |

## D04 — Computer Networks

Folder: `03_COMPUTER_NETWORKS`. Owner: Networking and API. Topics: 23.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D04-T001 | OSI and TCP/IP models | D01-T001, D01-T002, D03-T001, D03-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t001-osi-and-tcp-ip-models.md` |
| D04-T002 | IP addressing, subnetting, CIDR | D04-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t002-ip-addressing-subnetting-cidr.md` |
| D04-T003 | MAC addresses, ARP | D04-T002, D04-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t003-mac-addresses-arp.md` |
| D04-T004 | TCP vs UDP | D04-T003, D04-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t004-tcp-vs-udp.md` |
| D04-T005 | TCP handshake and connection termination | D04-T004, D04-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t005-tcp-handshake-and-connection-termination.md` |
| D04-T006 | Sequence numbers, ACKs, retransmission | D04-T005, D04-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t006-sequence-numbers-acks-retransmission.md` |
| D04-T007 | Flow control and congestion control | D04-T006, D04-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t007-flow-control-and-congestion-control.md` |
| D04-T008 | TCP connection states and TIME_WAIT | D04-T007, D04-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t008-tcp-connection-states-and-time-wait.md` |
| D04-T009 | HTTP/1.1, HTTP/2, HTTP/3 | D04-T008, D04-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t009-http-1-1-http-2-http-3.md` |
| D04-T010 | HTTP methods, headers, status codes | D04-T009, D04-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t010-http-methods-headers-status-codes.md` |
| D04-T011 | HTTP caching semantics | D04-T010, D04-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t011-http-caching-semantics.md` |
| D04-T012 | DNS resolution and record types | D04-T011, D04-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t012-dns-resolution-and-record-types.md` |
| D04-T013 | TLS/SSL handshake | D04-T012, D04-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t013-tls-ssl-handshake.md` |
| D04-T014 | Certificates, CAs, public/private keys | D04-T013, D04-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t014-certificates-cas-public-private-keys.md` |
| D04-T015 | Symmetric vs asymmetric encryption | D04-T014, D04-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t015-symmetric-vs-asymmetric-encryption.md` |
| D04-T016 | WebSockets and Server-Sent Events | D04-T015, D04-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t016-websockets-and-server-sent-events.md` |
| D04-T017 | Long polling | D04-T016, D04-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t017-long-polling.md` |
| D04-T018 | REST vs gRPC | D04-T017, D04-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t018-rest-vs-grpc.md` |
| D04-T019 | Proxies, reverse proxies and load balancers | D04-T018, D04-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t019-proxies-reverse-proxies-and-load-balancers.md` |
| D04-T020 | NAT, firewalls and ports | D04-T019, D04-T001, D01-T001, D01-T002, D03-T001, D03-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t020-nat-firewalls-and-ports.md` |
| D04-T021 | CDN and edge networking | D04-T020, D04-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t021-cdn-and-edge-networking.md` |
| D04-T022 | Connection pooling and keep-alive | D04-T021, D04-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t022-connection-pooling-and-keep-alive.md` |
| D04-T023 | Latency, bandwidth, throughput and packet loss | D04-T022, D04-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `03_COMPUTER_NETWORKS/notes/d04-t023-latency-bandwidth-throughput-and-packet-loss.md` |

## D05 — Backend Development Fundamentals

Folder: `04_BACKEND_FUNDAMENTALS`. Owner: Networking and API. Topics: 24.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D05-T001 | Client-server architecture | D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t001-client-server-architecture.md` |
| D05-T002 | Request-response lifecycle | D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t002-request-response-lifecycle.md` |
| D05-T003 | Routing and middleware | D05-T002, D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t003-routing-and-middleware.md` |
| D05-T004 | Controllers, services and repositories | D05-T003, D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t004-controllers-services-and-repositories.md` |
| D05-T005 | Dependency injection | D05-T004, D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t005-dependency-injection.md` |
| D05-T006 | Configuration and environment variables | D05-T005, D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t006-configuration-and-environment-variables.md` |
| D05-T007 | Input validation and sanitization | D05-T006, D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t007-input-validation-and-sanitization.md` |
| D05-T008 | Serialization and deserialization | D05-T007, D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t008-serialization-and-deserialization.md` |
| D05-T009 | Error handling and exception mapping | D05-T008, D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t009-error-handling-and-exception-mapping.md` |
| D05-T010 | Centralized logging | D05-T009, D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t010-centralized-logging.md` |
| D05-T011 | Authentication and authorization | D05-T010, D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t011-authentication-and-authorization.md` |
| D05-T012 | Pagination: offset vs cursor | D05-T011, D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t012-pagination-offset-vs-cursor.md` |
| D05-T013 | Filtering, sorting and searching | D05-T012, D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t013-filtering-sorting-and-searching.md` |
| D05-T014 | File uploads and downloads | D05-T013, D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t014-file-uploads-and-downloads.md` |
| D05-T015 | Background jobs | D05-T014, D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t015-background-jobs.md` |
| D05-T016 | Email, SMS and push notifications | D05-T015, D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t016-email-sms-and-push-notifications.md` |
| D05-T017 | Scheduled jobs and cron | D05-T016, D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t017-scheduled-jobs-and-cron.md` |
| D05-T018 | Graceful startup and shutdown | D05-T017, D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t018-graceful-startup-and-shutdown.md` |
| D05-T019 | Health checks and readiness checks | D05-T018, D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t019-health-checks-and-readiness-checks.md` |
| D05-T020 | API versioning | D05-T019, D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t020-api-versioning.md` |
| D05-T021 | Database connection pooling | D05-T020, D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t021-database-connection-pooling.md` |
| D05-T022 | Configuration and secret management | D05-T021, D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t022-configuration-and-secret-management.md` |
| D05-T023 | Request context and correlation IDs | D05-T022, D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t023-request-context-and-correlation-ids.md` |
| D05-T024 | Graceful degradation | D05-T023, D05-T001, D01-T001, D01-T002, D04-T001, D04-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `04_BACKEND_FUNDAMENTALS/notes/d05-t024-graceful-degradation.md` |

## D06 — API Design and REST

Folder: `05_API_DESIGN`. Owner: Networking and API. Topics: 21.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D06-T001 | REST architectural constraints | D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `05_API_DESIGN/notes/d06-t001-rest-architectural-constraints.md` |
| D06-T002 | Resource-oriented URL design | D06-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `05_API_DESIGN/notes/d06-t002-resource-oriented-url-design.md` |
| D06-T003 | HTTP methods and idempotency | D06-T002, D06-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `05_API_DESIGN/notes/d06-t003-http-methods-and-idempotency.md` |
| D06-T004 | HTTP status codes | D06-T003, D06-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `05_API_DESIGN/notes/d06-t004-http-status-codes.md` |
| D06-T005 | Request and response schemas | D06-T004, D06-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `05_API_DESIGN/notes/d06-t005-request-and-response-schemas.md` |
| D06-T006 | API contracts and schema evolution | D06-T005, D06-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `05_API_DESIGN/notes/d06-t006-api-contracts-and-schema-evolution.md` |
| D06-T007 | Path vs query vs header parameters | D06-T006, D06-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `05_API_DESIGN/notes/d06-t007-path-vs-query-vs-header-parameters.md` |
| D06-T008 | Validation and consistent error responses | D06-T007, D06-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `05_API_DESIGN/notes/d06-t008-validation-and-consistent-error-responses.md` |
| D06-T009 | Pagination, filtering and sorting | D06-T008, D06-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `05_API_DESIGN/notes/d06-t009-pagination-filtering-and-sorting.md` |
| D06-T010 | Versioning strategies | D06-T009, D06-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `05_API_DESIGN/notes/d06-t010-versioning-strategies.md` |
| D06-T011 | Idempotency keys | D06-T010, D06-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `05_API_DESIGN/notes/d06-t011-idempotency-keys.md` |
| D06-T012 | Rate limiting and quotas | D06-T011, D06-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `05_API_DESIGN/notes/d06-t012-rate-limiting-and-quotas.md` |
| D06-T013 | Conditional requests: ETag, If-Match | D06-T012, D06-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `05_API_DESIGN/notes/d06-t013-conditional-requests-etag-if-match.md` |
| D06-T014 | Caching: Cache-Control, ETag, Last-Modified | D06-T013, D06-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `05_API_DESIGN/notes/d06-t014-caching-cache-control-etag-last-modified.md` |
| D06-T015 | HATEOAS and when it is useful | D06-T014, D06-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `05_API_DESIGN/notes/d06-t015-hateoas-and-when-it-is-useful.md` |
| D06-T016 | OpenAPI and Swagger | D06-T015, D06-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `05_API_DESIGN/notes/d06-t016-openapi-and-swagger.md` |
| D06-T017 | API gateways | D06-T016, D06-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `05_API_DESIGN/notes/d06-t017-api-gateways.md` |
| D06-T018 | Webhooks and signature verification | D06-T017, D06-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `05_API_DESIGN/notes/d06-t018-webhooks-and-signature-verification.md` |
| D06-T019 | API deprecation strategies | D06-T018, D06-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `05_API_DESIGN/notes/d06-t019-api-deprecation-strategies.md` |
| D06-T020 | REST vs GraphQL vs gRPC vs RPC | D06-T019, D06-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `05_API_DESIGN/notes/d06-t020-rest-vs-graphql-vs-grpc-vs-rpc.md` |
| D06-T021 | API compatibility and backward compatibility | D06-T020, D06-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `05_API_DESIGN/notes/d06-t021-api-compatibility-and-backward-compatibility.md` |

## D07 — Database Fundamentals

Folder: `06_DATABASE_FUNDAMENTALS`. Owner: Database. Topics: 31.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D07-T001 | Relational vs non-relational databases | D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t001-relational-vs-non-relational-databases.md` |
| D07-T002 | Tables, rows, columns and schemas | D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t002-tables-rows-columns-and-schemas.md` |
| D07-T003 | Primary and foreign keys | D07-T002, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t003-primary-and-foreign-keys.md` |
| D07-T004 | Candidate, composite and surrogate keys | D07-T003, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t004-candidate-composite-and-surrogate-keys.md` |
| D07-T005 | Constraints and data integrity | D07-T004, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t005-constraints-and-data-integrity.md` |
| D07-T006 | Normalization: 1NF, 2NF, 3NF, BCNF | D07-T005, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t006-normalization-1nf-2nf-3nf-bcnf.md` |
| D07-T007 | Denormalization | D07-T006, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t007-denormalization.md` |
| D07-T008 | One-to-one, one-to-many, many-to-many relationships | D07-T007, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t008-one-to-one-one-to-many-many-to-many-relationships.md` |
| D07-T009 | Joins and subqueries | D07-T008, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t009-joins-and-subqueries.md` |
| D07-T010 | Aggregations and grouping | D07-T009, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t010-aggregations-and-grouping.md` |
| D07-T011 | Transactions | D07-T010, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t011-transactions.md` |
| D07-T012 | ACID properties | D07-T011, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t012-acid-properties.md` |
| D07-T013 | Isolation levels | D07-T012, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t013-isolation-levels.md` |
| D07-T014 | Dirty reads, non-repeatable reads, phantom reads | D07-T013, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t014-dirty-reads-non-repeatable-reads-phantom-reads.md` |
| D07-T015 | Locks and deadlocks | D07-T014, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t015-locks-and-deadlocks.md` |
| D07-T016 | Optimistic vs pessimistic concurrency control | D07-T015, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t016-optimistic-vs-pessimistic-concurrency-control.md` |
| D07-T017 | MVCC | D07-T016, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t017-mvcc.md` |
| D07-T018 | Database indexes | D07-T017, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t018-database-indexes.md` |
| D07-T019 | Composite and covering indexes | D07-T018, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t019-composite-and-covering-indexes.md` |
| D07-T020 | Clustered vs non-clustered indexes | D07-T019, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t020-clustered-vs-non-clustered-indexes.md` |
| D07-T021 | B-tree and hash indexes | D07-T020, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t021-b-tree-and-hash-indexes.md` |
| D07-T022 | Query execution plans | D07-T021, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t022-query-execution-plans.md` |
| D07-T023 | EXPLAIN and EXPLAIN ANALYZE | D07-T022, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t023-explain-and-explain-analyze.md` |
| D07-T024 | Slow query optimization | D07-T023, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t024-slow-query-optimization.md` |
| D07-T025 | Connection pooling | D07-T024, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t025-connection-pooling.md` |
| D07-T026 | Migrations and schema evolution | D07-T025, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t026-migrations-and-schema-evolution.md` |
| D07-T027 | Backup, restore and point-in-time recovery | D07-T026, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t027-backup-restore-and-point-in-time-recovery.md` |
| D07-T028 | Replication and failover | D07-T027, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t028-replication-and-failover.md` |
| D07-T029 | Partitioning and sharding | D07-T028, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t029-partitioning-and-sharding.md` |
| D07-T030 | Read replicas and read/write splitting | D07-T029, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t030-read-replicas-and-read-write-splitting.md` |
| D07-T031 | Data archival and retention | D07-T030, D07-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `06_DATABASE_FUNDAMENTALS/notes/d07-t031-data-archival-and-retention.md` |

## D08 — SQL — Advanced Topics

Folder: `07_ADVANCED_SQL`. Owner: Database. Topics: 23.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D08-T001 | Advanced joins | D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t001-advanced-joins.md` |
| D08-T002 | Correlated subqueries | D08-T001, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t002-correlated-subqueries.md` |
| D08-T003 | Common Table Expressions (CTEs) | D08-T002, D08-T001, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t003-common-table-expressions-ctes.md` |
| D08-T004 | Recursive CTEs | D08-T003, D08-T001, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t004-recursive-ctes.md` |
| D08-T005 | Window functions | D08-T004, D08-T001, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t005-window-functions.md` |
| D08-T006 | Ranking functions | D08-T005, D08-T001, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t006-ranking-functions.md` |
| D08-T007 | Running totals and moving averages | D08-T006, D08-T001, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t007-running-totals-and-moving-averages.md` |
| D08-T008 | CASE, COALESCE, NULLIF | D08-T007, D08-T001, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t008-case-coalesce-nullif.md` |
| D08-T009 | NULL semantics and three-valued logic | D08-T008, D08-T001, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t009-null-semantics-and-three-valued-logic.md` |
| D08-T010 | Upserts and conflict handling | D08-T009, D08-T001, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t010-upserts-and-conflict-handling.md` |
| D08-T011 | Transactions and savepoints | D08-T010, D08-T001, D07-T001, D07-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t011-transactions-and-savepoints.md` |
| D08-T012 | Locking reads | D08-T011, D08-T001, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t012-locking-reads.md` |
| D08-T013 | Advisory locks | D08-T012, D08-T001, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t013-advisory-locks.md` |
| D08-T014 | Generated and computed columns | D08-T013, D08-T001, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t014-generated-and-computed-columns.md` |
| D08-T015 | Views and materialized views | D08-T014, D08-T001, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t015-views-and-materialized-views.md` |
| D08-T016 | Stored procedures and triggers | D08-T015, D08-T001, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t016-stored-procedures-and-triggers.md` |
| D08-T017 | JSON and JSONB querying | D08-T016, D08-T001, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t017-json-and-jsonb-querying.md` |
| D08-T018 | Full-text search | D08-T017, D08-T001, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t018-full-text-search.md` |
| D08-T019 | Geospatial queries | D08-T018, D08-T001, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t019-geospatial-queries.md` |
| D08-T020 | Index selectivity and cardinality | D08-T019, D08-T001, D07-T001, D07-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t020-index-selectivity-and-cardinality.md` |
| D08-T021 | N+1 query problem | D08-T020, D08-T001, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t021-n-plus-1-query-problem.md` |
| D08-T022 | Keyset pagination | D08-T021, D08-T001, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t022-keyset-pagination.md` |
| D08-T023 | Database performance troubleshooting | D08-T022, D08-T001, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `07_ADVANCED_SQL/notes/d08-t023-database-performance-troubleshooting.md` |

## D09 — PostgreSQL Internals

Folder: `08_POSTGRESQL_INTERNALS`. Owner: Database. Topics: 18.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D09-T001 | PostgreSQL architecture | D07-T001, D07-T002, D08-T001, D08-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `08_POSTGRESQL_INTERNALS/notes/d09-t001-postgresql-architecture.md` |
| D09-T002 | MVCC and tuple visibility | D09-T001, D07-T001, D07-T002, D08-T001, D08-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `08_POSTGRESQL_INTERNALS/notes/d09-t002-mvcc-and-tuple-visibility.md` |
| D09-T003 | WAL (Write-Ahead Logging) | D09-T002, D09-T001, D07-T001, D07-T002, D08-T001, D08-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `08_POSTGRESQL_INTERNALS/notes/d09-t003-wal-write-ahead-logging.md` |
| D09-T004 | Checkpoints and crash recovery | D09-T003, D09-T001, D07-T001, D07-T002, D08-T001, D08-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `08_POSTGRESQL_INTERNALS/notes/d09-t004-checkpoints-and-crash-recovery.md` |
| D09-T005 | Vacuum and autovacuum | D09-T004, D09-T001, D07-T001, D07-T002, D08-T001, D08-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `08_POSTGRESQL_INTERNALS/notes/d09-t005-vacuum-and-autovacuum.md` |
| D09-T006 | Dead tuples and table bloat | D09-T005, D09-T001, D07-T001, D07-T002, D08-T001, D08-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `08_POSTGRESQL_INTERNALS/notes/d09-t006-dead-tuples-and-table-bloat.md` |
| D09-T007 | Heap storage and TOAST | D09-T006, D09-T001, D07-T001, D07-T002, D08-T001, D08-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `08_POSTGRESQL_INTERNALS/notes/d09-t007-heap-storage-and-toast.md` |
| D09-T008 | B-tree, GIN, GiST and BRIN indexes | D09-T007, D09-T001, D07-T001, D07-T002, D08-T001, D08-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `08_POSTGRESQL_INTERNALS/notes/d09-t008-b-tree-gin-gist-and-brin-indexes.md` |
| D09-T009 | Query planner and optimizer | D09-T008, D09-T001, D07-T001, D07-T002, D08-T001, D08-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `08_POSTGRESQL_INTERNALS/notes/d09-t009-query-planner-and-optimizer.md` |
| D09-T010 | Statistics and ANALYZE | D09-T009, D09-T001, D07-T001, D07-T002, D08-T001, D08-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `08_POSTGRESQL_INTERNALS/notes/d09-t010-statistics-and-analyze.md` |
| D09-T011 | Isolation and row-level locking | D09-T010, D09-T001, D07-T001, D07-T002, D08-T001, D08-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `08_POSTGRESQL_INTERNALS/notes/d09-t011-isolation-and-row-level-locking.md` |
| D09-T012 | Advisory locks | D09-T011, D09-T001, D07-T001, D07-T002, D08-T001, D08-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `08_POSTGRESQL_INTERNALS/notes/d09-t012-advisory-locks.md` |
| D09-T013 | Streaming and logical replication | D09-T012, D09-T001, D07-T001, D07-T002, D08-T001, D08-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `08_POSTGRESQL_INTERNALS/notes/d09-t013-streaming-and-logical-replication.md` |
| D09-T014 | Table partitioning | D09-T013, D09-T001, D07-T001, D07-T002, D08-T001, D08-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `08_POSTGRESQL_INTERNALS/notes/d09-t014-table-partitioning.md` |
| D09-T015 | Connection poolers | D09-T014, D09-T001, D07-T001, D07-T002, D08-T001, D08-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `08_POSTGRESQL_INTERNALS/notes/d09-t015-connection-poolers.md` |
| D09-T016 | Replication lag | D09-T015, D09-T001, D07-T001, D07-T002, D08-T001, D08-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `08_POSTGRESQL_INTERNALS/notes/d09-t016-replication-lag.md` |
| D09-T017 | Backup and recovery | D09-T016, D09-T001, D07-T001, D07-T002, D08-T001, D08-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `08_POSTGRESQL_INTERNALS/notes/d09-t017-backup-and-recovery.md` |
| D09-T018 | High availability and failover | D09-T017, D09-T001, D07-T001, D07-T002, D08-T001, D08-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `08_POSTGRESQL_INTERNALS/notes/d09-t018-high-availability-and-failover.md` |

## D10 — NoSQL Databases

Folder: `09_NOSQL_DATABASES`. Owner: Database. Topics: 19.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D10-T001 | SQL vs NoSQL trade-offs | D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `09_NOSQL_DATABASES/notes/d10-t001-sql-vs-nosql-trade-offs.md` |
| D10-T002 | Key-value stores | D10-T001, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `09_NOSQL_DATABASES/notes/d10-t002-key-value-stores.md` |
| D10-T003 | Document databases | D10-T002, D10-T001, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `09_NOSQL_DATABASES/notes/d10-t003-document-databases.md` |
| D10-T004 | Wide-column databases | D10-T003, D10-T001, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `09_NOSQL_DATABASES/notes/d10-t004-wide-column-databases.md` |
| D10-T005 | Graph databases | D10-T004, D10-T001, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `09_NOSQL_DATABASES/notes/d10-t005-graph-databases.md` |
| D10-T006 | Data modeling for access patterns | D10-T005, D10-T001, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `09_NOSQL_DATABASES/notes/d10-t006-data-modeling-for-access-patterns.md` |
| D10-T007 | Denormalization and embedding vs referencing | D10-T006, D10-T001, D07-T001, D07-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `09_NOSQL_DATABASES/notes/d10-t007-denormalization-and-embedding-vs-referencing.md` |
| D10-T008 | Secondary indexes | D10-T007, D10-T001, D07-T001, D07-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `09_NOSQL_DATABASES/notes/d10-t008-secondary-indexes.md` |
| D10-T009 | TTL and expiration | D10-T008, D10-T001, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `09_NOSQL_DATABASES/notes/d10-t009-ttl-and-expiration.md` |
| D10-T010 | Consistency models | D10-T009, D10-T001, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `09_NOSQL_DATABASES/notes/d10-t010-consistency-models.md` |
| D10-T011 | Partition keys and hot partitions | D10-T010, D10-T001, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `09_NOSQL_DATABASES/notes/d10-t011-partition-keys-and-hot-partitions.md` |
| D10-T012 | Replication and sharding | D10-T011, D10-T001, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `09_NOSQL_DATABASES/notes/d10-t012-replication-and-sharding.md` |
| D10-T013 | Quorums | D10-T012, D10-T001, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `09_NOSQL_DATABASES/notes/d10-t013-quorums.md` |
| D10-T014 | Eventual consistency | D10-T013, D10-T001, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `09_NOSQL_DATABASES/notes/d10-t014-eventual-consistency.md` |
| D10-T015 | MongoDB indexes and aggregation pipelines | D10-T014, D10-T001, D07-T001, D07-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `09_NOSQL_DATABASES/notes/d10-t015-mongodb-indexes-and-aggregation-pipelines.md` |
| D10-T016 | MongoDB transactions | D10-T015, D10-T001, D07-T001, D07-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `09_NOSQL_DATABASES/notes/d10-t016-mongodb-transactions.md` |
| D10-T017 | DynamoDB partition and sort keys | D10-T016, D10-T001, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `09_NOSQL_DATABASES/notes/d10-t017-dynamodb-partition-and-sort-keys.md` |
| D10-T018 | Cassandra data modeling | D10-T017, D10-T001, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `09_NOSQL_DATABASES/notes/d10-t018-cassandra-data-modeling.md` |
| D10-T019 | Choosing the right database for a workload | D10-T018, D10-T001, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `09_NOSQL_DATABASES/notes/d10-t019-choosing-the-right-database-for-a-workload.md` |

## D11 — Redis and Caching

Folder: `10_REDIS_AND_CACHING`. Owner: Database. Topics: 25.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D11-T001 | Why caching works | D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t001-why-caching-works.md` |
| D11-T002 | Cache hit ratio and cache efficiency | D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t002-cache-hit-ratio-and-cache-efficiency.md` |
| D11-T003 | Cache-aside | D11-T002, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t003-cache-aside.md` |
| D11-T004 | Read-through and write-through | D11-T003, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t004-read-through-and-write-through.md` |
| D11-T005 | Write-behind and write-around | D11-T004, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t005-write-behind-and-write-around.md` |
| D11-T006 | TTL and expiration | D11-T005, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t006-ttl-and-expiration.md` |
| D11-T007 | Cache invalidation | D11-T006, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t007-cache-invalidation.md` |
| D11-T008 | Cache stampede | D11-T007, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t008-cache-stampede.md` |
| D11-T009 | Cache penetration | D11-T008, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t009-cache-penetration.md` |
| D11-T010 | Cache avalanche | D11-T009, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t010-cache-avalanche.md` |
| D11-T011 | Hot keys and key design | D11-T010, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t011-hot-keys-and-key-design.md` |
| D11-T012 | Redis strings, hashes, lists, sets, sorted sets | D11-T011, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t012-redis-strings-hashes-lists-sets-sorted-sets.md` |
| D11-T013 | Redis Streams | D11-T012, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t013-redis-streams.md` |
| D11-T014 | Pub/Sub | D11-T013, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t014-pub-sub.md` |
| D11-T015 | Persistence: RDB and AOF | D11-T014, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t015-persistence-rdb-and-aof.md` |
| D11-T016 | Eviction policies | D11-T015, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t016-eviction-policies.md` |
| D11-T017 | Redis transactions and Lua scripts | D11-T016, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t017-redis-transactions-and-lua-scripts.md` |
| D11-T018 | Distributed locks and their limitations | D11-T017, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t018-distributed-locks-and-their-limitations.md` |
| D11-T019 | Rate limiting with Redis | D11-T018, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t019-rate-limiting-with-redis.md` |
| D11-T020 | Sliding-window counters | D11-T019, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t020-sliding-window-counters.md` |
| D11-T021 | Leaderboards and ranking | D11-T020, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t021-leaderboards-and-ranking.md` |
| D11-T022 | Redis replication and Sentinel | D11-T021, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t022-redis-replication-and-sentinel.md` |
| D11-T023 | Redis Cluster | D11-T022, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t023-redis-cluster.md` |
| D11-T024 | Cache consistency with a primary database | D11-T023, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t024-cache-consistency-with-a-primary-database.md` |
| D11-T025 | When not to use caching | D11-T024, D11-T001, D07-T001, D07-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `10_REDIS_AND_CACHING/notes/d11-t025-when-not-to-use-caching.md` |

## D12 — Authentication, Authorization and Security

Folder: `11_SECURITY`. Owner: Security. Topics: 31.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D12-T001 | Authentication vs authorization | D04-T001, D04-T002, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t001-authentication-vs-authorization.md` |
| D12-T002 | Sessions and cookies | D12-T001, D04-T001, D04-T002, D05-T001, D05-T002, D06-T001 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t002-sessions-and-cookies.md` |
| D12-T003 | JWT structure and validation | D12-T002, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t003-jwt-structure-and-validation.md` |
| D12-T004 | Access and refresh tokens | D12-T003, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t004-access-and-refresh-tokens.md` |
| D12-T005 | OAuth 2.0 | D12-T004, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t005-oauth-2-0.md` |
| D12-T006 | OpenID Connect | D12-T005, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t006-openid-connect.md` |
| D12-T007 | SSO and identity providers | D12-T006, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t007-sso-and-identity-providers.md` |
| D12-T008 | RBAC and ABAC | D12-T007, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t008-rbac-and-abac.md` |
| D12-T009 | Multi-factor authentication | D12-T008, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t009-multi-factor-authentication.md` |
| D12-T010 | Password hashing: Argon2, bcrypt | D12-T009, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t010-password-hashing-argon2-bcrypt.md` |
| D12-T011 | Password reset and account recovery | D12-T010, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t011-password-reset-and-account-recovery.md` |
| D12-T012 | API keys and service credentials | D12-T011, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t012-api-keys-and-service-credentials.md` |
| D12-T013 | TLS and certificate validation | D12-T012, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t013-tls-and-certificate-validation.md` |
| D12-T014 | CORS and preflight requests | D12-T013, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t014-cors-and-preflight-requests.md` |
| D12-T015 | CSRF | D12-T014, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t015-csrf.md` |
| D12-T016 | XSS | D12-T015, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t016-xss.md` |
| D12-T017 | SQL and NoSQL injection | D12-T016, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t017-sql-and-nosql-injection.md` |
| D12-T018 | SSRF | D12-T017, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t018-ssrf.md` |
| D12-T019 | Path traversal | D12-T018, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t019-path-traversal.md` |
| D12-T020 | Broken access control and IDOR/BOLA | D12-T019, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t020-broken-access-control-and-idor-bola.md` |
| D12-T021 | Request smuggling | D12-T020, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t021-request-smuggling.md` |
| D12-T022 | Replay attacks | D12-T021, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t022-replay-attacks.md` |
| D12-T023 | Rate limiting and brute-force protection | D12-T022, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t023-rate-limiting-and-brute-force-protection.md` |
| D12-T024 | Input validation and output encoding | D12-T023, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t024-input-validation-and-output-encoding.md` |
| D12-T025 | Secrets management and rotation | D12-T024, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t025-secrets-management-and-rotation.md` |
| D12-T026 | Encryption at rest and in transit | D12-T025, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t026-encryption-at-rest-and-in-transit.md` |
| D12-T027 | Audit logging | D12-T026, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t027-audit-logging.md` |
| D12-T028 | OWASP Top 10 | D12-T027, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t028-owasp-top-10.md` |
| D12-T029 | Least privilege and zero-trust principles | D12-T028, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t029-least-privilege-and-zero-trust-principles.md` |
| D12-T030 | Dependency and supply-chain security | D12-T029, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t030-dependency-and-supply-chain-security.md` |
| D12-T031 | Threat modeling and security testing | D12-T030, D12-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `11_SECURITY/notes/d12-t031-threat-modeling-and-security-testing.md` |

## D13 — Concurrency and Parallel Processing

Folder: `12_CONCURRENCY`. Owner: Programming and Algorithms. Topics: 22.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D13-T001 | Threads vs processes | D01-T001, D01-T002, D03-T001, D03-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `12_CONCURRENCY/notes/d13-t001-threads-vs-processes.md` |
| D13-T002 | Async/await | D13-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `12_CONCURRENCY/notes/d13-t002-async-await.md` |
| D13-T003 | Event-driven concurrency | D13-T002, D13-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `12_CONCURRENCY/notes/d13-t003-event-driven-concurrency.md` |
| D13-T004 | Thread pools and worker pools | D13-T003, D13-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `12_CONCURRENCY/notes/d13-t004-thread-pools-and-worker-pools.md` |
| D13-T005 | Futures and promises | D13-T004, D13-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `12_CONCURRENCY/notes/d13-t005-futures-and-promises.md` |
| D13-T006 | Race conditions and atomicity | D13-T005, D13-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `12_CONCURRENCY/notes/d13-t006-race-conditions-and-atomicity.md` |
| D13-T007 | Mutexes and semaphores | D13-T006, D13-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `12_CONCURRENCY/notes/d13-t007-mutexes-and-semaphores.md` |
| D13-T008 | Read-write locks | D13-T007, D13-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `12_CONCURRENCY/notes/d13-t008-read-write-locks.md` |
| D13-T009 | Lock-free programming basics | D13-T008, D13-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `12_CONCURRENCY/notes/d13-t009-lock-free-programming-basics.md` |
| D13-T010 | Producer-consumer pattern | D13-T009, D13-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `12_CONCURRENCY/notes/d13-t010-producer-consumer-pattern.md` |
| D13-T011 | Bounded queues and backpressure | D13-T010, D13-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `12_CONCURRENCY/notes/d13-t011-bounded-queues-and-backpressure.md` |
| D13-T012 | Concurrent collections | D13-T011, D13-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `12_CONCURRENCY/notes/d13-t012-concurrent-collections.md` |
| D13-T013 | Deadlock prevention | D13-T012, D13-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `12_CONCURRENCY/notes/d13-t013-deadlock-prevention.md` |
| D13-T014 | Task scheduling | D13-T013, D13-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `12_CONCURRENCY/notes/d13-t014-task-scheduling.md` |
| D13-T015 | CPU-bound vs I/O-bound workloads | D13-T014, D13-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `12_CONCURRENCY/notes/d13-t015-cpu-bound-vs-i-o-bound-workloads.md` |
| D13-T016 | Python GIL and multiprocessing | D13-T015, D13-T001, D01-T001, D01-T002, D03-T001, D03-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `12_CONCURRENCY/notes/d13-t016-python-gil-and-multiprocessing.md` |
| D13-T017 | Java memory model | D13-T016, D13-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `12_CONCURRENCY/notes/d13-t017-java-memory-model.md` |
| D13-T018 | Go goroutines and channels | D13-T017, D13-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `12_CONCURRENCY/notes/d13-t018-go-goroutines-and-channels.md` |
| D13-T019 | Node.js event loop and worker threads | D13-T018, D13-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `12_CONCURRENCY/notes/d13-t019-node-js-event-loop-and-worker-threads.md` |
| D13-T020 | Concurrency limits and bulkheads | D13-T019, D13-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `12_CONCURRENCY/notes/d13-t020-concurrency-limits-and-bulkheads.md` |
| D13-T021 | Cancellation and timeouts | D13-T020, D13-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `12_CONCURRENCY/notes/d13-t021-cancellation-and-timeouts.md` |
| D13-T022 | Structured concurrency concepts | D13-T021, D13-T001, D01-T001, D01-T002, D03-T001, D03-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `12_CONCURRENCY/notes/d13-t022-structured-concurrency-concepts.md` |

## D14 — Messaging and Event-Driven Architecture

Folder: `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE`. Owner: Messaging and Distributed Systems. Topics: 32.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D14-T001 | Message queues vs event streams | D04-T001, D04-T002, D05-T001, D05-T002, D13-T001, D13-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t001-message-queues-vs-event-streams.md` |
| D14-T002 | Synchronous vs asynchronous communication | D14-T001, D04-T001, D04-T002, D05-T001, D05-T002, D13-T001 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t002-synchronous-vs-asynchronous-communication.md` |
| D14-T003 | Kafka architecture | D14-T002, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t003-kafka-architecture.md` |
| D14-T004 | Topics, partitions and offsets | D14-T003, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t004-topics-partitions-and-offsets.md` |
| D14-T005 | Producers and consumers | D14-T004, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t005-producers-and-consumers.md` |
| D14-T006 | Consumer groups and rebalancing | D14-T005, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t006-consumer-groups-and-rebalancing.md` |
| D14-T007 | Partition keys and ordering | D14-T006, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t007-partition-keys-and-ordering.md` |
| D14-T008 | Replication and ISR | D14-T007, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t008-replication-and-isr.md` |
| D14-T009 | Delivery semantics: at-most-once, at-least-once, exactly-once | D14-T008, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t009-delivery-semantics-at-most-once-at-least-once-exactly-once.md` |
| D14-T010 | Idempotent producers | D14-T009, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t010-idempotent-producers.md` |
| D14-T011 | Idempotent consumers | D14-T010, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t011-idempotent-consumers.md` |
| D14-T012 | Retries and retry topics | D14-T011, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t012-retries-and-retry-topics.md` |
| D14-T013 | Dead-letter queues (DLQs) | D14-T012, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t013-dead-letter-queues-dlqs.md` |
| D14-T014 | Delayed messages | D14-T013, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t014-delayed-messages.md` |
| D14-T015 | Backpressure and consumer lag | D14-T014, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t015-backpressure-and-consumer-lag.md` |
| D14-T016 | Offset commits | D14-T015, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t016-offset-commits.md` |
| D14-T017 | Message schemas and schema registry | D14-T016, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t017-message-schemas-and-schema-registry.md` |
| D14-T018 | Schema evolution and compatibility | D14-T017, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t018-schema-evolution-and-compatibility.md` |
| D14-T019 | Event sourcing | D14-T018, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t019-event-sourcing.md` |
| D14-T020 | CQRS | D14-T019, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t020-cqrs.md` |
| D14-T021 | Transactional outbox | D14-T020, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t021-transactional-outbox.md` |
| D14-T022 | CDC (Change Data Capture) | D14-T021, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t022-cdc-change-data-capture.md` |
| D14-T023 | Sagas and compensating actions | D14-T022, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t023-sagas-and-compensating-actions.md` |
| D14-T024 | RabbitMQ exchanges, queues and bindings | D14-T023, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t024-rabbitmq-exchanges-queues-and-bindings.md` |
| D14-T025 | Acknowledgments and redelivery | D14-T024, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t025-acknowledgments-and-redelivery.md` |
| D14-T026 | RabbitMQ vs Kafka | D14-T025, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t026-rabbitmq-vs-kafka.md` |
| D14-T027 | Pub/Sub systems | D14-T026, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t027-pub-sub-systems.md` |
| D14-T028 | Ordering guarantees | D14-T027, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t028-ordering-guarantees.md` |
| D14-T029 | Poison messages | D14-T028, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t029-poison-messages.md` |
| D14-T030 | Message deduplication | D14-T029, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t030-message-deduplication.md` |
| D14-T031 | Replay and reprocessing | D14-T030, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t031-replay-and-reprocessing.md` |
| D14-T032 | Workflow orchestration vs choreography | D14-T031, D14-T001, D04-T001, D04-T002, D05-T001, D05-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `13_MESSAGING_AND_EVENT_DRIVEN_ARCHITECTURE/notes/d14-t032-workflow-orchestration-vs-choreography.md` |

## D15 — Distributed Systems

Folder: `14_DISTRIBUTED_SYSTEMS`. Owner: Messaging and Distributed Systems. Topics: 34.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D15-T001 | Distributed system fundamentals | D03-T001, D03-T002, D04-T001, D04-T002, D13-T001, D13-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t001-distributed-system-fundamentals.md` |
| D15-T002 | Partial failures | D15-T001, D03-T001, D03-T002, D04-T001, D04-T002, D13-T001 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t002-partial-failures.md` |
| D15-T003 | Network partitions | D15-T002, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t003-network-partitions.md` |
| D15-T004 | CAP theorem | D15-T003, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t004-cap-theorem.md` |
| D15-T005 | PACELC theorem | D15-T004, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t005-pacelc-theorem.md` |
| D15-T006 | Strong, eventual and causal consistency | D15-T005, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t006-strong-eventual-and-causal-consistency.md` |
| D15-T007 | Linearizability and sequential consistency | D15-T006, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t007-linearizability-and-sequential-consistency.md` |
| D15-T008 | Availability and fault tolerance | D15-T007, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t008-availability-and-fault-tolerance.md` |
| D15-T009 | Replication strategies | D15-T008, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t009-replication-strategies.md` |
| D15-T010 | Leader-follower architecture | D15-T009, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t010-leader-follower-architecture.md` |
| D15-T011 | Leader election | D15-T010, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t011-leader-election.md` |
| D15-T012 | Quorum reads and writes | D15-T011, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t012-quorum-reads-and-writes.md` |
| D15-T013 | Split-brain scenarios | D15-T012, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t013-split-brain-scenarios.md` |
| D15-T014 | Consensus: Raft and Paxos concepts | D15-T013, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t014-consensus-raft-and-paxos-concepts.md` |
| D15-T015 | Distributed locking | D15-T014, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t015-distributed-locking.md` |
| D15-T016 | Clock skew and clock synchronization | D15-T015, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t016-clock-skew-and-clock-synchronization.md` |
| D15-T017 | Logical clocks and vector clocks | D15-T016, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t017-logical-clocks-and-vector-clocks.md` |
| D15-T018 | At-most-once and at-least-once execution | D15-T017, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t018-at-most-once-and-at-least-once-execution.md` |
| D15-T019 | Idempotency | D15-T018, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t019-idempotency.md` |
| D15-T020 | Exactly-once processing limitations | D15-T019, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t020-exactly-once-processing-limitations.md` |
| D15-T021 | Retries, timeouts and exponential backoff | D15-T020, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t021-retries-timeouts-and-exponential-backoff.md` |
| D15-T022 | Jitter and retry storms | D15-T021, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t022-jitter-and-retry-storms.md` |
| D15-T023 | Circuit breakers | D15-T022, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t023-circuit-breakers.md` |
| D15-T024 | Bulkheads | D15-T023, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t024-bulkheads.md` |
| D15-T025 | Failover and recovery | D15-T024, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t025-failover-and-recovery.md` |
| D15-T026 | Service discovery | D15-T025, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t026-service-discovery.md` |
| D15-T027 | Heartbeats and failure detection | D15-T026, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t027-heartbeats-and-failure-detection.md` |
| D15-T028 | Distributed transactions | D15-T027, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t028-distributed-transactions.md` |
| D15-T029 | Two-phase commit | D15-T028, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t029-two-phase-commit.md` |
| D15-T030 | Sagas | D15-T029, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t030-sagas.md` |
| D15-T031 | Data partitioning and rebalancing | D15-T030, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t031-data-partitioning-and-rebalancing.md` |
| D15-T032 | Hotspots and load skew | D15-T031, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t032-hotspots-and-load-skew.md` |
| D15-T033 | Split-brain prevention | D15-T032, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t033-split-brain-prevention.md` |
| D15-T034 | Graceful degradation | D15-T033, D15-T001, D03-T001, D03-T002, D04-T001, D04-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `14_DISTRIBUTED_SYSTEMS/notes/d15-t034-graceful-degradation.md` |

## D16 — System Design Fundamentals

Folder: `15_SYSTEM_DESIGN_FUNDAMENTALS`. Owner: Architecture and System Design. Topics: 33.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D16-T001 | Functional requirements | D05-T001, D05-T002, D06-T001, D06-T002, D07-T001, D07-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t001-functional-requirements.md` |
| D16-T002 | Non-functional requirements | D16-T001, D05-T001, D05-T002, D06-T001, D06-T002, D07-T001 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t002-non-functional-requirements.md` |
| D16-T003 | Requirement clarification | D16-T002, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t003-requirement-clarification.md` |
| D16-T004 | Capacity estimation | D16-T003, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t004-capacity-estimation.md` |
| D16-T005 | QPS and peak traffic estimation | D16-T004, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t005-qps-and-peak-traffic-estimation.md` |
| D16-T006 | Bandwidth and storage estimation | D16-T005, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t006-bandwidth-and-storage-estimation.md` |
| D16-T007 | Latency budgets | D16-T006, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t007-latency-budgets.md` |
| D16-T008 | SLOs and availability targets | D16-T007, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t008-slos-and-availability-targets.md` |
| D16-T009 | API and data model design | D16-T008, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t009-api-and-data-model-design.md` |
| D16-T010 | High-level architecture diagrams | D16-T009, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t010-high-level-architecture-diagrams.md` |
| D16-T011 | Low-level design | D16-T010, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t011-low-level-design.md` |
| D16-T012 | Monolith vs modular monolith vs microservices | D16-T011, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t012-monolith-vs-modular-monolith-vs-microservices.md` |
| D16-T013 | Layered architecture | D16-T012, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t013-layered-architecture.md` |
| D16-T014 | Hexagonal / ports-and-adapters architecture | D16-T013, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t014-hexagonal-ports-and-adapters-architecture.md` |
| D16-T015 | Clean architecture | D16-T014, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t015-clean-architecture.md` |
| D16-T016 | Domain-driven design (DDD) | D16-T015, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t016-domain-driven-design-ddd.md` |
| D16-T017 | Bounded contexts and aggregates | D16-T016, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t017-bounded-contexts-and-aggregates.md` |
| D16-T018 | SOLID principles | D16-T017, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t018-solid-principles.md` |
| D16-T019 | Design patterns | D16-T018, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t019-design-patterns.md` |
| D16-T020 | Separation of concerns | D16-T019, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t020-separation-of-concerns.md` |
| D16-T021 | Stateless vs stateful services | D16-T020, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t021-stateless-vs-stateful-services.md` |
| D16-T022 | Horizontal vs vertical scaling | D16-T021, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t022-horizontal-vs-vertical-scaling.md` |
| D16-T023 | Load balancing | D16-T022, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t023-load-balancing.md` |
| D16-T024 | Caching layers | D16-T023, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t024-caching-layers.md` |
| D16-T025 | Database selection | D16-T024, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t025-database-selection.md` |
| D16-T026 | Replication and partitioning | D16-T025, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t026-replication-and-partitioning.md` |
| D16-T027 | Synchronous vs asynchronous workflows | D16-T026, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t027-synchronous-vs-asynchronous-workflows.md` |
| D16-T028 | Single points of failure | D16-T027, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t028-single-points-of-failure.md` |
| D16-T029 | Failure scenarios and recovery | D16-T028, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t029-failure-scenarios-and-recovery.md` |
| D16-T030 | Consistency vs availability trade-offs | D16-T029, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t030-consistency-vs-availability-trade-offs.md` |
| D16-T031 | Cost optimization | D16-T030, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t031-cost-optimization.md` |
| D16-T032 | Security and observability | D16-T031, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t032-security-and-observability.md` |
| D16-T033 | Architecture decision records (ADRs) | D16-T032, D16-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `15_SYSTEM_DESIGN_FUNDAMENTALS/notes/d16-t033-architecture-decision-records-adrs.md` |

## D17 — Common System Design Problems

Folder: `16_SYSTEM_DESIGN_PROBLEMS`. Owner: Architecture and System Design. Topics: 36.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D17-T001 | URL shortener | D16-T001, D16-T002, D07-T001, D07-T002, D11-T001, D11-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t001-url-shortener.md` |
| D17-T002 | Rate limiter | D17-T001, D16-T001, D16-T002, D07-T001, D07-T002, D11-T001 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t002-rate-limiter.md` |
| D17-T003 | API gateway | D17-T002, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t003-api-gateway.md` |
| D17-T004 | Notification service | D17-T003, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t004-notification-service.md` |
| D17-T005 | Email delivery system | D17-T004, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t005-email-delivery-system.md` |
| D17-T006 | Chat application | D17-T005, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t006-chat-application.md` |
| D17-T007 | WhatsApp/Telegram-like messaging | D17-T006, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t007-whatsapp-telegram-like-messaging.md` |
| D17-T008 | Slack-like multi-tenant application | D17-T007, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t008-slack-like-multi-tenant-application.md` |
| D17-T009 | Social media news feed | D17-T008, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t009-social-media-news-feed.md` |
| D17-T010 | File storage / Google Drive | D17-T009, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t010-file-storage-google-drive.md` |
| D17-T011 | S3-style object storage | D17-T010, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t011-s3-style-object-storage.md` |
| D17-T012 | Video streaming platform | D17-T011, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t012-video-streaming-platform.md` |
| D17-T013 | Search autocomplete | D17-T012, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t013-search-autocomplete.md` |
| D17-T014 | Web crawler | D17-T013, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t014-web-crawler.md` |
| D17-T015 | E-commerce platform | D17-T014, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t015-e-commerce-platform.md` |
| D17-T016 | Amazon-like order management | D17-T015, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t016-amazon-like-order-management.md` |
| D17-T017 | Inventory management | D17-T016, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t017-inventory-management.md` |
| D17-T018 | Payment processing system | D17-T017, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t018-payment-processing-system.md` |
| D17-T019 | Ticket booking system | D17-T018, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t019-ticket-booking-system.md` |
| D17-T020 | Ride-hailing service | D17-T019, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t020-ride-hailing-service.md` |
| D17-T021 | Food delivery platform | D17-T020, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t021-food-delivery-platform.md` |
| D17-T022 | Hotel reservation system | D17-T021, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t022-hotel-reservation-system.md` |
| D17-T023 | Job scheduler | D17-T022, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t023-job-scheduler.md` |
| D17-T024 | Distributed task queue | D17-T023, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t024-distributed-task-queue.md` |
| D17-T025 | Logging and metrics platform | D17-T024, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t025-logging-and-metrics-platform.md` |
| D17-T026 | Metrics monitoring system | D17-T025, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t026-metrics-monitoring-system.md` |
| D17-T027 | Feature flag service | D17-T026, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t027-feature-flag-service.md` |
| D17-T028 | Distributed cache | D17-T027, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t028-distributed-cache.md` |
| D17-T029 | Recommendation system | D17-T028, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t029-recommendation-system.md` |
| D17-T030 | Multi-tenant SaaS platform | D17-T029, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t030-multi-tenant-saas-platform.md` |
| D17-T031 | Real-time location tracking | D17-T030, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t031-real-time-location-tracking.md` |
| D17-T032 | Leaderboard service | D17-T031, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t032-leaderboard-service.md` |
| D17-T033 | Webhook delivery platform | D17-T032, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t033-webhook-delivery-platform.md` |
| D17-T034 | Audit log service | D17-T033, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t034-audit-log-service.md` |
| D17-T035 | Search engine | D17-T034, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t035-search-engine.md` |
| D17-T036 | AI/RAG inference service | D17-T035, D17-T001, D16-T001, D16-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `16_SYSTEM_DESIGN_PROBLEMS/notes/d17-t036-ai-rag-inference-service.md` |

## D18 — Low-Level Design (LLD) and Object-Oriented Design

Folder: `17_LOW_LEVEL_DESIGN`. Owner: Architecture and System Design. Topics: 28.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D18-T001 | SOLID principles | D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t001-solid-principles.md` |
| D18-T002 | DRY, KISS and YAGNI | D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t002-dry-kiss-and-yagni.md` |
| D18-T003 | Encapsulation and composition | D18-T002, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t003-encapsulation-and-composition.md` |
| D18-T004 | Interfaces and abstractions | D18-T003, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t004-interfaces-and-abstractions.md` |
| D18-T005 | Dependency inversion and injection | D18-T004, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t005-dependency-inversion-and-injection.md` |
| D18-T006 | UML class and sequence diagrams | D18-T005, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t006-uml-class-and-sequence-diagrams.md` |
| D18-T007 | Class responsibility and collaboration | D18-T006, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t007-class-responsibility-and-collaboration.md` |
| D18-T008 | Object lifecycle and ownership | D18-T007, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t008-object-lifecycle-and-ownership.md` |
| D18-T009 | Factory and Abstract Factory | D18-T008, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t009-factory-and-abstract-factory.md` |
| D18-T010 | Builder | D18-T009, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t010-builder.md` |
| D18-T011 | Singleton and its pitfalls | D18-T010, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t011-singleton-and-its-pitfalls.md` |
| D18-T012 | Prototype | D18-T011, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t012-prototype.md` |
| D18-T013 | Strategy | D18-T012, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t013-strategy.md` |
| D18-T014 | Observer | D18-T013, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t014-observer.md` |
| D18-T015 | Adapter | D18-T014, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t015-adapter.md` |
| D18-T016 | Decorator | D18-T015, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t016-decorator.md` |
| D18-T017 | Facade | D18-T016, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t017-facade.md` |
| D18-T018 | Proxy | D18-T017, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t018-proxy.md` |
| D18-T019 | Command | D18-T018, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t019-command.md` |
| D18-T020 | State | D18-T019, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t020-state.md` |
| D18-T021 | Template Method | D18-T020, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t021-template-method.md` |
| D18-T022 | Chain of Responsibility | D18-T021, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t022-chain-of-responsibility.md` |
| D18-T023 | Repository and Unit of Work | D18-T022, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t023-repository-and-unit-of-work.md` |
| D18-T024 | Dependency injection containers | D18-T023, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t024-dependency-injection-containers.md` |
| D18-T025 | Extensibility and testability | D18-T024, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t025-extensibility-and-testability.md` |
| D18-T026 | Concurrency-safe object design | D18-T025, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t026-concurrency-safe-object-design.md` |
| D18-T027 | Domain modeling and invariants | D18-T026, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t027-domain-modeling-and-invariants.md` |
| D18-T028 | Refactoring and avoiding overengineering | D18-T027, D18-T001, D01-T001, D01-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `17_LOW_LEVEL_DESIGN/notes/d18-t028-refactoring-and-avoiding-overengineering.md` |

## D19 — Microservices Architecture

Folder: `18_MICROSERVICES`. Owner: Architecture and System Design. Topics: 30.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D19-T001 | Microservices principles | D15-T001, D15-T002, D16-T001, D16-T002, D14-T001, D14-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t001-microservices-principles.md` |
| D19-T002 | Service boundaries | D19-T001, D15-T001, D15-T002, D16-T001, D16-T002, D14-T001 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t002-service-boundaries.md` |
| D19-T003 | Domain-driven decomposition | D19-T002, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t003-domain-driven-decomposition.md` |
| D19-T004 | API gateway patterns | D19-T003, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t004-api-gateway-patterns.md` |
| D19-T005 | Service discovery | D19-T004, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t005-service-discovery.md` |
| D19-T006 | Inter-service communication | D19-T005, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t006-inter-service-communication.md` |
| D19-T007 | REST vs gRPC between services | D19-T006, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t007-rest-vs-grpc-between-services.md` |
| D19-T008 | Synchronous vs asynchronous calls | D19-T007, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t008-synchronous-vs-asynchronous-calls.md` |
| D19-T009 | Centralized configuration | D19-T008, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t009-centralized-configuration.md` |
| D19-T010 | Distributed tracing | D19-T009, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t010-distributed-tracing.md` |
| D19-T011 | Service authentication | D19-T010, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t011-service-authentication.md` |
| D19-T012 | Resilience patterns | D19-T011, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t012-resilience-patterns.md` |
| D19-T013 | Circuit breakers and bulkheads | D19-T012, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t013-circuit-breakers-and-bulkheads.md` |
| D19-T014 | Timeouts and retries | D19-T013, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t014-timeouts-and-retries.md` |
| D19-T015 | Saga pattern | D19-T014, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t015-saga-pattern.md` |
| D19-T016 | Transactional outbox | D19-T015, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t016-transactional-outbox.md` |
| D19-T017 | CQRS and event sourcing | D19-T016, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t017-cqrs-and-event-sourcing.md` |
| D19-T018 | Distributed data ownership | D19-T017, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t018-distributed-data-ownership.md` |
| D19-T019 | Database-per-service | D19-T018, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t019-database-per-service.md` |
| D19-T020 | Cross-service consistency | D19-T019, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t020-cross-service-consistency.md` |
| D19-T021 | API composition | D19-T020, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t021-api-composition.md` |
| D19-T022 | Aggregation and fan-out | D19-T021, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t022-aggregation-and-fan-out.md` |
| D19-T023 | Service versioning | D19-T022, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t023-service-versioning.md` |
| D19-T024 | Backward-compatible deployments | D19-T023, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t024-backward-compatible-deployments.md` |
| D19-T025 | Strangler pattern | D19-T024, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t025-strangler-pattern.md` |
| D19-T026 | Service mesh basics | D19-T025, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t026-service-mesh-basics.md` |
| D19-T027 | Sidecars and proxies | D19-T026, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t027-sidecars-and-proxies.md` |
| D19-T028 | Monolith-to-microservices migration | D19-T027, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t028-monolith-to-microservices-migration.md` |
| D19-T029 | Microservices failure modes | D19-T028, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t029-microservices-failure-modes.md` |
| D19-T030 | When not to use microservices | D19-T029, D19-T001, D15-T001, D15-T002, D16-T001, D16-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `18_MICROSERVICES/notes/d19-t030-when-not-to-use-microservices.md` |

## D20 — Software Testing

Folder: `19_TESTING`. Owner: Testing and Performance. Topics: 26.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D20-T001 | Unit testing | D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t001-unit-testing.md` |
| D20-T002 | Integration testing | D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t002-integration-testing.md` |
| D20-T003 | Component testing | D20-T002, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t003-component-testing.md` |
| D20-T004 | API testing | D20-T003, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t004-api-testing.md` |
| D20-T005 | End-to-end testing | D20-T004, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t005-end-to-end-testing.md` |
| D20-T006 | Contract testing | D20-T005, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t006-contract-testing.md` |
| D20-T007 | Consumer-driven contracts | D20-T006, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t007-consumer-driven-contracts.md` |
| D20-T008 | Regression testing | D20-T007, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t008-regression-testing.md` |
| D20-T009 | Smoke and sanity testing | D20-T008, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t009-smoke-and-sanity-testing.md` |
| D20-T010 | Acceptance testing | D20-T009, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t010-acceptance-testing.md` |
| D20-T011 | Test doubles, mocks, stubs and fakes | D20-T010, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t011-test-doubles-mocks-stubs-and-fakes.md` |
| D20-T012 | Fixtures and test data management | D20-T011, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t012-fixtures-and-test-data-management.md` |
| D20-T013 | Database integration tests | D20-T012, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t013-database-integration-tests.md` |
| D20-T014 | Testing transactions and rollbacks | D20-T013, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t014-testing-transactions-and-rollbacks.md` |
| D20-T015 | Testing asynchronous workflows | D20-T014, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t015-testing-asynchronous-workflows.md` |
| D20-T016 | Testing Kafka consumers and producers | D20-T015, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t016-testing-kafka-consumers-and-producers.md` |
| D20-T017 | Concurrency and race testing | D20-T016, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t017-concurrency-and-race-testing.md` |
| D20-T018 | Property-based testing | D20-T017, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t018-property-based-testing.md` |
| D20-T019 | Fuzz testing | D20-T018, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t019-fuzz-testing.md` |
| D20-T020 | Mutation testing | D20-T019, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t020-mutation-testing.md` |
| D20-T021 | Performance testing | D20-T020, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t021-performance-testing.md` |
| D20-T022 | Load, stress, spike and soak testing | D20-T021, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t022-load-stress-spike-and-soak-testing.md` |
| D20-T023 | Fault injection and chaos testing | D20-T022, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t023-fault-injection-and-chaos-testing.md` |
| D20-T024 | Test coverage vs test quality | D20-T023, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t024-test-coverage-vs-test-quality.md` |
| D20-T025 | CI test pipelines | D20-T024, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t025-ci-test-pipelines.md` |
| D20-T026 | Testcontainers and ephemeral dependencies | D20-T025, D20-T001, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `19_TESTING/notes/d20-t026-testcontainers-and-ephemeral-dependencies.md` |

## D21 — Performance Engineering

Folder: `20_PERFORMANCE_ENGINEERING`. Owner: Testing and Performance. Topics: 25.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D21-T001 | Latency percentiles: p50, p90, p95, p99 | D02-T001, D02-T002, D07-T001, D07-T002, D13-T001, D13-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t001-latency-percentiles-p50-p90-p95-p99.md` |
| D21-T002 | Throughput and concurrency | D21-T001, D02-T001, D02-T002, D07-T001, D07-T002, D13-T001 | common | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t002-throughput-and-concurrency.md` |
| D21-T003 | Profiling CPU and memory | D21-T002, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t003-profiling-cpu-and-memory.md` |
| D21-T004 | Flame graphs | D21-T003, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t004-flame-graphs.md` |
| D21-T005 | Memory leaks and allocation pressure | D21-T004, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t005-memory-leaks-and-allocation-pressure.md` |
| D21-T006 | Garbage collection tuning | D21-T005, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t006-garbage-collection-tuning.md` |
| D21-T007 | Database query optimization | D21-T006, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t007-database-query-optimization.md` |
| D21-T008 | Index tuning | D21-T007, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t008-index-tuning.md` |
| D21-T009 | N+1 queries | D21-T008, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t009-n-plus-1-queries.md` |
| D21-T010 | Connection pool tuning | D21-T009, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t010-connection-pool-tuning.md` |
| D21-T011 | Caching and cache hit rates | D21-T010, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t011-caching-and-cache-hit-rates.md` |
| D21-T012 | Async I/O | D21-T011, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t012-async-i-o.md` |
| D21-T013 | Batching and bulk operations | D21-T012, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t013-batching-and-bulk-operations.md` |
| D21-T014 | Compression | D21-T013, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t014-compression.md` |
| D21-T015 | Payload size optimization | D21-T014, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t015-payload-size-optimization.md` |
| D21-T016 | Network overhead | D21-T015, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t016-network-overhead.md` |
| D21-T017 | Thread pool sizing | D21-T016, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t017-thread-pool-sizing.md` |
| D21-T018 | Backpressure | D21-T017, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t018-backpressure.md` |
| D21-T019 | Queue depth and consumer lag | D21-T018, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t019-queue-depth-and-consumer-lag.md` |
| D21-T020 | Load testing and benchmarking | D21-T019, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t020-load-testing-and-benchmarking.md` |
| D21-T021 | Little's Law | D21-T020, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t021-little-s-law.md` |
| D21-T022 | Amdahl's Law | D21-T021, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t022-amdahl-s-law.md` |
| D21-T023 | Bottleneck identification | D21-T022, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t023-bottleneck-identification.md` |
| D21-T024 | Tail latency | D21-T023, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t024-tail-latency.md` |
| D21-T025 | Capacity planning | D21-T024, D21-T001, D02-T001, D02-T002, D07-T001, D07-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `20_PERFORMANCE_ENGINEERING/notes/d21-t025-capacity-planning.md` |

## D22 — Observability and Production Operations

Folder: `21_OBSERVABILITY_AND_SRE`. Owner: DevOps, Cloud and SRE. Topics: 26.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D22-T001 | Structured logging | D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t001-structured-logging.md` |
| D22-T002 | Log levels and log sampling | D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t002-log-levels-and-log-sampling.md` |
| D22-T003 | Metrics, logs and traces | D22-T002, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t003-metrics-logs-and-traces.md` |
| D22-T004 | Golden signals | D22-T003, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t004-golden-signals.md` |
| D22-T005 | RED and USE methods | D22-T004, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t005-red-and-use-methods.md` |
| D22-T006 | Prometheus | D22-T005, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t006-prometheus.md` |
| D22-T007 | Grafana | D22-T006, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t007-grafana.md` |
| D22-T008 | OpenTelemetry | D22-T007, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t008-opentelemetry.md` |
| D22-T009 | Distributed tracing | D22-T008, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t009-distributed-tracing.md` |
| D22-T010 | Correlation and trace IDs | D22-T009, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t010-correlation-and-trace-ids.md` |
| D22-T011 | Loki / Elasticsearch-based logging | D22-T010, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t011-loki-elasticsearch-based-logging.md` |
| D22-T012 | Health, liveness and readiness probes | D22-T011, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t012-health-liveness-and-readiness-probes.md` |
| D22-T013 | SLIs, SLOs and SLAs | D22-T012, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t013-slis-slos-and-slas.md` |
| D22-T014 | Error budgets | D22-T013, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t014-error-budgets.md` |
| D22-T015 | Alert design and noise reduction | D22-T014, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t015-alert-design-and-noise-reduction.md` |
| D22-T016 | Dashboards | D22-T015, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t016-dashboards.md` |
| D22-T017 | Incident response | D22-T016, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t017-incident-response.md` |
| D22-T018 | Root cause analysis (RCA) | D22-T017, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t018-root-cause-analysis-rca.md` |
| D22-T019 | Postmortems and corrective actions | D22-T018, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t019-postmortems-and-corrective-actions.md` |
| D22-T020 | On-call fundamentals | D22-T019, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t020-on-call-fundamentals.md` |
| D22-T021 | Runbooks and playbooks | D22-T020, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t021-runbooks-and-playbooks.md` |
| D22-T022 | Production debugging | D22-T021, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t022-production-debugging.md` |
| D22-T023 | Memory, CPU and connection saturation | D22-T022, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t023-memory-cpu-and-connection-saturation.md` |
| D22-T024 | Queue lag and database saturation | D22-T023, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t024-queue-lag-and-database-saturation.md` |
| D22-T025 | Dependency failures | D22-T024, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t025-dependency-failures.md` |
| D22-T026 | Service-level and end-to-end monitoring | D22-T025, D22-T001, D05-T001, D05-T002, D21-T001, D21-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `21_OBSERVABILITY_AND_SRE/notes/d22-t026-service-level-and-end-to-end-monitoring.md` |

## D23 — Docker and Containerization

Folder: `22_DOCKER`. Owner: DevOps, Cloud and SRE. Topics: 22.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D23-T001 | Containers vs virtual machines | D03-T001, D03-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `22_DOCKER/notes/d23-t001-containers-vs-virtual-machines.md` |
| D23-T002 | Images and layers | D23-T001, D03-T001, D03-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `22_DOCKER/notes/d23-t002-images-and-layers.md` |
| D23-T003 | Dockerfile instructions | D23-T002, D23-T001, D03-T001, D03-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `22_DOCKER/notes/d23-t003-dockerfile-instructions.md` |
| D23-T004 | Multi-stage builds | D23-T003, D23-T001, D03-T001, D03-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `22_DOCKER/notes/d23-t004-multi-stage-builds.md` |
| D23-T005 | Image size optimization | D23-T004, D23-T001, D03-T001, D03-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `22_DOCKER/notes/d23-t005-image-size-optimization.md` |
| D23-T006 | Build cache | D23-T005, D23-T001, D03-T001, D03-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `22_DOCKER/notes/d23-t006-build-cache.md` |
| D23-T007 | Docker Compose | D23-T006, D23-T001, D03-T001, D03-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `22_DOCKER/notes/d23-t007-docker-compose.md` |
| D23-T008 | Container networking | D23-T007, D23-T001, D03-T001, D03-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `22_DOCKER/notes/d23-t008-container-networking.md` |
| D23-T009 | Volumes and bind mounts | D23-T008, D23-T001, D03-T001, D03-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `22_DOCKER/notes/d23-t009-volumes-and-bind-mounts.md` |
| D23-T010 | Environment variables and secrets | D23-T009, D23-T001, D03-T001, D03-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `22_DOCKER/notes/d23-t010-environment-variables-and-secrets.md` |
| D23-T011 | Health checks | D23-T010, D23-T001, D03-T001, D03-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `22_DOCKER/notes/d23-t011-health-checks.md` |
| D23-T012 | Resource limits | D23-T011, D23-T001, D03-T001, D03-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `22_DOCKER/notes/d23-t012-resource-limits.md` |
| D23-T013 | Container logs | D23-T012, D23-T001, D03-T001, D03-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `22_DOCKER/notes/d23-t013-container-logs.md` |
| D23-T014 | Non-root containers | D23-T013, D23-T001, D03-T001, D03-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `22_DOCKER/notes/d23-t014-non-root-containers.md` |
| D23-T015 | Image scanning | D23-T014, D23-T001, D03-T001, D03-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `22_DOCKER/notes/d23-t015-image-scanning.md` |
| D23-T016 | Container registries | D23-T015, D23-T001, D03-T001, D03-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `22_DOCKER/notes/d23-t016-container-registries.md` |
| D23-T017 | Container startup and shutdown | D23-T016, D23-T001, D03-T001, D03-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `22_DOCKER/notes/d23-t017-container-startup-and-shutdown.md` |
| D23-T018 | Service dependency management | D23-T017, D23-T001, D03-T001, D03-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `22_DOCKER/notes/d23-t018-service-dependency-management.md` |
| D23-T019 | Docker debugging | D23-T018, D23-T001, D03-T001, D03-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `22_DOCKER/notes/d23-t019-docker-debugging.md` |
| D23-T020 | Persistent storage | D23-T019, D23-T001, D03-T001, D03-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `22_DOCKER/notes/d23-t020-persistent-storage.md` |
| D23-T021 | Development vs production images | D23-T020, D23-T001, D03-T001, D03-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `22_DOCKER/notes/d23-t021-development-vs-production-images.md` |
| D23-T022 | Reproducible builds | D23-T021, D23-T001, D03-T001, D03-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `22_DOCKER/notes/d23-t022-reproducible-builds.md` |

## D24 — Kubernetes and Cloud Infrastructure

Folder: `23_KUBERNETES_AND_CLOUD`. Owner: DevOps, Cloud and SRE. Topics: 31.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D24-T001 | Kubernetes architecture | D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t001-kubernetes-architecture.md` |
| D24-T002 | Pods and Deployments | D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t002-pods-and-deployments.md` |
| D24-T003 | ReplicaSets | D24-T002, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t003-replicasets.md` |
| D24-T004 | Services and service discovery | D24-T003, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t004-services-and-service-discovery.md` |
| D24-T005 | Ingress and Gateway API | D24-T004, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t005-ingress-and-gateway-api.md` |
| D24-T006 | ConfigMaps and Secrets | D24-T005, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t006-configmaps-and-secrets.md` |
| D24-T007 | Namespaces | D24-T006, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t007-namespaces.md` |
| D24-T008 | Liveness, readiness and startup probes | D24-T007, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t008-liveness-readiness-and-startup-probes.md` |
| D24-T009 | Resource requests and limits | D24-T008, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t009-resource-requests-and-limits.md` |
| D24-T010 | Horizontal Pod Autoscaler | D24-T009, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t010-horizontal-pod-autoscaler.md` |
| D24-T011 | Persistent Volumes and Claims | D24-T010, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t011-persistent-volumes-and-claims.md` |
| D24-T012 | StatefulSets and DaemonSets | D24-T011, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t012-statefulsets-and-daemonsets.md` |
| D24-T013 | Jobs and CronJobs | D24-T012, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t013-jobs-and-cronjobs.md` |
| D24-T014 | Rolling updates and rollbacks | D24-T013, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t014-rolling-updates-and-rollbacks.md` |
| D24-T015 | Pod disruption budgets | D24-T014, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t015-pod-disruption-budgets.md` |
| D24-T016 | RBAC and service accounts | D24-T015, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t016-rbac-and-service-accounts.md` |
| D24-T017 | Network policies | D24-T016, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t017-network-policies.md` |
| D24-T018 | Helm | D24-T017, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t018-helm.md` |
| D24-T019 | Kubernetes troubleshooting | D24-T018, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t019-kubernetes-troubleshooting.md` |
| D24-T020 | Cloud networking fundamentals | D24-T019, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t020-cloud-networking-fundamentals.md` |
| D24-T021 | VPCs, subnets, routing and firewalls | D24-T020, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t021-vpcs-subnets-routing-and-firewalls.md` |
| D24-T022 | IAM and least privilege | D24-T021, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t022-iam-and-least-privilege.md` |
| D24-T023 | Compute, storage and managed databases | D24-T022, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t023-compute-storage-and-managed-databases.md` |
| D24-T024 | Object storage | D24-T023, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t024-object-storage.md` |
| D24-T025 | Load balancers and CDNs | D24-T024, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t025-load-balancers-and-cdns.md` |
| D24-T026 | Autoscaling | D24-T025, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t026-autoscaling.md` |
| D24-T027 | Availability zones and regions | D24-T026, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t027-availability-zones-and-regions.md` |
| D24-T028 | Disaster recovery | D24-T027, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t028-disaster-recovery.md` |
| D24-T029 | RTO and RPO | D24-T028, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t029-rto-and-rpo.md` |
| D24-T030 | Infrastructure as Code: Terraform | D24-T029, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t030-infrastructure-as-code-terraform.md` |
| D24-T031 | Cost monitoring and optimization | D24-T030, D24-T001, D23-T001, D23-T002, D22-T001, D22-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `23_KUBERNETES_AND_CLOUD/notes/d24-t031-cost-monitoring-and-optimization.md` |

## D25 — CI/CD and Release Engineering

Folder: `24_CI_CD`. Owner: DevOps, Cloud and SRE. Topics: 24.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D25-T001 | Git fundamentals and branching strategies | D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t001-git-fundamentals-and-branching-strategies.md` |
| D25-T002 | Pull requests and code reviews | D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t002-pull-requests-and-code-reviews.md` |
| D25-T003 | Merge vs rebase | D25-T002, D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t003-merge-vs-rebase.md` |
| D25-T004 | CI pipelines | D25-T003, D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t004-ci-pipelines.md` |
| D25-T005 | Automated testing | D25-T004, D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t005-automated-testing.md` |
| D25-T006 | Build artifacts and versioning | D25-T005, D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t006-build-artifacts-and-versioning.md` |
| D25-T007 | Container image publishing | D25-T006, D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t007-container-image-publishing.md` |
| D25-T008 | CD pipelines | D25-T007, D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t008-cd-pipelines.md` |
| D25-T009 | Jenkins / GitHub Actions / GitLab CI | D25-T008, D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t009-jenkins-github-actions-gitlab-ci.md` |
| D25-T010 | Environment promotion | D25-T009, D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t010-environment-promotion.md` |
| D25-T011 | Deployment strategies | D25-T010, D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t011-deployment-strategies.md` |
| D25-T012 | Rolling deployments | D25-T011, D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t012-rolling-deployments.md` |
| D25-T013 | Blue-green deployments | D25-T012, D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t013-blue-green-deployments.md` |
| D25-T014 | Canary releases | D25-T013, D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t014-canary-releases.md` |
| D25-T015 | Feature flags | D25-T014, D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t015-feature-flags.md` |
| D25-T016 | Database migration safety | D25-T015, D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t016-database-migration-safety.md` |
| D25-T017 | Backward-compatible changes | D25-T016, D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t017-backward-compatible-changes.md` |
| D25-T018 | Rollbacks and roll-forwards | D25-T017, D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t018-rollbacks-and-roll-forwards.md` |
| D25-T019 | Release automation | D25-T018, D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t019-release-automation.md` |
| D25-T020 | GitOps and Argo CD | D25-T019, D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t020-gitops-and-argo-cd.md` |
| D25-T021 | Artifact and dependency security | D25-T020, D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t021-artifact-and-dependency-security.md` |
| D25-T022 | Supply-chain security | D25-T021, D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t022-supply-chain-security.md` |
| D25-T023 | Secrets in CI/CD | D25-T022, D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t023-secrets-in-ci-cd.md` |
| D25-T024 | Release verification | D25-T023, D25-T001, D23-T001, D23-T002, D20-T001, D20-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `24_CI_CD/notes/d25-t024-release-verification.md` |

## D26 — Linux and Backend Troubleshooting

Folder: `25_LINUX_TROUBLESHOOTING`. Owner: DevOps, Cloud and SRE. Topics: 23.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D26-T001 | Filesystem and permissions | D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t001-filesystem-and-permissions.md` |
| D26-T002 | Users, groups and ownership | D26-T001, D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t002-users-groups-and-ownership.md` |
| D26-T003 | Processes: ps, top, htop | D26-T002, D26-T001, D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t003-processes-ps-top-htop.md` |
| D26-T004 | Signals and process termination | D26-T003, D26-T001, D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t004-signals-and-process-termination.md` |
| D26-T005 | grep, sed, awk, find | D26-T004, D26-T001, D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t005-grep-sed-awk-find.md` |
| D26-T006 | Pipes and redirection | D26-T005, D26-T001, D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t006-pipes-and-redirection.md` |
| D26-T007 | curl and wget | D26-T006, D26-T001, D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t007-curl-and-wget.md` |
| D26-T008 | ss, netstat, lsof | D26-T007, D26-T001, D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t008-ss-netstat-lsof.md` |
| D26-T009 | dig, nslookup, ping, traceroute | D26-T008, D26-T001, D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t009-dig-nslookup-ping-traceroute.md` |
| D26-T010 | Disk and memory diagnostics | D26-T009, D26-T001, D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t010-disk-and-memory-diagnostics.md` |
| D26-T011 | df, du, free, vmstat | D26-T010, D26-T001, D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t011-df-du-free-vmstat.md` |
| D26-T012 | CPU profiling and system load | D26-T011, D26-T001, D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t012-cpu-profiling-and-system-load.md` |
| D26-T013 | strace basics | D26-T012, D26-T001, D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t013-strace-basics.md` |
| D26-T014 | Environment variables | D26-T013, D26-T001, D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t014-environment-variables.md` |
| D26-T015 | Shell scripting | D26-T014, D26-T001, D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t015-shell-scripting.md` |
| D26-T016 | Log inspection and rotation | D26-T015, D26-T001, D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t016-log-inspection-and-rotation.md` |
| D26-T017 | File descriptor limits | D26-T016, D26-T001, D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t017-file-descriptor-limits.md` |
| D26-T018 | Port conflicts | D26-T017, D26-T001, D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t018-port-conflicts.md` |
| D26-T019 | TLS certificate debugging | D26-T018, D26-T001, D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t019-tls-certificate-debugging.md` |
| D26-T020 | DNS and connectivity debugging | D26-T019, D26-T001, D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t020-dns-and-connectivity-debugging.md` |
| D26-T021 | Out-of-memory failures | D26-T020, D26-T001, D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t021-out-of-memory-failures.md` |
| D26-T022 | Disk exhaustion | D26-T021, D26-T001, D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t022-disk-exhaustion.md` |
| D26-T023 | Process crashes and restarts | D26-T022, D26-T001, D03-T001, D03-T002, D23-T001, D23-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `25_LINUX_TROUBLESHOOTING/notes/d26-t023-process-crashes-and-restarts.md` |

## D27 — Software Engineering Principles

Folder: `26_SOFTWARE_ENGINEERING_PRINCIPLES`. Owner: Architecture and System Design. Topics: 22.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D27-T001 | SOLID | D01-T001, D01-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `26_SOFTWARE_ENGINEERING_PRINCIPLES/notes/d27-t001-solid.md` |
| D27-T002 | DRY, KISS, YAGNI | D27-T001, D01-T001, D01-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `26_SOFTWARE_ENGINEERING_PRINCIPLES/notes/d27-t002-dry-kiss-yagni.md` |
| D27-T003 | Separation of concerns | D27-T002, D27-T001, D01-T001, D01-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `26_SOFTWARE_ENGINEERING_PRINCIPLES/notes/d27-t003-separation-of-concerns.md` |
| D27-T004 | High cohesion and low coupling | D27-T003, D27-T001, D01-T001, D01-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `26_SOFTWARE_ENGINEERING_PRINCIPLES/notes/d27-t004-high-cohesion-and-low-coupling.md` |
| D27-T005 | Dependency inversion | D27-T004, D27-T001, D01-T001, D01-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `26_SOFTWARE_ENGINEERING_PRINCIPLES/notes/d27-t005-dependency-inversion.md` |
| D27-T006 | Encapsulation and information hiding | D27-T005, D27-T001, D01-T001, D01-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `26_SOFTWARE_ENGINEERING_PRINCIPLES/notes/d27-t006-encapsulation-and-information-hiding.md` |
| D27-T007 | Clean code and refactoring | D27-T006, D27-T001, D01-T001, D01-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `26_SOFTWARE_ENGINEERING_PRINCIPLES/notes/d27-t007-clean-code-and-refactoring.md` |
| D27-T008 | Technical debt management | D27-T007, D27-T001, D01-T001, D01-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `26_SOFTWARE_ENGINEERING_PRINCIPLES/notes/d27-t008-technical-debt-management.md` |
| D27-T009 | Code review practices | D27-T008, D27-T001, D01-T001, D01-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `26_SOFTWARE_ENGINEERING_PRINCIPLES/notes/d27-t009-code-review-practices.md` |
| D27-T010 | Design documentation | D27-T009, D27-T001, D01-T001, D01-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `26_SOFTWARE_ENGINEERING_PRINCIPLES/notes/d27-t010-design-documentation.md` |
| D27-T011 | Architecture Decision Records | D27-T010, D27-T001, D01-T001, D01-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `26_SOFTWARE_ENGINEERING_PRINCIPLES/notes/d27-t011-architecture-decision-records.md` |
| D27-T012 | API and schema compatibility | D27-T011, D27-T001, D01-T001, D01-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `26_SOFTWARE_ENGINEERING_PRINCIPLES/notes/d27-t012-api-and-schema-compatibility.md` |
| D27-T013 | Backward and forward compatibility | D27-T012, D27-T001, D01-T001, D01-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `26_SOFTWARE_ENGINEERING_PRINCIPLES/notes/d27-t013-backward-and-forward-compatibility.md` |
| D27-T014 | Semantic versioning | D27-T013, D27-T001, D01-T001, D01-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `26_SOFTWARE_ENGINEERING_PRINCIPLES/notes/d27-t014-semantic-versioning.md` |
| D27-T015 | Feature flags | D27-T014, D27-T001, D01-T001, D01-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `26_SOFTWARE_ENGINEERING_PRINCIPLES/notes/d27-t015-feature-flags.md` |
| D27-T016 | Configuration management | D27-T015, D27-T001, D01-T001, D01-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `26_SOFTWARE_ENGINEERING_PRINCIPLES/notes/d27-t016-configuration-management.md` |
| D27-T017 | Secure coding | D27-T016, D27-T001, D01-T001, D01-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `26_SOFTWARE_ENGINEERING_PRINCIPLES/notes/d27-t017-secure-coding.md` |
| D27-T018 | Maintainability and extensibility | D27-T017, D27-T001, D01-T001, D01-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `26_SOFTWARE_ENGINEERING_PRINCIPLES/notes/d27-t018-maintainability-and-extensibility.md` |
| D27-T019 | Debugging methodology | D27-T018, D27-T001, D01-T001, D01-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `26_SOFTWARE_ENGINEERING_PRINCIPLES/notes/d27-t019-debugging-methodology.md` |
| D27-T020 | Root cause analysis | D27-T019, D27-T001, D01-T001, D01-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `26_SOFTWARE_ENGINEERING_PRINCIPLES/notes/d27-t020-root-cause-analysis.md` |
| D27-T021 | Engineering trade-offs | D27-T020, D27-T001, D01-T001, D01-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `26_SOFTWARE_ENGINEERING_PRINCIPLES/notes/d27-t021-engineering-trade-offs.md` |
| D27-T022 | Documentation and knowledge sharing | D27-T021, D27-T001, D01-T001, D01-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `26_SOFTWARE_ENGINEERING_PRINCIPLES/notes/d27-t022-documentation-and-knowledge-sharing.md` |

## D28 — Advanced Backend Topics That Make You Stand Out

Folder: `27_ADVANCED_BACKEND`. Owner: Architecture and System Design. Topics: 30.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D28-T001 | Multi-tenancy: shared DB vs schema vs database per tenant | D15-T001, D15-T002, D19-T001, D19-T002, D12-T001, D12-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t001-multi-tenancy-shared-db-vs-schema-vs-database-per-tenant.md` |
| D28-T002 | Tenant isolation and tenant-aware authorization | D28-T001, D15-T001, D15-T002, D19-T001, D19-T002, D12-T001 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t002-tenant-isolation-and-tenant-aware-authorization.md` |
| D28-T003 | Fairness and noisy-neighbor protection | D28-T002, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t003-fairness-and-noisy-neighbor-protection.md` |
| D28-T004 | API quotas and tenant-level rate limiting | D28-T003, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t004-api-quotas-and-tenant-level-rate-limiting.md` |
| D28-T005 | Distributed rate limiting | D28-T004, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t005-distributed-rate-limiting.md` |
| D28-T006 | Idempotent payment and order workflows | D28-T005, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t006-idempotent-payment-and-order-workflows.md` |
| D28-T007 | Double-entry ledger fundamentals | D28-T006, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t007-double-entry-ledger-fundamentals.md` |
| D28-T008 | Exactly-once business effects | D28-T007, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t008-exactly-once-business-effects.md` |
| D28-T009 | Transactional outbox and inbox patterns | D28-T008, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t009-transactional-outbox-and-inbox-patterns.md` |
| D28-T010 | CDC-based integrations | D28-T009, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t010-cdc-based-integrations.md` |
| D28-T011 | Distributed scheduling | D28-T010, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t011-distributed-scheduling.md` |
| D28-T012 | Leader election and leases | D28-T011, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t012-leader-election-and-leases.md` |
| D28-T013 | Workflow engines and durable execution | D28-T012, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t013-workflow-engines-and-durable-execution.md` |
| D28-T014 | Long-running transactions and compensations | D28-T013, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t014-long-running-transactions-and-compensations.md` |
| D28-T015 | Data consistency across services | D28-T014, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t015-data-consistency-across-services.md` |
| D28-T016 | Hot-key mitigation | D28-T015, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t016-hot-key-mitigation.md` |
| D28-T017 | Multi-region architecture | D28-T016, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t017-multi-region-architecture.md` |
| D28-T018 | Disaster recovery and failover | D28-T017, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t018-disaster-recovery-and-failover.md` |
| D28-T019 | Data retention and deletion workflows | D28-T018, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t019-data-retention-and-deletion-workflows.md` |
| D28-T020 | Auditability and compliance | D28-T019, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t020-auditability-and-compliance.md` |
| D28-T021 | Tenant migration | D28-T020, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t021-tenant-migration.md` |
| D28-T022 | Zero-downtime schema migrations | D28-T021, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t022-zero-downtime-schema-migrations.md` |
| D28-T023 | Backpressure and load shedding | D28-T022, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t023-backpressure-and-load-shedding.md` |
| D28-T024 | Admission control | D28-T023, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t024-admission-control.md` |
| D28-T025 | Graceful degradation | D28-T024, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t025-graceful-degradation.md` |
| D28-T026 | Cost-aware architecture | D28-T025, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t026-cost-aware-architecture.md` |
| D28-T027 | Feature flags and progressive delivery | D28-T026, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t027-feature-flags-and-progressive-delivery.md` |
| D28-T028 | Production readiness reviews | D28-T027, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t028-production-readiness-reviews.md` |
| D28-T029 | Chaos engineering | D28-T028, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t029-chaos-engineering.md` |
| D28-T030 | Capacity planning and load forecasting | D28-T029, D28-T001, D15-T001, D15-T002, D19-T001, D19-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `27_ADVANCED_BACKEND/notes/d28-t030-capacity-planning-and-load-forecasting.md` |

## D29 — Search and Specialized Storage

Folder: `28_SEARCH_AND_STORAGE`. Owner: Database. Topics: 15.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D29-T001 | Elasticsearch / OpenSearch architecture | D07-T001, D07-T002, D10-T001, D10-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `28_SEARCH_AND_STORAGE/notes/d29-t001-elasticsearch-opensearch-architecture.md` |
| D29-T002 | Inverted indexes | D29-T001, D07-T001, D07-T002, D10-T001, D10-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `28_SEARCH_AND_STORAGE/notes/d29-t002-inverted-indexes.md` |
| D29-T003 | Full-text search and analyzers | D29-T002, D29-T001, D07-T001, D07-T002, D10-T001, D10-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `28_SEARCH_AND_STORAGE/notes/d29-t003-full-text-search-and-analyzers.md` |
| D29-T004 | Tokenization and relevance scoring | D29-T003, D29-T001, D07-T001, D07-T002, D10-T001, D10-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `28_SEARCH_AND_STORAGE/notes/d29-t004-tokenization-and-relevance-scoring.md` |
| D29-T005 | Filtering, sorting and aggregations | D29-T004, D29-T001, D07-T001, D07-T002, D10-T001, D10-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `28_SEARCH_AND_STORAGE/notes/d29-t005-filtering-sorting-and-aggregations.md` |
| D29-T006 | Index mappings and schema evolution | D29-T005, D29-T001, D07-T001, D07-T002, D10-T001, D10-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `28_SEARCH_AND_STORAGE/notes/d29-t006-index-mappings-and-schema-evolution.md` |
| D29-T007 | Reindexing and alias swaps | D29-T006, D29-T001, D07-T001, D07-T002, D10-T001, D10-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `28_SEARCH_AND_STORAGE/notes/d29-t007-reindexing-and-alias-swaps.md` |
| D29-T008 | Search pagination and deep pagination | D29-T007, D29-T001, D07-T001, D07-T002, D10-T001, D10-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `28_SEARCH_AND_STORAGE/notes/d29-t008-search-pagination-and-deep-pagination.md` |
| D29-T009 | Geo-spatial queries | D29-T008, D29-T001, D07-T001, D07-T002, D10-T001, D10-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `28_SEARCH_AND_STORAGE/notes/d29-t009-geo-spatial-queries.md` |
| D29-T010 | Vector databases | D29-T009, D29-T001, D07-T001, D07-T002, D10-T001, D10-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `28_SEARCH_AND_STORAGE/notes/d29-t010-vector-databases.md` |
| D29-T011 | Object storage and multipart uploads | D29-T010, D29-T001, D07-T001, D07-T002, D10-T001, D10-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `28_SEARCH_AND_STORAGE/notes/d29-t011-object-storage-and-multipart-uploads.md` |
| D29-T012 | Pre-signed URLs | D29-T011, D29-T001, D07-T001, D07-T002, D10-T001, D10-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `28_SEARCH_AND_STORAGE/notes/d29-t012-pre-signed-urls.md` |
| D29-T013 | Content hashing and deduplication | D29-T012, D29-T001, D07-T001, D07-T002, D10-T001, D10-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `28_SEARCH_AND_STORAGE/notes/d29-t013-content-hashing-and-deduplication.md` |
| D29-T014 | Metadata storage vs blob storage | D29-T013, D29-T001, D07-T001, D07-T002, D10-T001, D10-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `28_SEARCH_AND_STORAGE/notes/d29-t014-metadata-storage-vs-blob-storage.md` |
| D29-T015 | Lifecycle and archival policies | D29-T014, D29-T001, D07-T001, D07-T002, D10-T001, D10-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `28_SEARCH_AND_STORAGE/notes/d29-t015-lifecycle-and-archival-policies.md` |

## D30 — AI/LLM Backend Engineering

Folder: `29_AI_LLM_BACKEND`. Owner: Framework and AI Backend. Topics: 29.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D30-T001 | LLM API integration | D05-T001, D05-T002, D12-T001, D12-T002, D29-T001, D29-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t001-llm-api-integration.md` |
| D30-T002 | Streaming responses | D30-T001, D05-T001, D05-T002, D12-T001, D12-T002, D29-T001 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t002-streaming-responses.md` |
| D30-T003 | Token budgets and context windows | D30-T002, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t003-token-budgets-and-context-windows.md` |
| D30-T004 | Rate limits and quotas | D30-T003, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t004-rate-limits-and-quotas.md` |
| D30-T005 | Retries and timeouts for model APIs | D30-T004, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t005-retries-and-timeouts-for-model-apis.md` |
| D30-T006 | Prompt templates and versioning | D30-T005, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t006-prompt-templates-and-versioning.md` |
| D30-T007 | Structured outputs and schema validation | D30-T006, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t007-structured-outputs-and-schema-validation.md` |
| D30-T008 | Tool calling | D30-T007, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t008-tool-calling.md` |
| D30-T009 | MCP (Model Context Protocol) | D30-T008, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t009-mcp-model-context-protocol.md` |
| D30-T010 | Agent orchestration | D30-T009, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t010-agent-orchestration.md` |
| D30-T011 | LangChain and LangGraph | D30-T010, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t011-langchain-and-langgraph.md` |
| D30-T012 | RAG architecture | D30-T011, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t012-rag-architecture.md` |
| D30-T013 | Document ingestion and chunking | D30-T012, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t013-document-ingestion-and-chunking.md` |
| D30-T014 | Embeddings and vector search | D30-T013, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t014-embeddings-and-vector-search.md` |
| D30-T015 | Hybrid retrieval and reranking | D30-T014, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t015-hybrid-retrieval-and-reranking.md` |
| D30-T016 | Retrieval evaluation | D30-T015, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t016-retrieval-evaluation.md` |
| D30-T017 | Hallucination and grounding controls | D30-T016, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t017-hallucination-and-grounding-controls.md` |
| D30-T018 | Conversation state and memory | D30-T017, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t018-conversation-state-and-memory.md` |
| D30-T019 | Background ingestion pipelines | D30-T018, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t019-background-ingestion-pipelines.md` |
| D30-T020 | Async inference jobs | D30-T019, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t020-async-inference-jobs.md` |
| D30-T021 | LLM caching and semantic caching | D30-T020, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t021-llm-caching-and-semantic-caching.md` |
| D30-T022 | Prompt injection and tool security | D30-T021, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t022-prompt-injection-and-tool-security.md` |
| D30-T023 | PII handling and data isolation | D30-T022, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t023-pii-handling-and-data-isolation.md` |
| D30-T024 | Model fallback and provider routing | D30-T023, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t024-model-fallback-and-provider-routing.md` |
| D30-T025 | Cost, latency and token observability | D30-T024, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t025-cost-latency-and-token-observability.md` |
| D30-T026 | LLM evaluation and regression tests | D30-T025, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t026-llm-evaluation-and-regression-tests.md` |
| D30-T027 | Queue-based inference scaling | D30-T026, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t027-queue-based-inference-scaling.md` |
| D30-T028 | Human-in-the-loop workflows | D30-T027, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | common | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t028-human-in-the-loop-workflows.md` |
| D30-T029 | AI service reliability and graceful degradation | D30-T028, D30-T001, D05-T001, D05-T002, D12-T001, D12-T002 | core | advanced | NOT_STARTED | NOT_STARTED | `29_AI_LLM_BACKEND/notes/d30-t029-ai-service-reliability-and-graceful-degradation.md` |

## D31 — Backend Frameworks — Choose One Deeply

Folder: `30_BACKEND_FRAMEWORKS`. Owner: Framework and AI Backend. Topics: 21.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D31-T001 | Spring Boot: IoC, beans, DI, auto-configuration | D01-T001, D01-T002, D05-T001, D05-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `30_BACKEND_FRAMEWORKS/notes/d31-t001-spring-boot-ioc-beans-di-auto-configuration.md` |
| D31-T002 | Spring MVC and request lifecycle | D31-T001, D01-T001, D01-T002, D05-T001, D05-T002, D07-T001 | common | intermediate | NOT_STARTED | NOT_STARTED | `30_BACKEND_FRAMEWORKS/notes/d31-t002-spring-mvc-and-request-lifecycle.md` |
| D31-T003 | Spring Security | D31-T002, D31-T001, D01-T001, D01-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `30_BACKEND_FRAMEWORKS/notes/d31-t003-spring-security.md` |
| D31-T004 | Spring Data JPA and Hibernate | D31-T003, D31-T001, D01-T001, D01-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `30_BACKEND_FRAMEWORKS/notes/d31-t004-spring-data-jpa-and-hibernate.md` |
| D31-T005 | Transactions and propagation | D31-T004, D31-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `30_BACKEND_FRAMEWORKS/notes/d31-t005-transactions-and-propagation.md` |
| D31-T006 | Entity lifecycle and persistence context | D31-T005, D31-T001, D01-T001, D01-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `30_BACKEND_FRAMEWORKS/notes/d31-t006-entity-lifecycle-and-persistence-context.md` |
| D31-T007 | Lazy vs eager loading | D31-T006, D31-T001, D01-T001, D01-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `30_BACKEND_FRAMEWORKS/notes/d31-t007-lazy-vs-eager-loading.md` |
| D31-T008 | N+1 queries | D31-T007, D31-T001, D01-T001, D01-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `30_BACKEND_FRAMEWORKS/notes/d31-t008-n-plus-1-queries.md` |
| D31-T009 | Bean scopes and lifecycle | D31-T008, D31-T001, D01-T001, D01-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `30_BACKEND_FRAMEWORKS/notes/d31-t009-bean-scopes-and-lifecycle.md` |
| D31-T010 | Filters, interceptors and AOP | D31-T009, D31-T001, D01-T001, D01-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `30_BACKEND_FRAMEWORKS/notes/d31-t010-filters-interceptors-and-aop.md` |
| D31-T011 | FastAPI routing and dependency injection | D31-T010, D31-T001, D01-T001, D01-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `30_BACKEND_FRAMEWORKS/notes/d31-t011-fastapi-routing-and-dependency-injection.md` |
| D31-T012 | Pydantic validation and serialization | D31-T011, D31-T001, D01-T001, D01-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `30_BACKEND_FRAMEWORKS/notes/d31-t012-pydantic-validation-and-serialization.md` |
| D31-T013 | ASGI and Uvicorn | D31-T012, D31-T001, D01-T001, D01-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `30_BACKEND_FRAMEWORKS/notes/d31-t013-asgi-and-uvicorn.md` |
| D31-T014 | SQLAlchemy sessions and transactions | D31-T013, D31-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `30_BACKEND_FRAMEWORKS/notes/d31-t014-sqlalchemy-sessions-and-transactions.md` |
| D31-T015 | FastAPI background tasks | D31-T014, D31-T001, D01-T001, D01-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `30_BACKEND_FRAMEWORKS/notes/d31-t015-fastapi-background-tasks.md` |
| D31-T016 | Node.js event loop and asynchronous I/O | D31-T015, D31-T001, D01-T001, D01-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `30_BACKEND_FRAMEWORKS/notes/d31-t016-node-js-event-loop-and-asynchronous-i-o.md` |
| D31-T017 | Express middleware and error handling | D31-T016, D31-T001, D01-T001, D01-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `30_BACKEND_FRAMEWORKS/notes/d31-t017-express-middleware-and-error-handling.md` |
| D31-T018 | Go net/http, contexts and goroutines | D31-T017, D31-T001, D01-T001, D01-T002, D05-T001, D05-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `30_BACKEND_FRAMEWORKS/notes/d31-t018-go-net-http-contexts-and-goroutines.md` |
| D31-T019 | Framework testing and dependency overrides | D31-T018, D31-T001, D01-T001, D01-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `30_BACKEND_FRAMEWORKS/notes/d31-t019-framework-testing-and-dependency-overrides.md` |
| D31-T020 | Framework security and performance | D31-T019, D31-T001, D01-T001, D01-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `30_BACKEND_FRAMEWORKS/notes/d31-t020-framework-security-and-performance.md` |
| D31-T021 | Production deployment and configuration | D31-T020, D31-T001, D01-T001, D01-T002, D05-T001, D05-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `30_BACKEND_FRAMEWORKS/notes/d31-t021-production-deployment-and-configuration.md` |

## D32 — Backend Interview Communication

Folder: `31_INTERVIEW_COMMUNICATION`. Owner: Interview and Validation. Topics: 17.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D32-T001 | Clarifying ambiguous requirements | D16-T001, D16-T002, D17-T001, D17-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `31_INTERVIEW_COMMUNICATION/notes/d32-t001-clarifying-ambiguous-requirements.md` |
| D32-T002 | Explaining assumptions explicitly | D32-T001, D16-T001, D16-T002, D17-T001, D17-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `31_INTERVIEW_COMMUNICATION/notes/d32-t002-explaining-assumptions-explicitly.md` |
| D32-T003 | Breaking down a problem systematically | D32-T002, D32-T001, D16-T001, D16-T002, D17-T001, D17-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `31_INTERVIEW_COMMUNICATION/notes/d32-t003-breaking-down-a-problem-systematically.md` |
| D32-T004 | Writing readable code under time pressure | D32-T003, D32-T001, D16-T001, D16-T002, D17-T001, D17-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `31_INTERVIEW_COMMUNICATION/notes/d32-t004-writing-readable-code-under-time-pressure.md` |
| D32-T005 | Explaining time and space complexity | D32-T004, D32-T001, D16-T001, D16-T002, D17-T001, D17-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `31_INTERVIEW_COMMUNICATION/notes/d32-t005-explaining-time-and-space-complexity.md` |
| D32-T006 | Discussing edge cases | D32-T005, D32-T001, D16-T001, D16-T002, D17-T001, D17-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `31_INTERVIEW_COMMUNICATION/notes/d32-t006-discussing-edge-cases.md` |
| D32-T007 | Comparing alternative designs | D32-T006, D32-T001, D16-T001, D16-T002, D17-T001, D17-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `31_INTERVIEW_COMMUNICATION/notes/d32-t007-comparing-alternative-designs.md` |
| D32-T008 | Justifying technology choices | D32-T007, D32-T001, D16-T001, D16-T002, D17-T001, D17-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `31_INTERVIEW_COMMUNICATION/notes/d32-t008-justifying-technology-choices.md` |
| D32-T009 | Explaining trade-offs rather than naming tools | D32-T008, D32-T001, D16-T001, D16-T002, D17-T001, D17-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `31_INTERVIEW_COMMUNICATION/notes/d32-t009-explaining-trade-offs-rather-than-naming-tools.md` |
| D32-T010 | Debugging unfamiliar code | D32-T009, D32-T001, D16-T001, D16-T002, D17-T001, D17-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `31_INTERVIEW_COMMUNICATION/notes/d32-t010-debugging-unfamiliar-code.md` |
| D32-T011 | Discussing failures and recovery | D32-T010, D32-T001, D16-T001, D16-T002, D17-T001, D17-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `31_INTERVIEW_COMMUNICATION/notes/d32-t011-discussing-failures-and-recovery.md` |
| D32-T012 | Explaining your own projects end-to-end | D32-T011, D32-T001, D16-T001, D16-T002, D17-T001, D17-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `31_INTERVIEW_COMMUNICATION/notes/d32-t012-explaining-your-own-projects-end-to-end.md` |
| D32-T013 | Presenting measurable project outcomes | D32-T012, D32-T001, D16-T001, D16-T002, D17-T001, D17-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `31_INTERVIEW_COMMUNICATION/notes/d32-t013-presenting-measurable-project-outcomes.md` |
| D32-T014 | Handling follow-up questions | D32-T013, D32-T001, D16-T001, D16-T002, D17-T001, D17-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `31_INTERVIEW_COMMUNICATION/notes/d32-t014-handling-follow-up-questions.md` |
| D32-T015 | Communicating uncertainty honestly | D32-T014, D32-T001, D16-T001, D16-T002, D17-T001, D17-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `31_INTERVIEW_COMMUNICATION/notes/d32-t015-communicating-uncertainty-honestly.md` |
| D32-T016 | Explaining a production incident using root cause and remediation | D32-T015, D32-T001, D16-T001, D16-T002, D17-T001, D17-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `31_INTERVIEW_COMMUNICATION/notes/d32-t016-explaining-a-production-incident-using-root-cause-and-remediation.md` |
| D32-T017 | Describing ownership, collaboration and technical decisions | D32-T016, D32-T001, D16-T001, D16-T002, D17-T001, D17-T002 | core | fundamentals | NOT_STARTED | NOT_STARTED | `31_INTERVIEW_COMMUNICATION/notes/d32-t017-describing-ownership-collaboration-and-technical-decisions.md` |

## D33 — Real-World Engineering Scenarios

Folder: `32_PRODUCTION_SCENARIOS`. Owner: Interview and Validation. Topics: 24.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D33-T001 | API latency suddenly increases | D15-T001, D15-T002, D22-T001, D22-T002, D07-T001, D07-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t001-api-latency-suddenly-increases.md` |
| D33-T002 | Database CPU reaches 100% | D33-T001, D15-T001, D15-T002, D22-T001, D22-T002, D07-T001 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t002-database-cpu-reaches-100.md` |
| D33-T003 | Connection pool is exhausted | D33-T002, D33-T001, D15-T001, D15-T002, D22-T001, D22-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t003-connection-pool-is-exhausted.md` |
| D33-T004 | Redis becomes unavailable | D33-T003, D33-T001, D15-T001, D15-T002, D22-T001, D22-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t004-redis-becomes-unavailable.md` |
| D33-T005 | Kafka consumer lag grows continuously | D33-T004, D33-T001, D15-T001, D15-T002, D22-T001, D22-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t005-kafka-consumer-lag-grows-continuously.md` |
| D33-T006 | Duplicate events create duplicate orders | D33-T005, D33-T001, D15-T001, D15-T002, D22-T001, D22-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t006-duplicate-events-create-duplicate-orders.md` |
| D33-T007 | An external payment provider times out | D33-T006, D33-T001, D15-T001, D15-T002, D22-T001, D22-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t007-an-external-payment-provider-times-out.md` |
| D33-T008 | A service returns intermittent 5xx errors | D33-T007, D33-T001, D15-T001, D15-T002, D22-T001, D22-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t008-a-service-returns-intermittent-5xx-errors.md` |
| D33-T009 | A deployment causes elevated errors | D33-T008, D33-T001, D15-T001, D15-T002, D22-T001, D22-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t009-a-deployment-causes-elevated-errors.md` |
| D33-T010 | Database migration fails halfway | D33-T009, D33-T001, D15-T001, D15-T002, D22-T001, D22-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t010-database-migration-fails-halfway.md` |
| D33-T011 | A cache stampede overloads the database | D33-T010, D33-T001, D15-T001, D15-T002, D22-T001, D22-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t011-a-cache-stampede-overloads-the-database.md` |
| D33-T012 | A tenant monopolizes shared resources | D33-T011, D33-T001, D15-T001, D15-T002, D22-T001, D22-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t012-a-tenant-monopolizes-shared-resources.md` |
| D33-T013 | A distributed lock expires during work | D33-T012, D33-T001, D15-T001, D15-T002, D22-T001, D22-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t013-a-distributed-lock-expires-during-work.md` |
| D33-T014 | A retry storm overloads dependencies | D33-T013, D33-T001, D15-T001, D15-T002, D22-T001, D22-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t014-a-retry-storm-overloads-dependencies.md` |
| D33-T015 | A message is permanently failing | D33-T014, D33-T001, D15-T001, D15-T002, D22-T001, D22-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t015-a-message-is-permanently-failing.md` |
| D33-T016 | A region becomes unavailable | D33-T015, D33-T001, D15-T001, D15-T002, D22-T001, D22-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t016-a-region-becomes-unavailable.md` |
| D33-T017 | Data is accidentally deleted | D33-T016, D33-T001, D15-T001, D15-T002, D22-T001, D22-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t017-data-is-accidentally-deleted.md` |
| D33-T018 | A secret or credential is exposed | D33-T017, D33-T001, D15-T001, D15-T002, D22-T001, D22-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t018-a-secret-or-credential-is-exposed.md` |
| D33-T019 | A queue grows faster than consumers process it | D33-T018, D33-T001, D15-T001, D15-T002, D22-T001, D22-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t019-a-queue-grows-faster-than-consumers-process-it.md` |
| D33-T020 | A service must handle 10× traffic | D33-T019, D33-T001, D15-T001, D15-T002, D22-T001, D22-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t020-a-service-must-handle-10-traffic.md` |
| D33-T021 | An API change breaks old clients | D33-T020, D33-T001, D15-T001, D15-T002, D22-T001, D22-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t021-an-api-change-breaks-old-clients.md` |
| D33-T022 | A background job runs twice | D33-T021, D33-T001, D15-T001, D15-T002, D22-T001, D22-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t022-a-background-job-runs-twice.md` |
| D33-T023 | Two requests update the same resource concurrently | D33-T022, D33-T001, D15-T001, D15-T002, D22-T001, D22-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t023-two-requests-update-the-same-resource-concurrently.md` |
| D33-T024 | A downstream service is slow but not fully down | D33-T023, D33-T001, D15-T001, D15-T002, D22-T001, D22-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `32_PRODUCTION_SCENARIOS/notes/d33-t024-a-downstream-service-is-slow-but-not-fully-down.md` |

## D34 — Practical Project Validation Checklist

Folder: `33_PRACTICAL_PROJECTS`. Owner: Architecture and System Design. Topics: 18.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D34-T001 | Clear requirements and architecture diagrams | D05-T001, D05-T002, D06-T001, D06-T002, D07-T001, D07-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `33_PRACTICAL_PROJECTS/notes/d34-t001-clear-requirements-and-architecture-diagrams.md` |
| D34-T002 | REST APIs with documented contracts | D34-T001, D05-T001, D05-T002, D06-T001, D06-T002, D07-T001 | core | intermediate | NOT_STARTED | NOT_STARTED | `33_PRACTICAL_PROJECTS/notes/d34-t002-rest-apis-with-documented-contracts.md` |
| D34-T003 | Authentication and authorization | D34-T002, D34-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `33_PRACTICAL_PROJECTS/notes/d34-t003-authentication-and-authorization.md` |
| D34-T004 | PostgreSQL schema and optimized queries | D34-T003, D34-T001, D05-T001, D05-T002, D06-T001, D06-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `33_PRACTICAL_PROJECTS/notes/d34-t004-postgresql-schema-and-optimized-queries.md` |
| D34-T005 | Redis caching where justified | D34-T004, D34-T001, D05-T001, D05-T002, D06-T001, D06-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `33_PRACTICAL_PROJECTS/notes/d34-t005-redis-caching-where-justified.md` |
| D34-T006 | Background processing or message queues where justified | D34-T005, D34-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `33_PRACTICAL_PROJECTS/notes/d34-t006-background-processing-or-message-queues-where-justified.md` |
| D34-T007 | Idempotency and duplicate-request protection | D34-T006, D34-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `33_PRACTICAL_PROJECTS/notes/d34-t007-idempotency-and-duplicate-request-protection.md` |
| D34-T008 | Retries, timeouts and failure handling | D34-T007, D34-T001, D05-T001, D05-T002, D06-T001, D06-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `33_PRACTICAL_PROJECTS/notes/d34-t008-retries-timeouts-and-failure-handling.md` |
| D34-T009 | Unit, integration and API tests | D34-T008, D34-T001, D05-T001, D05-T002, D06-T001, D06-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `33_PRACTICAL_PROJECTS/notes/d34-t009-unit-integration-and-api-tests.md` |
| D34-T010 | Load testing and performance measurements | D34-T009, D34-T001, D05-T001, D05-T002, D06-T001, D06-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `33_PRACTICAL_PROJECTS/notes/d34-t010-load-testing-and-performance-measurements.md` |
| D34-T011 | Structured logs, metrics and distributed tracing | D34-T010, D34-T001, D05-T001, D05-T002, D06-T001, D06-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `33_PRACTICAL_PROJECTS/notes/d34-t011-structured-logs-metrics-and-distributed-tracing.md` |
| D34-T012 | Dockerized services and reproducible startup | D34-T011, D34-T001, D05-T001, D05-T002, D06-T001, D06-T002 | core | intermediate | NOT_STARTED | NOT_STARTED | `33_PRACTICAL_PROJECTS/notes/d34-t012-dockerized-services-and-reproducible-startup.md` |
| D34-T013 | CI/CD pipeline | D34-T012, D34-T001, D05-T001, D05-T002, D06-T001, D06-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `33_PRACTICAL_PROJECTS/notes/d34-t013-ci-cd-pipeline.md` |
| D34-T014 | Database migrations and recovery plan | D34-T013, D34-T001, D05-T001, D05-T002, D06-T001, D06-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `33_PRACTICAL_PROJECTS/notes/d34-t014-database-migrations-and-recovery-plan.md` |
| D34-T015 | Security review | D34-T014, D34-T001, D05-T001, D05-T002, D06-T001, D06-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `33_PRACTICAL_PROJECTS/notes/d34-t015-security-review.md` |
| D34-T016 | Failure scenarios documented | D34-T015, D34-T001, D05-T001, D05-T002, D06-T001, D06-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `33_PRACTICAL_PROJECTS/notes/d34-t016-failure-scenarios-documented.md` |
| D34-T017 | README, API docs and architecture diagrams | D34-T016, D34-T001, D05-T001, D05-T002, D06-T001, D06-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `33_PRACTICAL_PROJECTS/notes/d34-t017-readme-api-docs-and-architecture-diagrams.md` |
| D34-T018 | Measurable benchmarks and documented trade-offs | D34-T017, D34-T001, D05-T001, D05-T002, D06-T001, D06-T002 | common | intermediate | NOT_STARTED | NOT_STARTED | `33_PRACTICAL_PROJECTS/notes/d34-t018-measurable-benchmarks-and-documented-trade-offs.md` |

## D35 — Advanced and Specialized Topics

Folder: `34_ADVANCED_SPECIALIZED_TOPICS`. Owner: Messaging and Distributed Systems. Topics: 23.

| ID | Exact topic name | Dependencies | Importance | Complexity | Doc status | Validation | Note path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D35-T001 | Raft consensus in depth | D15-T001, D15-T002, D09-T001, D09-T002, D02-T001, D02-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t001-raft-consensus-in-depth.md` |
| D35-T002 | Distributed transactions and isolation | D35-T001, D15-T001, D15-T002, D09-T001, D09-T002, D02-T001 | core | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t002-distributed-transactions-and-isolation.md` |
| D35-T003 | CRDTs and conflict-free replication | D35-T002, D35-T001, D15-T001, D15-T002, D09-T001, D09-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t003-crdts-and-conflict-free-replication.md` |
| D35-T004 | LSM trees and storage-engine internals | D35-T003, D35-T001, D15-T001, D15-T002, D09-T001, D09-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t004-lsm-trees-and-storage-engine-internals.md` |
| D35-T005 | B-trees and database storage internals | D35-T004, D35-T001, D15-T001, D15-T002, D09-T001, D09-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t005-b-trees-and-database-storage-internals.md` |
| D35-T006 | Write amplification and compaction | D35-T005, D35-T001, D15-T001, D15-T002, D09-T001, D09-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t006-write-amplification-and-compaction.md` |
| D35-T007 | Bloom filters | D35-T006, D35-T001, D15-T001, D15-T002, D09-T001, D09-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t007-bloom-filters.md` |
| D35-T008 | Consistent hashing and virtual nodes | D35-T007, D35-T001, D15-T001, D15-T002, D09-T001, D09-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t008-consistent-hashing-and-virtual-nodes.md` |
| D35-T009 | Gossip protocols | D35-T008, D35-T001, D15-T001, D15-T002, D09-T001, D09-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t009-gossip-protocols.md` |
| D35-T010 | Merkle trees and anti-entropy | D35-T009, D35-T001, D15-T001, D15-T002, D09-T001, D09-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t010-merkle-trees-and-anti-entropy.md` |
| D35-T011 | Distributed snapshots | D35-T010, D35-T001, D15-T001, D15-T002, D09-T001, D09-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t011-distributed-snapshots.md` |
| D35-T012 | Eventual consistency repair | D35-T011, D35-T001, D15-T001, D15-T002, D09-T001, D09-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t012-eventual-consistency-repair.md` |
| D35-T013 | Tail-tolerant systems | D35-T012, D35-T001, D15-T001, D15-T002, D09-T001, D09-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t013-tail-tolerant-systems.md` |
| D35-T014 | Hedged requests | D35-T013, D35-T001, D15-T001, D15-T002, D09-T001, D09-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t014-hedged-requests.md` |
| D35-T015 | Adaptive concurrency limits | D35-T014, D35-T001, D15-T001, D15-T002, D09-T001, D09-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t015-adaptive-concurrency-limits.md` |
| D35-T016 | Queueing theory | D35-T015, D35-T001, D15-T001, D15-T002, D09-T001, D09-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t016-queueing-theory.md` |
| D35-T017 | Load shedding and overload control | D35-T016, D35-T001, D15-T001, D15-T002, D09-T001, D09-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t017-load-shedding-and-overload-control.md` |
| D35-T018 | Multi-region replication | D35-T017, D35-T001, D15-T001, D15-T002, D09-T001, D09-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t018-multi-region-replication.md` |
| D35-T019 | Data locality and placement | D35-T018, D35-T001, D15-T001, D15-T002, D09-T001, D09-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t019-data-locality-and-placement.md` |
| D35-T020 | eBPF and advanced Linux observability | D35-T019, D35-T001, D15-T001, D15-T002, D09-T001, D09-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t020-ebpf-and-advanced-linux-observability.md` |
| D35-T021 | Kernel networking and socket internals | D35-T020, D35-T001, D15-T001, D15-T002, D09-T001, D09-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t021-kernel-networking-and-socket-internals.md` |
| D35-T022 | Advanced JVM / Python / Go runtime profiling | D35-T021, D35-T001, D15-T001, D15-T002, D09-T001, D09-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t022-advanced-jvm-python-go-runtime-profiling.md` |
| D35-T023 | Storage and network cost optimization | D35-T022, D35-T001, D15-T001, D15-T002, D09-T001, D09-T002 | advanced | advanced | NOT_STARTED | NOT_STARTED | `34_ADVANCED_SPECIALIZED_TOPICS/notes/d35-t023-storage-and-network-cost-optimization.md` |

"""Remaining D18 topics (T002-T028)."""
from __future__ import annotations

from textwrap import dedent

from d18_helpers import ans
from d18_topic_data import _topic, pattern

REST_TOPICS: list[dict] = []

# T002 DRY KISS YAGNI
REST_TOPICS.append(
    _topic(
        "D18-T002",
        "d18-t002-dry-kiss-and-yagni",
        "DRY, KISS and YAGNI",
        dedent(
            """
            DRY (Don't Repeat Yourself), KISS (Keep It Simple, Stupid), and YAGNI (You Aren't Gonna Need It) are simplicity disciplines
            that balance reuse against premature abstraction. They keep backend services understandable under on-call pressure.
            They complement SOLID: SOLID shapes modules; DRY/KISS/YAGNI decide how much structure to add today.
            """
        ),
        dedent(
            """
            Duplication is not only copy-paste—it is knowledge repeated in two places that can diverge (validation in API and DB trigger).
            KISS prefers the design a new engineer can modify at 3 a.m. without a pattern catalog.
            YAGNI delays speculative frameworks until a second use case proves the abstraction.
            """
        ),
        dedent(
            """
            Apply DRY at the right level: shared libraries for true invariants, not forced base classes for cosmetic similarity.
            KISS shows up in flat service methods versus deep inheritance.
            YAGNI gates feature flags for hypothetical multi-tenant modes.
            """
        ),
        """flowchart LR
  change[RequirementChange]
  dry{DuplicatedKnowledge}
  kiss{SimplestDesign}
  yagni{NeededNow}
  change --> dry
  dry -->|yes| extract[ExtractSharedModule]
  dry -->|no| kiss
  kiss --> yagni""",
        "Decision flow when a new requirement arrives.",
        "Copy-paste twice is a signal; copy-paste once is fine. KISS rejects cleverness without measured pain.",
        "File: examples/d18_t002_dry.py (unexecuted).",
        dedent(
            '''
            # unexecuted
            def validate_email(value: str) -> str:
                if "@" not in value:
                    raise ValueError("email")
                return value.strip().lower()

            # DRY: one validator used by CLI and HTTP layer, not two regex copies.
            '''
        ),
        "Single validator imported by multiple entry points prevents diverging rules.",
        "Extract shared validation and pricing rules; avoid abstract factories until a second payment provider ships.",
        """| Rule | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| DRY | One source of truth | Wrong abstraction | Identical business rule | Superficial similarity |
| KISS | Readable code | Less 'elegant' | On-call heavy services | Performance-critical hot path needing tuning |
| YAGNI | Faster ship | Rework later | Uncertain roadmap | Compliance mandated early |""",
        ["DRYing accidental duplication into a wrong abstraction.", "KISS as excuse for no tests.", "YAGNI ignoring known roadmap items.", "Shared utils god package.", "Premature plugin architecture."],
        "Incident: two validators disagree—search for duplicated regex and consolidate.",
        "three simplicity rules that prevent speculative abstraction",
        "Find duplicated pagination parsing in two controllers; extract one function.",
        "Team added strategy pattern for one tax rate—argue YAGNI.",
        "When is duplication safer than the wrong abstraction?",
        "Extract `parse_page_params` shared helper.",
        "Remove strategy until second jurisdiction appears; use simple function.",
        "When domains differ, duplication can be safer than forced sharing.",
        "- DRY is about knowledge, not characters.\n- KISS favors boring code.\n- YAGNI delays speculative layers.",
        "After `D18-T001`. Leads to `D18-T003`.",
        ["Apply DRY/KISS/YAGNI to a sample PR.", "Name a harmful DRY refactor.", "Defend YAGNI to a stakeholder."],
    )
)

# T003 Encapsulation
REST_TOPICS.append(
    _topic(
        "D18-T003",
        "d18-t003-encapsulation-and-composition",
        "Encapsulation and composition",
        dedent("Encapsulation hides invariants behind a public API; composition builds behavior by wiring objects instead of deep inheritance. Backend domains (money, inventory) need strong invariants."),
        dedent("Data structures alone do not protect rules—methods enforce them. Composition `has-a` avoids fragile base classes when behaviors mix."),
        dedent("Entities expose intent-revealing methods (`debit`, `reserve`) not raw setters. Services compose repositories, clocks, and policies."),
        """flowchart TD
  client[Client]
  wallet[Wallet]
  ledger[LedgerEntry]
  client -->|debit| wallet
  wallet --> ledger""",
        "Clients call behavior; internal ledger structure stays private.",
        "Wallet composes ledger entries instead of subclassing Account for every feature.",
        "examples/d18_t003_wallet.java (unexecuted).",
        dedent(
            """
            // unexecuted
            final class Wallet {
              private long balanceCents;
              void debit(long cents) {
                if (cents > balanceCents) throw new IllegalStateException("insufficient");
                balanceCents -= cents;
              }
              long balanceCents() { return balanceCents; }
            }
            """
        ),
        "Private balance with checked debit preserves invariant.",
        "Domain models in services should not leak ORM entities to controllers.",
        """| Approach | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Encapsulation | Invariants enforced | Boilerplate getters | Money, auth tokens | Pure DTO transport |
| Composition | Flexible mixing | More wiring | Multiple behaviors | Single tiny struct |
| Inheritance | Reuse by is-a | Fragile overrides | True subtype LSP | Behavior mashups |""",
        ["Anemic domain models with all logic in services.", "Public mutable collections.", "Inheritance for code reuse only.", "Leaking ORM session into entities.", "Composition without clear ownership."],
        "Bug: negative balance—search for setter bypassing debit.",
        "hide state enforce invariants compose behaviors",
        "Add `reserve` to encapsulated inventory object.",
        "Subclass stack for features—refactor to composition.",
        "Trade encapsulation vs performance for hot counters.",
        "Implement method on entity; no public setters.",
        "Replace inheritance chain with composed policies.",
        "Document thread-safety if exposing balance reads.",
        "- Encapsulation guards invariants.\n- Composition over inheritance.\n- Tell, don't ask.",
        "`D18-T002`, `D18-T004`.",
        ["Implement invariant-preserving method.", "Refactor inheritance to composition.", "Explain anemic model risk."],
    )
)

# T004 Interfaces
REST_TOPICS.append(
    _topic(
        "D18-T004",
        "d18-t004-interfaces-and-abstractions",
        "Interfaces and abstractions",
        dedent("Abstractions name stable contracts; interfaces (or protocols) let multiple implementations coexist. They are the hinge for testing and swapping infrastructure."),
        dedent("Callers depend on meaning (save order) not mechanism (JDBC). Abstractions should be owned by the high-level module per DIP."),
        dedent("Ports in hexagonal architecture are interfaces. Adapters implement them. Default methods in Java can share small helpers without a base class."),
        """flowchart LR
  app[ApplicationService]
  port[NotificationPort]
  email[EmailAdapter]
  sms[SmsAdapter]
  app --> port
  port <|.. email
  port <|.. sms""",
        "Application depends on port; adapters plug in.",
        "Notification port with email/SMS adapters.",
        "examples/d18_t004_ports.java (unexecuted).",
        dedent(
            """
            // unexecuted
            interface NotificationPort { void send(String userId, String message); }
            class EmailNotification implements NotificationPort {
              public void send(String userId, String message) { /* SMTP */ }
            }
            """
        ),
        "Interface owned by domain package, implemented in infrastructure.",
        "Define ports at service boundaries; keep DTOs separate from ports unless they are the contract.",
        """| Abstraction | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Interface | Swappable IO | Extra type | Multiple implementations | Single stable IO |
| Abstract class | Shared helper code | Inheritance coupling | Shared template | Only behavior differs |
| Protocol/duck typing | Flexible in Python | Implicit contract | Small scripts | Large cross-team API |""",
        ["Leaking framework types into port signatures.", "God interface with 20 methods.", "Interface per class reflex.", "Changing port breaks all adapters silently.", "Returning ORM entities from ports."],
        "Mock works but prod fails—check port method throws checked exceptions mismatch.",
        "stable contracts hiding infrastructure details",
        "Design `AuditPort` with two implementations.",
        "Fat interface forces empty stubs—apply ISP.",
        "Python Protocol vs Java interface trade-off.",
        "Split interfaces; adapter implements subset.",
        "Document which methods optional.",
        "Protocols for internal modules; explicit types at HTTP boundary.",
        "- Abstractions face inward from domain.\n- ISP splits fat ports.\n- Adapters implement details.",
        "`D18-T003`, `D18-T005`.",
        ["Sketch port/adapter diagram.", "Split a fat interface.", "Place port package correctly."],
    )
)

# T005 DI
REST_TOPICS.append(
    _topic(
        "D18-T005",
        "d18-t005-dependency-inversion-and-injection",
        "Dependency inversion and injection",
        dedent("Dependency inversion says high-level modules should not depend on low-level details. Injection supplies implementations from outside rather than hard-coding `new`."),
        dedent("Inversion flips import direction: infrastructure implements interfaces defined by application code. Injection is constructor, setter, or framework-managed."),
        dedent("Composition root (main or Spring config) wires the graph. Request scope vs singleton affects thread safety."),
        """flowchart TD
  main[CompositionRoot]
  svc[ReportService]
  repo[ReportRepository]
  main -->|injects| svc
  main -->|binds| repo
  svc --> repo""",
        "Root builds object graph; services receive dependencies.",
        "Spring `@Bean` methods are a composition root.",
        "examples/d18_t005_di.java (unexecuted).",
        dedent(
            """
            // unexecuted
            record ReportService(ReportRepository repo) {
              String monthly() { return repo.loadSummary(); }
            }
            """
        ),
        "Constructor injection makes dependencies explicit and immutable.",
        "Use DI for DB, HTTP clients, clocks; avoid service locator hidden globals.",
        """| Style | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Constructor injection | Clear required deps | Long ctor lists | Default in services | Optional rarely-used deps |
| Setter injection | Optional deps | Mutable object | Legacy frameworks | Immutable domain |
| Framework DI | Consistent wiring | Magic to newcomers | Spring/Guice apps | 50-line scripts |""",
        ["Service locator anti-pattern.", "Field injection in tests.", "Cyclic dependencies.", "Injecting concrete classes everywhere.", "God module wiring 200 beans manually."],
        "Bean not found at startup—trace composition root and profile.",
        "depend on abstractions inject implementations at the edge",
        "Wire `Clock` port for testable time-based billing.",
        "Circular dependency between two services—fix design.",
        "Constructor vs field injection in Spring.",
        "Inject `Clock.systemUTC()` vs fixed clock in tests.",
        "Extract shared interface or event to break cycle.",
        "Prefer constructor; use `@RequiredArgsConstructor`.",
        "- Inversion owns interface direction.\n- Injection at composition root.\n- Avoid service locator.",
        "`D18-T004`, `D18-T024`.",
        ["Draw composition root.", "Break a dependency cycle.", "Test with injected fake clock."],
    )
)

# T006 UML
REST_TOPICS.append(
    _topic(
        "D18-T006",
        "d18-t006-uml-class-and-sequence-diagrams",
        "UML class and sequence diagrams",
        dedent("UML class diagrams show types, fields, and relationships; sequence diagrams show message order over time. They are communication tools for LLD interviews and design reviews."),
        dedent("Class diagrams capture structure; sequence diagrams capture behavior for one scenario. Neither replaces code—they align teams before implementation."),
        dedent("Use minimal notation: associations, implements, extends. Sequence: lifelines, synchronous calls, return dashed lines."),
        """sequenceDiagram
  participant Client
  participant Service
  participant Repo
  Client->>Service: placeOrder
  Service->>Repo: save
  Repo-->>Service: id
  Service-->>Client: 201""",
        "Sequence for one happy-path request.",
        "Whiteboard class diagram for order service collaborators.",
        "examples/d18_t006_notes.md — diagram only (unexecuted).",
        "# Diagrams are not executed code; they guide implementation and reviews.",
        "Keep diagrams at the abstraction level reviewers care about—omit every private helper.",
        "Attach sequence diagram to RFC for new endpoints; update when async steps added.",
        """| Diagram | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Class | Structure at a glance | Stale quickly | LLD interview | Auto-generated dumps |
| Sequence | Ordering clarity | Tedious for many paths | One critical flow | Whole system map |""",
        ["Over-modeling every class.", "Diagrams diverging from code.", "Using UML when a short paragraph suffices.", "Hiding async in synchronous sequence.", "Too many stereotypes."],
        "Review mismatch—compare diagram to actual call stack trace.",
        "visual contracts for structure and message order",
        "Draw class diagram for checkout module.",
        "Sequence missing async callback—fix diagram.",
        "When is a diagram waste?",
        "Include Service, Ports, Adapters only.",
        "Add async message to queue lifeline.",
        "Skip UML for trivial CRUD; use for cross-team flows.",
        "- Class = structure.\n- Sequence = time.\n- Keep minimal.",
        "`D18-T005`, `D18-T007`.",
        ["Draw sequence for login.", "Read associations on a sample diagram.", "Know when to skip UML."],
    )
)

# T007 CRC
REST_TOPICS.append(
    _topic(
        "D18-T007",
        "d18-t007-class-responsibility-and-collaboration",
        "Class responsibility and collaboration",
        dedent("CRC cards list Class, Responsibilities, and Collaborators—a lightweight way to assign OOD roles before coding. They prevent god services in LLD sessions."),
        dedent("Responsibility is a reason to exist; collaborator is another class this one talks to. One card should fit a sticky note."),
        dedent("Walk scenarios: place order touches Order, Inventory, Payment, Notification. Split when responsibilities argue."),
        """flowchart TD
  order[Order]
  inv[Inventory]
  pay[Payment]
  order --> inv
  order --> pay""",
        "Collaborators for one scenario.",
        "CRC for `RefundService`: calculate eligibility, call payment port, emit audit event.",
        "examples/d18_t007_crc.txt (unexecuted).",
        "Order: R: validate lines; C: Inventory, Pricing.",
        "Run CRC session before sprint for new bounded context.",
        """| Technique | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| CRC cards | Fast role split | Subjective | LLD interview | Post-hoc documentation only |
| SRP check | Clear ownership | Debates | Code review | Nitpicking tiny classes |""",
        ["Everything on one card.", "Confusing data class with responsibility.", "Collaborator list as implementation spec.", "Skipping scenarios.", "Cards never updated after refactor."],
        "New feature touches five classes—revisit CRC for scattered responsibility.",
        "assign responsibilities before writing classes",
        "Write CRC cards for library checkout LLD.",
        "God class discovered—map CRC to split.",
        "CRC vs full UML timebox.",
        "Four cards: Member, Book, Loan, Notification.",
        "Move payment out of Loan into PaymentPort collaborator.",
        "CRC in interview; UML optional if time short.",
        "- One primary responsibility per class.\n- Collaborators are peers.\n- Scenario walk first.",
        "`D18-T006`, `D18-T008`.",
        ["Produce CRC for parking lot.", "Split god class using CRC.", "Facilitate a 15-minute CRC session."],
    )
)

# T008 Lifecycle
REST_TOPICS.append(
    _topic(
        "D18-T008",
        "d18-t008-object-lifecycle-and-ownership",
        "Object lifecycle and ownership",
        dedent("Lifecycle covers creation, use, and disposal of objects; ownership defines who may mutate or destroy shared state. Critical for connection pools, caches, and domain aggregates."),
        dedent("RAII in C++; GC in Java/Python; scope rules still matter for resources (files, sockets). Clear ownership prevents use-after-free and double-close bugs."),
        dedent("Factory creates; aggregate root owns children; container owns singletons. Document transfer of ownership when passing references."),
        """stateDiagram-v2
  [*] --> Created
  Created --> InUse: borrow
  InUse --> Idle: release
  Idle --> Disposed: shutdown
  Disposed --> [*]""",
        "Typical pooled resource lifecycle.",
        "Who closes the HTTP response body—the caller or the wrapper?",
        "examples/d18_t008_lifecycle.java (unexecuted).",
        dedent(
            """
            // unexecuted
            try (Connection c = dataSource.getConnection()) {
              // caller owns scope; pool owns physical connection
            }
            """
        ),
        "Try-with-resources expresses lexical ownership.",
        "Per-request objects vs singleton caches—document thread safety.",
        """| Ownership | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Caller closes | Explicit | Easy to forget | Streams, connections | Framework-managed |
| Container owns | Central shutdown | Hidden rules | DataSource beans | Quick scripts |
| Aggregate owns children | Consistent invariants | Careful graph | DDD aggregates | Flat DTO graphs |""",
        ["Returning owned resource to caller without docs.", "Shared mutable singleton.", "Closing twice.", "Leak on exception path.", "Wrong scope (request bean holding user session in singleton)."],
        "Connection leak—heap dump or pool metrics; check missing close in finally.",
        "clear creation use disposal and who mutates",
        "Design lifecycle for connection pool wrapper.",
        "Memory leak from thread-local cache—fix ownership.",
        "Singleton vs prototype scope trade-off.",
        "Document borrow/release API.",
        "Clear thread-local on request end.",
        "Prototype for per-request state; singleton for stateless clients.",
        "- Own resources explicitly.\n- Pools recycle, callers borrow.\n- Match scope to thread safety.",
        "`D18-T007`, creational patterns `D18-T009`+.",
        ["Explain try-with-resources ownership.", "Pick Spring bean scope.", "Find a leak scenario."],
    )
)

# Patterns T009-T022
REST_TOPICS.append(
    pattern(
        "D18-T009",
        "d18-t009-factory-and-abstract-factory",
        "Factory and Abstract Factory",
        "Define an interface for creating an object but let subclasses or dedicated factory types decide which class to instantiate.",
        "Skip when construction is a single `new` with no variation, or when a DI container already acts as the factory.",
        """classDiagram
  class Client
  class PaymentFactory
  class StripePayment
  class AdyenPayment
  Client --> PaymentFactory
  PaymentFactory <|.. StripeFactory
  PaymentFactory <|.. AdyenFactory
  StripeFactory ..> StripePayment
  AdyenFactory ..> AdyenPayment""",
        """flowchart TD
  client[Client]
  factory[PaymentFactory]
  product[PaymentGateway]
  client --> factory
  factory --> product""",
        dedent(
            """
            // unexecuted
            interface PaymentFactory { PaymentGateway create(); }
            class StripeFactory implements PaymentFactory {
              public PaymentGateway create() { return new StripeGateway(); }
            }
            """
        ),
        "Select payment provider per merchant config without `if` chains in checkout.",
        "centralize object creation behind an interface",
        "Implement factory choosing S3 vs GCS client from config.",
        "Tests instantiate wrong product—debug factory binding.",
        "Factory vs Abstract Factory for one vs families of products.",
        "Config-driven factory method.",
        "Check env profile and bean name.",
        "Abstract factory when UI+API families vary together.",
        "Related: `D18-T010` Builder, `D18-T024` DI containers.",
    )
)

REST_TOPICS.append(
    pattern(
        "D18-T010",
        "d18-t010-builder",
        "Builder",
        "Separate construction of a complex object from its representation so the same process can create different representations.",
        "Skip for immutable data classes with three fields; use constructors or records.",
        """classDiagram
  class CheckoutRequestBuilder
  class CheckoutRequest
  CheckoutRequestBuilder --> CheckoutRequest : builds""",
        """flowchart LR
  builder[Builder]
  steps[StepByStepSetters]
  product[ComplexObject]
  builder --> steps
  steps --> product""",
        dedent(
            """
            // unexecuted
            CheckoutRequest req = CheckoutRequest.builder()
              .cartId("c1").currency("USD").build();
            """
        ),
        "HTTP request with optional fields, headers, and metadata assembled safely.",
        "stepwise assembly with validation at build()",
        "Builder for `SearchFilter` with defaults.",
        "Forgot to call build—debug null object.",
        "Builder vs telescoping constructors.",
        "Validate required fields in build().",
        "Immutable product; builder mutable until build.",
        "Telescoping ctor unreadable; builder wins.",
        "`D18-T009`, `D18-T011`.",
    )
)

REST_TOPICS.append(
    pattern(
        "D18-T011",
        "d18-t011-singleton-and-its-pitfalls",
        "Singleton and its pitfalls",
        "Ensure a class has only one instance and provide a global access point.",
        "Avoid for testability and hidden dependencies; prefer DI-scoped singletons managed by the container.",
        """classDiagram
  class Singleton
  Singleton : -static instance
  Singleton : +getInstance()""",
        """flowchart TD
  thread1[Thread1]
  thread2[Thread2]
  single[SingletonInstance]
  thread1 --> single
  thread2 --> single""",
        dedent(
            """
            // unexecuted
            // Prefer: container-managed @Singleton bean instead of static getInstance()
            """
        ),
        "Config cache as container singleton—not static mutable global.",
        "one controlled instance vs hidden global state",
        "Identify singleton abuse in legacy code.",
        "Flaky tests due to shared singleton state—fix.",
        "Container singleton vs static singleton.",
        "Replace static with injected bean.",
        "Reset or isolate state in tests.",
        "Framework manages lifecycle; static hides deps.",
        "`D18-T012`, concurrency `D18-T026`.",
    )
)

REST_TOPICS.append(
    pattern(
        "D18-T012",
        "d18-t012-prototype",
        "Prototype",
        "Specify the kinds of objects to create using a prototypical instance, and create new objects by copying this prototype.",
        "Skip when deep copy is expensive or objects are not clone-safe; prefer factories.",
        """classDiagram
  class Prototype
  class Client
  Prototype <|-- ConcretePrototype
  Client --> Prototype : clone()""",
        """flowchart LR
  proto[Prototype]
  clone[Clone]
  newObj[NewInstance]
  proto --> clone
  clone --> newObj""",
        dedent(
            """
            // unexecuted
            interface DocumentTemplate extends Cloneable {
              DocumentTemplate duplicate();
            }
            """
        ),
        "Duplicate invoice template per tenant with customized header.",
        "copy configured template instead of rebuilding",
        "Clone report template with new parameters.",
        "Shallow copy mutates shared list—debug.",
        "Prototype vs factory for expensive setup.",
        "Deep copy collections in duplicate().",
        "Use factory when construction cheap.",
        "Prototype when setup heavy and similar.",
        "`D18-T011`, `D18-T009`.",
    )
)

REST_TOPICS.append(
    pattern(
        "D18-T013",
        "d18-t013-strategy",
        "Strategy",
        "Define a family of algorithms, encapsulate each one, and make them interchangeable.",
        "Skip when only one algorithm exists or selection is static forever.",
        """classDiagram
  class Context
  class Strategy
  Context --> Strategy
  Strategy <|.. FastStrategy
  Strategy <|.. SafeStrategy""",
        """flowchart TD
  ctx[Context]
  strat[Strategy]
  ctx --> strat""",
        dedent(
            """
            // unexecuted
            interface RetryStrategy { void backoff(int attempt); }
            class ExponentialBackoff implements RetryStrategy { /* ... */ }
            """
        ),
        "Retry/backoff policies per downstream dependency.",
        "pluggable algorithms selected at runtime",
        "Strategy for tax calculation per region.",
        "Wrong strategy picked via config typo.",
        "Strategy vs if-else chain.",
        "Enum map of strategy implementations.",
        "Log strategy name in metrics.",
        "Replace switch with registry.",
        "`D18-T014`, rate limiter service in repo.",
    )
)

REST_TOPICS.append(
    pattern(
        "D18-T014",
        "d18-t014-observer",
        "Observer",
        "Define a one-to-many dependency so when one object changes state, all dependents are notified.",
        "Skip when synchronous side effects must be transactional—use domain events and outbox instead.",
        """classDiagram
  class Subject
  class Observer
  Subject --> Observer
  Observer <|.. AuditObserver""",
        """flowchart TD
  subject[Subject]
  obs1[ObserverA]
  obs2[ObserverB]
  subject --> obs1
  subject --> obs2""",
        dedent(
            """
            // unexecuted
            interface OrderListener { void onPlaced(Order o); }
            class OrderService {
              private final List<OrderListener> listeners = new ArrayList<>();
            }
            """
        ),
        "Notify analytics and email on order placed—watch ordering and failures.",
        "publish state changes to interested listeners",
        "Register listeners for domain events.",
        "Listener throws and rolls back order—fix error isolation.",
        "Observer vs message bus.",
        "Try/catch per listener or async queue.",
        "Use outbox for cross-service fan-out.",
        "In-process observer OK for same transaction cautiously.",
        "`D18-T015`, event-driven topics.",
    )
)

REST_TOPICS.append(
    pattern(
        "D18-T015",
        "d18-t015-adapter",
        "Adapter",
        "Convert the interface of a class into another interface clients expect.",
        "Skip when you own both sides and can change the API instead.",
        """classDiagram
  class Client
  class Target
  class Adaptee
  class Adapter
  Client --> Target
  Adapter ..|> Target
  Adapter --> Adaptee""",
        """flowchart LR
  client[Client]
  adapter[Adapter]
  legacy[LegacyApi]
  client --> adapter
  adapter --> legacy""",
        dedent(
            """
            // unexecuted
            class LegacySmsClient { void sendRaw(String payload) {} }
            class SmsPortAdapter implements SmsPort {
              private final LegacySmsClient legacy;
              public void send(String user, String msg) { legacy.sendRaw(format(user, msg)); }
            }
            """
        ),
        "Wrap third-party SDK behind your port interface.",
        "translate interfaces without changing legacy vendor code",
        "Adapter for old payment SDK to new port.",
        "Double encoding in adapter—debug payload.",
        "Adapter vs anti-corruption layer.",
        "Map errors to domain exceptions.",
        "Log raw vendor code on failure.",
        "ACL may include translation rules beyond syntax.",
        "`D18-T016` Decorator.",
    )
)

REST_TOPICS.append(
    pattern(
        "D18-T016",
        "d18-t016-decorator",
        "Decorator",
        "Attach additional responsibilities to an object dynamically.",
        "Skip when subclass explosion or when behavior order is unclear.",
        """classDiagram
  class Component
  class Decorator
  Component <|-- ConcreteComponent
  Decorator ..|> Component
  Decorator o-- Component""",
        """flowchart TD
  client[Client]
  deco[LoggingDecorator]
  inner[CoreService]
  client --> deco
  deco --> inner""",
        dedent(
            """
            // unexecuted
            class TimingDecorator implements HttpClient {
              private final HttpClient delegate;
              public Response execute(Request r) { long t=System.nanoTime(); var res=delegate.execute(r); log(t); return res; }
            }
            """
        ),
        "Logging/metrics wrappers around HTTP clients.",
        "stack behaviors around same interface",
        "Decorator adding retry around repository.",
        "Decorator order changes semantics—document.",
        "Decorator vs subclass.",
        "Outer retry, inner cache—define order.",
        "Keep interface stable.",
        "Subclass for true subtype behavior only.",
        "`D18-T017` Facade.",
    )
)

REST_TOPICS.append(
    pattern(
        "D18-T017",
        "d18-t017-facade",
        "Facade",
        "Provide a unified interface to a set of interfaces in a subsystem.",
        "Skip when it becomes another god object hiding necessary detail.",
        """classDiagram
  class Facade
  class SubA
  class SubB
  Facade --> SubA
  Facade --> SubB""",
        """flowchart TD
  client[Client]
  facade[OnboardingFacade]
  sub1[AccountService]
  sub2[KycService]
  client --> facade
  facade --> sub1
  facade --> sub2""",
        dedent(
            """
            // unexecuted
            class OnboardingFacade {
              void register(User u) { accounts.create(u); kyc.start(u); }
            }
            """
        ),
        "Single entry for multi-step onboarding orchestration.",
        "simplify subsystem access for callers",
        "Facade coordinating billing steps.",
        "Facade grows god methods—split use cases.",
        "Facade vs orchestrator service.",
        "One method per use case on facade.",
        "Delegate to domain services.",
        "Orchestrator may include saga logic.",
        "`D18-T018` Proxy.",
    )
)

REST_TOPICS.append(
    pattern(
        "D18-T018",
        "d18-t018-proxy",
        "Proxy",
        "Provide a surrogate or placeholder for another object to control access.",
        "Skip when transparent pass-through adds no value.",
        """classDiagram
  class Subject
  class Proxy
  class RealSubject
  Subject <|.. RealSubject
  Subject <|.. Proxy
  Proxy --> RealSubject""",
        """flowchart LR
  client[Client]
  proxy[AuthProxy]
  real[RealService]
  client --> proxy
  proxy --> real""",
        dedent(
            """
            // unexecuted
            class SecuredOrderService implements OrderService {
              private final OrderService delegate;
              public void cancel(String id) { authz.check(); delegate.cancel(id); }
            }
            """
        ),
        "Authorization wrapper before delegating to core service.",
        "control access lazy load caching remote calls",
        "Proxy adding caching to read repository.",
        "Stale cache in proxy—invalidate strategy.",
        "Proxy vs decorator intent.",
        "Document cache TTL.",
        "Proxy controls access; decorator adds behavior.",
        "Virtual proxy for lazy load expensive graph.",
        "`D18-T019` Command.",
    )
)

REST_TOPICS.append(
    pattern(
        "D18-T019",
        "d18-t019-command",
        "Command",
        "Encapsulate a request as an object.",
        "Skip for trivial one-line actions without undo/queue needs.",
        """classDiagram
  class Invoker
  class Command
  class Receiver
  Invoker --> Command
  Command --> Receiver""",
        """flowchart TD
  inv[Invoker]
  cmd[Command]
  recv[Receiver]
  inv --> cmd
  cmd --> recv""",
        dedent(
            """
            // unexecuted
            interface Job { void execute(); }
            class SendEmailJob implements Job { public void execute() { /* ... */ } }
            """
        ),
        "Background job queue items as commands.",
        "requests as objects for queue undo audit",
        "Command for undoable text edit or admin action.",
        "Command replay double-charges—idempotency keys.",
        "Command vs event.",
        "Store command idempotency token.",
        "Events are facts; commands are intentions.",
        "Replay needs deterministic handlers.",
        "`D18-T020` State.",
    )
)

REST_TOPICS.append(
    pattern(
        "D18-T020",
        "d18-t020-state",
        "State",
        "Allow an object to alter its behavior when its internal state changes.",
        "Skip when state is a simple enum with no polymorphic transitions.",
        """classDiagram
  class Context
  class State
  Context --> State
  State <|.. Draft
  State <|.. Published""",
        """flowchart TD
  ctx[Document]
  draft[DraftState]
  pub[PublishedState]
  ctx --> draft
  ctx --> pub""",
        dedent(
            """
            // unexecuted
            interface OrderState { void pay(Order ctx); }
            class PendingState implements OrderState { public void pay(Order ctx) { ctx.transition(new PaidState()); } }
            """
        ),
        "Order status transitions with guarded methods.",
        "behavior changes with internal state object",
        "Model subscription lifecycle states.",
        "Illegal transition bug—table of allowed edges.",
        "State vs strategy.",
        "State knows transitions; strategy interchangeable.",
        "Document transition matrix.",
        "Test illegal transitions throw.",
        "`D18-T021` Template Method.",
    )
)

REST_TOPICS.append(
    pattern(
        "D18-T021",
        "d18-t021-template-method",
        "Template Method",
        "Define the skeleton of an algorithm deferring some steps to subclasses.",
        "Skip when composition with strategy is clearer than inheritance.",
        """classDiagram
  class AbstractWorkflow
  class ConcreteWorkflow
  AbstractWorkflow <|-- ConcreteWorkflow""",
        """flowchart TD
  base[TemplateMethod]
  step1[StepOneHook]
  step2[FixedStep]
  base --> step1
  base --> step2""",
        dedent(
            """
            // unexecuted
            abstract class ImportJob {
              final void run() { open(); parse(); persist(); close(); }
              abstract void parse();
            }
            """
        ),
        "Batch import with shared open/close, varying parse.",
        "fixed algorithm skeleton with overridable steps",
        "Template for ETL pipeline stages.",
        "Subclass breaks invariant by overriding wrong hook.",
        "Template method vs pipeline framework.",
        "Mark hooks protected final where needed.",
        "Prefer strategy for runtime variation.",
        "Framework middleware stacks use template idea.",
        "`D18-T022` Chain.",
    )
)

REST_TOPICS.append(
    pattern(
        "D18-T022",
        "d18-t022-chain-of-responsibility",
        "Chain of Responsibility",
        "Give more than one object a chance to handle a request by chaining receivers.",
        "Skip when exactly one handler must run—use simple dispatch.",
        """classDiagram
  class Handler
  Handler --> Handler : next
  Handler <|.. AuthHandler
  Handler <|.. RateLimitHandler""",
        """flowchart LR
  req[Request]
  h1[Auth]
  h2[RateLimit]
  h3[Handler]
  req --> h1
  h1 --> h2
  h2 --> h3""",
        dedent(
            """
            // unexecuted
            abstract class Filter {
              private Filter next;
              void handle(Request r) { if (can(r)) doHandle(r); else if (next!=null) next.handle(r); }
            }
            """
        ),
        "HTTP filter chain or middleware pipeline.",
        "linked handlers each optionally processing",
        "Chain for validation filters on upload.",
        "Request falls through unhandled—ensure terminal handler.",
        "Chain vs decorator.",
        "Set explicit terminal handler.",
        "Chain stops when handled; decorator always delegates.",
        "Document short-circuit rules.",
        "`D18-T023` Repository.",
    )
)

# T023 Repository UoW
REST_TOPICS.append(
    _topic(
        "D18-T023",
        "d18-t023-repository-and-unit-of-work",
        "Repository and Unit of Work",
        dedent("Repository mediates between domain and data mapping, presenting a collection-like interface. Unit of Work tracks changes and commits one transaction."),
        dedent("Domain code speaks `save(Order)` not SQL. UoW ensures atomic commit across repositories sharing a session."),
        dedent("Implementation uses ORM session or JDBC connection bound to UoW scope—typically request or transaction scope."),
        """flowchart TD
  svc[OrderService]
  repo[OrderRepository]
  uow[UnitOfWork]
  db[(Database)]
  svc --> uow
  svc --> repo
  repo --> db
  uow --> db""",
        "Service coordinates UoW; repositories share connection.",
        "Spring `@Transactional` often plays UoW role.",
        "examples/d18_t023_repo.java (unexecuted).",
        dedent(
            """
            // unexecuted
            interface OrderRepository { Optional<Order> findById(Id id); void save(Order o); }
            """
        ),
        "Repository returns domain types, not JDBC rows.",
        "Keep queries behind repository; avoid query objects in controllers.",
        """| Pattern | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Repository | Testable persistence | Mapping layer | Rich domain | Simple CRUD anemic |
| Unit of Work | Atomic commit | Scope discipline | Multiple repos per txn | Read-only endpoints |""",
        ["Repository leaking SQL strings to services.", "One repository per table god.", "UoW wider than request.", "No transaction on write path.", "Domain depending on JPA annotations."],
        "Partial commit—UoW boundary too small or missing @Transactional.",
        "collection-like persistence with transactional unit of work",
        "Design OrderRepository interface and fake.",
        "Double save without transaction—find UoW gap.",
        "Repository per aggregate vs per table.",
        "In-memory fake implementing same interface.",
        "Wrap service method in transaction.",
        "One repo per aggregate root.",
        "- Repo hides persistence.\n- UoW defines transaction boundary.\n- Domain types at boundary.",
        "`D18-T022`, `D18-T005`, `D07` database topics.",
        ["Sketch repo for one aggregate.", "Explain UoW scope.", "Test service with fake repo."],
    )
)

# T024 DI containers
REST_TOPICS.append(
    _topic(
        "D18-T024",
        "d18-t024-dependency-injection-containers",
        "Dependency injection containers",
        dedent("Containers (Spring, Guice) build object graphs from configuration, scopes, and qualifiers. They replace manual composition roots in large apps."),
        dedent("Container reads metadata (annotations, modules) to instantiate beans, resolve dependencies, and manage lifecycles."),
        dedent("Startup: scan, create bean definitions, topological sort for injection, expose context. Request scope creates proxies in servlet apps."),
        """flowchart TD
  config[Configuration]
  container[Container]
  beans[Beans]
  config --> container
  container --> beans""",
        "Config drives container; beans are wired instances.",
        "Spring ApplicationContext as container.",
        "examples/d18_t024_spring.java (unexecuted).",
        "@Configuration @Bean methods register implementations of ports.",
        "Use container for wiring only—keep business logic out of config classes.",
        """| Feature | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Container | Consistent wiring | Learning curve | Large services | 100-line CLI |
| Auto-config | Fast bootstrap | Opaque magic | Standard stacks | Exotic deps |""",
        ["Business logic in @Configuration.", "Too many @Component scans.", "Circular dependency at startup.", "Wrong scope causing leaks.", "Testing without @SpringBootTest slice."],
        "BeanCreationException—read caused by chain for missing dependency.",
        "framework-managed object graph and scopes",
        "Register two PaymentPort beans with @Qualifier.",
        "Prototype bean injected into singleton—explain bug.",
        "Full context vs @WebMvcTest slice tests.",
        "@Bean methods with qualifiers.",
        "Singleton holds stale prototype—fix scope.",
        "Use slice tests for controllers.",
        "- Container is composition root at scale.\n- Scopes matter.\n- Keep config thin.",
        "`D18-T005`, `D18-T025`.",
        ["Explain bean scopes.", "Debug BeanCreationException.", "Write minimal @Configuration."],
    )
)

# T025 Extensibility
REST_TOPICS.append(
    _topic(
        "D18-T025",
        "d18-t025-extensibility-and-testability",
        "Extensibility and testability",
        dedent("Extensibility is adding behavior with small diffs; testability is verifying behavior without full infrastructure. Both need seams (ports, strategies)."),
        dedent("Design for change: stable abstractions, pure domain functions where possible, fakes for IO."),
        dedent("Characterization tests protect refactors. Feature toggles extend behavior in production safely."),
        """flowchart LR
  code[ProductionCode]
  seam[SeamInterface]
  fake[FakeForTests]
  code --> seam
  fake ..|> seam""",
        "Tests replace seam with fake.",
        "Extract port before second payment provider.",
        "examples/d18_t025_test.java (unexecuted).",
        "@Test void uses InMemoryRepo() { ... }",
        "Measure testability by whether service tests need Docker.",
        """| Tactic | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Ports/adapters | Fast unit tests | More types | External IO | Trivial scripts |
| Contract tests | Cross-service safety | Maintenance | Public APIs | Internal only |
| Toggles | Safe rollout | State complexity | Gradual enable | Simple bugfix |""",
        ["Testing only happy path.", "No seams—@SpringBootTest for everything.", "Over-mocking internals.", "Flaky integration tests as only safety.", "Extensibility without tests."],
        "Slow CI—profile test pyramid; add fakes at service layer.",
        "seams and tests that enable safe change",
        "Add fake clock to billing tests.",
        "Flaky test depends on real HTTP—introduce seam.",
        "Extensibility vs YAGNI debate with data.",
        "Inject Clock.fixed().",
        "HttpPort fake returns canned responses.",
        "Ship interface when second variant scheduled.",
        "- Test behavior not wiring.\n- Fakes at IO seams.\n- Contract tests at boundaries.",
        "`D18-T024`, `D18-T026`.",
        ["Improve test pyramid for a service.", "Name three seams.", "Plan extensibility for feature flag."],
    )
)

# T026 Concurrency
REST_TOPICS.append(
    _topic(
        "D18-T026",
        "d18-t026-concurrency-safe-object-design",
        "Concurrency-safe object design",
        dedent("Shared mutable objects in multi-threaded servers need clear synchronization or immutability. Design choices affect correctness under load."),
        dedent("Prefer immutable values; confine mutability to single-threaded actors; use concurrent collections when sharing."),
        dedent("Read-mostly caches need visibility rules; `@Synchronized` on wrong granularity hurts throughput."),
        """flowchart TD
  req1[RequestThread1]
  req2[RequestThread2]
  immutable[ImmutableDto]
  shared[SharedMutableCache]
  req1 --> immutable
  req2 --> immutable
  req1 --> shared
  req2 --> shared""",
        "Immutable per request; shared cache needs locks.",
        "Do not store per-user state in singleton service fields.",
        "examples/d18_t026_concurrent.java (unexecuted).",
        "private final ConcurrentHashMap<> cache = new ConcurrentHashMap<>();",
        "Document thread safety on each bean scope.",
        """| Approach | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Immutability | Safe sharing | Copy cost | DTOs, messages | Huge graphs |
| Confinement | No locks | Single thread | Event loop worker | Pool threads sharing |
| Locks | Correct mutability | Contention | In-memory cache | High write contention |""",
        ["Mutable singleton fields.", "Check-then-act races.", "Lock on interned string.", "Exposing internal mutable list.", "Deadlock between nested locks."],
        "Rare corruption under load—race on non-atomic compound action.",
        "immutability confinement or synchronized shared state",
        "Make order summary DTO immutable.",
        "Find race in lazy-init singleton.",
        "ConcurrentHashMap vs synchronized map.",
        "Record or final fields only.",
        "Use holder idiom or enum singleton.",
        "CHM for concurrent cache; synchronize compound ops.",
        "- Immutable by default.\n- Scope mutable state.\n- Document bean thread safety.",
        "`D18-T011`, OS concurrency `D03`.",
        ["Review bean for shared mutation.", "Fix check-then-act.", "Choose concurrent collection."],
    )
)

# T027 Domain modeling
REST_TOPICS.append(
    _topic(
        "D18-T027",
        "d18-t027-domain-modeling-and-invariants",
        "Domain modeling and invariants",
        dedent("Domain modeling names entities, value objects, and invariants that must always hold. LLD interviews often start here before patterns."),
        dedent("Value objects are immutable and compared by value; entities have identity. Invariants are enforced inside the aggregate."),
        dedent("Ubiquitous language aligns code terms with product language. Invalid states should be unrepresentable."),
        """flowchart TD
  aggregate[OrderAggregate]
  lines[LineItems]
  money[MoneyValue]
  aggregate --> lines
  aggregate --> money""",
        "Aggregate root owns consistency boundary.",
        "Money as value object with currency + minor units.",
        "examples/d18_t027_money.java (unexecuted).",
        dedent(
            """
            // unexecuted
            record Money(long cents, Currency currency) {
              Money add(Money other) {
                if (!currency.equals(other.currency)) throw new IllegalArgumentException();
                return new Money(cents + other.cents, currency);
              }
            }
            """
        ),
        "Enforce currency match in domain, not in controller.",
        "Map ORM entities to domain at repository boundary if needed.",
        """| Concept | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Value object | Safe math | Mapping | Money, email | Identity-heavy rows |
| Aggregate | Consistency | Load design | Transaction boundary | Entire schema one root |
| Invariant in ctor | No invalid object | Strict API | Critical rules | Draft states need flexibility |""",
        ["Primitive obsession (string money).", "Invariant only in service layer.", "Anemic entities.", "Aggregate too large.", "Leaking persistence into domain language."],
        "Invalid order shipped—invariant bypassed via setter.",
        "entities values and rules that must always hold",
        "Model Email value object with validation.",
        "Double currency addition bug—fix domain type.",
        "Aggregate size vs performance.",
        "Normalize and validate in factory.",
        "Use Money type; reject mixed currency.",
        "Split aggregate if load too heavy.",
        "- Value vs entity.\n- Invariants inside aggregate.\n- Ubiquitous language.",
        "`D18-T003`, `D18-T023`, DDD further reading.",
        ["Design value object.", "List invariants for library loan.", "Draw aggregate boundary."],
    )
)

# T028 Refactoring
REST_TOPICS.append(
    _topic(
        "D18-T028",
        "d18-t028-refactoring-and-avoiding-overengineering",
        "Refactoring and avoiding overengineering",
        dedent("Refactoring improves structure without changing behavior. Avoiding overengineering keeps designs aligned to real variation and team size."),
        dedent("Use tests as safety net; refactor in small steps; measure pain before introducing patterns."),
        dedent("Rule of three: tolerate duplication twice, abstract on third. Replace conditional with polymorphism when variants stabilize."),
        """flowchart LR
  smell[CodeSmell]
  test[AddTest]
  refactor[SmallRefactor]
  smell --> test
  test --> refactor
  refactor --> smell""",
        "Iterative loop with tests guarding behavior.",
        "Extract method before extract class; introduce interface when second implementation arrives.",
        "examples/d18_t028_refactor.py (unexecuted).",
        dedent(
            '''
            # unexecuted
            # Step 1: extract function; Step 2: move to class when second caller needs state
            def compute_total(lines): return sum(l.qty * l.price for l in lines)
            '''
        ),
        "Refactor after characterization test on pricing.",
        "Resist pattern stacking in week-one microservice.",
        """| Move | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Extract method | Clarity | None | Long method | Premature |
| Introduce pattern | Handles variation | Indirection | Second variant | Hypothetical future |
| Leave as is | Simplicity | Debt | Low churn area | Active incident magnet |""",
        ["Refactor without tests.", "Big bang rewrite.", "Pattern for one case.", "Gold plating extensibility.", "Ignoring team skill ceiling."],
        "Regression after refactor—missing characterization test on edge case.",
        "safe structural change without behavior change",
        "Plan refactor steps for god service.",
        "Over-abstracted code hard to change—simplify.",
        "When to stop refactoring.",
        "List extract class, move method, introduce port.",
        "Collapse unused strategy hierarchy.",
        "Stop when tests green and next feature cheaper.",
        "- Test first.\n- Small steps.\n- Pattern on third variant.",
        "`D18-T002`, entire D18 path.",
        ["Outline refactor plan.", "Name overengineering smell.", "Apply rule of three."],
    )
)

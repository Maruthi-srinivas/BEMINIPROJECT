# D01-T007 — Encapsulation, abstraction, inheritance, polymorphism

Topic ID: `D01-T007`
Domain: Programming Language Fundamentals
Subdomain: Encapsulation, abstraction, inheritance, polymorphism
Importance: core
Complexity: fundamentals
Dependencies: `D01-T006`, `D01-T001`
Execution status of the code in section F: executed (CPython, local)

## A. Topic Overview

Encapsulation hides internal representation behind a public API. Abstraction names essential behavior and hides incidental detail. Inheritance reuses and specializes a parent class. Polymorphism lets code use a supertype reference and run the subtype's implementation.

These four ideas are the usual pillars taught with OOP. They exist so modules can evolve independently: callers depend on stable operations, not on field layout or concrete classes.

In backend work they appear in ports and adapters, plugin payment providers, storage backends, and exception hierarchies. Interviewers probe whether you know when inheritance breaks and when interfaces are enough.

Prerequisites: objects and classes (`D01-T006`). Leads into composition versus inheritance (`D01-T008`) and interfaces or generics (`D01-T009`).

## B. First-Principles Explanation

**Encapsulation** means the object controls access to its state. External code cannot set `balance = -1` if only `withdraw` enforces non-negative results. Languages enforce with `private`, packages, or convention (`_field`).

**Abstraction** is the named contract: `PaymentGateway.charge(amount)` without exposing TLS socket details. The caller reasons about outcomes, not steps.

**Inheritance** copies the parent's method table and fields into a child. The child overrides some methods and may call `super()` for shared setup. Method resolution order walks the chain.

**Polymorphism** is the runtime effect: `gateway.charge(req)` invokes `StripeGateway.charge` or `FakeGateway.charge` depending on the object's class, through one variable typed as `PaymentGateway`.

Internally, a vtable or dictionary lookup happens on each virtual call unless optimized. `super()` in Python uses C3 MRO; Java uses single inheritance for classes and interfaces for extra contracts.

Why it works: stable abstractions reduce recompilation and retesting when implementations change. Limitations: deep inheritance couples children to parent internals; protected fields are still global within the hierarchy. Favor composition when behavior mixes (`D01-T008`).

## C. Internal Working and Architecture

Encapsulation at compile time: Java rejects `account.balance` if private. At runtime Python still allows `account._balance` if someone insists; encapsulation is discipline plus tooling.

Abstraction layers in a service:

1. **Domain port**: interface `PaymentGateway`.
2. **Adapter**: `StripeGateway` implements HTTP to Stripe.
3. **Application service**: `BillingService` depends on the port, not Stripe.

Inheritance layout: subclass object contains superclass fields first, then subclass fields. Constructor chains run base-before-derived.

Polymorphic call path:

1. Load reference typed as interface.
2. Read actual class from object header.
3. Resolve method slot; if not found, walk parents.
4. Invoke function with receiver.

Backend data flow: controller → service (abstraction) → adapter → external API. Errors bubble as domain exceptions, not as raw HTTP library types crossing inward.

## D. Diagrams and Visual Models

```mermaid
flowchart TB
  billing[BillingService]
  port[PaymentGateway interface]
  stripe[StripeGateway]
  fake[FakeGateway]
  billing --> port
  port <|.. stripe
  port <|.. fake
  billing -->|charge at runtime| stripe
```

The service depends on the port. At runtime the injected bean is concrete. Tests inject `FakeGateway` without changing `BillingService`.

## E. Examples and Analogies

Encapsulation analogy: a car's speed is changed via pedals, not by grabbing the drive shaft. Abstraction: you steer; you do not manage tire friction coefficients.

Inheritance analogy: a `SavingsAccount` is-a `Account` with extra rules. That is only valid if substituting `SavingsAccount` everywhere `Account` is expected preserves behavior (Liskov).

Polymorphism: a report generator calls `storage.read(path)`; S3 and disk implementations differ. No `if` on provider name in the report code.

Avoid: inheriting only to reuse `log()` from a `BaseService`. Avoid: overriding a method to throw "not supported". Avoid: protected mutable collections on a base class that subclasses expose.

## F. Code Examples

File: `examples/d01_t007_pillars.py`

Dependencies: Python 3 standard library only.

```python
class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, request: ChargeRequest) -> ChargeResult:
        raise NotImplementedError


class BillingService:
    def __init__(self, gateway: PaymentGateway) -> None:
        self._gateway = gateway

    def bill(self, request: ChargeRequest) -> ChargeResult:
        if request.amount_cents <= 0:
            raise ValueError("amount must be positive")
        return self._gateway.charge(request)
```

How to run: `python examples/d01_t007_pillars.py` or `backend-engineering-knowledge-base/EXERCISES/examples/d01_t007_pillars.py`.

Expected output: `ok fake-ok`

Important lines: `BillingService` encapsulates validation; gateways encapsulate provider protocol. Abstract `charge` forces each adapter to implement. Injection at construction is the polymorphic wiring point.

Edge cases: null gateway in languages without nullable types is a construction bug. Charging zero is rejected before the adapter sees it. Thread safety of a shared gateway bean depends on adapter implementation, not polymorphism itself.

This example was executed with the system Python. Output was `ok fake-ok`.

## G. Practical Backend Application

Define ports in the domain or application layer: `PaymentGateway`, `EmailSender`, `Clock`. Adapters live in infrastructure. Spring `@Autowired PaymentGateway` resolves the bean; tests `@MockBean` or pass fakes in constructors.

Encapsulation keeps Stripe SDK types out of domain code. Abstraction lets you swap sandbox and production adapters via config. Inheritance is for true taxonomies (`HttpException` subclasses), not for every shared utility.

Errors: adapter maps HTTP 402 to `PaymentDeclined`; service does not parse JSON error bodies. Observability: trace spans on adapter boundary. Scaling: stateless adapters scale horizontally; encapsulation does not add latency worth measuring.

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Encapsulation | Invariants enforced | More boilerplate getters | Mutable domain state | Pure data transfer |
| Interface abstraction | Swappable implementations | Indirection, more types | External systems | One implementation forever |
| Class inheritance | Shared code in base | Fragile base class | True is-a taxonomy | Reusing unrelated helpers |
| Polymorphism | Open for extension | Harder to trace call path | Plugin architectures | Single branch if-else is clearer |
| Protected members | Subclass access | Breaks encapsulation | Template method pattern | Public API surface |

Failure modes: **violating Liskov** (subclass tightens preconditions), **leaky abstraction** (port methods expose S3 ARNs to domain), **diamond confusion** (multiple inheritance without clear MRO).

## I. Common Mistakes and Misconceptions

- Thinking encapsulation equals getters/setters for every field.
- Using inheritance for code reuse only; breaks when child is not substitutable for parent.
- Giant interface with twenty methods; implementers stub half with `NotImplementedError`.
- Polymorphism via string `type` fields and switch statements instead of types the compiler checks.
- Calling `super()` incorrectly in constructors, leaving parent fields uninitialized.

Strong interview answers name Liskov or fragile base class, not only define the four words.

## J. Debugging and Troubleshooting

Symptoms: wrong payment provider called in prod. `AbstractMethodError` at runtime. Subclass `save` skips audit hook in parent.

Diagnosis:

1. Log implementation class name at adapter entry (once per request).
2. Print MRO if override not picked up (Python `Class.mro()`).
3. Search for `instanceof` chains that bypass polymorphism.
4. Compare test doubles with production bean wiring in DI config.

Example: `TypeError: Can't instantiate abstract class PaymentGateway`.

Mitigation: fail at startup if bean missing; integration test with real wiring profile. Long-term: keep interfaces small; prefer composition (`D01-T008`).

## K. Interview Preparation

### Beginner

#### Q1. What is encapsulation?

**Answer:** Hiding internal state and requiring interaction through methods. The object can change representation without breaking callers if the public methods stay consistent. It is about controlling access, not secrecy from attackers in the same process.

#### Q2. What is abstraction?

**Answer:** Showing only what a consumer needs to know. A `Repository` exposes `save` and `get`; it hides SQL and connection pooling. Abstraction can be an interface, an abstract class, or even a well-named module.

#### Q3. What is inheritance?

**Answer:** A class derives from a parent and acquires its fields and methods unless overridden. It models specialization when the child is substitutable for the parent. It is not the default tool for code reuse.

#### Q4. What is polymorphism?

**Answer:** One interface, many implementations. Code written against the supertype runs the subtype's method at runtime. Enables plugging adapters without editing the caller.

#### Q5. Give a backend example of polymorphism.

**Answer:** `BillingService` calls `PaymentGateway.charge`. Production wires Stripe; tests wire a fake that records calls. The service source does not branch on provider name.

### Intermediate

#### Q1. What is the Liskov substitution principle?

**Answer:** Subtypes must be usable wherever the base type is expected without surprising behavior. If `Account.withdraw` allows overdraft in a subclass but the base forbids it, callers break. Preconditions cannot strengthen; postconditions cannot weaken in ways that matter to callers.

#### Q2. What is a fragile base class?

**Answer:** A parent change breaks subclasses because they depended on protected fields or call order in `super()`. Composition avoids subclass coupling to parent implementation details.

#### Q3. Encapsulation versus module privacy?

**Answer:** Encapsulation is per-object instance state. Module privacy hides functions in a file or package. You need both: public API on services and objects, internal helpers not exported.

#### Q4. When is an abstract class better than an interface?

**Answer:** When several implementations share real code (template method, shared validation). Interfaces stay lean when implementations are unrelated. Java allows both; pick the smallest contract.

#### Q5. How does polymorphism help testing?

**Answer:** Inject fakes that implement the same port. Tests avoid network and assert interactions on the fake. Without polymorphism you patch globals or use heavy integration tests only.

### Advanced

#### Q1. How does double dispatch differ from single dispatch?

**Answer:** Single dispatch chooses method by receiver only. Double dispatch (visitor pattern, some multimethod languages) also considers argument types. Most OO languages are single dispatch; overloaded methods are resolved at compile time by static types, not runtime argument classes (Java), which surprises people.

#### Q2. What is the template method pattern?

**Answer:** A base class defines `process()` calling abstract steps `load`, `transform`, `save`. Subclasses fill steps. Inheritance shares the skeleton; hooks specialize. Risk: fragile base if step order changes.

#### Q3. How do you avoid god interfaces?

**Answer:** Split by client need (interface segregation). `Readable` and `Writable` instead of one `Repository` with twelve methods. Callers depend only on what they use.

#### Q4. Polymorphism with generics together?

**Answer:** `Repository<User, Long>` is polymorphic over storage and type-safe at compile time. See `D01-T009`. Generics fix casts; interfaces fix swapping implementations.

#### Q5. How does Spring AOP interact with encapsulation?

**Answer:** Aspects wrap public methods on beans, adding logging or transactions outside class source. Encapsulation of business rules stays in the class; cross-cutting concerns attach at proxy boundary. Misuse wraps everything and hides control flow.

### Scenarios

#### Q1. Subclass `FileStorage` overrides `delete` and skips virus scan in parent. Incidents follow. Fix?

**Answer:** Violates Liskov and fragile base. Make `delete` final in parent or use composition: `Storage` delegates to `Scanner` pipeline. Subclasses should not bypass safety hooks.

#### Q2. Team adds `if (gateway instanceof StripeGateway)` in billing for a feature flag. Review comment?

**Answer:** Breaks polymorphism. Extend the port with `supportsFeature()` or pass config into adapter. Caller stays on `PaymentGateway`.

#### Q3. Protected `List<Order> orders` on base `Customer` leaked to API. What went wrong?

**Answer:** Encapsulation broken at hierarchy level. Expose `addOrder` and return unmodifiable views. Protected is still part of the family API; treat it as public to subclasses.

#### Q4. Tests pass with mock; prod fails with real adapter. Likely gap?

**Answer:** Mock does not emulate failure modes, idempotency, or timeouts of real adapter. Contract tests against provider sandbox; align exception mapping.

#### Q5. Two payment adapters, one interface with `charge` and `refund`. Third adapter only supports charge. Design?

**Answer:** Split `RefundableGateway` extends `PaymentGateway`, or use optional capability interface. Do not throw unsupported on `refund` at runtime without documentation.

### Follow-ups

#### Q1. Composition versus inheritance for the payment example?

**Answer:** Inheritance between gateways is wrong; they are siblings under a port. Composition wires `BillingService` with a `PaymentGateway` instance. See `D01-T008`.

#### Q2. How do custom exceptions relate to inheritance?

**Answer:** Exception hierarchies use inheritance for catch granularity. Map base `DomainError` to 409 and subclasses to specific codes. See `D01-T010`.

#### Q3. Connection to API versioning?

**Answer:** Stable abstractions at the port let you add v2 adapters while keeping service code on v1 interface until migration completes.

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/D01-T007.md`. Try these before opening that file.

### Exercise 1 — implementation

Implement `BillingService` with `PaymentGateway` and a fake gateway; add `refund` on a separate optional protocol. Acceptance: positive charge works, zero amount raises, fake records call count.

### Exercise 2 — debugging

Subclass overrides parent `afterSave` but forgets `super().afterSave()`, skipping audit. Explain fragile base class and one structural fix. Acceptance: you name missed `super` or template method risk and composition alternative.

### Exercise 3 — trade-off

Replace `instanceof` provider branching with polymorphism for file storage. Acceptance: you describe a `StorageBackend` port and two adapters without `if provider` in the handler.

## M. Revision Notes

- Encapsulation: control access, enforce invariants.
- Abstraction: stable contract, hidden detail.
- Inheritance: is-a, substitutable specialization.
- Polymorphism: runtime choice of implementation.
- Liskov: subtypes must not break callers.
- Prefer small interfaces; avoid fragile base classes.
- Tests use the same ports as production.

Flashcards:

- Liskov? Subtypes substitutable for base.
- Fragile base class? Parent change breaks children.
- Port and adapter? Domain depends on port; infra implements.

## N. Related Topics

Understand this before: `D01-T006` OOP basics.

This topic supports: `D01-T008` composition, `D01-T009` interfaces and generics, `D06-T004` hexagonal architecture.

Often confused with: polymorphism as only inheritance (interfaces and duck typing count too).

Interviewers combine this with `D12-T018` testing doubles and `D03-T012` REST client adapters.

## O. Completion Criteria

- Define encapsulation, abstraction, inheritance, polymorphism with backend examples.
- Draw port/adapter diagram for payments.
- Implement billing against an abstract gateway with a fake.
- Explain a Liskov violation scenario and fix.
- Critique `instanceof` branching in a service.
- Choose abstract class versus interface for a shared template.

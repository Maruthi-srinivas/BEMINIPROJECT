# D18-T001 — SOLID principles

Topic ID: `D18-T001`
Domain: Low-Level Design (LLD) and Object-Oriented Design
Subdomain: SOLID principles
Importance: core
Complexity: intermediate
Dependencies: `D01-T001`, `D01-T002`
Execution status of the code in section F: unexecuted

## A. Topic Overview

SOLID is five design constraints for classes and modules: Single responsibility, Open-closed, Liskov substitution, Interface segregation, and Dependency inversion. They exist so teams can change one reason for change without rewriting unrelated code. Backend interviews treat SOLID as the vocabulary for reviewing services, repositories, and DTO layers. Dependencies: basic OOP from domain 1 (`D01-T001`, `D01-T002`).

## B. First-Principles Explanation

Software changes because product, compliance, and infrastructure change—not because types enjoy abstraction. Each principle attacks a failure mode: god classes, fragile base classes, fat interfaces, and concrete dependencies that block testing. SOLID is not a checklist tattoo; it is a conflict resolver when two simple designs disagree. Alternatives include functional cores with imperative shells, or small modules without classes—still map to the same forces.

## C. Internal Working and Architecture

SRP: one class, one actor's reason to change. OCP: extend via new types, not edits to stable code. LSP: subtypes honor contracts. ISP: many small interfaces beat one kitchen-sink. DIP: high-level policy depends on abstractions; details implement them. In a layered service, controllers depend on application services, which depend on port interfaces, not JDBC drivers.

## D. Diagrams and Visual Models

```mermaid
flowchart TD
  handler[HttpHandler]
  service[OrderService]
  port[OrderRepositoryPort]
  adapter[JdbcOrderRepository]
  handler --> service
  service --> port
  port <|.. adapter
```

High-level policy points at abstractions; infrastructure implements them.

## E. Examples and Analogies

Violating SRP: a `UserService` that sends email, charges cards, and builds PDFs—any marketing change edits payments code. OCP: add a new tax strategy class instead of extending a 400-line `calculateTax` switch. DIP: unit-test `OrderService` with an in-memory fake repository.

## F. Code Examples

File: `examples/d18_t001_solid.java` (unexecuted).

```java
// unexecuted
interface PaymentPort { void charge(Money amount); }
final class StripeAdapter implements PaymentPort {
  public void charge(Money amount) { /* call Stripe */ }
}
final class CheckoutService {
  private final PaymentPort payments;
  CheckoutService(PaymentPort payments) { this.payments = payments; }
  void checkout(Order order) { payments.charge(order.total()); }
}
```

Constructor injection here supports DIP and test doubles without subclassing `CheckoutService`.

## G. Practical Backend Application

Apply SOLID at module boundaries: keep domain rules free of SQL and HTTP client types. Code review rubric: can we test this service without a database? Does this class name match a single actor? Observability: smaller classes make blame and ownership clearer in incidents.

## H. Advantages, Limitations and Trade-offs

| Principle | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| SRP | Localized change | More classes | Multiple actors edit one file | Splitting trivial 20-line helpers |
| OCP | Safer extension | Indirection | Frequent new variants | No variation on horizon |
| LSP | Safe polymorphism | Strict contracts | Shared interfaces | Subtypes break invariants |
| ISP | Smaller mocks | More interfaces | Clients use subsets | One cohesive protocol |
| DIP | Testable core | Wiring layer | External systems | Script with no IO |

## I. Common Mistakes and Misconceptions

- Treating every class as needing an interface on day one.
- Confusing SRP with 'one method per class'.
- Subclassing for reuse when composition fits.
- LSP violations that throw in overrides.
- DIP only in name—service still news concrete JDBC inside methods.

## J. Debugging and Troubleshooting

Smell: a PR touches ten unrelated features because one service owns them all. Fix: extract collaborators by actor. Symptom: unit tests require a database—look for missing ports. Mitigation: introduce interfaces at IO boundaries first.

## K. Interview Preparation

### Beginner

#### Q1. What is SOLID in one sentence?

**Answer:** SOLID is five rules that keep each module focused, extensible, and testable by constraining how responsibilities and dependencies are arranged. Single responsibility limits reasons to change; open-closed favors extension over modification. Liskov substitution keeps polymorphism honest; interface segregation avoids fat contracts. Dependency inversion points high-level code at abstractions instead of vendors.

#### Q2. Why does SOLID matter in backend code?

**Answer:** Backend services integrate databases, queues, and third-party APIs that change on independent schedules. Without SOLID, a pricing tweak can break email delivery because both lived in one class. SOLID gives reviewers a shared language to spot that coupling before merge. It also makes unit tests feasible by swapping IO with fakes.

#### Q3. Give a small example of SOLID.

**Answer:** A `CheckoutService` that calls a `PaymentPort` interface illustrates DIP and ISP: checkout knows only `charge`, not Stripe HTTP details. Adding Adyen means a new adapter, not edits to checkout (OCP). If checkout also sent email, split notification into its own collaborator (SRP).

#### Q4. When would you skip strict SOLID?

**Answer:** Throwaway scripts and one-off migrations do not need full port/adapter layering. Applying SOLID everywhere on day one adds types that obscure a 50-line feature. Skip when there is no second implementation and no test need for fakes. Revisit when the second variant or integration test pain appears.

#### Q5. How is SOLID different from 'clean code' slogans?

**Answer:** SOLID names specific forces and violations, not vague aesthetics. You can argue whether a class violates SRP using actors and change history. Clean code without principles devolves into taste debates. SOLID connects directly to test doubles and release risk.

### Intermediate

#### Q1. How does each letter map to a code smell?

**Answer:** SRP maps to god services; OCP to giant switches; LSP to subclasses that throw on override; ISP to interfaces with many unused methods; DIP to `new ConcreteClient()` inside domain code. Naming the smell speeds refactors because the fix is stereotyped. Interviewers want you to connect letter to symptom, not recite definitions only.

#### Q2. How do you test DIP-compliant services?

**Answer:** Inject fakes or in-memory implementations of ports in unit tests. The service under test should not start Spring or Docker. Contract tests validate adapters against real vendors separately. This split keeps CI fast while still protecting integrations.

#### Q3. What metrics suggest SOLID violations?

**Answer:** Rising churn on one file across unrelated tickets signals SRP issues. High cyclomatic complexity in a single method suggests missing strategies or commands. Many `#ifdef` or `if (provider)` chains suggest missing OCP. Track these in code review, not only in static analysis dashboards.

#### Q4. Introduce SOLID in legacy code how?

**Answer:** Strangle the worst seam first—usually payment or notification IO. Extract an interface at that boundary without moving business rules yet. Add one characterization test, then move implementation behind an adapter. Expand only when the second change touches the same class again.

#### Q5. SOLID vs composition?

**Answer:** Composition is the mechanism; SOLID tells you what to compose. You compose collaborators to satisfy SRP and DIP. Inheritance can satisfy OCP but risks LSP violations. Prefer composition when behavior mixes unpredictably.

### Advanced

#### Q1. Thread-safety and SOLID?

**Answer:** SOLID does not imply thread safety. A correctly scoped SRP class can still be a mutable singleton shared across threads. DIP helps you inject a thread-safe clock or id generator. Document bean scopes when applying SOLID in Spring.

#### Q2. Performance cost of SOLID?

**Answer:** Extra indirection costs nanoseconds; database calls cost milliseconds. SOLID rarely dominates latency in IO-bound APIs. Profile before inlining abstractions. The cost of wrong coupling is incident time, not virtual calls.

#### Q3. SOLID in framework-heavy code?

**Answer:** Frameworks already provide template methods and proxies. Apply SOLID where you own business rules, not inside every `@Controller`. Use framework DI as the composition root for DIP. Do not fight the framework with parallel pattern stacks.

#### Q4. Versioning APIs with SOLID?

**Answer:** Keep HTTP DTOs stable; vary behavior with new strategy or adapter classes behind the same port. SOLID enables adding providers without breaking callers of the application service. Publish which adapters are active per API version.

#### Q5. Security and SOLID?

**Answer:** DIP lets you centralize authz in decorators or proxies without duplicating checks in every service method. ISP keeps security interfaces small and auditable. SRP ensures security code is not mixed with pricing logic that interns edit frequently.

### Scenarios

#### Q1. Staging-only bug—how does SOLID help?

**Answer:** Swap the staging-bound adapter in the composition root while keeping production wiring unchanged. With DIP, diff configs to see which implementation is active. Narrow blast radius because bug likely lives in one adapter, not entire service.

#### Q2. Pattern vs inline—what data decides?

**Answer:** Count real variants shipped in the last year and expected next quarter. If zero, inline is fine. If many, OCP/strategy likely pays. Measure test setup time without ports. Let data override fashion.

#### Q3. Parking-lot LLD—where SOLID?

**Answer:** Assign SRP to entry gate, spot allocator, payment, and display. Use DIP for payment gateway. Mention OCP when discussing multiple vehicle types. Draw dependencies inward to domain services.

#### Q4. One-day refactor slice?

**Answer:** Extract one port for the volatile dependency and inject it. Do not introduce six patterns. Add one test with a fake. Ship behind flag if behavior risk is high.

#### Q5. What to log?

**Answer:** Log which adapter implementation handled the request and correlation id. Do not log card data through payment ports. SOLID seams are ideal places for consistent audit logging.

### Follow-ups

#### Q1. What topic comes next?

**Answer:** DRY, KISS, and YAGNI (`D18-T002`) balance how much structure SOLID adds. Patterns (`D18-T009` onward) are recurring shapes that satisfy SOLID forces. Return to SOLID when reviews feel subjective.

#### Q2. SOLID and microservices?

**Answer:** Service boundaries are deployment units; SOLID applies inside each service. Do not split every interface into a microservice. Share nothing mutable between services; use events at the boundary.

#### Q3. Books vs reviews?

**Answer:** Books teach vocabulary; reviews teach your codebase's conventions. After reading SOLID, find one god service in your repo and propose a DIP extraction. Teach with diffs, not slides.

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/D18-T001.md`. Try these before opening that file.

### Exercise 1 — implementation

Refactor a god `InvoiceService` into SRP-aligned classes and inject a `PaymentPort`.

### Exercise 2 — debugging

Tests fail only when `MockPayment` is used—production uses real Stripe. Find the DIP violation.

### Exercise 3 — trade-off

Team wants interfaces for every DTO. Argue ISP vs YAGNI with a concrete example.

## M. Revision Notes

- SRP: one actor, one reason to change.
- OCP: extend with new types.
- LSP: subtypes must honor contracts.
- ISP: small interfaces.
- DIP: depend on abstractions.

## N. Related Topics

Supports all D18 patterns. Often confused with DRY (`D18-T002`). Prerequisites: `D01-T001`, `D01-T002`.

## O. Completion Criteria

- Name all five principles with a backend example each.
- Spot an SRP violation in a sample service.
- Sketch DIP wiring for a repository.
- Explain LSP with a counterexample.
- Trade ISP against YAGNI in a review.

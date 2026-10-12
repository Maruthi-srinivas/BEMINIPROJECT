# D18-T004 — Interfaces and abstractions

Topic ID: `D18-T004`
Domain: Low-Level Design (LLD) and Object-Oriented Design
Subdomain: Interfaces and abstractions
Importance: core
Complexity: intermediate
Dependencies: `D18-T003`, `D18-T001`, `D01-T001`, `D01-T002`
Execution status of the code in section F: unexecuted

## A. Topic Overview

Abstractions name stable contracts; interfaces (or protocols) let multiple implementations coexist. They are the hinge for testing and swapping infrastructure.

## B. First-Principles Explanation

Callers depend on meaning (save order) not mechanism (JDBC). Abstractions should be owned by the high-level module per DIP.

## C. Internal Working and Architecture

Ports in hexagonal architecture are interfaces. Adapters implement them. Default methods in Java can share small helpers without a base class.

## D. Diagrams and Visual Models

```mermaid
flowchart LR
  app[ApplicationService]
  port[NotificationPort]
  email[EmailAdapter]
  sms[SmsAdapter]
  app --> port
  port <|.. email
  port <|.. sms
```

Application depends on port; adapters plug in.

## E. Examples and Analogies

Notification port with email/SMS adapters.

## F. Code Examples

examples/d18_t004_ports.java (unexecuted).

```java
// unexecuted
interface NotificationPort { void send(String userId, String message); }
class EmailNotification implements NotificationPort {
  public void send(String userId, String message) { /* SMTP */ }
}
```

Interface owned by domain package, implemented in infrastructure.

## G. Practical Backend Application

Define ports at service boundaries; keep DTOs separate from ports unless they are the contract.

## H. Advantages, Limitations and Trade-offs

| Abstraction | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Interface | Swappable IO | Extra type | Multiple implementations | Single stable IO |
| Abstract class | Shared helper code | Inheritance coupling | Shared template | Only behavior differs |
| Protocol/duck typing | Flexible in Python | Implicit contract | Small scripts | Large cross-team API |

## I. Common Mistakes and Misconceptions

- Leaking framework types into port signatures.
- God interface with 20 methods.
- Interface per class reflex.
- Changing port breaks all adapters silently.
- Returning ORM entities from ports.

## J. Debugging and Troubleshooting

Mock works but prod fails—check port method throws checked exceptions mismatch.

## K. Interview Preparation

### Beginner

#### Q1. What is Interfaces and abstractions in one sentence?

**Answer:** Interfaces and abstractions is stable contracts hiding infrastructure details. Interviewers want a concrete backend example, not a glossary quote. Tie the definition to a change you would make in a service class or module boundary. Mention testability or deploy isolation as the payoff.

#### Q2. Why does Interfaces and abstractions matter in backend code?

**Answer:** Backend code lives for years and is changed under incident pressure. Interfaces and abstractions reduces the blast radius when requirements shift. Services integrate databases, queues, and third parties; rigid designs break at those seams. Strong answers name a bug class prevented, not only 'clean code'.

#### Q3. Give a small example of Interfaces and abstractions.

**Answer:** Pick one class in a payment or auth flow and show how stable contracts hiding infrastructure details applies. Keep the example to three types so the whiteboard stays readable. State inputs, outputs, and who calls whom. End with how you would unit-test the seam.

#### Q4. When would you skip Interfaces and abstractions?

**Answer:** Skips are valid for throwaway scripts and one-off migrations. Over-applying Interfaces and abstractions adds indirection that obscures a 50-line feature. If the variation never appears in requirements, do not build the abstraction early. YAGNI still applies inside OOD.

#### Q5. How is Interfaces and abstractions different from a random utility class?

**Answer:** Utilities are stateless bags of functions without a modeled responsibility. Interfaces and abstractions encodes a deliberate collaboration contract between roles. The difference shows up when you mock one side in tests. If you cannot draw the roles, it is probably not intentional design.

### Intermediate

#### Q1. How does Interfaces and abstractions interact with SOLID?

**Answer:** SOLID is the constraint system; patterns are recurring shapes that satisfy it. Interfaces and abstractions often supports dependency inversion and open-closed goals. Violations of single responsibility usually break the pattern silently. In reviews, map each class to one principle before naming a pattern.

#### Q2. How do you test code structured with Interfaces and abstractions?

**Answer:** Replace slow or external collaborators with fakes at the abstraction introduced by the design. For Interfaces and abstractions, tests should exercise the public contract, not private construction details. Use contract tests at integration boundaries. Avoid testing the pattern itself; test behavior.

#### Q3. What metrics or smells suggest missing Interfaces and abstractions?

**Answer:** God classes, long switch statements, and copy-pasted integration code are common smells. When every new feature edits the same method, Interfaces and abstractions may help. Rising cyclomatic complexity in one class is a signal. Also watch for duplicate error handling across adapters.

#### Q4. How would you introduce Interfaces and abstractions in a legacy service?

**Answer:** Strangler approach: extract one seam behind an interface without rewriting the world. Keep old entry points until callers migrate to the Interfaces and abstractions shape. Add characterization tests before moving code. Ship behind a feature flag if behavior could diverge.

#### Q5. Compare Interfaces and abstractions with composition.

**Answer:** Composition favors has-a wiring; patterns often compose multiple objects. Interfaces and abstractions does not replace composition; it structures it. Prefer composition when inheritance depth grows. Patterns should make collaboration explicit, not magical.

### Advanced

#### Q1. Thread-safety concerns with Interfaces and abstractions?

**Answer:** Shared mutable singletons and registries are the usual hazard. If Interfaces and abstractions caches state, document visibility and locking. In web apps, prefer request-scoped objects over global caches. Load tests expose races that unit tests miss.

#### Q2. Performance cost of Interfaces and abstractions?

**Answer:** Indirection adds allocation and virtual dispatch; usually negligible in I/O bound services. Interfaces and abstractions shines when variation is rare compared to steady-state requests. Profile before collapsing abstractions for micro-optimizations. Watch N+1 calls hidden inside facades.

#### Q3. How does Interfaces and abstractions appear in frameworks (Spring, Django)?

**Answer:** Frameworks often embed the pattern in lifecycle hooks you override. Recognize Interfaces and abstractions in template methods of middleware stacks. Do not fight the framework with a second parallel pattern. Document where your code plugs in.

#### Q4. Versioning APIs while using Interfaces and abstractions?

**Answer:** Keep DTOs stable at the boundary; vary behavior behind the pattern. Interfaces and abstractions lets you add a new strategy without breaking old clients. Publish which implementations are supported per API version. Deprecation is a product policy, not a pattern feature.

#### Q5. Security implications of Interfaces and abstractions?

**Answer:** Proxies and decorators are natural choke points for authz logging. Do not let Interfaces and abstractions bypass central validation. Command objects should not carry secrets in logs. Audit who can register implementations at runtime.

### Scenarios

#### Q1. Production bug: behavior differs only in staging. How does Interfaces and abstractions help debug?

**Answer:** Swap the implementation in staging with a recording fake. With Interfaces and abstractions, compare traces per collaborator. Check configuration wiring first. Replay the command or event that triggered the path.

#### Q2. Team debate: pattern vs inline code. What data decides?

**Answer:** Count variation points expected in the next two quarters. If only one implementation exists, Interfaces and abstractions is speculative. Measure test pain when mocking is hard. Choose the design that reduces coordinated releases.

#### Q3. Interview design: parking lot / LLD. Where Interfaces and abstractions?

**Answer:** Identify entities and lifecycles before patterns. Apply Interfaces and abstractions at the variation point the interviewer highlights. Explain trade-offs aloud while drawing. Start simple; refactor to pattern when second variant appears.

#### Q4. Refactor deadline tomorrow. Minimal Interfaces and abstractions slice?

**Answer:** Extract interface plus one alternate implementation behind factory. Move only the volatile code path into Interfaces and abstractions. Leave data classes dumb. Add one integration test on the critical path.

#### Q5. Observability: what to log with Interfaces and abstractions?

**Answer:** Log correlation id, chosen implementation name, and latency per collaborator. Avoid logging payloads that Interfaces and abstractions transforms secretly. Metrics per strategy help detect misconfiguration. Trace spans should cross the abstraction boundary.

### Follow-ups

#### Q1. Related topic after Interfaces and abstractions?

**Answer:** See the next D18 topic in the learning path for the adjacent pattern or principle. DDD and microservice boundaries reuse the same collaboration thinking. Link to dependency injection containers when wiring appears. Return to SOLID if reviews feel subjective.

#### Q2. How does Interfaces and abstractions relate to microservices?

**Answer:** Patterns are in-process; services are deployment boundaries. Do not distribute a Interfaces and abstractions graph without a compelling scaling reason. Use events between services; use patterns inside a service. Watch for duplicated pattern layers in every microservice.

#### Q3. Books vs code review for learning Interfaces and abstractions?

**Answer:** Books teach vocabulary; reviews teach local conventions. After reading Interfaces and abstractions, find it in your repo's framework integration. Keep a personal catalog of smells that triggered each pattern. Teach juniors with before-and-after diffs, not slides only.


## L. Practical Exercises

Solutions are in `EXERCISES/solutions/D18-T004.md`. Try these before opening that file.

### Exercise 1 — implementation

Design `AuditPort` with two implementations.

### Exercise 2 — debugging

Fat interface forces empty stubs—apply ISP.

### Exercise 3 — trade-off

Python Protocol vs Java interface trade-off.

## M. Revision Notes

- Abstractions face inward from domain.
- ISP splits fat ports.
- Adapters implement details.

## N. Related Topics

`D18-T003`, `D18-T005`.

## O. Completion Criteria

- Sketch port/adapter diagram.
- Split a fat interface.
- Place port package correctly.

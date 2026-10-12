# D18-T025 — Extensibility and testability

Topic ID: `D18-T025`
Domain: Low-Level Design (LLD) and Object-Oriented Design
Subdomain: Extensibility and testability
Importance: core
Complexity: intermediate
Dependencies: `D18-T024`, `D18-T001`, `D01-T001`, `D01-T002`
Execution status of the code in section F: unexecuted

## A. Topic Overview

Extensibility is adding behavior with small diffs; testability is verifying behavior without full infrastructure. Both need seams (ports, strategies).

## B. First-Principles Explanation

Design for change: stable abstractions, pure domain functions where possible, fakes for IO.

## C. Internal Working and Architecture

Characterization tests protect refactors. Feature toggles extend behavior in production safely.

## D. Diagrams and Visual Models

```mermaid
flowchart LR
  code[ProductionCode]
  seam[SeamInterface]
  fake[FakeForTests]
  code --> seam
  fake ..|> seam
```

Tests replace seam with fake.

## E. Examples and Analogies

Extract port before second payment provider.

## F. Code Examples

examples/d18_t025_test.java (unexecuted).

```java
@Test void uses InMemoryRepo() { ... }
```

Measure testability by whether service tests need Docker.

## G. Practical Backend Application

Use Extensibility and testability when a backend module is about to grow a second variation.

## H. Advantages, Limitations and Trade-offs

| Tactic | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Ports/adapters | Fast unit tests | More types | External IO | Trivial scripts |
| Contract tests | Cross-service safety | Maintenance | Public APIs | Internal only |
| Toggles | Safe rollout | State complexity | Gradual enable | Simple bugfix |

## I. Common Mistakes and Misconceptions

- Testing only happy path.
- No seams—@SpringBootTest for everything.
- Over-mocking internals.
- Flaky integration tests as only safety.
- Extensibility without tests.

## J. Debugging and Troubleshooting

Slow CI—profile test pyramid; add fakes at service layer.

## K. Interview Preparation

### Beginner

#### Q1. What is Extensibility and testability in one sentence?

**Answer:** Extensibility and testability is seams and tests that enable safe change. Interviewers want a concrete backend example, not a glossary quote. Tie the definition to a change you would make in a service class or module boundary. Mention testability or deploy isolation as the payoff.

#### Q2. Why does Extensibility and testability matter in backend code?

**Answer:** Backend code lives for years and is changed under incident pressure. Extensibility and testability reduces the blast radius when requirements shift. Services integrate databases, queues, and third parties; rigid designs break at those seams. Strong answers name a bug class prevented, not only 'clean code'.

#### Q3. Give a small example of Extensibility and testability.

**Answer:** Pick one class in a payment or auth flow and show how seams and tests that enable safe change applies. Keep the example to three types so the whiteboard stays readable. State inputs, outputs, and who calls whom. End with how you would unit-test the seam.

#### Q4. When would you skip Extensibility and testability?

**Answer:** Skips are valid for throwaway scripts and one-off migrations. Over-applying Extensibility and testability adds indirection that obscures a 50-line feature. If the variation never appears in requirements, do not build the abstraction early. YAGNI still applies inside OOD.

#### Q5. How is Extensibility and testability different from a random utility class?

**Answer:** Utilities are stateless bags of functions without a modeled responsibility. Extensibility and testability encodes a deliberate collaboration contract between roles. The difference shows up when you mock one side in tests. If you cannot draw the roles, it is probably not intentional design.

### Intermediate

#### Q1. How does Extensibility and testability interact with SOLID?

**Answer:** SOLID is the constraint system; patterns are recurring shapes that satisfy it. Extensibility and testability often supports dependency inversion and open-closed goals. Violations of single responsibility usually break the pattern silently. In reviews, map each class to one principle before naming a pattern.

#### Q2. How do you test code structured with Extensibility and testability?

**Answer:** Replace slow or external collaborators with fakes at the abstraction introduced by the design. For Extensibility and testability, tests should exercise the public contract, not private construction details. Use contract tests at integration boundaries. Avoid testing the pattern itself; test behavior.

#### Q3. What metrics or smells suggest missing Extensibility and testability?

**Answer:** God classes, long switch statements, and copy-pasted integration code are common smells. When every new feature edits the same method, Extensibility and testability may help. Rising cyclomatic complexity in one class is a signal. Also watch for duplicate error handling across adapters.

#### Q4. How would you introduce Extensibility and testability in a legacy service?

**Answer:** Strangler approach: extract one seam behind an interface without rewriting the world. Keep old entry points until callers migrate to the Extensibility and testability shape. Add characterization tests before moving code. Ship behind a feature flag if behavior could diverge.

#### Q5. Compare Extensibility and testability with composition.

**Answer:** Composition favors has-a wiring; patterns often compose multiple objects. Extensibility and testability does not replace composition; it structures it. Prefer composition when inheritance depth grows. Patterns should make collaboration explicit, not magical.

### Advanced

#### Q1. Thread-safety concerns with Extensibility and testability?

**Answer:** Shared mutable singletons and registries are the usual hazard. If Extensibility and testability caches state, document visibility and locking. In web apps, prefer request-scoped objects over global caches. Load tests expose races that unit tests miss.

#### Q2. Performance cost of Extensibility and testability?

**Answer:** Indirection adds allocation and virtual dispatch; usually negligible in I/O bound services. Extensibility and testability shines when variation is rare compared to steady-state requests. Profile before collapsing abstractions for micro-optimizations. Watch N+1 calls hidden inside facades.

#### Q3. How does Extensibility and testability appear in frameworks (Spring, Django)?

**Answer:** Frameworks often embed the pattern in lifecycle hooks you override. Recognize Extensibility and testability in template methods of middleware stacks. Do not fight the framework with a second parallel pattern. Document where your code plugs in.

#### Q4. Versioning APIs while using Extensibility and testability?

**Answer:** Keep DTOs stable at the boundary; vary behavior behind the pattern. Extensibility and testability lets you add a new strategy without breaking old clients. Publish which implementations are supported per API version. Deprecation is a product policy, not a pattern feature.

#### Q5. Security implications of Extensibility and testability?

**Answer:** Proxies and decorators are natural choke points for authz logging. Do not let Extensibility and testability bypass central validation. Command objects should not carry secrets in logs. Audit who can register implementations at runtime.

### Scenarios

#### Q1. Production bug: behavior differs only in staging. How does Extensibility and testability help debug?

**Answer:** Swap the implementation in staging with a recording fake. With Extensibility and testability, compare traces per collaborator. Check configuration wiring first. Replay the command or event that triggered the path.

#### Q2. Team debate: pattern vs inline code. What data decides?

**Answer:** Count variation points expected in the next two quarters. If only one implementation exists, Extensibility and testability is speculative. Measure test pain when mocking is hard. Choose the design that reduces coordinated releases.

#### Q3. Interview design: parking lot / LLD. Where Extensibility and testability?

**Answer:** Identify entities and lifecycles before patterns. Apply Extensibility and testability at the variation point the interviewer highlights. Explain trade-offs aloud while drawing. Start simple; refactor to pattern when second variant appears.

#### Q4. Refactor deadline tomorrow. Minimal Extensibility and testability slice?

**Answer:** Extract interface plus one alternate implementation behind factory. Move only the volatile code path into Extensibility and testability. Leave data classes dumb. Add one integration test on the critical path.

#### Q5. Observability: what to log with Extensibility and testability?

**Answer:** Log correlation id, chosen implementation name, and latency per collaborator. Avoid logging payloads that Extensibility and testability transforms secretly. Metrics per strategy help detect misconfiguration. Trace spans should cross the abstraction boundary.

### Follow-ups

#### Q1. Related topic after Extensibility and testability?

**Answer:** See the next D18 topic in the learning path for the adjacent pattern or principle. DDD and microservice boundaries reuse the same collaboration thinking. Link to dependency injection containers when wiring appears. Return to SOLID if reviews feel subjective.

#### Q2. How does Extensibility and testability relate to microservices?

**Answer:** Patterns are in-process; services are deployment boundaries. Do not distribute a Extensibility and testability graph without a compelling scaling reason. Use events between services; use patterns inside a service. Watch for duplicated pattern layers in every microservice.

#### Q3. Books vs code review for learning Extensibility and testability?

**Answer:** Books teach vocabulary; reviews teach local conventions. After reading Extensibility and testability, find it in your repo's framework integration. Keep a personal catalog of smells that triggered each pattern. Teach juniors with before-and-after diffs, not slides only.


## L. Practical Exercises

Solutions are in `EXERCISES/solutions/D18-T025.md`. Try these before opening that file.

### Exercise 1 — implementation

Add fake clock to billing tests.

### Exercise 2 — debugging

Flaky test depends on real HTTP—introduce seam.

### Exercise 3 — trade-off

Extensibility vs YAGNI debate with data.

## M. Revision Notes

- Test behavior not wiring.
- Fakes at IO seams.
- Contract tests at boundaries.

## N. Related Topics

`D18-T024`, `D18-T026`.

## O. Completion Criteria

- Improve test pyramid for a service.
- Name three seams.
- Plan extensibility for feature flag.

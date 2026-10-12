# D18-T014 — Observer

Topic ID: `D18-T014`
Domain: Low-Level Design (LLD) and Object-Oriented Design
Subdomain: Observer
Importance: core
Complexity: intermediate
Dependencies: `D18-T013`, `D18-T001`, `D01-T001`, `D01-T002`
Execution status of the code in section F: unexecuted

## A. Topic Overview

The **Observer** pattern is a recurring object collaboration that solves a specific design force in backend services.
Define a one-to-many dependency so when one object changes state, all dependents are notified.
Interviewers use it to see whether you can separate variation from stable contracts instead of growing conditional logic.
Prerequisites: `D18-T001` (SOLID) and encapsulation topics through `D18-T008` help you place the pattern correctly.

## B. First-Principles Explanation

Object-oriented design is about assigning responsibilities so that change localizes.
The Observer pattern names a small set of roles and how messages pass between them.
At runtime, the graph is ordinary method calls; the pattern is the intentional shape that keeps those calls maintainable.
Alternatives include inline switches, inheritance towers, or framework magic—each trades explicitness for brevity.

## C. Internal Working and Architecture

Components are the roles in the structure diagram: clients depend on abstractions, creators/builders/proxies hide construction or cross-cutting steps.
Execution begins at the entry point (client, invoker, or facade) and flows along the composed objects until the domain operation completes.
State is owned by the object that mutates domain data; collaborators should be stateless or document their shared state.
In a Spring or similar stack, the same graph is often assembled by a container rather than `new` calls in application code.

## D. Diagrams and Visual Models

```mermaid
flowchart TD
  subject[Subject]
  obs1[ObserverA]
  obs2[ObserverB]
  subject --> obs1
  subject --> obs2
```

Flow for Observer: client code depends on the abstraction, not the concrete variant.

## E. Examples and Analogies

### Pattern intent

          Define a one-to-many dependency so when one object changes state, all dependents are notified.

          ### Structure

          ```mermaid
          classDiagram
class Subject
class Observer
Subject --> Observer
Observer <|.. AuditObserver
          ```

          ### When not to use this pattern

          Skip when synchronous side effects must be transactional—use domain events and outbox instead.

Backend analogy: Notify analytics and email on order placed—watch ordering and failures.
Analogy: the pattern is like a interchangeable lens on a camera—body stays, lens changes the behavior without rewiring the shutter button.
Do not confuse the pattern name with every class named `*Factory` in a codebase; verify the collaboration matches the intent.

## F. Code Examples

File: `examples/d18-t014-observer.java` (illustrative, not executed in CI).

```java
// unexecuted
interface OrderListener { void onPlaced(Order o); }
class OrderService {
  private final List<OrderListener> listeners = new ArrayList<>();
}
```

This example is labeled unexecuted unless you compile it locally. Focus on role names and dependency direction.

## G. Practical Backend Application

In HTTP handlers, keep Observer behind a service interface so controllers stay thin.
Wire implementations in the composition root (module config or DI container).
Log which implementation handled a request when multiple strategies exist.
Feature flags can select implementations without rewriting business rules.

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Apply the pattern | Clear seams, easier tests | More types and wiring | Second variant is real | One implementation forever |
| Inline logic | Fast to read initially | Switch statements grow | Prototype only | Variation is production-critical |
| Framework default | Less custom code | Hidden behavior | Framework matches need | You need explicit contracts |
| Composition root | Central wiring | Bootstrap complexity | Many implementations | Tiny CLI tools |

## I. Common Mistakes and Misconceptions

- Using Observer when only one implementation will ever exist.
- Letting concrete types leak into controllers or repositories.
- Forgetting to document lifecycle (singleton vs per-request).
- Testing the wiring instead of behavior.
- Creating circular dependencies between pattern roles.

## J. Debugging and Troubleshooting

Symptom: behavior changes when you add a second implementation—usually a missing interface binding.
Check: composition root, profile-specific beans, and environment variables selecting variants.
Mitigation: add a contract test that asserts the expected implementation is active per environment.

## K. Interview Preparation

### Beginner

#### Q1. What is Observer in one sentence?

**Answer:** Observer is publish state changes to interested listeners. Interviewers want a concrete backend example, not a glossary quote. Tie the definition to a change you would make in a service class or module boundary. Mention testability or deploy isolation as the payoff.

#### Q2. Why does Observer matter in backend code?

**Answer:** Backend code lives for years and is changed under incident pressure. Observer reduces the blast radius when requirements shift. Services integrate databases, queues, and third parties; rigid designs break at those seams. Strong answers name a bug class prevented, not only 'clean code'.

#### Q3. Give a small example of Observer.

**Answer:** Pick one class in a payment or auth flow and show how publish state changes to interested listeners applies. Keep the example to three types so the whiteboard stays readable. State inputs, outputs, and who calls whom. End with how you would unit-test the seam.

#### Q4. When would you skip Observer?

**Answer:** Skips are valid for throwaway scripts and one-off migrations. Over-applying Observer adds indirection that obscures a 50-line feature. If the variation never appears in requirements, do not build the abstraction early. YAGNI still applies inside OOD.

#### Q5. How is Observer different from a random utility class?

**Answer:** Utilities are stateless bags of functions without a modeled responsibility. Observer encodes a deliberate collaboration contract between roles. The difference shows up when you mock one side in tests. If you cannot draw the roles, it is probably not intentional design.

### Intermediate

#### Q1. How does Observer interact with SOLID?

**Answer:** SOLID is the constraint system; patterns are recurring shapes that satisfy it. Observer often supports dependency inversion and open-closed goals. Violations of single responsibility usually break the pattern silently. In reviews, map each class to one principle before naming a pattern.

#### Q2. How do you test code structured with Observer?

**Answer:** Replace slow or external collaborators with fakes at the abstraction introduced by the design. For Observer, tests should exercise the public contract, not private construction details. Use contract tests at integration boundaries. Avoid testing the pattern itself; test behavior.

#### Q3. What metrics or smells suggest missing Observer?

**Answer:** God classes, long switch statements, and copy-pasted integration code are common smells. When every new feature edits the same method, Observer may help. Rising cyclomatic complexity in one class is a signal. Also watch for duplicate error handling across adapters.

#### Q4. How would you introduce Observer in a legacy service?

**Answer:** Strangler approach: extract one seam behind an interface without rewriting the world. Keep old entry points until callers migrate to the Observer shape. Add characterization tests before moving code. Ship behind a feature flag if behavior could diverge.

#### Q5. Compare Observer with composition.

**Answer:** Composition favors has-a wiring; patterns often compose multiple objects. Observer does not replace composition; it structures it. Prefer composition when inheritance depth grows. Patterns should make collaboration explicit, not magical.

### Advanced

#### Q1. Thread-safety concerns with Observer?

**Answer:** Shared mutable singletons and registries are the usual hazard. If Observer caches state, document visibility and locking. In web apps, prefer request-scoped objects over global caches. Load tests expose races that unit tests miss.

#### Q2. Performance cost of Observer?

**Answer:** Indirection adds allocation and virtual dispatch; usually negligible in I/O bound services. Observer shines when variation is rare compared to steady-state requests. Profile before collapsing abstractions for micro-optimizations. Watch N+1 calls hidden inside facades.

#### Q3. How does Observer appear in frameworks (Spring, Django)?

**Answer:** Frameworks often embed the pattern in lifecycle hooks you override. Recognize Observer in template methods of middleware stacks. Do not fight the framework with a second parallel pattern. Document where your code plugs in.

#### Q4. Versioning APIs while using Observer?

**Answer:** Keep DTOs stable at the boundary; vary behavior behind the pattern. Observer lets you add a new strategy without breaking old clients. Publish which implementations are supported per API version. Deprecation is a product policy, not a pattern feature.

#### Q5. Security implications of Observer?

**Answer:** Proxies and decorators are natural choke points for authz logging. Do not let Observer bypass central validation. Command objects should not carry secrets in logs. Audit who can register implementations at runtime.

### Scenarios

#### Q1. Production bug: behavior differs only in staging. How does Observer help debug?

**Answer:** Swap the implementation in staging with a recording fake. With Observer, compare traces per collaborator. Check configuration wiring first. Replay the command or event that triggered the path.

#### Q2. Team debate: pattern vs inline code. What data decides?

**Answer:** Count variation points expected in the next two quarters. If only one implementation exists, Observer is speculative. Measure test pain when mocking is hard. Choose the design that reduces coordinated releases.

#### Q3. Interview design: parking lot / LLD. Where Observer?

**Answer:** Identify entities and lifecycles before patterns. Apply Observer at the variation point the interviewer highlights. Explain trade-offs aloud while drawing. Start simple; refactor to pattern when second variant appears.

#### Q4. Refactor deadline tomorrow. Minimal Observer slice?

**Answer:** Extract interface plus one alternate implementation behind factory. Move only the volatile code path into Observer. Leave data classes dumb. Add one integration test on the critical path.

#### Q5. Observability: what to log with Observer?

**Answer:** Log correlation id, chosen implementation name, and latency per collaborator. Avoid logging payloads that Observer transforms secretly. Metrics per strategy help detect misconfiguration. Trace spans should cross the abstraction boundary.

### Follow-ups

#### Q1. Related topic after Observer?

**Answer:** See the next D18 topic in the learning path for the adjacent pattern or principle. DDD and microservice boundaries reuse the same collaboration thinking. Link to dependency injection containers when wiring appears. Return to SOLID if reviews feel subjective.

#### Q2. How does Observer relate to microservices?

**Answer:** Patterns are in-process; services are deployment boundaries. Do not distribute a Observer graph without a compelling scaling reason. Use events between services; use patterns inside a service. Watch for duplicated pattern layers in every microservice.

#### Q3. Books vs code review for learning Observer?

**Answer:** Books teach vocabulary; reviews teach local conventions. After reading Observer, find it in your repo's framework integration. Keep a personal catalog of smells that triggered each pattern. Teach juniors with before-and-after diffs, not slides only.


## L. Practical Exercises

Solutions are in `EXERCISES/solutions/D18-T014.md`. Try these before opening that file.

### Exercise 1 — implementation

Register listeners for domain events.

### Exercise 2 — debugging

Listener throws and rolls back order—fix error isolation.

### Exercise 3 — trade-off

Observer vs message bus.

## M. Revision Notes

- Observer: intent in one sentence.
- Draw structure with client on the left.
- Name when not to use it.
- Map to a backend integration example.

## N. Related Topics

`D18-T015`, event-driven topics.

## O. Completion Criteria

- Explain Observer intent without reading notes.
- Draw the structure mermaid from memory.
- Implement a minimal example in Java or Python.
- State two smells that suggest the pattern.
- Describe how you would test the collaboration.

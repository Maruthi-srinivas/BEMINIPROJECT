"""Topic payloads for D18-T001..D18-T028."""
from __future__ import annotations

from textwrap import dedent

from d18_helpers import ans, mk_interview


def _mistakes(items: list[str]) -> str:
    return "\n".join(f"- {x}" for x in items)


def _ex_section(e1: str, e2: str, e3: str) -> str:
    return dedent(
        f"""
        ### Exercise 1 — implementation

        {e1}

        ### Exercise 2 — debugging

        {e2}

        ### Exercise 3 — trade-off

        {e3}
        """
    ).strip()


def _completion(bullets: list[str]) -> str:
    return "\n".join(f"- {b}" for b in bullets)


def _iq(name: str, seed: str) -> list[tuple[str, str, str]]:
    """23 interview tuples: (level label for ordering, bank question, answer)."""
    return [
        ("b", f"What is {name} in one sentence?", ans(f"{name} is {seed}.", "Interviewers want a concrete backend example, not a glossary quote.", "Tie the definition to a change you would make in a service class or module boundary.", "Mention testability or deploy isolation as the payoff.")),
        ("b", f"Why does {name} matter in backend code?", ans("Backend code lives for years and is changed under incident pressure.", f"{name} reduces the blast radius when requirements shift.", "Services integrate databases, queues, and third parties; rigid designs break at those seams.", "Strong answers name a bug class prevented, not only 'clean code'.")),
        ("b", f"Give a small example of {name}.", ans(f"Pick one class in a payment or auth flow and show how {seed} applies.", "Keep the example to three types so the whiteboard stays readable.", "State inputs, outputs, and who calls whom.", "End with how you would unit-test the seam.")),
        ("b", f"When would you skip {name}?", ans("Skips are valid for throwaway scripts and one-off migrations.", f"Over-applying {name} adds indirection that obscures a 50-line feature.", "If the variation never appears in requirements, do not build the abstraction early.", "YAGNI still applies inside OOD.")),
        ("b", f"How is {name} different from a random utility class?", ans("Utilities are stateless bags of functions without a modeled responsibility.", f"{name} encodes a deliberate collaboration contract between roles.", "The difference shows up when you mock one side in tests.", "If you cannot draw the roles, it is probably not intentional design.")),
        ("i", f"How does {name} interact with SOLID?", ans("SOLID is the constraint system; patterns are recurring shapes that satisfy it.", f"{name} often supports dependency inversion and open-closed goals.", "Violations of single responsibility usually break the pattern silently.", "In reviews, map each class to one principle before naming a pattern.")),
        ("i", f"How do you test code structured with {name}?", ans("Replace slow or external collaborators with fakes at the abstraction introduced by the design.", f"For {name}, tests should exercise the public contract, not private construction details.", "Use contract tests at integration boundaries.", "Avoid testing the pattern itself; test behavior.")),
        ("i", f"What metrics or smells suggest missing {name}?", ans("God classes, long switch statements, and copy-pasted integration code are common smells.", f"When every new feature edits the same method, {name} may help.", "Rising cyclomatic complexity in one class is a signal.", "Also watch for duplicate error handling across adapters.")),
        ("i", f"How would you introduce {name} in a legacy service?", ans("Strangler approach: extract one seam behind an interface without rewriting the world.", f"Keep old entry points until callers migrate to the {name} shape.", "Add characterization tests before moving code.", "Ship behind a feature flag if behavior could diverge.")),
        ("i", f"Compare {name} with composition.", ans("Composition favors has-a wiring; patterns often compose multiple objects.", f"{name} does not replace composition; it structures it.", "Prefer composition when inheritance depth grows.", "Patterns should make collaboration explicit, not magical.")),
        ("a", f"Thread-safety concerns with {name}?", ans("Shared mutable singletons and registries are the usual hazard.", f"If {name} caches state, document visibility and locking.", "In web apps, prefer request-scoped objects over global caches.", "Load tests expose races that unit tests miss.")),
        ("a", f"Performance cost of {name}?", ans("Indirection adds allocation and virtual dispatch; usually negligible in I/O bound services.", f"{name} shines when variation is rare compared to steady-state requests.", "Profile before collapsing abstractions for micro-optimizations.", "Watch N+1 calls hidden inside facades.")),
        ("a", f"How does {name} appear in frameworks (Spring, Django)?", ans("Frameworks often embed the pattern in lifecycle hooks you override.", f"Recognize {name} in template methods of middleware stacks.", "Do not fight the framework with a second parallel pattern.", "Document where your code plugs in.")),
        ("a", f"Versioning APIs while using {name}?", ans("Keep DTOs stable at the boundary; vary behavior behind the pattern.", f"{name} lets you add a new strategy without breaking old clients.", "Publish which implementations are supported per API version.", "Deprecation is a product policy, not a pattern feature.")),
        ("a", f"Security implications of {name}?", ans("Proxies and decorators are natural choke points for authz logging.", f"Do not let {name} bypass central validation.", "Command objects should not carry secrets in logs.", "Audit who can register implementations at runtime.")),
        ("s", f"Production bug: behavior differs only in staging. How does {name} help debug?", ans("Swap the implementation in staging with a recording fake.", f"With {name}, compare traces per collaborator.", "Check configuration wiring first.", "Replay the command or event that triggered the path.")),
        ("s", f"Team debate: pattern vs inline code. What data decides?", ans("Count variation points expected in the next two quarters.", f"If only one implementation exists, {name} is speculative.", "Measure test pain when mocking is hard.", "Choose the design that reduces coordinated releases.")),
        ("s", f"Interview design: parking lot / LLD. Where {name}?", ans("Identify entities and lifecycles before patterns.", f"Apply {name} at the variation point the interviewer highlights.", "Explain trade-offs aloud while drawing.", "Start simple; refactor to pattern when second variant appears.")),
        ("s", f"Refactor deadline tomorrow. Minimal {name} slice?", ans("Extract interface plus one alternate implementation behind factory.", f"Move only the volatile code path into {name}.", "Leave data classes dumb.", "Add one integration test on the critical path.")),
        ("s", f"Observability: what to log with {name}?", ans("Log correlation id, chosen implementation name, and latency per collaborator.", f"Avoid logging payloads that {name} transforms secretly.", "Metrics per strategy help detect misconfiguration.", "Trace spans should cross the abstraction boundary.")),
        ("f", f"Related topic after {name}?", ans("See the next D18 topic in the learning path for the adjacent pattern or principle.", "DDD and microservice boundaries reuse the same collaboration thinking.", "Link to dependency injection containers when wiring appears.", "Return to SOLID if reviews feel subjective.")),
        ("f", f"How does {name} relate to microservices?", ans("Patterns are in-process; services are deployment boundaries.", f"Do not distribute a {name} graph without a compelling scaling reason.", "Use events between services; use patterns inside a service.", "Watch for duplicated pattern layers in every microservice.")),
        ("f", f"Books vs code review for learning {name}?", ans("Books teach vocabulary; reviews teach local conventions.", f"After reading {name}, find it in your repo's framework integration.", "Keep a personal catalog of smells that triggered each pattern.", "Teach juniors with before-and-after diffs, not slides only.")),
    ]


def _topic(
    tid: str,
    slug: str,
    name: str,
    overview: str,
    first: str,
    internal: str,
    flow: str,
    caption: str,
    examples: str,
    code_intro: str,
    code: str,
    code_footer: str,
    practical: str,
    table: str,
    mistakes: list[str],
    debugging: str,
    seed: str,
    ex1: str,
    ex2: str,
    ex3: str,
    sol1: str,
    sol2: str,
    sol3: str,
    revision: str,
    related: str,
    completion: list[str] | None = None,
    pattern: dict | None = None,
    code_lang: str = "java",
    code_run: str = "unexecuted",
) -> dict:
    if isinstance(table, list) and isinstance(practical, str) and practical.lstrip().startswith("|"):
        # Some topic calls omit the practical paragraph and land the table one slot early.
        completion = related if isinstance(related, list) else completion
        related = revision
        revision = sol3
        sol3 = sol2
        sol2 = sol1
        sol1 = ex3
        ex3 = ex2
        ex2 = ex1
        ex1 = seed
        seed = debugging if isinstance(debugging, str) else name
        debugging = mistakes if isinstance(mistakes, str) else f"Trace a failing case of {name}."
        mistakes = table
        table = practical
        practical = f"Use {name} when a backend module is about to grow a second variation."
    iq = _iq(name, str(seed))
    interview = mk_interview(iq)
    return {
        "meta": {"id": tid, "slug": slug, "note_path": "", "name": name, "subdomain": "", "dependencies": []},
        "pattern": pattern,
        "overview": overview.strip(),
        "first_principles": first.strip(),
        "internal": internal.strip(),
        "mermaid_flow": flow.strip(),
        "diagram_caption": caption.strip(),
        "examples": examples.strip(),
        "code_intro": code_intro.strip(),
        "code": code.strip(),
        "code_footer": code_footer.strip(),
        "code_lang": code_lang,
        "code_run": code_run,
        "practical": practical.strip(),
        "tradeoffs_table": table.strip(),
        "mistakes": _mistakes(mistakes),
        "debugging": debugging.strip(),
        "interview": interview,
        "exercises_section": _ex_section(ex1, ex2, ex3),
        "exercise_prompts": [ex1, ex2, ex3],
        "exercise_solutions": [sol1, sol2, sol3],
        "revision": revision.strip(),
        "related": related.strip(),
        "completion": _completion(
            completion
            or [
                f"Explain {name} without reading the note.",
                "Sketch the types and the call order.",
                "Name one case where you would not use it.",
            ]
        ),
    }


TABLE_GENERIC = """| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Apply the pattern | Clear seams, easier tests | More types and wiring | Second variant is real | One implementation forever |
| Inline logic | Fast to read initially | Switch statements grow | Prototype only | Variation is production-critical |
| Framework default | Less custom code | Hidden behavior | Framework matches need | You need explicit contracts |
| Composition root | Central wiring | Bootstrap complexity | Many implementations | Tiny CLI tools |"""


def pattern(
    tid: str,
    slug: str,
    name: str,
    intent: str,
    when_not: str,
    structure: str,
    flow: str,
    code: str,
    backend: str,
    seed: str,
    ex1: str,
    ex2: str,
    ex3: str,
    sol1: str,
    sol2: str,
    sol3: str,
    related_ids: str,
) -> dict:
    overview = dedent(
        f"""
        The **{name}** pattern is a recurring object collaboration that solves a specific design force in backend services.
        {intent}
        Interviewers use it to see whether you can separate variation from stable contracts instead of growing conditional logic.
        Prerequisites: `D18-T001` (SOLID) and encapsulation topics through `D18-T008` help you place the pattern correctly.
        """
    )
    first = dedent(
        f"""
        Object-oriented design is about assigning responsibilities so that change localizes.
        The {name} pattern names a small set of roles and how messages pass between them.
        At runtime, the graph is ordinary method calls; the pattern is the intentional shape that keeps those calls maintainable.
        Alternatives include inline switches, inheritance towers, or framework magic—each trades explicitness for brevity.
        """
    )
    internal = dedent(
        f"""
        Components are the roles in the structure diagram: clients depend on abstractions, creators/builders/proxies hide construction or cross-cutting steps.
        Execution begins at the entry point (client, invoker, or facade) and flows along the composed objects until the domain operation completes.
        State is owned by the object that mutates domain data; collaborators should be stateless or document their shared state.
        In a Spring or similar stack, the same graph is often assembled by a container rather than `new` calls in application code.
        """
    )
    examples = dedent(
        f"""
        Backend analogy: {backend}
        Analogy: the pattern is like a interchangeable lens on a camera—body stays, lens changes the behavior without rewiring the shutter button.
        Do not confuse the pattern name with every class named `*Factory` in a codebase; verify the collaboration matches the intent.
        """
    )
    return _topic(
        tid,
        slug,
        name,
        overview,
        first,
        internal,
        flow,
        f"Flow for {name}: client code depends on the abstraction, not the concrete variant.",
        examples,
        f"File: `examples/{slug}.java` (illustrative, not executed in CI).",
        code,
        "This example is labeled unexecuted unless you compile it locally. Focus on role names and dependency direction.",
        dedent(
            f"""
            In HTTP handlers, keep {name} behind a service interface so controllers stay thin.
            Wire implementations in the composition root (module config or DI container).
            Log which implementation handled a request when multiple strategies exist.
            Feature flags can select implementations without rewriting business rules.
            """
        ),
        TABLE_GENERIC,
        [
            f"Using {name} when only one implementation will ever exist.",
            "Letting concrete types leak into controllers or repositories.",
            "Forgetting to document lifecycle (singleton vs per-request).",
            "Testing the wiring instead of behavior.",
            "Creating circular dependencies between pattern roles.",
        ],
        dedent(
            f"""
            Symptom: behavior changes when you add a second implementation—usually a missing interface binding.
            Check: composition root, profile-specific beans, and environment variables selecting variants.
            Mitigation: add a contract test that asserts the expected implementation is active per environment.
            """
        ),
        seed,
        ex1,
        ex2,
        ex3,
        sol1,
        sol2,
        sol3,
        dedent(
            f"""
            - {name}: intent in one sentence.
            - Draw structure with client on the left.
            - Name when not to use it.
            - Map to a backend integration example.
            """
        ),
        related_ids,
        [
            f"Explain {name} intent without reading notes.",
            f"Draw the structure mermaid from memory.",
            f"Implement a minimal example in Java or Python.",
            f"State two smells that suggest the pattern.",
            f"Describe how you would test the collaboration.",
        ],
        pattern={"intent": intent, "when_not": when_not, "mermaid": structure},
    )


TOPICS: list[dict] = []

# --- Principles & practices T001-T008, T023-T028 ---

TOPICS.append(
    _topic(
        "D18-T001",
        "d18-t001-solid-principles",
        "SOLID principles",
        dedent(
            """
            SOLID is five design constraints for classes and modules: Single responsibility, Open-closed, Liskov substitution,
            Interface segregation, and Dependency inversion. They exist so teams can change one reason for change without rewriting unrelated code.
            Backend interviews treat SOLID as the vocabulary for reviewing services, repositories, and DTO layers.
            Dependencies: basic OOP from domain 1 (`D01-T001`, `D01-T002`).
            """
        ),
        dedent(
            """
            Software changes because product, compliance, and infrastructure change—not because types enjoy abstraction.
            Each principle attacks a failure mode: god classes, fragile base classes, fat interfaces, and concrete dependencies that block testing.
            SOLID is not a checklist tattoo; it is a conflict resolver when two simple designs disagree.
            Alternatives include functional cores with imperative shells, or small modules without classes—still map to the same forces.
            """
        ),
        dedent(
            """
            SRP: one class, one actor's reason to change. OCP: extend via new types, not edits to stable code. LSP: subtypes honor contracts.
            ISP: many small interfaces beat one kitchen-sink. DIP: high-level policy depends on abstractions; details implement them.
            In a layered service, controllers depend on application services, which depend on port interfaces, not JDBC drivers.
            """
        ),
        """flowchart TD
  handler[HttpHandler]
  service[OrderService]
  port[OrderRepositoryPort]
  adapter[JdbcOrderRepository]
  handler --> service
  service --> port
  port <|.. adapter""",
        "High-level policy points at abstractions; infrastructure implements them.",
        dedent(
            """
            Violating SRP: a `UserService` that sends email, charges cards, and builds PDFs—any marketing change edits payments code.
            OCP: add a new tax strategy class instead of extending a 400-line `calculateTax` switch.
            DIP: unit-test `OrderService` with an in-memory fake repository.
            """
        ),
        "File: `examples/d18_t001_solid.java` (unexecuted).",
        dedent(
            """
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
            """
        ),
        "Constructor injection here supports DIP and test doubles without subclassing `CheckoutService`.",
        dedent(
            """
            Apply SOLID at module boundaries: keep domain rules free of SQL and HTTP client types.
            Code review rubric: can we test this service without a database? Does this class name match a single actor?
            Observability: smaller classes make blame and ownership clearer in incidents.
            """
        ),
        """| Principle | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| SRP | Localized change | More classes | Multiple actors edit one file | Splitting trivial 20-line helpers |
| OCP | Safer extension | Indirection | Frequent new variants | No variation on horizon |
| LSP | Safe polymorphism | Strict contracts | Shared interfaces | Subtypes break invariants |
| ISP | Smaller mocks | More interfaces | Clients use subsets | One cohesive protocol |
| DIP | Testable core | Wiring layer | External systems | Script with no IO |""",
        [
            "Treating every class as needing an interface on day one.",
            "Confusing SRP with 'one method per class'.",
            "Subclassing for reuse when composition fits.",
            "LSP violations that throw in overrides.",
            "DIP only in name—service still news concrete JDBC inside methods.",
        ],
        "Smell: a PR touches ten unrelated features because one service owns them all. Fix: extract collaborators by actor.",
        "five cooperating constraints that keep backend modules testable and change-local",
        "Refactor a god `InvoiceService` into SRP-aligned classes and inject a `PaymentPort`.",
        "Tests fail only when `MockPayment` is used—production uses real Stripe. Find the DIP violation.",
        "Team wants interfaces for every DTO. Argue ISP vs YAGNI with a concrete example.",
        "Split into `InvoiceReader`, `InvoiceWriter`, `PaymentCoordinator`; keep DTOs separate.",
        "Concrete `new StripeClient()` inside `InvoiceService`—inject port.",
        "Interfaces on stable DTOs add noise; interfaces on IO ports add value.",
        dedent(
            """
            - SRP: one actor, one reason to change.
            - OCP: extend with new types.
            - LSP: subtypes must honor contracts.
            - ISP: small interfaces.
            - DIP: depend on abstractions.
            """
        ),
        "Supports all D18 patterns. Often confused with DRY (`D18-T002`).",
        [
            "Name all five principles with a backend example each.",
            "Spot an SRP violation in a sample service.",
            "Sketch DIP wiring for a repository.",
            "Explain LSP with a counterexample.",
            "Trade ISP against YAGNI in a review.",
        ],
    )
)

# Append remaining topics via compact definitions in part 2
from d18_topic_data_rest import REST_TOPICS  # noqa: E402

TOPICS.extend(REST_TOPICS)

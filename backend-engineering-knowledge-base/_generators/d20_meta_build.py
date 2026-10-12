# ruff: noqa: E501
"""Build TOPIC_META entries for D20 topics."""
from __future__ import annotations

TAXONOMY_BLOCK = """**How this topic fits the test taxonomy.** **Unit tests** exercise one module in isolation with doubles for I/O and finish in milliseconds. **Integration tests** wire real adapters (database, HTTP client, message broker) and prove collaborators agree on protocols. **Contract tests** freeze request/response shapes between services so teams can deploy independently. **Load tests** hold expected concurrent traffic to measure latency and error rate under normal demand. **Soak tests** run that load for hours or days to expose memory leaks, connection pool exhaustion, and gradual degradation. **Spike tests** jump traffic far above baseline in minutes to see autoscaling and queue backlogs behave. **Chaos tests** deliberately inject faults (killed pods, latency, partition) in production-like environments to validate resilience—not the same as functional correctness."""

PYTEST_FOOTER = (
    "\n\nHow to run: `pytest path/to/test_file.py -q` from your service repo.\n\n"
    "This example was **not executed** in the knowledge-base CI. Treat it as illustrative structure only."
)


def qa(q: str, a1: str, a2: str, a3: str, a4: str) -> tuple[str, str]:
    return (q, f"{a1} {a2} {a3} {a4}")


def mk_interview(
    name: str,
    focus: str,
    beginner_extra: str,
    pitfall: str,
    tool: str,
    scenario_hook: str,
) -> dict[str, list[tuple[str, str]]]:
    return {
        "beginner": [
            qa(
                f"What is {name.lower()}?",
                f"{name} is a deliberate quality activity that targets {focus}.",
                "It exists because shipping without evidence that the system behaves under real constraints is a gamble on luck.",
                "Teams schedule it where the risk is highest: before merge, before release, or before trusting a new dependency version.",
                beginner_extra,
            ),
            qa(
                f"When should you run {name.lower()} in a delivery pipeline?",
                "Run it after the change is buildable but before the change reaches users who cannot roll back easily.",
                "Fast feedback belongs on every pull request; expensive runs belong on main or nightly schedules.",
                "The gate should fail the pipeline when invariants break, not only when someone remembers to look at a dashboard.",
                f"For {focus}, that usually means blocking merge on failures that reproduce customer impact.",
            ),
            qa(
                f"How is {name.lower()} different from clicking through the UI manually?",
                "Manual exploration is valuable for usability and surprises, but it is not repeatable at scale.",
                "Automated checks encode the same steps and assertions so two engineers on two machines get the same verdict.",
                "Automation also runs on every commit, which manual passes cannot afford.",
                f"{name} should leave an artifact: logs, junit XML, or a metrics report tied to a git SHA.",
            ),
            qa(
                "Where does this sit in the test pyramid?",
                "The pyramid is a budget: many fast tests at the bottom, fewer slow tests at the top.",
                f"{name} typically sits {scenario_hook} because of runtime, flakiness, or infrastructure cost.",
                "Pushing everything to the top creates a slow pipeline and teams stop running tests.",
                "Pushing everything to the bottom misses failures that only appear when real wires are connected.",
            ),
            qa(
                f"What is a minimal passing bar for {name.lower()} on a new microservice?",
                "Start with one happy path and one failure path that matches your SLA story.",
                "Add assertions on observability: correlation id in logs, correct status code, idempotent retry behavior.",
                "Document how to run locally in the README so onboarding is not blocked on CI secrets.",
                f"Expand coverage when {pitfall} has burned you once in staging or production.",
            ),
        ],
        "intermediate": [
            qa(
                f"How do you keep {name.lower()} from becoming flaky?",
                "Flakiness is a product bug in the test suite: it trains engineers to ignore red builds.",
                "Eliminate wall-clock sleeps; wait on conditions with timeouts and clear failure messages.",
                "Isolate shared state: unique tenants, random suffixes, and cleanup in fixtures.",
                f"For {focus}, the usual flake source is {pitfall}.",
            ),
            qa(
                f"What data strategy works best for {name.lower()}?",
                "Prefer builders or factories that create the smallest object graph that still exercises the path.",
                "Avoid copying production dumps into CI; they are huge, sensitive, and stale.",
                "Seed reference data once per suite when it is read-only; mutate per test when isolation matters.",
                "Version fixture schemas with migrations so tests fail when the database shape drifts.",
            ),
            qa(
                f"How should failures in {name.lower()} be triaged?",
                "First classify: product regression, test bug, or environment drift.",
                "Re-run from the same commit with the same seed; if it passes, treat as flake and quarantine the test.",
                "Capture service logs, SQL, and request/response bodies at failure time.",
                f"When {tool} is involved, compare versions and configuration against the last green main build.",
            ),
            qa(
                "How does this relate to unit versus integration testing?",
                "Unit tests prove logic with collaborators replaced by fakes; integration tests prove wiring.",
                f"{name} often assumes some real infrastructure, so it is closer to integration than to pure unit work.",
                "Keep business rules in unit tests so integration suites stay short.",
                "Use contract tests at boundaries so integration does not require every downstream service online.",
            ),
            qa(
                f"What metrics prove {name.lower()} is worth the CI minutes?",
                "Track time to signal: median and p95 duration per stage.",
                "Track defect escape rate: bugs found in prod that this stage would have caught.",
                "Track flake rate: percentage of failed builds that pass on retry without code change.",
                "If duration grows without escape rate dropping, refactor the suite before adding more cases.",
            ),
        ],
        "advanced": [
            qa(
                f"How do you parallelize {name.lower()} safely?",
                "Parallelism only works when tests do not share mutable global resources.",
                "Partition by tenant, database schema, or ephemeral container per worker.",
                "Use deterministic ports or dynamic allocation from the test runner.",
                "Collect junit per shard and merge in CI so one slow shard does not hide failures.",
            ),
            qa(
                f"How do you test backward compatibility while evolving {focus}?",
                "Keep golden files or contract fixtures for the previous version.",
                "Run consumer tests against both old and new provider builds in a matrix job.",
                "Feature-flag behavior and assert both paths until the flag is removed.",
                "Never delete a field consumers still parse without a deprecation window and telemetry.",
            ),
            qa(
                "How do chaos or load tests differ from functional tests?",
                "Functional tests ask whether the answer is correct for a given input.",
                "Load and soak tests ask whether latency and error rate stay within SLO under sustained demand.",
                "Spike tests ask whether autoscaling and queues absorb a sudden jump.",
                "Chaos tests ask whether the system degrades gracefully when dependencies fail; they do not replace assertions on business rules.",
            ),
            qa(
                f"When is {name.lower()} the wrong tool?",
                "Do not use it to prove visual design or copywriting.",
                "Do not use a full end-to-end suite to check a pure function; that hides the failing line.",
                "Do not run destructive chaos in shared staging without blast-radius controls.",
                f"If {pitfall} is the only risk, a lighter technique may suffice.",
            ),
            qa(
                "How do you design tests for microservices ownership boundaries?",
                "Each team owns tests for its deployable artifact and publishes contracts for its API.",
                "Cross-team journeys belong in a thin smoke suite, not in every service repo.",
                "Shared staging environments need namespace isolation and synthetic identities.",
                "Failure ownership follows the service that changed, proven by tracing the failing contract or integration test to a team.",
            ),
        ],
        "scenarios": [
            qa(
                "CI is green but production errors spike after deploy. What testing gap do you suspect?",
                "Suspect missing coverage on the changed integration path or a config difference between CI and prod.",
                "Check whether canary metrics diverged before the full rollout completed.",
                "Compare feature flags, connection strings, and dependency versions.",
                f"{name} should have caught a mismatch in {focus} if the scenario was represented in data and environment parity.",
            ),
            qa(
                "A test passes locally and fails only in CI. What do you check first?",
                "Compare language runtime, dependency lockfiles, and timezone/locale settings.",
                "Look for tests that bind to localhost ports already in use on the shared runner.",
                "Ensure secrets and service URLs come from CI env vars, not developer `.env` files.",
                f"Reproduce with the same container image CI uses; {pitfall} often appears only under resource limits.",
            ),
            qa(
                "Product wants to skip tests to hit a deadline. How do you respond?",
                "Quantify risk: what paths changed, what is untested, and what rollback looks like.",
                "Offer a scoped test plan: smoke plus targeted regression on touched modules.",
                "Never disable the entire pipeline silently; use a tracked waiver with an expiry date.",
                "Schedule a hardening sprint immediately after launch if waivers are granted.",
            ),
            qa(
                "Two services blame each other for a broken release. How do tests settle it?",
                "Run consumer contract tests against the provider artifact at the failing SHA.",
                "Replay production traffic samples in a sandbox if privacy policy allows.",
                "Use distributed tracing ids from a failing integration test to see which hop changed.",
                "The failing contract or integration test becomes the ticket owner for the team that broke compatibility.",
            ),
            qa(
                "Latency SLO is missed only under load. Which tests do you add?",
                "Add a load test at expected RPS with pass/fail thresholds on p95 latency and error rate.",
                "Follow with a soak test to catch connection leaks that appear after hours.",
                "Add a spike test if marketing events cause step jumps in traffic.",
                "Functional tests alone will stay green while thread pools or GC pressure kill throughput.",
            ),
        ],
        "followups": [
            qa(
                "How does this connect to CI test pipelines?",
                "Pipelines should stage fast unit work first, then integration, then optional performance or chaos jobs.",
                "Artifacts from each stage must be retained long enough to debug flakes.",
                "Branch protection should require the stages that map to your risk model.",
                "See `D20-T025` for job graph patterns and caching.",
            ),
            qa(
                "How does Testcontainers change this topic?",
                "Ephemeral containers give real Postgres, Redis, or Kafka without a shared pet staging server.",
                "Startup time trades against fidelity; cache images on runners.",
                "Wire health waits instead of fixed sleeps.",
                "See `D20-T026` for lifecycle and parallel worker patterns.",
            ),
            qa(
                "How does test coverage relate to confidence here?",
                "Coverage counts lines executed, not assertions about behavior.",
                "High coverage with weak asserts creates false confidence.",
                "Use coverage to find untested branches, then add meaningful cases.",
                "See `D20-T024` for quality signals beyond a percentage gate.",
            ),
        ],
    }


def code_block(filename: str, body: str) -> str:
    return (
        f"File: `examples/{filename}`\n\n"
        "Dependencies: `pytest` (illustrative; not installed in this knowledge-base repo by default).\n\n"
        f"```python\n{body.strip()}\n```"
        + PYTEST_FOOTER
    )


def exercises_block(ex1: str, ex2: str, ex3: str) -> str:
    return f"""### Exercise 1 — implementation

{ex1}

### Exercise 2 — debugging

{ex2}

### Exercise 3 — trade-off

{ex3}"""


def build_topic(
    tid: str,
    name: str,
    focus: str,
    overview_extra: str,
    principles: str,
    internal: str,
    mermaid: str,
    diagram_caption: str,
    examples: str,
    code_filename: str,
    code_body: str,
    practical: str,
    tradeoffs: str,
    mistakes: str,
    debugging: str,
    pitfall: str,
    tool: str,
    pyramid_hint: str,
    ex1: str,
    ex2: str,
    ex3: str,
    sol1: str,
    sol2: str,
    sol3: str,
    revision: str,
    completion: str,
    *,
    include_taxonomy: bool = True,
    prereq: str | None = None,
    confused_with: str | None = None,
    beginner_extra: str | None = None,
) -> dict:
    be = beginner_extra or (
        f"Interviewers expect you to name what is in scope for {name.lower()} and what belongs in another layer."
    )
    return {
        "include_taxonomy": include_taxonomy,
        "overview": (
            f"{name} is how backend teams gain evidence that {focus} works before customers depend on it. "
            f"{overview_extra} "
            "In production systems the cost of a missed defect is downtime, bad data, or security exposure—not a red IDE squiggle. "
            "Interviewers use this topic to see whether you can choose the right test layer and keep pipelines fast enough that engineers still run them."
        ),
        "first_principles": principles,
        "internal": internal,
        "mermaid": mermaid,
        "diagram_caption": diagram_caption,
        "examples": examples,
        "code_section": code_block(code_filename, code_body),
        "practical": practical,
        "tradeoffs": tradeoffs,
        "mistakes": mistakes,
        "debugging": debugging,
        "interview": mk_interview(name, focus, be, pitfall, tool, pyramid_hint),
        "exercises": exercises_block(ex1, ex2, ex3),
        "exercise_list": [ex1.split("Acceptance")[0].strip(), ex2.split("Acceptance")[0].strip(), ex3.split("Acceptance")[0].strip()],
        "solution_list": [sol1, sol2, sol3],
        "revision": revision,
        "completion": completion,
        "prereq": prereq,
        "confused_with": confused_with or "manual QA versus automated regression",
    }


def all_topics() -> dict[str, dict]:
    topics: dict[str, dict] = {}

    topics["D20-T001"] = build_topic(
        "D20-T001",
        "Unit testing",
        "a single function or class with collaborators replaced by test doubles",
        "Unit tests are the default safety net for pricing rules, validation, and state machines.",
        "A unit under test is one cohesive module whose public API you call directly. Dependencies that touch disk, network, or time are replaced with fakes so the test proves logic, not wiring. The Arrange-Act-Assert pattern keeps each test one behavior. Tests should be deterministic: same input, same output, no hidden order dependence.",
        "Components: test runner (pytest, JUnit), test case, assertions, and optional fixtures for shared setup. Execution flow: discover tests, run setup hooks, invoke the unit, assert outcomes, teardown. CI publishes junit XML and coverage if configured. Failures should print expected versus actual without scrolling through framework noise.",
        """flowchart LR
  dev[Developer edits code]
  ut[Unit test suite]
  cov[Coverage report optional]
  dev --> ut
  ut -->|fail| fix[Fix locally]
  ut -->|pass| pr[Pull request]
  pr --> ci[CI unit stage]
  ci --> cov""",
        "Read left to right: unit tests are the first gate before slower stages run.",
        "Analogy: unit tests are spell-check on one paragraph, not proof that the whole essay persuades. Backend example: test that `apply_discount` rejects negative percentages without starting Spring or Postgres.",
        "d20_t001_unit_discount.py",
        '''import pytest\nfrom decimal import Decimal\n\n\ndef apply_discount_cents(amount_cents: int, percent: int) -> int:\n    if percent < 0 or percent > 100:\n        raise ValueError("percent out of range")\n    return amount_cents - (amount_cents * percent // 100)\n\n\ndef test_apply_discount_rejects_negative_percent():\n    with pytest.raises(ValueError, match="percent"):\n        apply_discount_cents(1000, -1)\n\n\ndef test_apply_discount_rounds_down_on_cents():\n    assert apply_discount_cents(1000, 15) == 850''',
        "Every service should keep unit tests for domain rules near the domain package. Handlers stay thin; heavy logic is testable without HTTP. Run them on every push with a sub-minute budget. Pair with mutation testing later if asserts feel weak.",
        "| Choice | Benefit | Cost | Choose when | Avoid when |\n| --- | --- | --- | --- | --- |\n| Heavy mocking | Fast, isolated | Brittle if over-mocked | External I/O at edges | Testing trivial data classes |\n| Real objects | Less mock drift | Slower setup | Pure domain graphs | Need network |\n| Parameterized tests | Many cases, one test | Harder to debug one case | Tables of inputs | Each case needs unique setup |",
        "- Calling unit tests on code that only works with a live database—that is integration testing.\n- Asserting only `not None` instead of business outcomes.\n- Sharing mutable global fixtures between tests.\n- Testing private methods instead of public behavior.",
        "Symptom: suite passes but prod math is wrong. Check whether tests use floats while prod uses integer cents. Symptom: slow unit suite. Profile imports and replace Spring context tests with plain tests.",
        "shared clock or random seeds without injection",
        "pytest",
        "at the wide base of the pyramid",
        "Write unit tests for a `parse_page_token` cursor helper: valid token round-trips, malformed token raises, empty means first page. Acceptance: three tests, no network.",
        "A unit test passes but production still applies the wrong tax rate. The test mocked the tax service to always return 0.08. Name the testing smell and the fix. Acceptance: you say the mock lied about behavior and you need a contract or integration test for the real rate source.",
        "Team debates testing private `calculate_fee` versus public `quote_order`. Argue for testing through the public API only. Acceptance: mention refactor freedom and behavior-focused asserts.",
        "Use `@pytest.mark.parametrize` for three discount percentages on 999 cents. Keep asserts on integer results.",
        "The smell is an over-specified mock that hides integration drift. Add a contract test against the tax provider fixture or an integration test with recorded responses.",
        "Public API tests survive refactors; private tests break on rename without catching new user-visible bugs.",
        "- Unit = one module, doubles for I/O.\n- AAA pattern; one behavior per test.\n- Not integration; not load.\n- Fast enough for every commit.\n- Assert outcomes, not implementation details.",
        "- Write a unit test without starting the framework server.\n- Explain unit versus integration versus contract in one minute.\n- Spot a bad mock that hides a production bug.\n- Keep a unit stage under one minute on CI.",
        confused_with="integration tests that boot the whole application context",
    )

    topics["D20-T002"] = build_topic(
        "D20-T002",
        "Integration testing",
        "real adapters wired together (database, HTTP, cache) in one process or test harness",
        "Integration tests catch mistakes unit tests miss: wrong SQL, migration drift, and serializer mismatches.",
        "Integration testing validates that modules cooperate through real protocols. The database is real (often containerized); HTTP may use an in-memory server or Testcontainers wiremock. Scope is a vertical slice: repository plus service, or API plus database. Tests are slower and fewer than unit tests.",
        "Typical stack: application under test, test database, migration runner, fixture loader, HTTP client. Lifecycle: start dependencies, apply migrations, run test, truncate or rollback, stop containers. Parallel runs need schema-per-worker or disposable databases.",
        """flowchart TD
  api[API layer]
  svc[Service layer]
  repo[Repository]
  db[(Test database)]
  api --> svc --> repo --> db""",
        "This is the slice integration tests usually cover—real persistence, real SQL.",
        "Analogy: unit tests check each instrument; integration tests check they stay in tune together. Example: create order via repository, assert row and outbox message exist.",
        "d20_t002_integration_order_repo.py",
        '''import pytest\n\npytestmark = pytest.mark.integration\n\n\ndef test_create_order_persists_row(order_repo, db_conn):\n    order_id = order_repo.create(user_id=7, total_cents=2500)\n    row = db_conn.execute("SELECT total_cents FROM orders WHERE id=%s", (order_id,)).fetchone()\n    assert row[0] == 2500''',
        "Run integration tests on main and nightly if they exceed five minutes. Tag with `@pytest.mark.integration` so developers can skip locally. Use the same migration path as production.",
        "| Real DB | Fidelity | Setup time | Core persistence paths | Pure logic |\n| In-memory H2 | Fast | Divergent SQL | Java quick checks | Postgres-specific features |\n| Shared staging | Realistic | Flaky multi-team | Manual exploration | Automated PR gates |",
        "- Calling every test integration and losing speed.\n- No cleanup between tests causing order-dependent failures.\n- Using production connection strings in CI.",
        "Failure: connection refused. Check container health and port mapping. Failure: migration mismatch. Run flyway/alembic against empty DB in CI.",
        "leftover rows from parallel tests",
        "Testcontainers or docker-compose",
        "above unit tests, below full E2E",
        "Add an integration test that proves a unique constraint on `email` surfaces as your domain exception. Acceptance: two inserts, second fails predictably.",
        "Flaky test: order total wrong every tenth run. Suspect race in async outbox publish. Describe isolation fix. Acceptance: mention transactional outbox or await with timeout.",
        "Choose between H2 and Postgres for CI. Acceptance: name SQL dialect risk versus fidelity.",
        "Second insert expects `DuplicateEmailError` from service layer.",
        "Use transactional test rollback per case or serial execution with row-level locks; assert outbox only after commit.",
        "Postgres for CI when you use JSONB, partial indexes, or advisory locks; H2 only for ORM smoke.",
        "- Integration = real wires, limited slice.\n- Slower than unit; tag and stage in CI.\n- Migrations must match prod.\n- Clean data per test.\n- Not the same as contract or E2E.",
        "- Draw the slice your integration test covers.\n- Explain cleanup strategy.\n- Compare unit vs integration for a repository bug.",
        confused_with="end-to-end tests that drive the UI",
    )

    # Remaining topics: compact but complete definitions
    specs = [
        (
            "D20-T003",
            "Component testing",
            "a deployable component (service jar, lambda) with external systems stubbed at boundaries",
            "Component tests sit between integration and E2E: real binary, faked neighbors.",
            "You boot the service artifact and replace downstream HTTP with stubs. Validates configuration, health checks, and message serialization for one box.",
            """flowchart LR
  comp[Service component]
  stub[Stub downstream API]
  bus[In-memory broker optional]
  comp --> stub
  comp --> bus""",
            "d20_t003_component_health.py",
            '''def test_health_returns_ok(component_client):\n    resp = component_client.get("/health")\n    assert resp.status_code == 200\n    assert resp.json()["status"] == "ok"''',
            "wiremock",
            "mid-pyramid, one deployable at a time",
        ),
        (
            "D20-T004",
            "API testing",
            "HTTP/gRPC handlers against running app with real serialization and auth middleware",
            "API tests assert status codes, headers, and JSON schema at the boundary.",
            "Client issues requests; server runs full stack except optional external SaaS. Covers validation errors, authz, and pagination contracts.",
            """sequenceDiagram
  client[Test HTTP client]
  api[API server]
  client->>api: POST /orders
  api-->>client: 201 + body""",
            "d20_t004_api_create_order.py",
            '''def test_create_order_returns_201(api_client, auth_header):\n    r = api_client.post("/orders", json={"sku": "A1", "qty": 2}, headers=auth_header)\n    assert r.status_code == 201\n    assert "id" in r.json()''',
            "httpx or requests",
            "service boundary layer",
        ),
        (
            "D20-T005",
            "End-to-end testing",
            "user-visible flows across multiple services and UIs",
            "E2E proves critical journeys work; keep the count tiny.",
            "Scripts drive browser or mobile client through checkout-like flows. Highest fidelity, highest flake and maintenance cost.",
            """flowchart LR
  ui[Browser driver]
  fe[Frontend]
  be[Backend APIs]
  ui --> fe --> be""",
            "d20_t005_e2e_checkout.py",
            '''def test_guest_checkout_happy_path(playwright_page, base_url):\n    page = playwright_page\n    page.goto(f"{base_url}/cart")\n    page.click("text=Checkout")\n    assert page.locator("text=Thank you").is_visible()''',
            "Playwright",
            "top of pyramid, few tests",
        ),
        (
            "D20-T006",
            "Contract testing",
            "published API schemas between consumer and provider teams",
            "Contract tests stop independent deploys from breaking JSON field shapes.",
            "Provider verifies it still satisfies recorded interactions; consumer verifies it can parse provider responses. Not a substitute for business logic unit tests.",
            """flowchart LR
  consumer[Consumer tests]
  pact[Pact broker]
  provider[Provider verification]
  consumer --> pact
  provider --> pact""",
            "d20_t006_contract_pact.py",
            '''def test_get_user_contract(pact_verify):\n    expected = {"id": "1", "email": "a@b.c"}\n    pact_verify("GET", "/users/1", response=expected)''',
            "Pact or Spring Cloud Contract",
            "horizontal boundary, not full stack depth",
            include_taxonomy=True,
        ),
        (
            "D20-T007",
            "Consumer-driven contracts",
            "consumers defining expected interactions that providers must satisfy",
            "CDC flips the usual integration model: demand flows from clients.",
            "Consumers publish expected requests/responses; providers run verification jobs before release. Enables parallel team velocity.",
            """flowchart TD
  c1[Consumer A pact]
  c2[Consumer B pact]
  prov[Provider verify job]
  c1 --> prov
  c2 --> prov""",
            "d20_t007_cdc_consumer.py",
            '''def test_list_orders_shape(given, api):\n    given("orders service").upon_receiving("list").will_respond_with(200, body=[{"id": "1"}])\n    with api:\n        assert api.list_orders()[0]["id"] == "1"''',
            "Pact consumer DSL",
            "contract layer between services",
        ),
        (
            "D20-T008",
            "Regression testing",
            "re-running tests to ensure old behavior still holds after change",
            "Regression suites protect against silent breakage in stable features.",
            "Any automated test can be regression; the practice is selective re-run of high-value cases on each change.",
            """flowchart LR
  change[Code change]
  suite[Regression suite]
  change --> suite
  suite -->|fail| block[Block release]""",
            "d20_t008_regression_marker.py",
            '''import pytest\n\n@pytest.mark.regression\ndef test_legacy_tax_rounding():\n    assert round_tax(199) == 200''',
            "pytest markers",
            "entire pyramid on each merge",
        ),
        (
            "D20-T009",
            "Smoke and sanity testing",
            "minimal checks that the build is testable and core paths respond",
            "Smoke runs after deploy; sanity targets one area after a fix.",
            "Smoke is wide and shallow; sanity is narrow after a patch. Both should finish in minutes.",
            """flowchart TD
  deploy[Deploy]
  smoke[Smoke tests]
  deploy --> smoke
  smoke -->|pass| promote[Promote]
  smoke -->|fail| rollback[Rollback]""",
            "d20_t009_smoke.py",
            '''def test_smoke_health_and_readiness(client):\n    assert client.get("/health").status_code == 200\n    assert client.get("/ready").status_code == 200''',
            "curl or pytest smoke job",
            "first after deploy, before deep suites",
        ),
        (
            "D20-T010",
            "Acceptance testing",
            "behavior described in business language, often BDD",
            "Acceptance proves the feature matches product intent, not only technical correctness.",
            "Gherkin scenarios executed against a test environment; stakeholders read failures.",
            """flowchart LR
  story[User story]
  scen[Gherkin scenario]
  impl[Test automation]
  story --> scen --> impl""",
            "d20_t010_acceptance_bdd.py",
            '''def test_user_can_reset_password(bdd_context):\n    bdd_context.given_registered_user("u@x.com")\n    bdd_context.when_requests_reset()\n    bdd_context.then_email_queued()''',
            "pytest-bdd",
            "near E2E, business-readable",
        ),
        (
            "D20-T011",
            "Test doubles (mocks, stubs, fakes)",
            "replacing collaborators with controlled implementations",
            "Doubles let unit tests run fast without network.",
            "Stub returns canned data; mock verifies interactions; fake has working but simplified logic; spy records calls.",
            """flowchart TD
  unit[Unit under test]
  fake[Fake payment gateway]
  unit --> fake""",
            "d20_t011_fake_clock.py",
            '''class FakeClock:\n    def __init__(self):\n        self.now = 0\n    def advance(self, sec):\n        self.now += sec\n\n\ndef test_token_expires(fake_clock):\n    tok = issue_token(fake_clock, ttl=60)\n    fake_clock.advance(61)\n    assert is_expired(tok, fake_clock)''',
            "unittest.mock or pytest fixtures",
            "inside unit tests primarily",
        ),
        (
            "D20-T012",
            "Fixtures and test data management",
            "repeatable setup and teardown of data and dependencies",
            "Good fixtures make tests readable and isolated.",
            "Factory functions build graphs; session fixtures amortize cost; per-test fixtures guarantee isolation.",
            """flowchart LR
  factory[Data factory]
  fixture[pytest fixture]
  test[Test case]
  factory --> fixture --> test""",
            "d20_t012_fixture_user.py",
            '''@pytest.fixture\ndef user(db):\n    u = UserFactory.create(email="t@example.com")\n    yield u\n    db.delete(u)''',
            "factory_boy or builders",
            "supports all layers",
        ),
        (
            "D20-T013",
            "Database integration tests",
            "SQL, migrations, and transactions against a real engine",
            "Proves ORM mappings and constraints match the schema.",
            "Runs migrations, seeds minimal rows, asserts queries and transactions.",
            """flowchart TD
  mig[Migrations]
  db[(Postgres)]
  test[Repository test]
  mig --> db --> test""",
            "d20_t013_db_migration.py",
            '''def test_migration_adds_status_column(db, migrator):\n    migrator.up("20240101_add_status")\n    cols = db.inspect_columns("orders")\n    assert "status" in cols''',
            "Flyway/Liquibase + Testcontainers",
            "integration sub-layer",
        ),
        (
            "D20-T014",
            "Testing transactions and rollbacks",
            "ACID behavior and failure recovery paths",
            "Money movement requires proving rollback leaves no partial state.",
            "Tests begin transactions, force failures, assert invariants and idempotency keys.",
            """sequenceDiagram
  svc[Service]
  db[Database]
  svc->>db: BEGIN
  svc->>db: INSERT
  svc->>db: ROLLBACK
  Note over db: no row visible""",
            "d20_t014_tx_rollback.py",
            '''def test_transfer_rolls_back_on_insufficient_funds(db, accounts):\n    with pytest.raises(InsufficientFunds):\n        transfer(accounts.a, accounts.b, cents=999999)\n    assert accounts.a.balance == accounts.a.initial''',
            "transactional pytest fixtures",
            "database integration focus",
        ),
        (
            "D20-T015",
            "Testing asynchronous workflows",
            "events, queues, and outbox patterns over time",
            "Async bugs are timing and ordering bugs.",
            "Use await helpers, test containers for Kafka/Rabbit, assert eventual state with timeouts.",
            """flowchart LR
  pub[Publisher]
  q[Queue]
  worker[Worker]
  pub --> q --> worker""",
            "d20_t015_async_outbox.py",
            '''def test_outbox_publishes_after_commit(db, outbox_worker):\n    create_order(db, id="o1")\n    outbox_worker.run_until_idle(timeout=5)\n    assert message_seen(topic="orders", key="o1")''',
            "asyncio + test broker",
            "integration with time",
        ),
        (
            "D20-T016",
            "Testing Kafka consumers and producers",
            "message serialization, partitions, and consumer offsets",
            "Streaming systems need tests for replay and poison pills.",
            "Use testcontainers-kafka, produce records, assert consumer handling and commits.",
            """flowchart TD
  prod[Producer test]
  topic[Kafka topic]
  cons[Consumer under test]
  prod --> topic --> cons""",
            "d20_t016_kafka_consumer.py",
            '''def test_consumer_commits_offset(kafka_producer, consumer):\n    kafka_producer.send("events", b"{\\"id\\":1}")\n    msg = consumer.poll_one(timeout=10)\n    assert msg.value["id"] == 1''',
            "testcontainers Kafka",
            "messaging integration",
        ),
        (
            "D20-T017",
            "Concurrency and race testing",
            "parallel threads or processes exposing data races",
            "Races rarely show in single-threaded unit tests.",
            "Stress tests, deterministic schedulers, and tools like thread sanitizers find unsafe shared state.",
            """flowchart LR
  t1[Thread 1]
  t2[Thread 2]
  shared[(Shared counter)]
  t1 --> shared
  t2 --> shared""",
            "d20_t017_race.py",
            '''def test_increment_is_atomic_under_threads(counter):\n    threads = [Thread(target=counter.inc) for _ in range(50)]\n    for th in threads: th.start()\n    for th in threads: th.join()\n    assert counter.value == 50''',
            "pytest with thread stress",
            "specialized layer atop unit/integration",
        ),
        (
            "D20-T018",
            "Property-based testing",
            "generating many inputs to check invariants",
            "Finds edge cases humans forget.",
            "Frameworks like Hypothesis generate inputs subject to properties (sort is ordered, decode(encode(x))==x).",
            """flowchart LR
  gen[Input generator]
  prop[Property assert]
  shrink[Shrink on failure]
  gen --> prop --> shrink""",
            "d20_t018_hypothesis_sort.py",
            '''from hypothesis import given, strategies as st\n\n@given(st.lists(st.integers()))\ndef test_sort_is_ordered(xs):\n    ys = sorted(xs)\n    assert all(ys[i] <= ys[i+1] for i in range(len(ys)-1))''',
            "Hypothesis",
            "augments unit tests",
        ),
        (
            "D20-T019",
            "Fuzz testing",
            "random or malformed inputs hunting crashes and security holes",
            "Fuzzing is exploration without human-chosen cases.",
            "Feed bytes to parsers; use coverage-guided fuzzers for native code; assert no panics and bounded memory.",
            """flowchart TD
  fuzz[Fuzzer]
  target[Parser]
  crash[Crash found]
  fuzz --> target
  target -->|panic| crash""",
            "d20_t019_fuzz_json.py",
            '''def test_parser_never_raises_on_random_bytes(random_bytes):\n    try:\n        safe_parse(random_bytes)\n    except ParseError:\n        pass  # expected rejection\n    except Exception as exc:\n        pytest.fail(f"unexpected: {exc}")''',
            "AFL/libFuzzer or python fuzz",
            "security and parser layers",
        ),
        (
            "D20-T020",
            "Mutation testing",
            "introducing small code mutants to see if tests catch them",
            "Measures assertion strength, not line coverage alone.",
            "Mutants change `>` to `>=`; surviving mutants mean weak tests.",
            """flowchart LR
  code[Source]
  mutant[Mutant]
  tests[Test suite]
  mutant --> tests
  tests -->|pass| weak[Weak test]
  tests -->|fail| strong[Strong test]""",
            "d20_t020_mutation_survivor.py",
            '''# mutant: changed < to <= in production code\n# this test should fail on that mutant\ndef test_rejects_zero_quantity():\n    with pytest.raises(ValueError):\n        order_line(qty=0)''',
            "mutmut or PIT",
            "quality gate on unit suite",
        ),
        (
            "D20-T021",
            "Performance testing",
            "latency, throughput, and resource usage under workload",
            "Performance is a requirement with thresholds.",
            "Micro-benchmarks, profilers, and macro load tools answer different questions.",
            """flowchart LR
  bench[Benchmark]
  metrics[Latency CPU mem]
  bench --> metrics""",
            "d20_t021_perf_threshold.py",
            '''def test_p95_under_budget(benchmark_client):\n    stats = benchmark_client.post_many("/search", n=500)\n    assert stats.p95_ms < 120''',
            "k6 or locust hooks",
            "parallel track to functional tests",
        ),
        (
            "D20-T022",
            "Load, stress, spike and soak testing",
            "traffic-shaped experiments: sustained, overload, burst, and long-duration",
            "Load holds expected RPS; stress pushes until failure; spike jumps traffic; soak runs long to find leaks.",
            "Each type answers a different capacity question. Functional green does not imply SLO green.",
            """flowchart TD
  load[Load expected RPS]
  spike[Spike burst]
  soak[Soak hours]
  stress[Stress beyond capacity]
  load --> metrics[SLO metrics]
  spike --> metrics
  soak --> metrics
  stress --> metrics""",
            "d20_t022_load_profile.py",
            '''def test_load_profile_meets_slo(load_runner):\n    result = load_runner.run(profile="expected", duration_sec=300, rps=200)\n    assert result.error_rate < 0.01\n    assert result.p95_ms < 250''',
            "k6/Gatling",
            "outside default PR pipeline",
            True,
        ),
        (
            "D20-T023",
            "Fault injection and chaos testing",
            "deliberate failures in realistic environments to validate resilience",
            "Chaos is controlled experiments on redundancy, not random vandalism.",
            "Kill pods, add latency, partition networks; observe SLO and recovery. Distinct from load (which stresses volume) and unit tests (which check logic).",
            """flowchart LR
  steady[Steady traffic]
  fault[Inject fault]
  observe[Observe recovery]
  steady --> fault --> observe""",
            "d20_t023_chaos_latency.py",
            '''def test_checkout_survives_payment_latency(chaos, client):\n    chaos.inject_latency("payments", ms=2000)\n    r = client.post("/checkout", json={"cart": "c1"})\n    assert r.status_code in (200, 202)''',
            "Chaos Mesh / Litmus",
            "production-like staging only",
            True,
        ),
        (
            "D20-T024",
            "Test coverage vs test quality",
            "line/branch coverage as a signal, not a goal",
            "100% coverage with weak asserts still ships bugs.",
            "Pair coverage with mutation score, review of assertions, and risk-based case selection.",
            """flowchart LR
  cov[Coverage %]
  qual[Assertion strength]
  cov --> qual
  qual --> conf[Release confidence]""",
            "d20_t024_coverage_gate.py",
            '''def test_quality_not_just_coverage():\n    # anti-pattern: assert function_called()\n    result = compute_total([{"cents": 100}] )\n    assert result == 100''',
            "coverage.py",
            "meta across all tests",
        ),
        (
            "D20-T025",
            "CI test pipelines",
            "staged jobs, caching, and artifacts for automated quality gates",
            "Pipelines orchestrate unit, integration, contract, and optional perf stages.",
            "Fail fast on cheap stages; publish junit and docker logs; shard slow suites.",
            """flowchart TD
  pr[Pull request]
  unit[Unit stage]
  integ[Integration stage]
  contract[Contract stage]
  pr --> unit --> integ --> contract""",
            "d20_t025_ci_marker.py",
            '''import pytest\n\n@pytest.mark.ci_only\ndef test_requires_docker():\n    assert docker_available()''',
            "GitHub Actions / GitLab CI",
            "orchestrates all layers",
        ),
        (
            "D20-T026",
            "Testcontainers and ephemeral dependencies",
            "throwaway Docker containers per test run for real services",
            "Removes shared staging pets and drift.",
            "Start Postgres/Redis/Kafka on demand; wait for health; bind dynamic ports.",
            """flowchart LR
  test[Test process]
  tc[Testcontainers]
  pg[(Postgres container)]
  test --> tc --> pg""",
            "d20_t026_testcontainers.py",
            '''def test_with_postgres_container(postgres_url):\n    conn = connect(postgres_url)\n    assert conn.execute("SELECT 1").fetchone()[0] == 1''',
            "testcontainers-python",
            "enables integration locally and in CI",
        ),
    ]

    for item in specs:
        if len(item) == 10:
            tid, name, focus, overview_extra, principles, mermaid, code_file, code_body, tool, pyramid_hint = item
            include_tax = True
        else:
            tid, name, focus, overview_extra, principles, mermaid, code_file, code_body, tool, pyramid_hint, include_tax = item
        topics[tid] = build_topic(
            tid,
            name,
            focus,
            overview_extra,
            principles,
            f"Execution uses {tool} with explicit setup and teardown. Failures must attach logs and versions. Parallel CI requires isolated resources per worker.",
            mermaid,
            "Follow arrows as the runtime path under test, not organizational ownership.",
            f"Example: validate {focus} with the smallest environment that still fails when wiring breaks.",
            code_file,
            code_body,
            f"Wire this into CI with clear markers. Document how developers run it locally with the same containers CI uses.",
            "| Automated | Repeatable | Upfront cost | Regulated releases | Exploratory UX |\n| Manual | Flexible | Slow | Early design | Regression at scale |",
            f"- Confusing {name.lower()} with another pyramid layer.\n- Skipping cleanup.\n- No assertions on observability.",
            f"Reproduce with CI image. Compare dependency versions. Inspect {tool} logs.",
            "environment drift between laptop and CI",
            tool,
            pyramid_hint,
            f"Design three cases for {name.lower()}: happy path, validation failure, and permission denied. Acceptance: table of inputs and expected signals.",
            f"A failure only appears in CI for {name.lower()}. List five environmental differences you would diff. Acceptance: mention containers, ports, and secrets.",
            f"Argue whether to run {name.lower()} on every PR or nightly. Acceptance: cost versus risk trade-off with numbers.",
            f"Implement the happy path test with clear AAA structure and one assertion on the user-visible outcome.",
            "Diff lockfiles, env vars, CPU limits, and parallel sharding; reproduce in the CI container locally.",
            "Every PR if under five minutes and blocking; otherwise nightly with mandatory run before release.",
            f"- {name}: {focus}.\n- Not a substitute for adjacent layers.\n- Keep artifacts and versions.\n- Isolate data.\n- Fail pipelines on real regressions.",
            f"- Explain {name.lower()} in one minute and place it on the pyramid.\n- Write or review one pytest example.\n- Triage a flake with evidence.\n- Name how it differs from unit, integration, contract, load, soak, spike, and chaos where relevant.",
            include_taxonomy=include_tax,
        )

    # Enrich D20-T022 and D20-T023 with explicit taxonomy in overview
    topics["D20-T022"]["overview"] += (
        " **Load** validates SLOs at expected traffic. **Stress** finds breaking points. "
        "**Spike** tests autoscaling on bursts. **Soak** hunts slow leaks over hours."
    )
    topics["D20-T023"]["overview"] += (
        " **Chaos** differs from **load** (volume) and **spike** (burst): it injects faults while traffic flows."
    )
    topics["D20-T006"]["overview"] += (
        " **Contract** tests differ from **integration**: they check message shape compatibility, not every business branch."
    )
    topics["D20-T001"]["overview"] += (
        " **Unit** tests are not **integration**, **contract**, **load**, **soak**, **spike**, or **chaos**—those answer wiring, compatibility, capacity, endurance, bursts, and resilience respectively."
    )

    return topics

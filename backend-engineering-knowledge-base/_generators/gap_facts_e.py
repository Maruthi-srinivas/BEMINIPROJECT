"""Topic facts for remaining design problems and testing topics."""

from __future__ import annotations

from gap_facts_a import add

add(
    "D17-T024",
    "A distributed task queue accepts a unit of work, stores it durably, and hands it to one of many workers. The API is enqueue and status. At-least-once delivery means workers must be idempotent. A visibility timeout hides a task while a worker runs it and returns it if the worker dies. The queue depth and the age of the oldest task are the capacity signals. A single consumer process is not this design.",
    ["Accept the task and persist it", "A worker leases it", "The worker completes or the lease expires", "Retries move it to a dead-letter path after a bound"],
    "two workers running the same task because the lease expired, or a poison task blocking one partition",
    "oldest task age, lease expirations, and duplicate execution count",
    "def enqueue(db, task):\n    db.insert('tasks', id=task['id'], status='ready', payload=task)\n",
    "The queue is a workshop clipboard. A lease is a mechanic writing their name next to a job. If they vanish, the name is erased after a timer and someone else can take the job.",
    "An image-processing API stores a job row, returns 202, and workers in several processes lease jobs with SELECT FOR UPDATE SKIP LOCKED. The handler upserts by job id so a second lease does not double-charge the customer.",
    "work must survive the API process and run on a pool of workers",
    "the work is a request-scoped function that can finish before the HTTP response",
    ["In-memory queues.", "No idempotency key.", "A visibility timeout shorter than the job."],
)

add(
    "D17-T025",
    "A logging and metrics platform collects events and numbers from many services, indexes or aggregates them, and answers 'what happened' during an incident. Logs are for a specific request. Metrics are for rates and saturation. The pipeline must drop or sample under its own overload rather than take the product down. Cardinality of labels is the cost driver.",
    ["Emit a structured log or a measurement", "Ship it out of the request path", "Index or aggregate within a budget", "Query by request id and by service"],
    "a high-cardinality label such as user id on every metric, or a logging agent that blocks the request when the collector is down",
    "ingest lag, dropped events, and unique time series",
    "def emit(logger, request_id, msg):\n    logger.info('%s %s', request_id, msg)\n",
    "The platform is the building's incident notebook and the gauges on the boiler. The notebook can miss a line. The boiler gauge should not be labeled with every tenant's name or you will buy a gauge factory.",
    "Each service logs JSON with a request id and exports latency histograms. A collector buffers and drops debug logs first. Engineers search one request id across API and worker during a failed checkout.",
    "more than one service must be debugged together",
    "you log a line per function call and put user ids on metrics",
    ["Synchronous logging to a remote service on the request path.", "Unbounded labels.", "No sampling story when ingest falls behind."],
)

add(
    "D17-T026",
    "A metrics monitoring system stores time series and evaluates alert rules. A sample is a name, labels, a value, and a time. Alerting on symptoms that users feel, such as error rate and latency, beats alerting on causes such as CPU alone. The system needs a push or pull scrape, a retention policy, and a page route that a human will answer. A dashboard nobody alerts on is a picture.",
    ["Scrape or receive samples", "Store them at a resolution that matches the questions", "Evaluate rules on symptoms", "Route a page and record a silence"],
    "a page on a noisy gauge that trains people to ignore the real outage, or a rule that fires for a single blip",
    "page precision, time to detect, and number of series",
    "def burn(error_rate, budget):\n    return error_rate > budget\n",
    "Monitoring is a smoke alarm, not a scrapbook. It should ring when the room is filling with smoke, not every time someone strikes a match.",
    "The API pages when the five-minute 5xx rate and p99 latency both break the SLO for ten minutes. CPU is a chart on the same dashboard and is not a page by itself.",
    "you need to wake a human for a user-visible failure",
    "you alert on every container restart",
    ["High-cardinality labels.", "No runbook on the alert.", "Thresholds copied from another service."],
)

add(
    "D17-T027",
    "A feature flag service answers whether a subject should see a behavior. Flags have a default, a set of rules, and a kill switch. Evaluation should be local and fast after a snapshot is fetched, so a flag service outage does not become an application outage. The snapshot has a TTL. Experiments need stable assignment. Flags that stay forever are unfinished code.",
    ["Fetch a snapshot", "Evaluate locally", "Keep a safe default", "Remove the flag after the decision"],
    "a flag check that calls the network on every request, or a default that enables a broken feature when the snapshot is missing",
    "evaluation latency, snapshot age, and flags older than the cleanup budget",
    "def enabled(snapshot, name, default=False):\n    flag = snapshot.get(name)\n    if flag is None:\n        return default\n    return flag['on']\n",
    "A flag is a light switch with a known off position. If the switchboard is unreachable, the light should fall to the safe position you chose in advance, not to a random one.",
    "Checkout fetches flag snapshots every 30 seconds and evaluates in process. The new payment path defaults off. A kill switch flips the snapshot. Requests do not wait on the flag service.",
    "a behavior must change without a redeploy, and the safe default is known",
    "you put durable authorization or pricing in a flag with no audit",
    ["Remote evaluation on the hot path.", "No default.", "Flags that are never deleted."],
)

add(
    "D17-T028",
    "A distributed cache spreads keys across nodes so memory and throughput exceed one machine. Clients hash a key to a node. Consistent hashing or numbered slots reduce movement when a node is added. Replication covers a node failure and can serve stale reads. The hard problems are hot keys, thundering herds, and invalidation when the database changes. The cache is not the system of record.",
    ["Hash the key to a node", "Replicate if loss of a node matters", "Invalidate or TTL on writes", "Plan the database load when the cache is cold"],
    "a hot key on one node, or a cold start that melts the database",
    "hit ratio, per-node CPU, and database QPS during a cache failure",
    "def node_for(key, nodes):\n    return nodes[hash(key) % len(nodes)]\n",
    "A distributed cache is a row of photocopy cabinets. The index on the door says which cabinet holds a name. If that cabinet burns, you either have a second copy or you go back to the archive.",
    "Sessions and product JSON live in a sharded cache with TTLs. Prices are deleted on write. Losing the cluster hurts latency and must not lose orders, which live in the database.",
    "a read working set is hot and larger than one cache node, and the database remains authoritative",
    "you store the only copy of a payment in the cache",
    ["No TTL and no invalidation.", "One key for a global counter.", "No capacity plan for a cold cache."],
)

add(
    "D17-T029",
    "A recommendation system generates a ranked list of items for a user from signals such as clicks and purchases. Online serving must meet a latency budget, so it reads precomputed candidates and features, then ranks a small set. Offline jobs train models and build those candidates. The feedback loop is biased by what you already showed. A cold start has no history.",
    ["Collect impressions and actions", "Build candidates offline", "Rank a bounded set online", "Log what was shown so the next model is not blind"],
    "serving a model that reads the live database for every candidate and misses the latency SLO, or training only on clicked items and ignoring what was not shown",
    "serving p99, candidate count, and online metric movement after a model deploy",
    "def rank(candidates, limit):\n    return sorted(candidates, key=lambda c: c['score'], reverse=True)[:limit]\n",
    "Recommendations are a short list prepared before the guest arrives, not a librarian running into the stacks after the guest asks. The list is only as honest as the notes about what the guest ignored.",
    "The home page reads a precomputed candidate list from a cache and applies a lightweight ranker. A nightly job rebuilds candidates. A brand-new user gets a popularity list. The service logs impressions.",
    "you need a ranked list and you can precompute",
    "you compute a huge model inside the user request",
    ["No impression log.", "No cold-start path.", "An unbounded candidate set on the request."],
)

add(
    "D17-T030",
    "A multi-tenant SaaS platform serves many customers from shared software. Isolation is the design: a tenant must not read another's rows, exhaust the database, or see another's cache entries. Models range from a shared schema with a tenant id, to a schema per tenant, to a database per tenant. Noisy-neighbor controls cap a tenant's rate and pool usage. Authorization checks the tenant on every request, not only at login.",
    ["Resolve the tenant from the credential", "Scope every query", "Cap each tenant's resource use", "Test a cross-tenant access as a failure"],
    "a missing tenant predicate that returns another customer's rows, or one tenant's batch job saturating the shared pool",
    "cross-tenant test results, per-tenant rate, and pool wait time",
    "def scope(query, tenant_id):\n    query['tenant_id'] = tenant_id\n    return query\n",
    "Multi-tenancy is one apartment building. Shared plumbing is cheaper. The locks and the fuse boxes are what stop one apartment from opening another's door or tripping the whole block.",
    "Every order row carries tenant_id and every repository method requires it. A load test runs a noisy tenant beside a quiet one. The noisy tenant is rate-limited before the quiet tenant's p99 moves.",
    "many customers share a deployment",
    "you bolt on a tenant id in the UI and not in the queries and caches",
    ["Trusting a tenant id from the body.", "A shared cache key with no tenant prefix.", "No per-tenant quota."],
)

add(
    "D17-T031",
    "Real-time location tracking ingests frequent position updates and answers 'where is this entity now' and sometimes 'which entities are in this area.' The write rate is the design. A durable history is separate from the hot latest-point store. Geospatial indexes answer area queries. Clients interpolate between updates. Stale points must expire so a parked device does not look live.",
    ["Ingest a point with a timestamp and an entity id", "Store the latest point in a hot store", "Index it for area queries", "Expire points that stop arriving"],
    "writing every point through a transactional database at high frequency and falling behind, or an area query that scans every entity",
    "ingest lag, points per second per partition, and area-query p99",
    "def accept(point, now, max_age):\n    return now - point['ts'] <= max_age\n",
    "Tracking is a pegboard of last-known pins, not a filing cabinet of every step. The cabinet can exist, but the pegboard is what the dispatcher looks at.",
    "Drivers send a point every few seconds to a partitioned hot store keyed by driver id, with a geohash index for nearby search. The full trail is batched to cheap storage. A driver who goes silent drops off the live map after the TTL.",
    "the product needs current positions at a high write rate",
    "you store every raw point in the same transactional table you use for payments",
    ["No expiry.", "A global lock on the map.", "Area queries that scan all drivers."],
)

add(
    "D17-T032",
    "A leaderboard service updates a score and returns a rank or a top-k list. Updates are frequent. Exact global rank for a huge population is expensive. Approximate ranks, windows by time, and sharded boards are the usual escapes. Ties need a rule. A read of the top ten should not lock the writers. Cheating is a product problem: the server, not the client, computes the score.",
    ["Validate the score on the server", "Update the ordered structure", "Serve top-k from memory", "Define ties and the time window"],
    "a single hot key for the whole world, or a client-supplied score that a cheater sets to infinity",
    "update QPS per shard and top-k latency",
    "def better(a, b):\n    return a['score'] > b['score'] or (a['score'] == b['score'] and a['id'] < b['id'])\n",
    "A leaderboard is a ranked board on a wall. The top of the board is easy to read. Numbering every person in the stadium is a different, heavier job.",
    "A game submits match results. The server adds the delta. Daily regional sorted sets answer the top 100. A player's own rank can be approximate. One global key is avoided.",
    "you need ordered scores and top-k at interactive latency",
    "you need arbitrary analytics, which is a warehouse query",
    ["Client-authoritative scores.", "One key for every player.", "An unstable tie break."],
)

add(
    "D17-T033",
    "A webhook delivery platform sends an HTTP callback to a customer's URL when an event happens. Delivery is at-least-once. The receiver must be idempotent. The platform signs the body, retries with backoff, and stops after a bound. A slow receiver must not block other tenants. Endpoints are verified before they receive production traffic. Secrets rotate.",
    ["Persist the event and the subscription", "POST a signed body", "Retry on failure with backoff", "Disable an endpoint that never succeeds"],
    "one tenant's slow URL occupying every worker, or a retry that the receiver treats as a second order",
    "delivery success rate, oldest undelivered event, and per-endpoint concurrency",
    "def signature(secret, body):\n    import hmac, hashlib\n    return hmac.new(secret, body, hashlib.sha256).hexdigest()\n",
    "A webhook is a promised phone call to a number the customer gave you. You keep a log of attempts. You do not let one number that never answers tie up every phone in the office.",
    "The platform stores an outbox per endpoint, signs the payload, and retries for a day. Each endpoint has a concurrency limit. Customers dedupe on the event id. A failing endpoint is automatically paused and emailed.",
    "customers must be told about events on their own HTTP server",
    "you call the URL inside the user request and ignore failures",
    ["No signature.", "Unbounded retries.", "A shared worker pool with no per-endpoint limit."],
)

add(
    "D17-T034",
    "An audit log service records who did what to which object, and when, in a form that is append-only for investigators. It is not the debug log. Entries are written in the same transaction as the change when the answer must not diverge, or via an outbox. Queries are by actor, object, and time. Retention is a legal requirement. The log itself needs access control.",
    ["Capture actor, action, object, and time", "Append the record with the change", "Forbid updates of past records", "Retain and protect the log"],
    "an audit row written only after a later request succeeds, so a crash leaves a change with no record, or an audit API that leaks other tenants",
    "gaps between commits and audit rows, and unauthorized audit reads",
    "def entry(actor, action, object_id):\n    return {'actor': actor, 'action': action, 'object_id': object_id}\n",
    "An audit log is a bound book written in ink. A debug log is a whiteboard. Investigators will not accept the whiteboard, and they will notice a torn-out page.",
    "Changing a role inserts the membership row and the audit row in one transaction, including the actor from the token. Support searches by user id. The log is retained for the contractual period and is tenant-scoped.",
    "a later investigation must reconstruct a privileged change",
    "you grep application logs and call that an audit",
    ["Mutable audit rows.", "Missing tenant scope.", "Writing the audit only from the UI."],
)

add(
    "D17-T035",
    "A search engine indexes documents into inverted structures so a text query does not scan the source of truth. Indexing is asynchronous, so search can lag writes. Analyzers decide tokens. Relevance ranks matches. Filters and permissions must be in the query, not applied only in the UI. Reindexing is how you change an analyzer. The database remains the source of document truth.",
    ["Write the document to the source of truth", "Index asynchronously", "Query the index with the user's permissions", "Reindex when the analysis changes"],
    "a search result that includes a document the user must not see, or a new product that is unsearchable and looks lost",
    "index lag, query p99, and permission-filter misses in tests",
    "def visible(hit, tenant_id):\n    return hit['tenant_id'] == tenant_id\n",
    "A search engine is the index at the back of a book. It is built after the pages exist. If you reprint the pages with a new hyphenation rule, you rebuild the index or the entries point at the wrong words.",
    "Products are stored in PostgreSQL and indexed into a search cluster. The query includes tenant and ACL filters. A user who just created a product may not see it in search for a second and the UI says so. Changing the analyzer is a reindex, not a config hope.",
    "users need text or ranked retrieval beyond what a B-tree does well",
    "you make the search index the only copy of the product",
    ["No permission filter.", "Synchronous indexing on the user request with no timeout story.", "No reindex plan."],
)

add(
    "D20-T002",
    "An integration test runs a slice of the system with real collaborators you chose not to fake, such as a database or a queue, and checks a behavior across that boundary. It is slower than a unit test and catches SQL, migrations, and serialization bugs. It should still be deterministic. It does not need the whole production mesh.",
    ["Start the real dependency", "Run the behavior through the public function or port", "Assert the persisted outcome", "Tear down state so order does not matter"],
    "a test that shares a database row with another test and fails only in CI",
    "flake rate and time spent in the integration stage",
    "def test_insert_roundtrip(db):\n    db.insert('items', {'id': 1})\n    assert db.get('items', 1)['id'] == 1\n",
    "An integration test is cooking on the real stove, not miming a flame. You still do not invite the whole city into the kitchen.",
    "A repository test starts PostgreSQL, runs the migration, writes an order, and reads it back. It does not mock the SQL. A second test uses its own transaction or schema so it cannot see the first order.",
    "the bug you fear lives in the boundary between your code and a real dependency",
    "you boot the entire platform for a one-line calculation",
    ["Shared mutable fixtures.", "Mocking the database in a test you called integration.", "No cleanup."],
)

add(
    "D20-T003",
    "A component test checks one service or module through its external interface while replacing the systems it depends on with fakes you control. It sits between a unit test and a full end-to-end test. The fake must implement the contract you actually rely on. If the fake is kinder than production, the test is fiction.",
    ["Boot the component", "Point it at fakes", "Drive it through its API", "Assert the response and the calls that matter"],
    "a fake that never times out or returns an error, so production failures are untested",
    "bugs found only in staging that the component tests could have injected",
    "def test_timeout(client, fake_db):\n    fake_db.delay = 2\n    assert client.get('/items').status_code == 504\n",
    "A component test is rehearsing one actor with a stand-in for the rest of the cast. The stand-in has to be able to forget a line, or the rehearsal never practices a mistake.",
    "The order API runs in a test with a fake payment service that can return 503. The test asserts the order stays unpaid and the client receives a retryable error. The fake is not a copy of the entire payment company.",
    "you want the service's behavior without the real neighbors",
    "the fake cannot reproduce the failure you claim to test",
    ["Happy-path fakes only.", "Asserting on private methods.", "A component test that is secretly end-to-end and flaky."],
)

add(
    "D20-T004",
    "API testing calls the HTTP or RPC interface and asserts status, body, headers, and side effects. It includes authentication, validation, and the error contract. Generated cases from the schema catch drift. A test that only checks 200 with a happy body misses the contract clients actually break on.",
    ["Issue the request as a client would", "Assert the status and the body", "Assert the side effect", "Cover one unauthorized and one invalid case"],
    "a suite that accepts any 2xx and any JSON shape, so a breaking change stays green",
    "contract mismatches found by clients after a green API suite",
    "def test_create_unauthorized(client):\n    response = client.post('/orders', json={'sku': 'a'})\n    assert response.status_code == 401\n",
    "API testing is reading the menu the customer sees and sending the order back, including the orders the kitchen should refuse.",
    "A test creates an order with a token, expects 201 and a body with an id, then fetches that id. A second test omits the token and expects 401. A third sends a negative quantity and expects 400, not 500.",
    "clients depend on a network contract",
    "you only unit-test the controller function and never the serialization",
    ["Ignoring error codes.", "Sharing one token for every case including the unauthorized one.", "Asserting the whole JSON including volatile timestamps without a matcher."],
)

add(
    "D20-T005",
    "An end-to-end test runs a user journey through the deployed system, or a close stand-in, including the UI or the public API and the real path to the database. It catches wiring mistakes. It is slow and flake-prone, so a few journeys are enough. It does not replace the tests that pinpoint a function. Setup and data must be isolated.",
    ["Boot the path a user needs", "Perform one journey", "Assert the outcome the user would notice", "Keep the suite small and deterministic"],
    "a large end-to-end suite that fails on shared data or timing and gets ignored",
    "flake rate and the number of defects that only the journey test could see",
    "def test_checkout_journey(browser):\n    browser.login()\n    browser.buy('sku-1')\n    assert browser.sees('Order confirmed')\n",
    "An end-to-end test is walking through the building from the front door to the exit. You do not measure every hinge that way. You check that the doors you need actually open.",
    "One test signs up, creates an order, and sees it in the history API. It runs against containers started for CI. It is not repeated for every validation rule, which live in API tests.",
    "you need confidence the wired system completes a journey",
    "you try to cover every branch this way",
    ["Shared staging data.", "Sleeps instead of waiting for a condition.", "A red suite people rerun until green."],
)

add(
    "D20-T006",
    "Contract testing checks that a provider and a consumer agree on a request and response without running the whole system together. The consumer publishes the interactions it needs. The provider verifies them against its real endpoints. The contract is the shared artifact. It catches a provider change that would break a consumer before production.",
    ["Record the consumer's expected interaction", "Verify it on the provider", "Publish the contract", "Fail the provider build on a mismatch"],
    "a contract that is never verified, or one that omits the error case the consumer actually handles",
    "breakages caught in the provider build versus in production",
    "contract = {'request': {'method': 'GET', 'path': '/items/1'}, 'response': {'status': 200}}\n",
    "A contract test is both sides signing the same drawing. It is not a promise scribbled by one side and left in a drawer.",
    "The web app's contract says GET /items/1 returns an id and a price. The item service's pipeline replays that interaction. Removing price fails the item service build, not the web app's production deploy.",
    "two teams deploy separately and share an API",
    "you keep a wiki page and call it a contract",
    ["Contracts that only cover 200.", "No provider verification.", "A contract generated and never committed."],
)

add(
    "D20-T007",
    "Consumer-driven contracts mean the consumer's expectations drive the contract, because the consumer is the one who breaks. Each consumer publishes its needs. The provider verifies the union. The provider may support several consumers and must not drop a field one of them requires. This is a social and a technical rule: the provider does not invent the contract alone.",
    ["Each consumer writes the interactions it depends on", "The provider verifies all of them", "A breaking change is negotiated", "Unused expectations are deleted when the consumer is"],
    "a provider shipping a change that satisfies a guessed contract and breaks a quiet consumer",
    "consumers broken in production after a provider release that was contract-green for a subset",
    "def covers(provider_contracts, consumer):\n    return consumer in provider_contracts\n",
    "Consumer-driven contracts are the diners writing down the dishes they still order. The kitchen may add a dish. It may not remove one that a diner still listed.",
    "Two clients need different fields of an order. Both publish contracts. The order service build runs both. A cleanup of an 'unused' field fails because the second client still requires it.",
    "several consumers evolve separately from the provider",
    "the provider dictates a schema and never runs the consumers' expectations",
    ["One contract written by the provider and labeled consumer-driven.", "Ignoring a consumer because it is internal.", "Never deleting a contract for a dead client, so you cannot evolve."],
)

add(
    "D20-T008",
    "Regression testing checks that a fixed bug or an existing behavior stays fixed after a change. The test should fail on the old code and pass on the new code. A suite that never caught a bug is not evidence. Regressions are named and small. Re-running the entire world is a pipeline choice, not the definition.",
    ["Reproduce the bug as a test", "Watch it fail", "Apply the fix", "Keep the test in the suite"],
    "a test written after the fix that would have passed on the broken code too",
    "escaped bugs that match a missing regression test",
    "def test_blank_name_rejected(validate):\n    assert validate('') is False\n",
    "A regression test is a photograph of a pothole you filled. If the photograph would also have matched the open hole, it does not protect you.",
    "A bug let an empty display name through. The test submits an empty name and expects a 400. It was observed red on the old commit. It stays next to the validator.",
    "a defect escaped or a behavior must not change",
    "you add a test that cannot fail for the reason the bug failed",
    ["Writing the test only on the fixed code and never checking it fails.", "Disabling a red test.", "Calling a full rerun a regression strategy with no new case."],
)

add(
    "D20-T009",
    "A smoke test is a shallow check that the build is alive enough to test further: it boots, a health endpoint answers, and a critical path returns. A sanity test is a narrow check after a small change that the obvious thing still works. Neither replaces functional tests. Their job is to fail fast. A smoke test that takes an hour is a suite with the wrong name.",
    ["Boot the artifact", "Hit a liveness or a single golden path", "Stop and reject the build if it fails", "Keep it shorter than the real suite"],
    "a green smoke test that does not touch the broken migration, so the real suite starts and fails late",
    "time to reject a dead build",
    "def test_smoke(client):\n    assert client.get('/health').status_code == 200\n",
    "Smoke is looking for fire before you unpack the boxes. Sanity is plugging in the lamp you just moved. Neither is inventorying the house.",
    "CI runs a two-minute smoke container that migrates a scratch database and calls health. If the image cannot boot, the long suite never starts.",
    "you need a fast reject of a broken artifact",
    "you expand smoke until it is the only suite and it is slow",
    ["A smoke test with no assertion.", "Hours of tests labeled smoke.", "Skipping the migration in the boot check."],
)

add(
    "D20-T010",
    "Acceptance testing checks a behavior against a requirement a stakeholder would recognize. It is written in the language of the outcome, not the language of a private class. It can be automated. It answers 'did we build the thing we agreed,' not 'did this function return 4.' The example should be readable by the person who asked for the feature.",
    ["State the requirement as an observable outcome", "Automate an example", "Run it against the interface the user has", "Keep the wording in domain language"],
    "a test named acceptance that only asserts a mock was called",
    "requirements that shipped without an example anyone can read",
    "def test_member_can_download_invoice(app):\n    app.login('member')\n    assert app.download('inv-1').startswith(b'%PDF')\n",
    "Acceptance is the customer tasting the dish and recognizing the order. It is not the cook weighing the salt in private.",
    "The story 'a member can download an invoice' becomes a test that logs in as a member and receives a PDF. A developer-only assertion on a private formatter is a unit test beside it, not instead of it.",
    "a requirement can be phrased as a user-visible outcome",
    "you mock the entire application and still call it acceptance",
    ["Technical assertions with no outcome.", "Manual-only checks that are never run.", "Examples that skip authorization."],
)

add(
    "D20-T011",
    "A test double stands in for a collaborator. A dummy is passed and unused. A stub returns canned answers. A mock expects specific calls. A fake has a working simpler implementation, such as an in-memory queue. Spies record calls. Over-mocking tests the mocks. A fake that skips a failure mode gives false confidence. Prefer a stub or fake at the edge and real logic inside.",
    ["Replace the slow or remote collaborator", "Choose the dumbest double that preserves the behavior under test", "Assert state when you can", "Verify interactions only when the interaction is the behavior"],
    "a test that breaks when a log line changes because a mock expected that call",
    "tests rewritten on every refactor that did not change behavior",
    "class InMemoryQueue:\n    def __init__(self):\n        self.items = []\n    def put(self, item):\n        self.items.append(item)\n",
    "A double is a stand-in actor. A fake is an understudy who can actually say the lines. A mock is a script supervisor who stops the scene if a line is missed. Supervisors are tiring if you hire one for every extra.",
    "The order service test uses an in-memory payment fake that can approve or decline. It does not mock the domain object's internal method calls. A contract test still checks the real payment HTTP shape elsewhere.",
    "the collaborator is remote, slow, or non-deterministic",
    "you mock the thing you are trying to test",
    ["Mocks of value objects.", "Fakes with only the happy path.", "Verifying call order that is not a requirement."],
)

add(
    "D20-T012",
    "A fixture is the arranged state a test starts from. Test data management decides how that state is created and isolated. Builders make only the fields the test cares about. Shared mutable fixtures cause order dependence. Production data snapshots are usually illegal or brittle. Each test should arrange what it needs and clean up.",
    ["Build the minimum data", "Isolate it from other tests", "Name the important fields", "Avoid a shared global row"],
    "a suite that passes alone and fails in parallel because two tests update the same user",
    "order-dependent failures and time spent debugging shared fixtures",
    "def order(**overrides):\n    base = {'id': 'o1', 'total': 10}\n    base.update(overrides)\n    return base\n",
    "A fixture is the set on a stage. If two plays share one set and both move the chair, the second play starts in the wrong room.",
    "Each test inserts its own user with a unique id inside a transaction that rolls back. A builder sets a default email. A test that cares about a locked account sets that field and no other.",
    "a test needs state",
    "you load a production dump into every test",
    ["Shared mutable fixtures.", "Giant JSON files nobody can edit.", "Cleanup that depends on test order."],
)

add(
    "D20-T013",
    "A database integration test runs real SQL against a real engine, usually in a container or an embedded mode that matches production closely enough. It applies migrations. It checks constraints, queries, and transactions. Mocking the database misses the bugs this test exists to catch. Isolation is a transaction rollback or a fresh schema.",
    ["Start the engine", "Migrate", "Run the query or repository", "Roll back or drop the schema"],
    "a test using a different database engine than production and missing a constraint behavior",
    "SQL bugs escaped to production, and suite time",
    "def test_unique_email(db):\n    db.insert('users', {'email': 'a@b.c'})\n    try:\n        db.insert('users', {'email': 'a@b.c'})\n        raised = False\n    except Exception:\n        raised = True\n    assert raised\n",
    "Testing SQL on a real engine is tasting the sauce in the real pan. Tasting a drawing of the pan does not tell you it is salty.",
    "CI starts PostgreSQL, runs migrations, and checks that a duplicate email fails. The test rolls back. SQLite is not used as a stand-in if the production constraint is PostgreSQL-specific.",
    "behavior depends on SQL, types, or constraints",
    "you mock the connection for this layer",
    ["A different engine.", "No migrations.", "Leftover rows."],
)

add(
    "D20-T014",
    "Testing transactions means proving that a failure rolls back every write in the unit, and that a commit is visible afterward. Open a transaction, write two rows, force a failure, and assert neither row remains. Also test the isolation bug you fear, such as two sessions creating a duplicate. A test that never forces a rollback does not test the transaction.",
    ["Begin a transaction", "Write partial work", "Force a failure", "Assert the database is unchanged"],
    "a catch block that commits, or a test that uses a connection that auto-commits and never notices",
    "partial rows after a forced failure",
    "def test_rollback(db):\n    try:\n        with db.transaction():\n            db.insert('a', {'id': 1})\n            raise RuntimeError('boom')\n    except RuntimeError:\n        pass\n    assert db.get('a', 1) is None\n",
    "A transaction test is knocking over the table mid-course and checking that the kitchen did not serve half a meal.",
    "The order and the outbox row are written in one transaction. The test throws after the order insert and asserts that neither the order nor the outbox row is visible. A second test commits and sees both.",
    "several writes must succeed or fail together",
    "you assert only the happy commit",
    ["Autocommit connections.", "Catching the error and continuing.", "Checking rollback on a mock."],
)

add(
    "D20-T015",
    "Testing asynchronous workflows means asserting an outcome that happens after the caller returns: a message consumed, a row updated, a timer fired. The test waits on the outcome with a timeout, not on a fixed sleep. It also tests a failure path and a duplicate delivery if the workflow is at-least-once. Time is controlled if the workflow depends on a clock.",
    ["Start the workflow", "Wait until the outcome or a timeout", "Assert the terminal state", "Advance a fake clock if time matters"],
    "a sleep that is too short on a slow CI machine, or a test that returns before the worker runs",
    "flake rate of async tests",
    "def wait_until(pred, timeout=2):\n    import time\n    end = time.time() + timeout\n    while time.time() < end:\n        if pred():\n            return\n    raise AssertionError('timeout')\n",
    "An async test is ordering a cake and waiting until the counter actually shows your name, not counting to ten and hoping.",
    "A test enqueues a job and polls the job row until it is done or two seconds pass. A second test delivers the same message twice and asserts one email row. The clock in a delay test is fake.",
    "the result happens off the calling stack",
    "you sleep and hope",
    ["Fixed sleeps.", "No timeout.", "Ignoring duplicate delivery."],
)

add(
    "D20-T016",
    "Testing Kafka producers and consumers uses a broker in a container or a focused fake only for serialization. A producer test asserts the record's topic, key, and payload. A consumer test produces a record, runs the handler, and asserts the side effect and the committed offset. It includes a redelivery. It does not require a multi-node production cluster.",
    ["Start a broker", "Produce a known record", "Run the consumer", "Assert the effect and that a second delivery is safe"],
    "a consumer test that never restarts the consumer, so the offset bug is invisible",
    "duplicate side effects in the redelivery test",
    "def test_redelivery(handler, event):\n    handler(event)\n    handler(event)\n    assert handler.side_effects == 1\n",
    "Testing a consumer is putting one letter in the slot, letting the clerk file it, and then handing the same letter over again to see whether the clerk pays twice.",
    "Testcontainers starts Kafka. The test publishes an order event, the consumer writes a row, the offset is committed, and publishing the same event id does not create a second row.",
    "a producer or consumer is part of the contract",
    "you mock the client and never check serialization or offsets",
    ["No redelivery case.", "Sharing a topic between tests.", "Asserting only that send() was called."],
)

add(
    "D20-T017",
    "Concurrency and race testing try to force the interleaving that loses an update. A barrier holds threads until they can enter the critical section together. The assertion is the invariant, such as a counter equaling the number of increments. A test that is green once did not prove much. Running it many times or under a scheduler that explores interleavings raises the chance of seeing the bug.",
    ["Name the invariant", "Start concurrent workers", "Release them together", "Assert the invariant"],
    "a lost update the test cannot see because it never overlaps the critical section",
    "invariant failures per thousand runs",
    "import threading\n\ndef test_increments():\n    n = {'v': 0}\n    lock = threading.Lock()\n    def add():\n        with lock:\n            n['v'] += 1\n    threads = [threading.Thread(target=add) for _ in range(20)]\n    for t in threads:\n        t.start()\n    for t in threads:\n        t.join()\n    assert n['v'] == 20\n",
    "A race test is starting the race at the same whistle. If runners start seconds apart, you did not test the collision.",
    "Two threads decrement the last seat. A barrier releases both inside the transaction. The assertion is that one booking exists and the seat count is not negative. The test repeats.",
    "a bug depends on timing",
    "you run two threads loosely and treat one green run as proof",
    ["No barrier.", "One iteration.", "Asserting a log line instead of the invariant."],
)

add(
    "D20-T018",
    "Property-based testing states a property that must hold for many generated inputs, instead of one example. A generator builds values. The framework shrinks a failing value to a smaller one. Properties include round-trip, idempotence, and invariants. A property that is too weak, such as 'does not throw,' proves little. You still keep a few examples for the cases humans must read.",
    ["State the property", "Generate inputs", "Shrink failures", "Keep an example test for the story"],
    "a property that encodes the same bug as the implementation, so both are wrong together",
    "failures found by generation that example tests missed",
    "def test_roundtrip(text):\n    assert decode(encode(text)) == text\n",
    "Property testing is claiming every loaf rises, then pulling random loaves out of the oven. Shrinking is cutting the failed loaf down until the smallest burnt piece remains.",
    "The encoder and decoder are tested by generating strings, including empty and unicode, and asserting a round trip. When a property fails, the shrunk input is added as an example.",
    "the correct behavior is a rule over a large input space",
    "you assert the implementation against a copy of itself",
    ["Properties that only check 'no exception'.", "Generators that never build the edge case.", "No shrinking."],
)

add(
    "D20-T019",
    "Fuzz testing feeds malformed and unexpected inputs to a parser or a service and watches for crashes, hangs, and sanitizer failures. Coverage-guided fuzzing mutates inputs that reach new code. It is good at finding panics and memory bugs. It does not know your business assertions unless you add them. Corpus inputs should be saved. A hang needs a timeout.",
    ["Start from seed inputs", "Mutate them", "Bound time and memory", "Treat a crash as a failing test with the saved input"],
    "a hang with no timeout, or a fuzzer that only finds crashes you do not replay in CI",
    "unique crashes and coverage growth",
    "def parse_or_error(raw):\n    try:\n        return ('ok', raw.decode())\n    except UnicodeError:\n        return ('error', None)\n",
    "Fuzzing is shaking a vending machine with coins of every bent shape to see whether it jams or dumps the drawer. You keep the bent coin that broke it.",
    "A JSON parser or a request decoder runs under a fuzzer with a one-second timeout per input. A crash is stored as a regression file and replayed in CI. Business rules stay in ordinary tests.",
    "the attack surface is a parser or a decoder",
    "you expect the fuzzer to judge business correctness alone",
    ["No timeout.", "Discarding the crashing input.", "Fuzzing only the happy corpus."],
)

add(
    "D20-T020",
    "Mutation testing changes the program in small ways, such as flipping a comparison, and checks that the tests fail. A mutant that survives means no test noticed the change. It measures whether tests can detect faults, not whether the line ran. It is expensive, so it is aimed at critical modules. Equivalent mutants are changes that do not alter behavior and should not be counted as a miss.",
    ["Mutate a critical function", "Run the tests", "Expect a failure", "Inspect survivors"],
    "a high line-coverage number with mutants that still survive",
    "survivor count in the module you care about",
    "def price_ok(total):\n    return total >= 0\n",
    "Mutation testing is secretly rewriting a sign in the shop and seeing whether any inspector complains. If nobody complains, the inspectors were not looking.",
    "The payment rounding function is mutated in CI nightly. A surviving mutant that flips a boundary becomes a new test. The whole monorepo is not mutated on every commit.",
    "you need to know whether tests can catch a real change",
    "you chase 100 percent on generated code",
    ["Treating coverage as mutation score.", "Mutating everything on every push.", "Counting equivalent mutants as failures of the suite."],
)

add(
    "D20-T021",
    "Performance testing measures latency, throughput, and resource use under a stated workload. It needs a baseline, a production-like data volume, and a pass/fail budget. A number without a workload is not a result. Warmup, percentiles, and saturation belong in the report. The test should fail the build or the release if the budget breaks, or it will never be read.",
    ["Define the workload and the budget", "Warm up", "Measure percentiles and errors", "Compare to the baseline"],
    "a mean latency hiding a bad tail, or a test on an empty database",
    "p99 latency and error rate against the budget",
    "def within_budget(p99_ms, budget_ms):\n    return p99_ms <= budget_ms\n",
    "A performance test is a timed drill with a full pack, not a stroll that you describe as 'feels fast.'",
    "The search endpoint is loaded with a production-sized index for ten minutes. The release fails if p99 exceeds 200 ms or errors exceed one percent. The report stores the workload, not only the number.",
    "a change can affect latency or throughput",
    "you benchmark a laptop once and paste the number into a ticket",
    ["Averages only.", "Empty data.", "No budget."],
)

add(
    "D20-T022",
    "Load testing uses the expected traffic. Stress testing pushes past it until something breaks, and you write down what broke. Spike testing applies a sudden jump. Soak testing runs long enough to see leaks, queue growth, and disk fill. They answer different questions. Running a five-minute load test does not tell you the daily disk curve.",
    ["Pick one question", "Shape the traffic for that question", "Watch saturation and errors", "Record the first limit you hit"],
    "a soak never run, so a connection leak appears on Saturday, or a spike test that ramps so slowly it is just load",
    "the limiting resource and the time-to-failure under soak",
    "def shape(kind, base):\n    if kind == 'spike':\n        return base * 10\n    if kind == 'stress':\n        return base * 3\n    return base\n",
    "Load is a normal Saturday. Stress is packing the room until a door breaks. Spike is a bus arriving at once. Soak is leaving the lights on all night to see what overheats.",
    "Before a sale, the team runs a spike to five times traffic and a soak overnight. The spike finds a pool queue. The soak finds a log disk fill. A ten-minute average test had missed both.",
    "you need a specific capacity question",
    "you use one short test as the answer to all four",
    ["No limiting-resource note.", "A spike that is actually a ramp.", "Stopping soak before leaks show."],
)

add(
    "D20-T023",
    "Fault injection and chaos testing deliberately break a dependency, a host, or a network path to see whether the system degrades as designed. Start with a hypothesis and a blast radius. Abort the experiment if the user impact exceeds the budget. The result is a fixed gap or a confirmed fallback, not a green dashboard. Production experiments need an owner.",
    ["Write the hypothesis", "Inject one fault", "Observe the user-facing symptom", "Stop and fix if the fallback fails"],
    "an experiment with no abort condition that becomes the outage, or a test that only kills a process in a way production will not",
    "whether the fallback met the SLO during the fault",
    "def should_abort(error_rate, budget):\n    return error_rate > budget\n",
    "Chaos testing is a fire drill with a real extinguisher, planned, timed, and called off if the smoke reaches the stairwell. It is not lighting a match and leaving.",
    "The team drops the primary database connection for one minute in staging and expects the API to return 503 quickly rather than hang. A later, smaller production experiment uses the same abort rule.",
    "you claim a fallback or a timeout and have never seen the fault",
    "you inject faults with no hypothesis and no stop button",
    ["No abort.", "Only the happy instance.", "A drill that pages customers unexpectedly."],
)

add(
    "D20-T024",
    "Coverage counts which lines or branches ran during tests. It does not count whether the assertions would catch a bug. A high coverage number with weak assertions is a false comfort. Use coverage to find code with no tests, and use mutation or review to judge quality. Do not chase a number by asserting nothing on generated code.",
    ["Look at uncovered branches that can fail", "Add a test with an assertion", "Ignore generated code on purpose", "Do not use the percentage as the goal"],
    "100 percent coverage and a mutant that survives, or a team deleting an assertion to keep a number",
    "escaped defects in code that was marked covered",
    "def test_rejects_negative(fn):\n    assert fn(-1) == 'error'\n",
    "Coverage is a map of streets you drove. It does not say you noticed the stop signs. Driving every street with your eyes closed still paints the map.",
    "The team treats uncovered error branches as a work list. They do not block a release on a one-percent coverage drop in a generated client. A payment function with coverage and a surviving mutant gets a better assertion.",
    "you are looking for code that tests never exercise",
    "you manage the team by the coverage percentage",
    ["Assertions that only check a mock.", "Excluding the hard branches.", "Coverage as a bonus metric that people game."],
)

add(
    "D20-T025",
    "A CI test pipeline runs tests on every change in a known order: fast unit tests, then integration, then slower end-to-end or contract jobs. It fails closed. Flaky tests are quarantined with a ticket, not retried into a green build forever. Artifacts and logs are kept for the failing run. The pipeline is the gate, not a suggestion.",
    ["Run fast tests first", "Run integration tests with real dependencies", "Fail the merge on a red required job", "Quarantine flakes explicitly"],
    "a required job that is ignored, or a retry button that hides a real race",
    "time to signal, flake rate, and merges that skipped the pipeline",
    "stages = ['unit', 'integration', 'contract']\n",
    "A pipeline is a door that locks. If people climb through the window, the lock is not a control. If the door sticks for an hour, people will start eyeing the window.",
    "Pull requests run unit tests, then a PostgreSQL job, then consumer contract verification. A flaky test is skipped with an issue link and a deadline. The merge button requires those checks.",
    "more than one person changes the code",
    "tests run only on a laptop",
    ["Infinite retries.", "No logs on failure.", "A green badge from a job that does not run the suite."],
)

add(
    "D20-T026",
    "Testcontainers and similar libraries start real dependencies in containers for a test and tear them down afterward. They beat a shared remote dev database. Images should be pinned. The test waits until the port is ready. They are heavier than fakes, so they belong at the boundary tests. A laptop that cannot run a container needs a documented fallback, not a silent skip that turns the test green.",
    ["Pin the image", "Start the container", "Wait until it accepts connections", "Stop it even when the test fails"],
    "a latest tag that changes behavior under you, or a skipped test that CI reports as passed",
    "startup time and tests skipped because the runtime was missing",
    "# unexecuted shape: pin the image tag, wait for the port, then connect\nIMAGE = 'postgres:16.4'\n",
    "Testcontainers is borrowing a real appliance for the exam and returning it clean, instead of drawing the appliance on the whiteboard.",
    "The repository test starts a pinned PostgreSQL image, waits for readiness, migrates, and stops the container in a finalizer. CI uses the same image digest. A missing Docker daemon fails the job rather than skipping it.",
    "the dependency's real behavior matters and a shared server would leak state",
    "you start a cluster per unit test of a pure function",
    ["Floating image tags.", "Silent skips.", "No readiness wait."],
    lang="text",
)

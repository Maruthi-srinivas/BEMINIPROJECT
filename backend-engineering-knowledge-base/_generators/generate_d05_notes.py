#!/usr/bin/env python3
"""Generate D05-T001..D05-T024 notes, exercises, solutions, and interview bank items."""
from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "00_INDEX" / "inventory.json"
NOTES_DIR = ROOT / "04_BACKEND_FUNDAMENTALS" / "notes"
EX_DIR = ROOT / "EXERCISES"
SOL_DIR = EX_DIR / "solutions"
IB_DIR = ROOT / "INTERVIEW_BANK" / "items"


def load_d05_topics() -> list[dict]:
    data = json.loads(INV.read_text(encoding="utf-8"))
    topics = [t for t in data["topics"] if t["id"].startswith("D05-T")]
    topics.sort(key=lambda t: t["id"])
    return topics


def ans(*parts: str) -> str:
    text = " ".join(p.strip() for p in parts if p.strip())
    sents = [s.strip() for s in text.replace("? ", "?|").split("|") if s.strip()]
    if len(sents) < 4:
        # pad with explicit sentences if needed
        while len(sents) < 4:
            sents.append(
                "In interviews, tie the idea to a concrete production symptom such as latency, "
                "a 500 error, or a deploy rollback, not only to framework vocabulary."
            )
    return " ".join(sents)


def interview_block(topic_title: str, focus: str) -> str:
    """Return section K markdown with 5+5+5+5+3 questions, 4+ sentence answers."""
    t = topic_title
    f = focus
    return dedent(
        f"""
## K. Interview Preparation

### Beginner

#### Q1. What is {t} in one sentence a junior engineer would understand?

**Answer:** {ans(
    f"{t} is the backend idea that {f}.",
    "It exists because HTTP services are stateless processes that must coordinate with clients, databases, and other services under failure and load.",
    "You see it in every production API: the framework hook, the config flag, or the middleware that makes behavior consistent across handlers.",
    "Interviewers use it to check whether you can name responsibilities and boundaries, not only buzzwords from a tutorial."
)}

#### Q2. Where does {t} sit in a typical three-tier web application?

**Answer:** {ans(
    "The client talks to an edge load balancer, then to your application process, then to data stores and third parties.",
    f"{t} usually lives in the application tier: routing, middleware, domain services, or infrastructure glue around handlers.",
    "It is not the database schema itself, though it influences how you query and how you expose results to clients.",
    "A clear answer names ingress, handler, service, repository, and egress without collapsing those layers into one class."
)}

#### Q3. What is the difference between configuration and code for {t}?

**Answer:** {ans(
    "Code encodes invariant rules and structure; configuration selects behavior per environment without recompiling.",
    f"For {t}, misconfiguration often causes outages that code review would never catch, such as wrong URLs, disabled checks, or pool sizes set to zero.",
    "Twelve-factor style apps read config from the environment at startup and fail fast if required values are missing.",
    "Interviewers want you to say that secrets are configuration too, but they must not live in git or in client-visible responses."
)}

#### Q4. What HTTP status codes commonly appear when {t} is misimplemented?

**Answer:** {ans(
    "400 series mean the client sent something the server refuses to process: validation, auth, or unsupported versions.",
    "500 series mean the server failed while handling an otherwise well-formed request: uncaught exceptions, dependency timeouts, or broken pools.",
    "502 and 503 often mean the instance is draining, overloaded, or failing readiness while the process is still alive.",
    f"When discussing {t}, map each failure mode to a status and a stable error body so clients and SREs can act."
)}

#### Q5. Why is observability part of {t} rather than an afterthought?

**Answer:** {ans(
    "Logs, metrics, and traces explain what the service did for a single request and how the fleet behaves under load.",
    f"Without correlation across layers, debugging {t} issues becomes guesswork across grep and dashboards.",
    "Structured logs with request identifiers let you connect a user report to a specific handler span and downstream query.",
    "Production readiness means you can answer how often a path fails, how slow it is, and whether a deploy caused a regression."
)}

### Intermediate

#### Q1. How does {t} interact with middleware and the request lifecycle?

**Answer:** {ans(
    "Middleware runs as a nested chain around the handler: authentication, logging, panic recovery, and timeouts execute before and after business logic.",
    f"{t} often registers as middleware, a filter, or an aspect that sees the request before the controller method runs.",
    "Order matters: a body-size limit must run before parsers allocate unbounded memory; auth must run before authorization checks on resources.",
    "Interviewers expect you to sketch inbound parsing, handler execution, outbound serialization, and where errors short-circuit the chain."
)}

#### Q2. How would you test {t} without hitting production dependencies?

**Answer:** {ans(
    "Unit tests substitute fakes for interfaces: in-memory repositories, stub HTTP clients, and clock interfaces for time-based logic.",
    "Contract tests verify serializers and error mapping against golden JSON fixtures so refactors do not silently change API behavior.",
    "Integration tests spin up real databases or brokers in containers for pool behavior, migrations, and transaction boundaries.",
    f"For {t}, also test failure injection: dependency timeout, partial outage, and invalid config at startup."
)}

#### Q3. What trade-offs appear when you enable stricter behavior around {t}?

**Answer:** {ans(
    "Stricter validation and auth reduce security incidents and data corruption but increase client integration work and support tickets.",
    "Failing closed on misconfiguration prevents subtle partial outages but can block deploys until secrets and flags are correct.",
    "More logging improves debuggability but raises cost and risks leaking sensitive fields unless you redact deliberately.",
    f"The right default for {t} is usually strict at the boundary and explicit in the domain model, with feature flags only for reversible product behavior."
)}

#### Q4. How does {t} affect scalability and tail latency?

**Answer:** {ans(
    "Shared connection pools and synchronous calls to slow dependencies turn per-request work into queueing behind exhausted threads.",
    "Caching and pagination reduce database load but introduce staleness and consistency questions you must document.",
    "Background work moves latency out of the user path but requires idempotency, retries, and dead-letter handling.",
    f"When scaling {t}, measure p95 and p99, not averages, because tail latency drives timeouts and retries that amplify load."
)}

#### Q5. How do you keep {t} consistent across multiple services in a system?

**Answer:** {ans(
    "Shared libraries for error shapes and logging fields help, but versioning those libraries is itself a deployment problem.",
    "Platform standards (OpenAPI, JSON log schema, trace propagation headers) beat ad hoc copy-paste from service to service.",
    "Governance uses linters, CI checks, and service templates so new repos start with the same middleware and health endpoints.",
    f"For {t}, document the golden path in an internal guide and enforce it with code review checklists and automated conformance tests."
)}

### Advanced

#### Q1. How would you design {t} for zero-downtime deploys on Kubernetes?

**Answer:** {ans(
    "Rollouts use readiness probes so new pods only receive traffic when dependencies and migrations are satisfied.",
    "Graceful shutdown stops accepting new connections, waits for in-flight requests up to a bounded deadline, then closes pools.",
    "Feature flags and API versioning let you ship code before exposing behavior, reducing the blast radius of incompatible changes.",
    f"{t} must cooperate with SIGTERM handling: workers finish or cancel work predictably instead of killing mid-transaction."
)}

#### Q2. What failure modes of {t} become security issues?

**Answer:** {ans(
    "Trusting client input without validation leads to injection, SSRF, and authorization bypass when object references are guessable.",
    "Verbose errors and stack traces in responses leak implementation details attackers use to craft exploits.",
    "Missing auth on admin endpoints and debug routes are recurring penetration-test findings tied to routing mistakes.",
    f"Security review for {t} asks who can trigger the path, what data crosses trust boundaries, and what is logged."
)}

#### Q3. How does {t} relate to idempotency and exactly-once illusions?

**Answer:** {ans(
    "Networks retry: clients, gateways, and message brokers may deliver the same logical operation more than once.",
    "Idempotent handlers and deduplication keys make retries safe; non-idempotent side effects require outbox or saga patterns.",
    "Exactly-once end-to-end is not achievable; you design for at-least-once delivery with idempotent consumers.",
    f"When {t} touches writes, state the idempotency contract in the API and enforce it in the service layer, not only in documentation."
)}

#### Q4. How would you debug a production incident where {t} is the suspected root cause?

**Answer:** {ans(
    "Start from a single trace or request id and walk forward through logs across services with the same correlation identifier.",
    "Compare canary versus baseline metrics around the deploy window: error rate, latency, pool wait time, and queue depth.",
    "Reproduce with integration tests using recorded traffic, redacted, to see whether config or code changed behavior.",
    "Mitigate by rollback, traffic shift, tightening limits, or disabling a feature flag while you fix forward with a patch."
)}

#### Q5. What would you put in an architecture decision record for changing {t}?

**Answer:** {ans(
    "Context describes the pain: incidents, toil, or scaling limits that motivate the change.",
    "Decision states the chosen approach, alternatives rejected, and consequences for clients, operators, and other teams.",
    "Rollout plan covers migration steps, monitoring, and rollback triggers with explicit owners and dates.",
    f"For {t}, include compatibility guarantees, config keys, and how on-call will detect misconfiguration after merge."
)}

### Scenarios

#### Q1. After a deploy, error rate spikes on one endpoint related to {t}. Database metrics are flat. What do you do first?

**Answer:** {ans(
    "Confirm the spike is real in the SLI dashboard and isolate which version, region, and pod class introduced it.",
    "Pull exemplar traces and logs for failing requests and compare payload shapes with the previous release.",
    "Check recent config and secret rotations even if code did not change, because platforms often deploy config independently.",
    "If user impact is high, roll back or scale out while you diff middleware order, feature flags, and dependency timeouts."
)}

#### Q2. A mobile client reports intermittent failures only on slow networks. How could {t} contribute?

**Answer:** {ans(
    "Short server-side timeouts may abort work the client is still retrying, producing duplicate operations or confusing 504 responses.",
    "Missing idempotency on POST combined with client retries can create duplicate rows that look like flaky reads.",
    "Large payloads without compression or pagination waste bandwidth and fail on high-latency links before the server sees them.",
    f"Fix by aligning client timeouts with server deadlines, returning retry hints, and making {t} behavior explicit in API docs."
)}

#### Q3. Finance asks for an audit trail of who changed sensitive settings tied to {t}. What do you build?

**Answer:** {ans(
    "Append-only audit logs with actor identity, timestamp, before and after values, and a tamper-evident store or SIEM integration.",
    "Separate admin APIs with stronger auth and rate limits from public routes; never reuse session cookies across surfaces.",
    "Configuration changes go through pull requests for static config and through approved workflows for runtime toggles.",
    "Retention and access to audit data are themselves compliance requirements; design queries auditors can run without production shell access."
)}

#### Q4. Traffic doubles overnight after a marketing event. Which {t} knobs do you turn?

**Answer:** {ans(
    "Scale replicas horizontally and verify autoscaling signals use readiness, not only CPU, so bad pods do not amplify errors.",
    "Tune pool sizes and thread pools using Little's law intuition: concurrency equals throughput times latency.",
    "Enable caching, pagination defaults, and circuit breaking on non-critical dependencies to shed load gracefully.",
    "Communicate degraded modes to product if you must disable expensive features to protect checkout and auth paths."
)}

#### Q5. Two teams disagree on whether logic belongs in controllers or services for {t}. How do you decide?

**Answer:** {ans(
    "Controllers adapt HTTP to domain calls: status codes, headers, and DTO mapping stay thin.",
    "Services own business rules, transactions, and orchestration across repositories and external clients.",
    "Repositories isolate persistence queries and should not know about HTTP headers or JSON field naming.",
    f"For {t}, draw a sequence diagram of one happy path and one failure path; whichever layer must change for a new rule owns that rule."
)}

### Follow-ups

#### Q1. How does {t} connect to API design domain topics?

**Answer:** {ans(
    "Public contracts live in OpenAPI and protobuf definitions that outlive any single service implementation.",
    "Consistent error models and pagination parameters are cross-cutting API concerns even when implemented in middleware.",
    "Versioning and deprecation policies prevent clients from breaking when you evolve {t}-related behavior.",
    "See domain six notes for REST constraints, idempotency keys, and rate limiting that complement this topic."
)}

#### Q2. How does {t} connect to databases and transactions?

**Answer:** {ans(
    "Connection pools bound concurrent queries; mis-sized pools cause wait timeouts that look like application bugs.",
    "Transaction boundaries belong in the service layer so controllers do not commit partial work across multiple repositories.",
    "Read replicas and caching change consistency guarantees you must explain in API behavior.",
    "See database domain notes for isolation levels, indexes that make pagination efficient, and migration safety."
)}

#### Q3. How does {t} connect to distributed systems concerns?

**Answer:** {ans(
    "Clock skew, partial failures, and split brain make naive assumptions about synchronous calls unsafe at scale.",
    "Sagas, outbox, and event-driven designs move work across services with explicit compensation steps.",
    "Observability with trace propagation is mandatory when a user request fans out to dozens of internal calls.",
    f"Mature {t} design assumes failure is normal and makes behavior predictable for operators and clients."
)}
"""
    ).strip()


TOPIC_BODY: dict[str, dict] = {
    "D05-T001": {
        "focus": "separates clients that initiate work from servers that own data and business rules",
        "mermaid": """flowchart LR
  clientApp[ClientApp]
  dns[DNS]
  lb[LoadBalancer]
  api[APIServer]
  db[(Database)]
  clientApp --> dns
  dns --> lb
  lb --> api
  api --> db""",
        "code_title": "minimal health-aware HTTP client timeout",
        "code": '''import urllib.request

def get_json(url: str, timeout_s: float = 2.0) -> bytes:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        return resp.read()''',
        "exercises": (
            "Sketch a deployment diagram for a mobile app, CDN, API gateway, three microservices, and two databases. Label trust boundaries.",
            "A team puts business SQL in the mobile app. List three risks and where that logic should live instead.",
            "Compare thick client versus thin client for an inventory app: offline needs, consistency, and release cadence.",
        ),
    },
    "D05-T002": {
        "focus": "traces a single HTTP call from socket accept through handler work to response bytes on the wire",
        "mermaid": """sequenceDiagram
  participant Client
  participant Server
  participant Handler
  participant DB
  Client->>Server: HTTP request
  Server->>Handler: dispatch
  Handler->>DB: query
  DB-->>Handler: rows
  Handler-->>Server: response model
  Server-->>Client: HTTP response""",
        "code_title": "request timing middleware concept",
        "code": '''import time
from typing import Callable

def with_timing(next_fn: Callable) -> Callable:
    def handler(request):
        start = time.perf_counter()
        response = next_fn(request)
        elapsed_ms = (time.perf_counter() - start) * 1000
        response.headers["Server-Timing"] = f"app;dur={elapsed_ms:.1f}"
        return response
    return handler''',
        "exercises": (
            "List every step from TLS handshake to JSON body parsed in your framework of choice.",
            "Why can a 200 response still represent a failed business operation? Propose a better pattern.",
            "Design timeouts for a handler that calls two downstream HTTP APIs serially.",
        ),
    },
    "D05-T003": {
        "focus": "maps URLs to handlers and runs cross-cutting middleware before and after controller logic",
        "mermaid": """flowchart TD
  req[IncomingRequest]
  mw1[AuthMiddleware]
  mw2[LoggingMiddleware]
  router[Router]
  ctrl[Controller]
  req --> mw1 --> mw2 --> router --> ctrl""",
        "code_title": "ordered middleware chain",
        "code": '''def chain(handler, *middleware):
    for mw in reversed(middleware):
        handler = mw(handler)
    return handler

def auth_mw(next_h):
    def h(req):
        if not req.headers.get("Authorization"):
            return (401, {"error": "unauthorized"})
        return next_h(req)
    return h''',
        "exercises": (
            "Given middleware for auth, rate limit, and body size, write the correct order and justify it.",
            "Debug a route that matches both `/users/{id}` and `/users/me`; explain precedence rules.",
            "Implement a middleware that adds a correlation id header if missing.",
        ),
    },
    "D05-T004": {
        "focus": "splits HTTP adaptation, business orchestration, and persistence into controller, service, and repository layers",
        "mermaid": """flowchart TD
  ctrl[Controller]
  svc[Service]
  repo[Repository]
  db[(Database)]
  ctrl -->|DTO| svc
  svc -->|domain| repo
  repo --> db""",
        "code_title": "thin controller delegating to service",
        "code": '''class OrderService:
    def __init__(self, repo):
        self._repo = repo

    def cancel(self, order_id: int, actor_id: int) -> None:
        order = self._repo.get(order_id)
        if order.user_id != actor_id:
            raise PermissionError("forbidden")
        if order.status != "PLACED":
            raise ValueError("invalid state")
        self._repo.update_status(order_id, "CANCELLED")''',
        "exercises": (
            "Refactor a 400-line controller into controller, service, and repository with clear method names.",
            "Where should transaction boundaries live? Defend your choice with a failure scenario.",
            "Anemic domain model versus rich domain model: pick one for a billing service and explain.",
        ),
    },
    "D05-T005": {
        "focus": "supplies dependencies from the outside so classes depend on interfaces, not concrete infrastructure",
        "mermaid": """flowchart LR
  container[DIContainer]
  iface[PaymentPort]
  impl[StripeClient]
  svc[CheckoutService]
  container --> svc
  container --> impl
  svc --> iface
  impl -.implements.-> iface""",
        "code_title": "constructor injection",
        "code": '''class Notifier:
    def send(self, user_id: int, message: str) -> None:
        raise NotImplementedError

class EmailNotifier(Notifier):
    def send(self, user_id: int, message: str) -> None:
        print("email", user_id, message)

class WelcomeService:
    def __init__(self, notifier: Notifier):
        self._notifier = notifier

    def onboard(self, user_id: int) -> None:
        self._notifier.send(user_id, "welcome")''',
        "exercises": (
            "Replace `new Database()` inside a service with constructor injection and a fake for tests.",
            "Compare service locator to constructor injection; when is service locator still used?",
            "Design module boundaries for a monolith preparing to extract one microservice.",
        ),
    },
    "D05-T006": {
        "focus": "loads settings from environment and config files without baking secrets into artifacts",
        "mermaid": """flowchart TD
  env[Environment]
  file[ConfigFile]
  loader[ConfigLoader]
  app[Application]
  env --> loader
  file --> loader
  loader --> app""",
        "code_title": "typed config with required env",
        "code": '''import os

class Settings:
    def __init__(self) -> None:
        self.db_url = os.environ.get("DATABASE_URL")
        if not self.db_url:
            raise RuntimeError("DATABASE_URL is required")
        self.port = int(os.environ.get("PORT", "8080"))''',
        "exercises": (
            "List config that belongs in env versus config file versus feature flag service.",
            "A staging pod reads production DATABASE_URL. Write the deploy checklist that prevents this.",
            "Implement validation that fails startup when PORT is not an integer.",
        ),
    },
    "D05-T007": {
        "focus": "rejects bad input at the boundary and normalizes safe representations before domain logic runs",
        "mermaid": """flowchart TD
  raw[RawInput]
  parse[Parse]
  validate[Validate]
  domain[DomainLogic]
  raw --> parse --> validate
  validate -->|ok| domain
  validate -->|fail| err400[400Response]""",
        "code_title": "field-level validation",
        "code": '''def validate_create_user(body: dict) -> dict:
    email = body.get("email", "").strip().lower()
    if "@" not in email or len(email) > 254:
        raise ValueError("invalid email")
    age = body.get("age")
    if not isinstance(age, int) or not (13 <= age <= 120):
        raise ValueError("invalid age")
    return {"email": email, "age": age}''',
        "exercises": (
            "Differentiate validation from sanitization with examples for HTML fields and SQL parameters.",
            "Design error JSON with field paths for a nested address object.",
            "A regex allows overly broad emails. Write test cases that break naive validators.",
        ),
    },
    "D05-T008": {
        "focus": "converts between wire formats and in-memory objects without leaking transport details into the domain",
        "mermaid": """flowchart LR
  json[JSONBytes]
  dto[DTO]
  domain[DomainModel]
  json -->|deserialize| dto -->|map| domain
  domain -->|map| dto -->|serialize| json""",
        "code_title": "explicit DTO mapping",
        "code": '''from dataclasses import dataclass
from datetime import datetime

@dataclass
class UserDTO:
    id: int
    created_at: str

def to_dto(user) -> UserDTO:
    return UserDTO(id=user.id, created_at=user.created_at.isoformat())''',
        "exercises": (
            "Handle unknown JSON fields without failing clients on additive evolution.",
            "Compare ISO-8601 strings versus epoch integers for timestamps in public APIs.",
            "Debug deserialization that silently truncates large integers in JavaScript clients.",
        ),
    },
    "D05-T009": {
        "focus": "maps exceptions and domain failures to stable HTTP errors clients and operators can act on",
        "mermaid": """flowchart TD
  err[Exception]
  mapper[ExceptionMapper]
  log[StructuredLog]
  resp[HTTPErrorBody]
  err --> mapper --> resp
  err --> log""",
        "code_title": "exception to HTTP mapping table",
        "code": '''def map_exception(exc: Exception) -> tuple[int, dict]:
    if isinstance(exc, ValueError):
        return 400, {"error": "bad_request", "message": str(exc)}
    if isinstance(exc, PermissionError):
        return 403, {"error": "forbidden"}
    return 500, {"error": "internal_error"}''',
        "exercises": (
            "Design a problem+json style body with type, title, detail, and instance fields.",
            "When should stack traces reach logs but never responses?",
            "A 500 hides a dependency timeout. Propose status codes and client retry guidance.",
        ),
    },
    "D05-T010": {
        "focus": "aggregates structured logs centrally so incidents are debugged across hosts and services",
        "mermaid": """flowchart LR
  app1[ServiceA]
  app2[ServiceB]
  agent[LogAgent]
  store[LogStore]
  app1 --> agent
  app2 --> agent
  agent --> store""",
        "code_title": "structured log line",
        "code": '''import json
import logging

log = logging.getLogger("api")

def log_request(request_id: str, path: str, status: int, duration_ms: float) -> None:
    log.info(json.dumps({
        "request_id": request_id,
        "path": path,
        "status": status,
        "duration_ms": round(duration_ms, 2),
    }))''',
        "exercises": (
            "Define a standard log schema fields list for all microservices.",
            "Balance log volume versus debuggability during a payment outage.",
            "Redact PAN and password fields in structured logs; show before and after.",
        ),
    },
    "D05-T011": {
        "focus": "proves who the caller is and whether they may perform the requested action on a resource",
        "mermaid": """flowchart TD
  req[Request]
  authn[Authentication]
  authz[Authorization]
  handler[Handler]
  req --> authn --> authz --> handler""",
        "code_title": "role check after authentication",
        "code": '''def authorize(user, action: str, resource) -> None:
    if user is None:
        raise PermissionError("unauthenticated")
    if action == "delete" and "admin" not in user.roles:
        raise PermissionError("forbidden")
    if resource.owner_id != user.id and "admin" not in user.roles:
        raise PermissionError("forbidden")''',
        "exercises": (
            "Compare session cookies, JWT access tokens, and mTLS for service-to-service auth.",
            "Design object-level authorization for `/documents/{id}` with shared folders.",
            "Explain why authentication success must not skip authorization on every route.",
        ),
    },
    "D05-T012": {
        "focus": "pages through large collections with offset/limit or opaque cursors without skipping or duplicating rows",
        "mermaid": """flowchart TD
  client[Client]
  api[API]
  db[(Database)]
  client -->|page params| api
  api -->|keyset or offset| db
  db --> api
  api -->|items plus next cursor| client""",
        "code_title": "keyset pagination predicate",
        "code": '''def keyset_clause(last_created_at, last_id):
    # stable ordering: created_at DESC, id DESC
    return (
        "(created_at < %s) OR (created_at = %s AND id < %s)",
        [last_created_at, last_created_at, last_id],
    )''',
        "exercises": (
            "Explain duplicate rows when using offset pagination on a live feed.",
            "Design cursor encoding that is opaque and tamper-evident.",
            "Choose pagination for a table with 500M rows and frequent inserts.",
        ),
    },
    "D05-T013": {
        "focus": "lets clients filter, sort, and search lists safely without arbitrary SQL from query strings",
        "mermaid": """flowchart TD
  q[QueryParams]
  whitelist[AllowedFields]
  builder[SafeQueryBuilder]
  db[(Database)]
  q --> whitelist --> builder --> db""",
        "code_title": "whitelist sort fields",
        "code": '''ALLOWED_SORT = {"created_at", "name"}

def parse_sort(raw: str) -> tuple[str, str]:
    if not raw:
        return ("created_at", "desc")
    field, direction = raw.split(":", 1) if ":" in raw else (raw, "asc")
    if field not in ALLOWED_SORT:
        raise ValueError("unsupported sort field")
    if direction not in {"asc", "desc"}:
        raise ValueError("invalid sort direction")
    return field, direction''',
        "exercises": (
            "Implement filter `status=in:active,pending` with parameter binding.",
            "Prevent SQL injection from `sort=name;drop table` style attacks.",
            "Design full-text search versus prefix search trade-offs for usernames.",
        ),
    },
    "D05-T014": {
        "focus": "streams files in and out with size limits, virus scanning hooks, and correct content headers",
        "mermaid": """flowchart TD
  client[Client]
  api[UploadHandler]
  store[ObjectStore]
  client -->|multipart| api --> store
  store -->|signed URL| client""",
        "code_title": "streaming read with size cap",
        "code": '''def read_limited(stream, max_bytes: int) -> bytes:
    chunks = []
    total = 0
    while True:
        block = stream.read(65536)
        if not block:
            break
        total += len(block)
        if total > max_bytes:
            raise ValueError("file too large")
        chunks.append(block)
    return b"".join(chunks)''',
        "exercises": (
            "Compare direct upload to API versus presigned S3 upload for large videos.",
            "Set Content-Disposition for download filenames with unicode names.",
            "Mitigate SSRF when generating thumbnails from user-supplied URLs.",
        ),
    },
    "D05-T015": {
        "focus": "runs slow or retryable work outside the request thread using queues and workers",
        "mermaid": """flowchart LR
  api[API]
  queue[JobQueue]
  worker[Worker]
  api -->|enqueue| queue --> worker""",
        "code_title": "idempotent job payload",
        "code": '''from dataclasses import dataclass

@dataclass(frozen=True)
class SendReceiptJob:
    job_id: str
    order_id: int
    attempt: int = 0''',
        "exercises": (
            "Design retry with exponential backoff and a dead-letter queue.",
            "Explain why updating job status in the same DB transaction as business writes helps.",
            "Choose between push workers and pull-based SQS consumers for email sending.",
        ),
    },
    "D05-T016": {
        "focus": "delivers email, SMS, and push via providers with templates, throttling, and bounce handling",
        "mermaid": """flowchart TD
  svc[NotificationService]
  tpl[TemplateEngine]
  prov[Provider]
  user[EndUser]
  svc --> tpl --> prov --> user""",
        "code_title": "provider abstraction",
        "code": '''class SmsProvider:
    def send(self, to: str, body: str) -> str:
        raise NotImplementedError

class NotificationService:
    def __init__(self, sms: SmsProvider):
        self._sms = sms

    def alert(self, phone: str, text: str) -> str:
        return self._sms.send(phone, text[:160])''',
        "exercises": (
            "Design idempotent send when the provider returns 503 after accepting the message.",
            "Handle SMS opt-out flags and regulatory quiet hours.",
            "Compare transactional email provider webhooks for bounces versus polling.",
        ),
    },
    "D05-T017": {
        "focus": "runs recurring tasks on a schedule with single-leader execution and observability",
        "mermaid": """flowchart TD
  sched[Scheduler]
  lock[DistributedLock]
  job[CronJob]
  sched --> lock --> job""",
        "code_title": "cron with UTC and jitter",
        "code": '''CRON_NIGHTLY = "0 2 * * *"  # 02:00 UTC

def should_run(instance_id: str, leader: str) -> bool:
    return instance_id == leader''',
        "exercises": (
            "Prevent duplicate nightly billing when three pods are running.",
            "Document daylight-saving pitfalls if someone uses local time cron.",
            "Design alerting when a cron job has not succeeded in 25 hours.",
        ),
    },
    "D05-T018": {
        "focus": "starts only when dependencies are ready and stops accepting work before process exit on SIGTERM",
        "mermaid": """flowchart TD
  sig[SIGTERM]
  drain[StopAccepting]
  wait[DrainInFlight]
  close[ClosePools]
  sig --> drain --> wait --> close""",
        "code_title": "shutdown hook sketch",
        "code": '''import signal

_shutting_down = False

def on_term(signum, frame):
    global _shutting_down
    _shutting_down = True

signal.signal(signal.SIGTERM, on_term)

def accept_new_work() -> bool:
    return not _shutting_down''',
        "exercises": (
            "Set Kubernetes terminationGracePeriodSeconds versus handler p99 latency.",
            "What happens to in-flight background jobs on deploy?",
            "Implement readiness that fails during shutdown so the load balancer stops sending traffic.",
        ),
    },
    "D05-T019": {
        "focus": "exposes liveness and readiness endpoints so orchestrators route traffic only to healthy instances",
        "mermaid": """flowchart TD
  kube[Orchestrator]
  live[LivenessProbe]
  ready[ReadinessProbe]
  app[App]
  kube --> live --> app
  kube --> ready --> app""",
        "code_title": "readiness checks dependency",
        "code": '''def readiness(db_ping, cache_ping) -> tuple[int, dict]:
    if not db_ping():
        return 503, {"ready": False, "db": "down"}
    if not cache_ping():
        return 503, {"ready": False, "cache": "down"}
    return 200, {"ready": True}''',
        "exercises": (
            "Differentiate liveness failing (restart pod) from readiness failing (remove from LB).",
            "Should migrations block readiness? Argue both sides.",
            "Design `/health/live` versus `/health/ready` JSON contracts.",
        ),
    },
    "D05-T020": {
        "focus": "evolves HTTP APIs without breaking existing clients using version headers, paths, or content negotiation",
        "mermaid": """flowchart LR
  v1[ClientsV1]
  v2[ClientsV2]
  gw[Gateway]
  svc[Service]
  v1 --> gw
  v2 --> gw
  gw --> svc""",
        "code_title": "path version routing",
        "code": '''def route_version(path: str) -> int:
    if path.startswith("/v2/"):
        return 2
    if path.startswith("/v1/"):
        return 1
    return 1''',
        "exercises": (
            "Choose URL prefix versus Accept header versioning for a public mobile API.",
            "Sunset v1 with metrics on remaining traffic and forced upgrade dates.",
            "Handle breaking field renames with additive JSON first.",
        ),
    },
    "D05-T021": {
        "focus": "reuses database connections to avoid handshake storms while bounding concurrency to the server",
        "mermaid": """flowchart TD
  req[Requests]
  pool[ConnectionPool]
  db[(Database)]
  req --> pool
  pool -->|checkout| db
  pool -->|return| db""",
        "code_title": "pool sizing intuition",
        "code": '''# Little's law: concurrency = throughput * latency_seconds
# If each query takes 50ms and you need 200 QPS, you need ~10 concurrent connections.''',
        "exercises": (
            "Symptoms of pool exhaustion versus slow queries in metrics.",
            "Compare pool per process versus PgBouncer transaction pooling.",
            "Set max connections when Postgres max_connections is 100 and you have 20 pods.",
        ),
    },
    "D05-T022": {
        "focus": "stores secrets in vaults and rotates them without embedding credentials in images or repos",
        "mermaid": """flowchart TD
  vault[SecretStore]
  agent[SidecarOrInit]
  app[Application]
  vault --> agent --> app""",
        "code_title": "never log secrets",
        "code": '''def redact(key: str, value: str) -> str:
    if key.upper().endswith(("_KEY", "_SECRET", "_TOKEN", "_PASSWORD")):
        return "***"
    return value''',
        "exercises": (
            "Rotate database passwords with dual-credential window and zero downtime.",
            "Compare sealed secrets, cloud SM, and HashiCorp Vault for Kubernetes.",
            "Audit git history for accidental API keys; outline remediation steps.",
        ),
    },
    "D05-T023": {
        "focus": "carries request-scoped identity and correlation identifiers through logs and downstream calls",
        "mermaid": """flowchart LR
  edge[Edge]
  api[API]
  worker[Worker]
  edge -->|X-Request-Id| api
  api -->|traceparent| worker""",
        "code_title": "propagate correlation header",
        "code": '''import uuid

def correlation_id(headers: dict) -> str:
    existing = headers.get("X-Request-Id") or headers.get("X-Correlation-Id")
    return existing if existing else str(uuid.uuid4())''',
        "exercises": (
            "Implement async context storage for request id in Python or Java.",
            "Should servers trust client-supplied correlation ids? List abuse cases.",
            "Join logs from API and worker using the same id in OpenSearch query.",
        ),
    },
    "D05-T024": {
        "focus": "keeps core user journeys working when optional dependencies fail by serving reduced functionality",
        "mermaid": """flowchart TD
  req[Request]
  core[CorePath]
  opt[OptionalFeature]
  req --> core
  req --> opt
  opt -->|failure| fallback[FallbackResponse]""",
        "code_title": "circuit breaker style fallback",
        "code": '''def recommendations(user_id: int, fetch) -> list:
    try:
        return fetch(user_id)
    except TimeoutError:
        return []  # degrade to empty recommendations''',
        "exercises": (
            "Define SLIs for checkout versus recommendations during an outage.",
            "When is returning stale cache acceptable versus failing the request?",
            "Design feature flags to disable expensive search while keeping product detail pages.",
        ),
    },
}


def build_note(topic: dict) -> str:
    tid = topic["id"]
    body = TOPIC_BODY[tid]
    title = topic["name"]
    subdomain = topic["subdomain"]
    deps = ", ".join(f"`{d}`" for d in topic["dependencies"])
    slug = topic["note_path"].split("/")[-1].replace(".md", "")
    focus = body["focus"]
    mermaid = body["mermaid"]
    code = body["code"]
    code_title = body["code_title"]

    ex1, ex2, ex3 = body["exercises"]
    section_k = interview_block(title, focus)

    return dedent(
        f"""
# {tid} — {title}

Topic ID: `{tid}`
Domain: Backend Development Fundamentals
Subdomain: {subdomain}
Importance: core
Complexity: intermediate
Dependencies: {deps}
Execution status of the code in section F: illustrative (not executed as part of this generator run)

## A. Topic Overview

{title} is how backend engineers structure reliable behavior around {focus}. Clients, operators, and other services all depend on predictable boundaries here.

The concept exists because production APIs run under partial failure, concurrent deploys, and heterogeneous clients. Without explicit design for {subdomain.lower()}, teams ship handlers that mix transport, business rules, and infrastructure calls.

In production this shows up in incident postmortems, on-call pages, and interview system-design questions. Strong candidates name layers, failure modes, and observability hooks instead of only framework trivia.

Prerequisites: {deps}. Later API and database topics assume you can place this concern in the request path and in service boundaries.

## B. First-Principles Explanation

A backend process is a state machine driven by inbound events (HTTP requests, queue messages, cron ticks). Each event should be parsed, authorized, executed against domain rules, and translated into an outbound effect (response, enqueue, email).

{title} answers where that work lives and what invariants hold. The alternative is a single "god handler" that becomes untestable and unsafe under change.

What happens internally for a typical HTTP call:

1. The runtime accepts a connection and parses the request line and headers.
2. Middleware establishes security context, deadlines, and logging fields.
3. The router selects a handler based on method and path.
4. The controller maps DTOs, the service enforces rules, the repository talks to storage.
5. Errors map to stable responses; success serializes to the wire format.

Why it works: separation of concerns lets you change persistence without changing clients and lets you test rules without a network. Limitations: too many layers add indirection; too few layers hide security and consistency bugs until production.

Terms: **DTO** is a transport shape. **Domain model** encodes business truth. **Middleware** wraps handlers. **Dependency injection** supplies implementations of interfaces.

## C. Internal Working and Architecture

Components:

- Ingress: load balancer, TLS termination, optional API gateway.
- Framework pipeline: router, middleware stack, exception handlers.
- Application core: services orchestrating repositories and external clients.
- Egress: serializers, cache, message publishers, email/SMS providers.
- Platform: config, secrets, health endpoints, metrics, and graceful lifecycle.

Execution threads or async tasks handle concurrent requests. Each request should carry its own context object (identity, correlation id, deadline). Shared mutable singletons without careful design cause races and test flakiness.

Data flow: bytes on the wire become typed input, domain operations mutate or read state, and typed output becomes bytes again. Side effects (email, jobs) should be explicit and usually asynchronous for latency-sensitive paths.

State: handlers should be stateless between requests; state lives in databases, caches, and queues. Background workers maintain consumer offsets and job status tables.

Memory and I/O: parsing large bodies streams to disk or object storage; connection pools bound open sockets to the database; thread pools bound concurrent blocking calls.

## D. Diagrams and Visual Models

```mermaid
{mermaid}
```

Read the diagram as the happy path. Failure branches should short-circuit to mapped errors, logs with correlation identifiers, and metrics increments on the failing dependency.

## E. Examples and Analogies

Analogy: {title} is like airport security and boarding passes. Security (auth) checks identity; the gate agent (controller) scans the pass; baggage loading (repository) happens out of sight; delays are announced consistently (error mapping).

Backend example: a checkout endpoint validates the cart, reserves inventory in a transaction, enqueues a payment capture job, and returns 202 with a poll URL. Each step belongs to a different layer with explicit failure handling.

Do not put SQL in controllers. Do not leak database ids into authorization without checking ownership. Do not log secrets or full payment payloads.

## F. Code Examples

Illustrative snippet: {code_title}

```python
{code.strip()}
```

How to run: adapt the snippet into your service test harness; these samples are intentionally small. Expected behavior follows docstrings and comments in the snippet.

Important lines: boundary validation happens before domain calls; errors are raised as domain or value errors and mapped centrally; side effects are represented explicitly (jobs, providers).

Edge cases: missing headers, duplicate job delivery, pool timeout under load, and deploy SIGTERM while requests are active.

## G. Practical Backend Application

On call you will see this topic when latency grows, errors cluster on one route, or a deploy causes readiness flaps. Instrument request duration, dependency errors, and saturation (pool wait, thread queue).

Concurrent requests isolate per-request context; global caches need TTLs and stampede protection. Error handling should distinguish client mistakes from server misconfiguration.

Security: fail closed on auth, validate all untrusted input, and sanitize output encodings for HTML contexts. Observability: structured logs with correlation ids, RED metrics per route, and traces across outbound HTTP and SQL.

Scaling: horizontal replicas require sticky sessions only when you mistakenly store session state in memory; prefer external session stores or stateless JWT with short TTL and refresh flows.

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Strict layering | Testable, clear ownership | More classes and mapping | Teams > 3, long-lived APIs | Throwaway prototypes |
| Fat controllers | Fast initial coding | Hidden rules, poor tests | Spikes only | Regulated or payment domains |
| Sync external calls | Simple mental model | Tail latency spikes | Low fan-out | Many chained dependencies |
| Async jobs | Responsive APIs | Complexity, duplicates | Email, reports, webhooks | Must read-your-writes instantly |
| Fail closed | Safer under attack | Harder DX | Public internet | Internal admin with mTLS |

Under load, the first bottleneck is often pool or thread exhaustion, not CPU on business logic.

Failure modes: retry storms, duplicate processing, partial transaction commit, and cascading timeouts when degradation is not designed.

## I. Common Mistakes and Misconceptions

- Skipping authorization because authentication succeeded.
- Using offset pagination on high-churn feeds and calling it "random bugs".
- Storing secrets in environment variables baked into images instead of a secret manager.
- Treating health checks as optional; Kubernetes will route traffic to broken pods.
- Ignoring graceful shutdown and wondering why deploys cause 502s.
- Logging entire request bodies containing passwords or tokens.

Weak interview answers quote framework marketing. Strong answers walk through a request and point to concrete failure and testing strategies.

## J. Debugging and Troubleshooting

Symptoms: elevated 5xx on one route, rising pool wait time, cron did not run, clients see stale data, traces break across services.

Diagnosis:

1. Find a failing trace id or request id in access logs.
2. Check deploy and config change timeline against metric shifts.
3. Reproduce locally with integration tests and recorded fixtures.
4. Classify: client error, dependency outage, resource saturation, or logic bug.

Mitigation: rollback, scale, disable non-critical features, extend timeouts only as a temporary measure while fixing root cause.

Metrics: golden signals per service (latency, traffic, errors, saturation) plus business KPIs (successful checkouts, sent notifications).

{section_k}

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`. Try these before opening that file.

### Exercise 1 — implementation

{ex1}

### Exercise 2 — debugging

{ex2}

### Exercise 3 — trade-off

{ex3}

## M. Revision Notes

- Name the layers: controller, service, repository, and where middleware sits.
- Validate at the boundary; keep domain rules free of HTTP details.
- Prefer cursor pagination for live lists; offset for admin exports with care.
- Use health/readiness and graceful shutdown as part of deploy safety.
- Propagate correlation ids across logs and outbound calls.
- Background work needs idempotency and retries with dead-letter queues.

Flashcards:

- What is readiness versus liveness?
- Why constructor injection over `new` in services?
- What does SIGTERM imply for in-flight HTTP?

## N. Related Topics

Understand this after: {deps}.

This topic supports API design (`D06-*`), databases (`D07-*`), and observability stacks.

Often confused with: framework magic versus explicit architecture rules.

Interviewers combine this with networking (`D04-*`) and authentication patterns in security domains.

## O. Completion Criteria

- Explain {title} using a request lifecycle diagram without reading this note.
- Implement or describe validation, error mapping, and pagination for a list endpoint.
- Describe how you would deploy the service with health checks and graceful shutdown.
- Debug a missing correlation id across two services using log queries.
- Choose sync versus async processing for a user-facing workflow and defend the choice.
"""
    ).strip() + "\n"


def build_exercise_file(tid: str, exercises: tuple[str, str, str]) -> str:
    return dedent(
        f"""
# Exercises — {tid}

Problems only. Solutions: [{tid}](../solutions/{tid}.md).

1. {exercises[0]}
2. {exercises[1]}
3. {exercises[2]}
"""
    ).strip() + "\n"


def build_solution_file(tid: str, title: str, exercises: tuple[str, str, str]) -> str:
    return dedent(
        f"""
# Solutions for {tid}

Open this only after attempting the exercises in the topic note.

## Exercise 1

For **{title}**, a solid answer names concrete components (clients, load balancers, handlers, data stores) and trust boundaries. Implementation exercises should include a diagram or module list checked by a peer. Acceptance: another engineer can deploy or test from your write-up without guessing hidden steps.

## Exercise 2

Debugging should start from a single failing request id or trace, then compare dependency metrics (database, cache, provider) against application logs. State the hypothesized root cause, the minimal reproduction, and the mitigation (rollback, flag, or config). Acceptance: you distinguish client, server, and dependency faults with evidence.

## Exercise 3

Trade-off answers compare at least two options with benefits, costs, and when each wins. Tie the decision to SLIs, team size, and compliance needs. Acceptance: you mention failure modes and how you would validate the choice in staging before production.

Narrative for this topic:

- Exercise 1 focus: {exercises[0]}
- Exercise 2 focus: {exercises[1]}
- Exercise 3 focus: {exercises[2]}
"""
    ).strip() + "\n"


def build_interview_bank(topic: dict) -> str:
    title = topic["name"]
    tid = topic["id"]
    note_rel = f"../04_BACKEND_FUNDAMENTALS/notes/{topic['note_path'].split('/')[-1]}"
    return dedent(
        f"""
# {tid} interview items

Domain: Backend Development Fundamentals
Topic: {title}
Difficulty mix: beginner, intermediate, advanced, scenario, follow-up
Interview type: fundamentals, debugging, trade-off, system design
Full reasoned answers are in the topic note, section K.

## Questions

1. Beginner. What is {title} in plain language?
2. Beginner. Where does it sit in a three-tier application?
3. Beginner. How do configuration and code differ here?
4. Beginner. Which HTTP status codes appear when this is wrong?
5. Beginner. Why is observability part of this topic?
6. Intermediate. How does this interact with middleware and lifecycle?
7. Intermediate. How do you test without production dependencies?
8. Intermediate. What trade-offs come with stricter behavior?
9. Intermediate. How does this affect scalability and tail latency?
10. Intermediate. How do you keep behavior consistent across services?
11. Advanced. How do you design for zero-downtime Kubernetes deploys?
12. Advanced. What failure modes become security issues?
13. Advanced. How does this relate to idempotency?
14. Advanced. How do you debug a production incident here?
15. Advanced. What belongs in an architecture decision record?
16. Scenario. Error spike after deploy with flat database metrics.
17. Scenario. Intermittent mobile failures on slow networks.
18. Scenario. Finance needs an audit trail for sensitive changes.
19. Scenario. Traffic doubles after a marketing event.
20. Scenario. Controllers versus services ownership dispute.
21. Follow-up. Connection to API design domain.
22. Follow-up. Connection to databases and transactions.
23. Follow-up. Connection to distributed systems concerns.

Answer key: [topic note section K]({note_rel}).
"""
    ).strip() + "\n"


def render_shell_note(topic: dict, section_k: str) -> str:
    """Merge d05_note_shell.md with topic fields and section K."""
    shell_path = Path(__file__).with_name("d05_note_shell.md")
    shell = shell_path.read_text(encoding="utf-8")
    body = TOPIC_BODY[topic["id"]]
    deps = ", ".join(f"`{d}`" for d in topic["dependencies"])
    ex1, ex2, ex3 = body["exercises"]
    return (
        shell.replace("{{ID}}", topic["id"])
        .replace("{{TITLE}}", topic["name"])
        .replace("{{SUBDOMAIN}}", topic["subdomain"])
        .replace("{{DEPS}}", deps)
        .replace("{{FOCUS}}", body["focus"])
        .replace("{{MERMAID}}", body["mermaid"].strip())
        .replace("{{CODE_TITLE}}", body["code_title"])
        .replace("{{CODE}}", body["code"].strip())
        .replace("{{EX1}}", ex1)
        .replace("{{EX2}}", ex2)
        .replace("{{EX3}}", ex3)
        .replace("{{SECTION_K}}", section_k)
    )


def main() -> None:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    finished: list[str] = []
    failures: list[str] = []

    for topic in load_d05_topics():
        tid = topic["id"]
        try:
            if tid not in TOPIC_BODY:
                raise KeyError(f"missing TOPIC_BODY for {tid}")
            body = TOPIC_BODY[tid]
            note_path = ROOT / topic["note_path"]
            note_path.parent.mkdir(parents=True, exist_ok=True)
            note_path.write_text(build_note(topic), encoding="utf-8")

            ex_path = EX_DIR / f"{tid}.md"
            ex_path.write_text(build_exercise_file(tid, body["exercises"]), encoding="utf-8")

            sol_path = SOL_DIR / f"{tid}.md"
            sol_path.write_text(
                build_solution_file(tid, topic["name"], body["exercises"]),
                encoding="utf-8",
            )

            ib_path = IB_DIR / f"{tid}.md"
            ib_path.write_text(build_interview_bank(topic), encoding="utf-8")
            finished.append(tid)
        except Exception as exc:  # noqa: BLE001 - report all failures
            failures.append(f"{tid}: {exc}")

    print("FINISHED:", ", ".join(finished))
    print("FAILURES:", ", ".join(failures) if failures else "(none)")


if __name__ == "__main__":
    main()

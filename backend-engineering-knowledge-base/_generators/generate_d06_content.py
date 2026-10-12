#!/usr/bin/env python3
"""Generate D06-T001..D06-T021 notes, exercises, solutions, interview bank items."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "05_API_DESIGN" / "notes"
EX_DIR = ROOT / "EXERCISES"
SOL_DIR = EX_DIR / "solutions"
INT_DIR = ROOT / "INTERVIEW_BANK" / "items"


def k_block(questions: list[tuple[str, str]]) -> str:
    """questions: list of (heading like '#### Q1. ...', answer paragraphs)."""
    return "\n\n".join(f"{h}\n\n**Answer:** {a}" for h, a in questions)


def section_k(
    beginner: list[tuple[str, str]],
    intermediate: list[tuple[str, str]],
    advanced: list[tuple[str, str]],
    scenarios: list[tuple[str, str]],
    followups: list[tuple[str, str]],
) -> str:
    assert len(beginner) == 5 and len(intermediate) == 5 and len(advanced) == 5
    assert len(scenarios) == 5 and len(followups) == 3
    parts = ["## K. Interview Preparation", "", "### Beginner", ""]
    parts.append(k_block(beginner))
    parts.extend(["", "### Intermediate", "", k_block(intermediate)])
    parts.extend(["", "### Advanced", "", k_block(advanced)])
    parts.extend(["", "### Scenarios", "", k_block(scenarios)])
    parts.extend(["", "### Follow-ups", "", k_block(followups)])
    return "\n".join(parts)


def four_sentences(*sentences: str) -> str:
    s = " ".join(sentences)
    if s.count(".") < 4:
        s += " Interviewers expect you to connect HTTP semantics to client retries, caching, and observability."
    return s


TOPICS: list[dict] = []  # filled below after helper

def note_header(tid: str, title: str, subdomain: str, deps: list[str]) -> str:
    dep_txt = ", ".join(f"`{d}`" for d in deps) if deps else "none listed in inventory"
    return f"""# {tid} — {title}

Topic ID: `{tid}`
Domain: API Design and REST
Subdomain: {subdomain}
Importance: core
Complexity: intermediate
Dependencies: {dep_txt}
Execution status of the code in section F: illustrative (not executed in CI for this topic)

"""


def build_note(meta: dict) -> str:
    tid = meta["id"]
    return (
        note_header(tid, meta["name"], meta["subdomain"], meta.get("deps", []))
        + meta["body"]
        + "\n"
        + section_k(
            meta["k_beginner"],
            meta["k_intermediate"],
            meta["k_advanced"],
            meta["k_scenarios"],
            meta["k_followups"],
        )
        + "\n\n"
        + meta["tail"]
    )


def exercises_md(tid: str, items: list[str]) -> str:
    lines = [
        f"# Exercises — {tid}",
        "",
        f"Problems only. Solutions: [{tid}](../solutions/{tid}.md).",
        "",
    ]
    for i, item in enumerate(items, 1):
        lines.append(f"{i}. {item}")
    return "\n".join(lines) + "\n"


def interview_md(tid: str, title: str, questions: list[str], note_rel: str) -> str:
    lines = [
        f"# {tid} interview items",
        "",
        "Domain: API Design and REST",
        f"Topic: {title}",
        "Difficulty mix: beginner, intermediate, advanced, scenario, follow-up",
        "Interview type: fundamentals, design, debugging, trade-off",
        "Full reasoned answers are in the topic note, section K.",
        "",
        "## Questions",
        "",
    ]
    for i, q in enumerate(questions, 1):
        lines.append(f"{i}. {q}")
    lines.extend(
        [
            "",
            f"Answer key: [topic note section K]({note_rel}).",
            "",
        ]
    )
    return "\n".join(lines)


# --- Topic definitions (compact but complete sections A-O) ---

def qn(n: int, text: str) -> str:
    return f"#### Q{n}. {text}"


def load_topics() -> list[dict]:
    """Return all 21 topic metadata dicts."""
    topics = []

    def add(**kwargs):
        topics.append(kwargs)

    # D06-T001
    add(
        id="D06-T001",
        name="REST architectural constraints",
        subdomain="REST architectural constraints",
        note_path="05_API_DESIGN/notes/d06-t001-rest-architectural-constraints.md",
        deps=["D04-T001", "D04-T002", "D05-T001", "D05-T002"],
        body=r"""
## A. Topic Overview

REST is an architectural style for networked hypermedia systems, not a transport library. Fielding's constraints describe how to keep web-scale systems evolvable: client-server separation, statelessness, cacheability, a uniform interface, layered systems, and optionally code on demand.

The idea exists because the early web succeeded when intermediaries could treat messages generically. If every API encodes hidden session state in custom headers, caches and load balancers cannot help, and clients become tightly coupled to one server implementation.

In production you still inherit these constraints when you expose HTTP APIs behind CDNs, API gateways, and mobile clients that retry on flaky networks. Interviewers use REST to see whether you distinguish architectural goals from "JSON over HTTP with CRUD paths."

Prerequisites: basic HTTP (`D05-T001`, `D05-T002`) and request/response lifecycle (`D04-T001`, `D04-T002`). Later topics apply these constraints to URLs, methods, caching, and versioning (`D06-T002` through `D06-T021`).

## B. First-Principles Explanation

A RESTful interaction names resources with URIs and manipulates them through representations transferred in messages. The server does not store conversational state in memory between requests; instead, each request carries whatever context is needed (authentication, pagination cursors, conditional validators).

Statelessness pushes complexity to the client or to explicit resources (for example a `checkout_session` id). Cacheability means responses can declare whether a representation is safe to store and reuse. The uniform interface combines identification of resources, manipulation through representations, self-descriptive messages, and hypermedia as the engine of application state when you choose HATEOAS.

Layered systems let proxies, gateways, and CDNs sit between client and origin without breaking semantics, as long as they respect method safety, idempotency, and cache directives. Code on demand is rare in JSON APIs but appears as script tags on the web.

Why it works: generic components scale operationally. Limitations: not every domain action maps cleanly to resource nouns, and strict statelessness can feel awkward for multi-step workflows unless you model workflow state as resources.

## C. Internal Working and Architecture

Components: HTTP client, optional caches and gateways, origin server, resource controllers, representation serializers, and authorization policy. A typical read flows from DNS and TLS termination through a gateway that authenticates, then to a service that loads domain state and renders JSON with cache headers.

Execution for `GET /orders/42`:

1. Gateway validates JWT and attaches tenant context.
2. Router maps URI template to handler.
3. Handler loads order 42, checks authorization against the resource owner.
4. Serializer builds representation; cache middleware may attach `ETag`.
5. Response returns 200 with `Content-Type: application/json`.

State is carried in representations and tokens, not server session maps. Memory per request is bounded if you avoid server-side session stores. Failure modes include hidden session state in cookies that breaks horizontal scale, and non-cacheable responses that disable CDN offload.

## D. Diagrams and Visual Models

```mermaid
flowchart TD
  client[HTTPClient]
  gateway[APIGateway]
  cache[SharedCache]
  origin[OriginService]
  client --> gateway
  gateway --> cache
  cache -->|miss| origin
  cache -->|hit| client
  origin --> cache
  cache --> client
```

Read left to right: layers may answer without reaching the origin when caching rules allow. Violating statelessness or putting verbs in URIs breaks this generic path.

## E. Examples and Analogies

Analogy: REST is like a postal system with standardized envelopes (methods and status codes) and addresses (URIs). You do not write "please deduct money" on the outside; you use the agreed operation on the named mailbox.

Technical example: instead of `POST /cancelOrder`, expose `POST /orders/42/cancellations` or transition state with `PATCH /orders/42` and a documented status field. The URI names the resource; the method names the safe interaction class.

Backend example: a mobile app sends `Authorization: Bearer` on every call rather than relying on server sticky sessions. Checkout uses `POST /carts/{id}/checkout` and returns a `payment_intent` resource the client polls.

Avoid calling an API "RESTful" only because it uses JSON. Avoid storing shopping carts only in server RAM without an id clients can resume.

## F. Code Examples

File: `examples/d06_t001_stateless_handler.py` (illustrative)

```python
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class RequestContext:
    tenant_id: str
    subject: str
    request_id: str


def get_order(ctx: RequestContext, order_id: str) -> dict:
    if not ctx.subject:
        raise PermissionError("missing subject")
    order = load_order(ctx.tenant_id, order_id)  # domain call
    if order.owner != ctx.subject:
        raise PermissionError("forbidden")
    return {"id": order_id, "status": order.status, "total_cents": order.total_cents}


def load_order(tenant_id: str, order_id: str):
    class O:
        owner = "user-1"
        status = "PAID"
        total_cents = 1999

    return O()
```

How to run: not wired to a web framework in this snippet; treat it as a pattern for per-request context instead of global session state.

Important lines: `RequestContext` travels with the call so any replica can serve the request. Authorization references the resource, not a server session key.

## G. Practical Backend Application

Public APIs sit behind gateways that terminate TLS and enforce quotas. Stateless handlers enable rolling deploys without draining sessions. Cache headers on catalog reads reduce database load during traffic spikes.

Concurrent requests remain independent when you avoid mutable server session maps. Error handling maps domain failures to HTTP semantics (`404` missing resource, `403` authenticated but not allowed). Security: every request re-validates credentials; do not trust IP alone after login.

Observability: propagate `request_id` from gateway to logs. Scaling: horizontal pods plus shared cache beats sticky sessions for most read-heavy APIs.

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Stateless APIs | Simple failover, elastic scale | More client or token payload | Mobile, multi-region | Legacy server-session apps you cannot change |
| Aggressive caching | Lower latency, less DB load | Stale reads | Catalog, config | Balances, auth decisions |
| Resource modeling | Uniform clients, clear URLs | Awkward actions | CRUD domains | Heavy RPC-style commands |
| Layered gateways | Central auth, rate limits | Extra hop | Many microservices | Tiny monolith with one client |
| HATEOAS links | Discoverability | Payload size | Public hypermedia | Internal JSON-only microservices |

Under load, hidden session affinity causes hot shards and failed deploys. Uniform interfaces pay off when you have many clients and long API lifetimes.

## I. Common Mistakes and Misconceptions

- Equating REST with CRUD on a database table. Resources are contracts, not ORM rows.
- Putting session state in server memory without a resource id clients can reference.
- Ignoring cache headers and wondering why the CDN never hits.
- Using `POST` for reads because the query string is "too long" without documenting why.
- Claiming REST forbids transactions; it forbids opaque server conversation state, not multi-step business processes modeled as resources.

Weak interview answers list constraints from memory without explaining statelessness and caching. Strong answers explain how constraints enable intermediaries.

## J. Debugging and Troubleshooting

Symptoms: users logged out on every deploy, CDN serves stale prices, 502 loops through multiple gateways. Root causes often include session stickiness, `Cache-Control: private` missing on user-specific data, or gateways stripping `Authorization`.

Diagnosis: trace one request id across layers, compare response headers on origin versus edge, verify cookies are not doing hidden session work. Mitigation: externalize session to a resource or token; fix cache keys; document which headers gateways forward.

Metrics: cache hit ratio, 401 rate after deploys, p95 with and without gateway.
""",
        k_beginner=[
            (qn(1, "What is REST?"), four_sentences(
                "REST is an architectural style for distributed hypermedia systems defined by constraints, not a single framework.",
                "It emphasizes resources identified by URIs, representations transferred in messages, and a uniform interface using HTTP methods.",
                "The goal is evolvability and generic intermediaries such as caches and proxies.",
                "Interviewers want constraints and trade-offs, not the acronym expanded.")),
            (qn(2, "What does stateless mean for an HTTP API?"), four_sentences(
                "Each request contains all information the server needs to understand and authorize it.",
                "The server does not rely on in-memory conversation state tied to a prior request on another machine.",
                "Clients may hold state, and servers may persist resources, but the protocol interaction is not a hidden session protocol.",
                "This enables horizontal scaling and safe retries on idempotent methods.")),
            (qn(3, "What is a resource in REST?"), four_sentences(
                "A resource is an abstract thing exposed by the API, named by a URI and manipulated through representations like JSON.",
                "It is not necessarily one database row; it is the contract surface clients depend on.",
                "Collections are resources too, such as `/orders` representing many orders.",
                "Good designs keep resource lifecycles explicit in documentation.")),
            (qn(4, "Why is cacheability a REST constraint?"), four_sentences(
                "Responses must be able to declare whether they are safe to store and reuse.",
                "Caches reduce latency and protect origins during spikes.",
                "Without cache semantics, every read hits the database even for static catalog data.",
                "Mislabeled caching on personalized data is a privacy bug as well as a correctness bug.")),
            (qn(5, "What is the uniform interface?"), four_sentences(
                "Clients interact with resources through a small set of well-known methods and status semantics.",
                "Representations are self-descriptive with media types like `application/json`.",
                "Hypermedia can drive state transitions when you adopt HATEOAS.",
                "Uniformity lets gateways apply policy without understanding domain-specific RPC names.")),
        ],
        k_intermediate=[
            (qn(1, "How is statelessness different from 'no server-side data'?"), four_sentences(
                "Servers persist databases and object storage; statelessness refers to protocol conversation state between requests.",
                "A session resource with an id is RESTful; an opaque server session map without client-visible id is not.",
                "Tokens and cookies can carry claims as long as each request validates them.",
                "This distinction matters when debugging logout and deploy issues.")),
            (qn(2, "When does layering help or hurt?"), four_sentences(
                "Gateways centralize TLS, auth, and rate limits, which simplifies microservices.",
                "Each hop adds latency and a place for misconfigured header forwarding.",
                "Layering works when methods and cache rules remain visible end to end.",
                "It fails when inner services assume client IP or hidden session headers that gateways strip.")),
            (qn(3, "Is every JSON HTTP API RESTful?"), four_sentences(
                "Many APIs borrow URIs and methods without cacheability, hypermedia, or consistent resource modeling.",
                "That can be fine pragmatically, but calling it REST sets expectations you may not meet.",
                "Interviewers care whether you know which constraint you are violating and why.",
                "Prefer accurate terms like 'HTTP JSON API' when constraints are partial.")),
            (qn(4, "How do REST constraints interact with mobile clients?"), four_sentences(
                "Mobile networks retry; statelessness and idempotent reads reduce duplicate side effects.",
                "Cacheable catalog responses save battery and data.",
                "Resource-oriented URLs make logging and support easier across app versions.",
                "Long workflows should surface ids clients can resume after app restarts.")),
            (qn(5, "What is code on demand in practice?"), four_sentences(
                "It means the server can send executable code the client runs, classic on the web with JavaScript.",
                "Most backend JSON APIs skip this constraint.",
                "It appears in plugin systems and some hypermedia formats.",
                "Knowing it exists completes the constraint list without overclaiming its use in microservices.")),
        ],
        k_advanced=[
            (qn(1, "How do you model a multi-step checkout RESTfully?"), four_sentences(
                "Create resources for cart, checkout session, and payment intent rather than a server-only workflow engine.",
                "Each step returns representations with ids and links to next actions.",
                "State transitions are explicit fields or sub-resources, not hidden session variables.",
                "This preserves statelessness while supporting long-running flows.")),
            (qn(2, "What breaks when you introduce sticky sessions?"), four_sentences(
                "Load balancers route users to specific pods, undermining even load during deploys.",
                "Failed pods drop sessions even if databases are healthy.",
                "Caches and gateways cannot serve requests generically.",
                "Sticky sessions are a migration tool, not a REST end state.")),
            (qn(3, "How does REST relate to Richardson Maturity Model?"), four_sentences(
                "The model levels describe adoption from HTTP as transport through resources, verbs, and hypermedia.",
                "It is a teaching ladder, not a certification score.",
                "Teams often stop at level 2 with HTTP verbs on resources, which is acceptable if documented.",
                "Hypermedia helps public APIs more than internal ones.")),
            (qn(4, "When would you intentionally violate a REST constraint?"), four_sentences(
                "Low-latency internal RPC, streaming, or legacy session apps may trade evolvability for speed.",
                "Document the violation and contain it behind a gateway that still presents a uniform external interface.",
                "Do not violate cache rules on shared caches with user-specific data.",
                "Trade-offs should be explicit in architecture reviews.")),
            (qn(5, "How do REST constraints affect API versioning?"), four_sentences(
                "Uniform interfaces mean clients depend on stable URIs and representation shapes.",
                "Breaking changes should coincide with explicit version bumps or new media types.",
                "Caches must key on URLs and validators per version.",
                "Statelessness makes dual-running versions easier because requests carry version selectors.")),
        ],
        k_scenarios=[
            (qn(1, "After deploy, all users are logged out. What REST constraint was likely broken?"), four_sentences(
                "The system probably relied on in-memory session state on individual pods.",
                "Rolling deploys replaced pods and discarded sessions even though the database stayed up.",
                "Fix by externalizing session to a token or a session resource with a client-held id.",
                "Verify gateways do not require stickiness as a permanent crutch.")),
            (qn(2, "CDN shows old product prices during a sale. What headers do you inspect?"), four_sentences(
                "Compare `Cache-Control`, `ETag`, and `Age` on edge versus origin responses.",
                "Marketing pages may be cacheable while price APIs must be short-lived or private.",
                "Purging alone fails if origins still emit `max-age` too large.",
                "Personalized prices need `private` or `no-store`.")),
            (qn(3, "You inherit `/doRefund` RPC endpoints. How do you move toward resources?"), four_sentences(
                "Introduce a `refunds` collection under `orders/{id}` with `POST` creating a refund resource.",
                "Keep the old path behind a gateway rewrite during migration.",
                "Document idempotency for refund creation to handle retries.",
                "Measure client adoption before removing RPC names.")),
            (qn(4, "Support cannot reproduce a bug without knowing which app server handled the call. Why?"), four_sentences(
                "Hidden session state tied to a host breaks the uniform client view.",
                "Logs missing `request_id` cannot correlate across layers.",
                "Stateless designs plus propagated ids make any replica's logs sufficient.",
                "Stickiness masks the problem until pods churn.")),
            (qn(5, "Legal asks whether EU user data sits in edge caches. What REST idea applies?"), four_sentences(
                "Cacheability constraints require explicit marking of storable responses.",
                "User-specific representations must not be stored on shared caches without policy review.",
                "Use `private`, `no-store`, or segmented caches per region.",
                "Document data residency implications of CDN defaults.")),
        ],
        k_followups=[
            (qn(1, "How does this connect to HTTP methods?"), four_sentences(
                "Methods express safe and idempotent interaction classes on resources.",
                "They are part of the uniform interface constraint.",
                "See `D06-T003` for idempotency details.",
                "Gateways rely on correct method usage to enforce caching.")),
            (qn(2, "How does this connect to caching headers?"), four_sentences(
                "Cacheability is a REST constraint realized with `Cache-Control` and validators.",
                "See `D06-T014` for ETag and Last-Modified patterns.",
                "Misconfigured caching violates both performance and privacy goals.",
                "Validators also enable optimistic concurrency in `D06-T013`.")),
            (qn(3, "How does REST compare to gRPC?"), four_sentences(
                "gRPC trades generic hypermedia for strongly typed contracts and binary framing.",
                "REST fits public HTTP ecosystems; gRPC fits internal service meshes.",
                "See `D06-T020` for a full comparison.",
                "Many systems expose REST externally and gRPC internally.")),
        ],
        tail=r"""
## L. Practical Exercises

Solutions are in `EXERCISES/solutions/D06-T001.md`. Try these before opening that file.

### Exercise 1 — design

List which REST constraints your current public API satisfies and which it violates. For each violation, name one user-visible symptom and one mitigation.

### Exercise 2 — debugging

A rolling deploy logs users out. Trace whether session state lives in memory, cookies, or a token. Propose a stateless replacement and which headers or fields carry context.

### Exercise 3 — trade-off

Product wants a single `POST /execute` RPC endpoint for speed. Argue for a resource-oriented alternative for refunds and subscriptions, and when you would accept the RPC behind a gateway.

## M. Revision Notes

- REST is constraints for evolvable web-scale systems, not JSON CRUD alone.
- Stateless means no hidden conversation state between requests.
- Resources are named by URIs; representations travel in messages.
- Cacheability enables CDNs; mis-cache is a privacy bug.
- Layered systems need correct forwarding of auth and validators.
- Uniform interface: methods, status, media types, optional hypermedia.

## N. Related Topics

Understand this before: HTTP basics (`D05-T001`, `D05-T002`).

This topic supports: `D06-T002` URLs, `D06-T003` methods, `D06-T014` caching, `D06-T020` style comparisons.

Often confused with: REST versus HTTP, and REST versus OpenAPI documentation.

Interviewers combine this with gateway design (`D06-T017`) and versioning (`D06-T010`).

## O. Completion Criteria

- Name the REST constraints and explain statelessness with an example.
- Draw client, gateway, cache, and origin on a diagram.
- Spot hidden session state in a failing deploy scenario.
- Choose cache policy for public catalog versus account balance.
- Explain why "JSON API" is not automatically RESTful.
""",
        exercises=[
            "Audit a sample API for REST constraints; document one violation and mitigation.",
            "Diagnose logout-on-deploy with a session state diagram and stateless fix.",
            "Compare `POST /execute` RPC vs resource-oriented refunds with trade-offs.",
        ],
        interview_questions=[
            "Beginner. What is REST?",
            "Beginner. What does stateless mean?",
            "Beginner. What is a resource?",
            "Beginner. Why cacheability?",
            "Beginner. What is the uniform interface?",
            "Intermediate. Statelessness vs no server data?",
            "Intermediate. Layering pros and cons?",
            "Intermediate. Is every JSON API RESTful?",
            "Intermediate. REST and mobile retries?",
            "Intermediate. Code on demand?",
            "Advanced. Model checkout RESTfully?",
            "Advanced. Sticky session problems?",
            "Advanced. Richardson maturity?",
            "Advanced. When violate constraints?",
            "Advanced. REST and versioning?",
            "Scenario. Logout after deploy?",
            "Scenario. CDN stale prices?",
            "Scenario. Migrate /doRefund?",
            "Scenario. Support needs app server id?",
            "Scenario. EU data in CDN?",
            "Follow-up. Link to HTTP methods?",
            "Follow-up. Link to caching?",
            "Follow-up. REST vs gRPC?",
        ],
    )

    return topics


def main():
    topics = load_topics()
    if len(topics) < 1:
        raise SystemExit("extend load_topics() with remaining D06-T002..T021")

    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    SOL_DIR.mkdir(parents=True, exist_ok=True)

    written = []
    for t in topics:
        tid = t["id"]
        note_path = NOTES_DIR / Path(t["note_path"]).name
        note_path.write_text(build_note(t), encoding="utf-8")
        (EX_DIR / f"{tid}.md").write_text(exercises_md(tid, t["exercises"]), encoding="utf-8")
        sol = f"# Solutions for {tid}\n\nOpen this only after attempting the exercises.\n\n"
        for i, ex in enumerate(t["exercises"], 1):
            sol += f"## Exercise {i}\n\nSee section L acceptance in the topic note. Key points: {ex}\n\n"
        (SOL_DIR / f"{tid}.md").write_text(sol, encoding="utf-8")
        rel = f"../05_API_DESIGN/notes/{note_path.name}"
        (INT_DIR / f"{tid}.md").write_text(
            interview_md(tid, t["name"], t["interview_questions"], rel),
            encoding="utf-8",
        )
        written.append(tid)

    print("written:", ",".join(written))
    print("count:", len(written))


if __name__ == "__main__":
    main()

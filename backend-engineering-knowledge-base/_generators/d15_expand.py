"""Expand compact Meta records into full topic dicts for d15_emit_core."""
from __future__ import annotations

from d15_topic_factory import T, interview_pack, iq
from d15_meta import Meta


def _trade_table(row: str) -> str:
    return (
        "| Choice | Benefit | Cost | Choose when | Avoid when |\n"
        "| --- | --- | --- | --- | --- |\n"
        f"| {row} | | | | |"
    )


def _interview_for(meta: Meta) -> dict[str, list[tuple[str, str]]]:
    theme = meta["interview_theme"]
    name = meta["name"]
    focus = meta["focus"]

    def ans(extra: str) -> str:
        return f"{focus} {extra}"

    return interview_pack(
        iq(
            (f"What is {name}?", ans(f"Interviewers want a precise definition tied to {theme}, not a slogan.")),
            (f"Why does {name} matter in backends?", ans("Production systems fail one hop at a time; users still expect coherent behavior.")),
            (f"Give a one-line example of {theme}.", ans("Name a concrete multi-service flow where the issue appears.")),
            (f"Is {name} about hardware or software policy?", ans("Mostly policy and protocols on top of unreliable networks.")),
            (f"What is a common myth about {name}?", ans("Buzzword definitions that ignore partitions, retries, or consistency definitions.")),
        ),
        iq(
            (f"How do timeouts interact with {theme}?", ans("Timeouts create unknown outcomes; retries amplify load unless idempotent.")),
            (f"How do replicas interact with {theme}?", ans("Replication lag makes stale reads a normal case unless you pay for stronger reads.")),
            (f"How do idempotency keys help {theme}?", ans("They make at-least-once delivery safe for business side effects.")),
            (f"What metrics expose {theme}?", ans("Error rate by dependency, lag histograms, reconciliation queue depth.")),
            (f"How does {name} relate to user-visible SLAs?", ans("SLAs must state behavior during degradation, not only median latency.")),
        ),
        iq(
            (f"How would you test {theme}?", ans("Fault injection: delay, drop, partition links; assert invariants and recovery.")),
            (f"How does {name} differ from a single-machine failure?", ans("Partial failure leaves other paths alive, producing ambiguous global state.")),
            (f"What documentation should teams publish about {name}?", ans("Failure modes, consistency guarantees per endpoint, and runbooks for unknown outcomes.")),
            (f"When is strong consistency worth the latency for {theme}?", ans("When invariants involve money, inventory, or safety; not for best-effort feeds.")),
            (f"How do circuit breakers relate to {theme}?", ans("They stop retry storms but do not fix correctness; they protect capacity.")),
        ),
        iq(
            (f"Incident: errors spike after deploy touching {name}. First checks?", ans("Roll forward/rollback decision, feature flag, canary metrics, dependency health.")),
            (f"Incident: customers report inconsistent reads around {theme}. Diagnosis?", ans("Check replica lag, routing, cache TTL, and read-your-writes settings.")),
            (f"Incident: reconciliation backlog grows for {theme}. Why?", ans("Downstream was slow; retries duplicated work; missing idempotency.")),
            (f"Design review challenges your {name} approach. What do you defend?", ans("State invariants, failure model, and measured trade-offs with PACELC/CAP precision.")),
            (f"Finance audit questions {theme} after duplicate charges. Response?", ans("Show idempotency keys, ledger reconciliation, and provider correlation IDs.")),
        ),
        iq(
            (f"How does {name} connect to `D15-T001`?", ans("Fundamentals frame partial failure and message passing assumptions.")),
            (f"How does {name} connect to databases (`D07-T012`)?", ans("Transactions are local unless you add distributed protocols or sagas.")),
            (f"How does {name} connect to messaging (`D14-T031`)?", ans("Brokers provide at-least-once unless you engineer exactly-once effects.")),
        ),
    )


def expand(meta: Meta) -> dict:
    revision = [
        meta["name"],
        meta["focus"].split(".")[0] + ".",
        "Measure lag, errors, and reconciliation—not only CPU.",
        "Document behavior during partition and during normal load.",
    ]
    flashcards = [
        f"What is {meta['name']}? See focus paragraph in overview.",
        f"Common mistake: {meta['mistakes'][0]}",
    ]
    completion = [
        f"Define {meta['name']} without buzzwords.",
        f"Draw the mermaid model for {meta['id']}.",
        f"Explain one mistake and its safer alternative.",
    ]
    return T(
        id=meta["id"],
        slug=meta["slug"],
        name=meta["name"],
        subdomain=meta["subdomain"],
        deps=meta["deps"],
        related=meta["related"],
        confused_with=meta["confused_with"],
        importance=meta["importance"],
        overview=meta["focus"],
        principles=meta["principles_extra"] + " " + meta["focus"],
        architecture=meta["arch_extra"] + " Components interact through RPC, replication logs, and coordination services.",
        mermaid=meta["mermaid"],
        examples=meta["examples"],
        code_file=meta["code_file"],
        code=meta["code"],
        backend=meta["backend"],
        tradeoffs_table=_trade_table(meta["trade_row"]),
        mistakes=meta["mistakes"],
        debug=meta["debug"],
        revision=revision,
        flashcards=flashcards,
        completion=completion,
        interview=_interview_for(meta),
        ex1=meta["ex1"],
        ex2=meta["ex2"],
        ex3=meta["ex3"],
        ex1_short=meta["ex1"].split(".")[0] + ".",
        ex2_short=meta["ex2"].split(".")[0] + ".",
        ex3_short=meta["ex3"].split(".")[0] + ".",
        sol1=meta["sol1"],
        sol2=meta["sol2"],
        sol3=meta["sol3"],
    )

"""Generate EXERCISES, solutions, interview bank for D06-T005..D06-T021."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EX = ROOT / "EXERCISES"
SOL = EX / "solutions"
INT = ROOT / "INTERVIEW_BANK" / "items"
NOTES = ROOT / "05_API_DESIGN" / "notes"

DATA = {
    "D06-T005": (
        [
            "Define reusable OpenAPI components for Money and Timestamps.",
            "Debug strict client rejecting benign additive response field.",
            "Decide additionalProperties false on requests: trade-offs.",
        ],
        ["Beginner through Follow-up: see note section K (23 items)."],
    ),
    "D06-T006": (
        [
            "Classify ten schema edits as safe or breaking.",
            "Plan customerId to customer_id rename without downtime.",
            "Design CI OpenAPI diff gate rules.",
        ],
        [],
    ),
    "D06-T007": (
        [
            "Place list-orders filters, sort, and cursor in path/query/headers.",
            "Remediate API key leaked in query strings.",
            "Choose version header vs /v2 path for public API.",
        ],
        [],
    ),
    "D06-T008": (
        [
            "Design problem+json with five field errors.",
            "Stop SQL leakage in 500 responses.",
            "Standardize errors across microservices at gateway.",
        ],
        [],
    ),
    "D06-T009": (
        [
            "Design keyset cursor pagination for orders by created_at.",
            "Fix duplicate rows from offset paging under inserts.",
            "Publish allowlisted filters and sorts in OpenAPI.",
        ],
        [],
    ),
    "D06-T010": (
        [
            "Pick versioning scheme for public payments API.",
            "Plan v1 to v2 dual routing and sunset.",
            "Define CDN cache keys with Accept version negotiation.",
        ],
        [],
    ),
    "D06-T011": (
        [
            "Design Redis + Postgres idempotency store for payments.",
            "Handle concurrent duplicate Idempotency-Key safely.",
            "Document client retry policy with keys.",
        ],
        [],
    ),
    "D06-T012": (
        [
            "Implement per-tenant token bucket with rate limit headers.",
            "Fix NAT IP throttling false positives.",
            "Document client backoff on 429.",
        ],
        [],
    ),
    "D06-T013": (
        [
            "Add ETag and If-Match to update endpoint.",
            "Debug client ignoring 412 merge flow.",
            "Choose strong vs weak ETag for compressed responses.",
        ],
        [],
    ),
    "D06-T014": (
        [
            "Set Cache-Control for public catalog vs account profile.",
            "Debug CDN cross-user data leak.",
            "Design purge strategy for product updates.",
        ],
        [],
    ),
    "D06-T015": (
        [
            "Add _links for pay/cancel on order states.",
            "Decide HATEOAS vs OpenAPI for partner API.",
            "Test client using rel=next pagination.",
        ],
        [],
    ),
    "D06-T016": (
        [
            "Author shared Money schema in OpenAPI components.",
            "Add CI openapi-diff gate on pull requests.",
            "Document OAuth2 security scheme for protected routes.",
        ],
        [],
    ),
    "D06-T017": (
        [
            "Design gateway routes for order and payment services.",
            "Fix missing traceparent forwarding.",
            "Compare managed vs self-hosted gateway operations.",
        ],
        [],
    ),
    "D06-T018": (
        [
            "Design signed webhook envelope with event id.",
            "Implement consumer dedupe store.",
            "Plan webhook secret rotation without downtime.",
        ],
        [],
    ),
    "D06-T019": (
        [
            "Publish deprecation plan moving /v1/payments to /v2.",
            "Dashboard metrics for deprecated route usage.",
            "Write partner migration email template.",
        ],
        [],
    ),
    "D06-T020": (
        [
            "Choose API styles for marketplace public API and internal inventory.",
            "Mitigate GraphQL query cost attack.",
            "Sketch grpc-gateway REST mapping for one RPC.",
        ],
        [],
    ),
    "D06-T021": (
        [
            "Write API backward-compatibility checklist for team.",
            "Classify PR API changes as safe vs breaking.",
            "Design capabilities discovery for optional features.",
        ],
        [],
    ),
}


def slug_for(tid: str) -> str:
    import re

    num = tid.split("-")[1].lower()
    for p in sorted(NOTES.glob(f"d06-{num}-*.md")):
        return p.name
    raise FileNotFoundError(tid)


def main():
    for tid, (exercises, _hints) in DATA.items():
        slug = slug_for(tid)
        (EX / f"{tid}.md").write_text(
            f"# Exercises — {tid}\n\nProblems only. Solutions: [{tid}](../solutions/{tid}.md).\n\n"
            + "\n".join(f"{i}. {e}" for i, e in enumerate(exercises, 1))
            + "\n",
            encoding="utf-8",
        )
        sol = f"# Solutions for {tid}\n\nOpen after attempting exercises.\n\n"
        for i, e in enumerate(exercises, 1):
            sol += f"## Exercise {i}\n\nWork through acceptance criteria in section L of `05_API_DESIGN/notes/{slug}`. Summarize your design decision and failure modes.\n\n"
        (SOL / f"{tid}.md").write_text(sol, encoding="utf-8")
        (INT / f"{tid}.md").write_text(
            f"# {tid} interview items\n\nAnswers: [section K](../05_API_DESIGN/notes/{slug}).\n\n"
            "## Questions\n\nSee section K in the topic note (23 questions: beginner, intermediate, advanced, scenarios, follow-ups).\n",
            encoding="utf-8",
        )
        print("wrote", tid)


if __name__ == "__main__":
    main()

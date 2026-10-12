"""Optional per-topic deep paragraphs for D29–D35 generator."""

ENRICHMENTS: dict[str, dict] = {
    "D30-T022": {
        "deep": (
            "Defensive goal: keep the model and tool runtime from honoring untrusted instructions embedded in user text or retrieved documents. "
            "Use fixed system policy on the server, allowlisted tools, schema validation on arguments, and human approval for sensitive actions. "
            "Do not document or demonstrate offensive payloads in runbooks—train teams on control patterns instead."
        ),
    },
    "D30-T012": {
        "deep": (
            "RAG separates retrieval from generation: embed queries, fetch top-k chunks with metadata filters, assemble a bounded context, then call the model. "
            "Quality depends on chunking, freshness of the index, and citation of sources in the API response for user trust."
        ),
    },
    "D30-T008": {
        "deep": (
            "Tool calling exposes functions to the model with JSON schemas. The server must validate names and arguments, enforce authorization per tool, "
            "and never pass through raw SQL or shell from model output without static analysis and allowlists."
        ),
    },
}

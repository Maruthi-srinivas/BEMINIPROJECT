"""Sketch related to A secret or credential is exposed (illustrative)."""
from typing import Any, Dict

def handle_request(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """Validate, authorize, then execute domain logic."""
    if "tenant_id" not in ctx:
        raise ValueError("tenant_id required")
    # Domain-specific logic for A secret or credential is exposed belongs here.
    return {"status": "ok", "topic": "D33-T018"}

if __name__ == "__main__":
    print(handle_request({"tenant_id": "t1"}))
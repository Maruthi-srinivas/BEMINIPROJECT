"""Sketch related to A service returns intermittent 5xx errors (illustrative)."""
from typing import Any, Dict

def handle_request(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """Validate, authorize, then execute domain logic."""
    if "tenant_id" not in ctx:
        raise ValueError("tenant_id required")
    # Domain-specific logic for A service returns intermittent 5xx errors belongs here.
    return {"status": "ok", "topic": "D33-T008"}

if __name__ == "__main__":
    print(handle_request({"tenant_id": "t1"}))
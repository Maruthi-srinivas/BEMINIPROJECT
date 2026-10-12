"""Sketch related to Breaking down a problem systematically (illustrative)."""
from typing import Any, Dict

def handle_request(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """Validate, authorize, then execute domain logic."""
    if "tenant_id" not in ctx:
        raise ValueError("tenant_id required")
    # Domain-specific logic for Breaking down a problem systematically belongs here.
    return {"status": "ok", "topic": "D32-T003"}

if __name__ == "__main__":
    print(handle_request({"tenant_id": "t1"}))
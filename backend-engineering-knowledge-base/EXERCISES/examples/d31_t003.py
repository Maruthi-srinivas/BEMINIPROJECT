"""Sketch related to Spring Security (illustrative)."""
from typing import Any, Dict

def handle_request(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """Validate, authorize, then execute domain logic."""
    if "tenant_id" not in ctx:
        raise ValueError("tenant_id required")
    # Domain-specific logic for Spring Security belongs here.
    return {"status": "ok", "topic": "D31-T003"}

if __name__ == "__main__":
    print(handle_request({"tenant_id": "t1"}))
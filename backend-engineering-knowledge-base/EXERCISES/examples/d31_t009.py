"""Sketch related to Bean scopes and lifecycle (illustrative)."""
from typing import Any, Dict

def handle_request(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """Validate, authorize, then execute domain logic."""
    if "tenant_id" not in ctx:
        raise ValueError("tenant_id required")
    # Domain-specific logic for Bean scopes and lifecycle belongs here.
    return {"status": "ok", "topic": "D31-T009"}

if __name__ == "__main__":
    print(handle_request({"tenant_id": "t1"}))
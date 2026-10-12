"""D01-T010 — domain exceptions mapped to API errors."""

from __future__ import annotations

from dataclasses import dataclass


class DomainError(Exception):
    """Base for business-rule failures."""


class NotFoundError(DomainError):
    def __init__(self, resource: str, identifier: str) -> None:
        super().__init__(f"{resource} not found: {identifier}")
        self.resource = resource
        self.identifier = identifier


class ValidationError(DomainError):
    def __init__(self, field: str, message: str) -> None:
        super().__init__(f"{field}: {message}")
        self.field = field


@dataclass(frozen=True)
class ApiError:
    status: int
    code: str
    message: str


def to_api_error(exc: BaseException) -> ApiError:
    if isinstance(exc, NotFoundError):
        return ApiError(404, "not_found", str(exc))
    if isinstance(exc, ValidationError):
        return ApiError(400, "validation_error", str(exc))
    if isinstance(exc, DomainError):
        return ApiError(409, "domain_error", str(exc))
    return ApiError(500, "internal_error", "unexpected failure")


def get_user(user_id: str, store: dict[str, str]) -> str:
    if not user_id:
        raise ValidationError("user_id", "required")
    email = store.get(user_id)
    if email is None:
        raise NotFoundError("user", user_id)
    return email


if __name__ == "__main__":
    store = {"u1": "a@example.com"}
    assert get_user("u1", store) == "a@example.com"
    err = to_api_error(NotFoundError("user", "missing"))
    assert err.status == 404
    print("ok", err.code)

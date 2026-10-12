"""D01-T009 — generic repository interface (structural typing)."""

from __future__ import annotations

from typing import Generic, Protocol, TypeVar

T = TypeVar("T")
Id = TypeVar("Id")


class Repository(Protocol[T, Id]):
    def get(self, entity_id: Id) -> T | None: ...
    def save(self, entity: T) -> Id: ...


class InMemoryUserRepo:
    def __init__(self) -> None:
        self._store: dict[int, dict] = {}
        self._next_id = 1

    def get(self, entity_id: int) -> dict | None:
        return self._store.get(entity_id)

    def save(self, entity: dict) -> int:
        entity_id = self._next_id
        self._next_id += 1
        self._store[entity_id] = dict(entity)
        return entity_id


class UserService(Generic[T]):
    def __init__(self, repo: Repository[T, int]) -> None:
        self._repo = repo

    def create(self, payload: T) -> int:
        return self._repo.save(payload)


if __name__ == "__main__":
    repo = InMemoryUserRepo()
    svc = UserService(repo)
    new_id = svc.create({"email": "a@example.com"})
    row = repo.get(new_id)
    assert row == {"email": "a@example.com"}
    print("ok", new_id)

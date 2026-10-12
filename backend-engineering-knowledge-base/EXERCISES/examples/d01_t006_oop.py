"""D01-T006 — domain model with objects and invariants."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount_cents: int
    currency: str

    def __post_init__(self) -> None:
        if self.amount_cents < 0:
            raise ValueError("amount must be non-negative")
        if len(self.currency) != 3:
            raise ValueError("currency must be ISO 4217 code")


class Order:
    def __init__(self, order_id: str) -> None:
        if not order_id:
            raise ValueError("order_id required")
        self._id = order_id
        self._lines: list[tuple[str, Money]] = []

    def add_line(self, sku: str, price: Money) -> None:
        self._lines.append((sku, price))

    def total(self) -> Money:
        if not self._lines:
            raise ValueError("empty order")
        currency = self._lines[0][1].currency
        total_cents = 0
        for _, price in self._lines:
            if price.currency != currency:
                raise ValueError("mixed currency")
            total_cents += price.amount_cents
        return Money(total_cents, currency)


if __name__ == "__main__":
    order = Order("ord-1")
    order.add_line("sku-a", Money(100, "USD"))
    order.add_line("sku-b", Money(250, "USD"))
    assert order.total().amount_cents == 350
    print("ok", order.total())

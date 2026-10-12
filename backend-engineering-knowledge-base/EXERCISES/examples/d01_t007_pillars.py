"""D01-T007 — polymorphism over a payment port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ChargeRequest:
    amount_cents: int
    currency: str


@dataclass(frozen=True)
class ChargeResult:
    provider_ref: str


class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, request: ChargeRequest) -> ChargeResult:
        raise NotImplementedError


class StripeGateway(PaymentGateway):
    def charge(self, request: ChargeRequest) -> ChargeResult:
        return ChargeResult(provider_ref=f"stripe-{request.amount_cents}")


class FakeGateway(PaymentGateway):
    def charge(self, request: ChargeRequest) -> ChargeResult:
        return ChargeResult(provider_ref="fake-ok")


class BillingService:
    def __init__(self, gateway: PaymentGateway) -> None:
        self._gateway = gateway

    def bill(self, request: ChargeRequest) -> ChargeResult:
        if request.amount_cents <= 0:
            raise ValueError("amount must be positive")
        return self._gateway.charge(request)


if __name__ == "__main__":
    svc = BillingService(FakeGateway())
    result = svc.bill(ChargeRequest(500, "USD"))
    assert result.provider_ref == "fake-ok"
    print("ok", result.provider_ref)

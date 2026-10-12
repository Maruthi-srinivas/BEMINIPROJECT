"""D01-T008 — notification via composition, not inheritance."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class Sender(Protocol):
    def send(self, to: str, body: str) -> None: ...


class EmailSender:
    def send(self, to: str, body: str) -> None:
        self.last = (to, body)


class SmsSender:
    def send(self, to: str, body: str) -> None:
        self.last = (to, body)


@dataclass
class Notifier:
    sender: Sender

    def notify_user(self, user_id: str, message: str) -> None:
        self.sender.send(to=user_id, body=message)


if __name__ == "__main__":
    email = EmailSender()
    notifier = Notifier(email)
    notifier.notify_user("user-42", "hello")
    assert email.last == ("user-42", "hello")
    print("ok", email.last)

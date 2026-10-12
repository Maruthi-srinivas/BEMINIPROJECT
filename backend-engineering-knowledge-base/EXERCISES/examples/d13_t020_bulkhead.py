import threading

payment_sem = threading.Semaphore(5)


def call_payment() -> None:
    with payment_sem:
        pass  # invoke partner

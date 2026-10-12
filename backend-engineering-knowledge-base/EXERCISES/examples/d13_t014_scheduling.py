import heapq
import time

q: list[tuple[float, str]] = []


def schedule(at: float, name: str) -> None:
    heapq.heappush(q, (at, name))


if __name__ == "__main__":
    now = time.time()
    schedule(now + 0.1, "b")
    schedule(now + 0.05, "a")
    while q:
        at, name = heapq.heappop(q)
        print(name)

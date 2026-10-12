import queue
import threading

q: queue.Queue[str] = queue.Queue()


def producer() -> None:
    for i in range(5):
        q.put(f"item-{i}")


def consumer() -> None:
    for _ in range(5):
        print(q.get())


if __name__ == "__main__":
    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

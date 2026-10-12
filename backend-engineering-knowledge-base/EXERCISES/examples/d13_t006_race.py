import threading

counter = 0
lock = threading.Lock()


def bump(n: int) -> None:
    global counter
    for _ in range(n):
        with lock:
            counter += 1


if __name__ == "__main__":
    threads = [threading.Thread(target=bump, args=(100_000,)) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert counter == 400_000
    print("ok")

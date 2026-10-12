import threading

value = 0
lock = threading.Lock()


def cas_increment(times: int) -> None:
    global value
    for _ in range(times):
        with lock:
            value += 1  # stand-in; real lock-free uses extension atomics


if __name__ == "__main__":
    threads = [threading.Thread(target=cas_increment, args=(50_000,)) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert value == 200_000
    print("ok")

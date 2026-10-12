import threading

sem = threading.Semaphore(2)
active = 0
lock = threading.Lock()


def work() -> None:
    global active
    with sem:
        with lock:
            active += 1
            peak = active
        assert peak <= 2
        with lock:
            active -= 1


if __name__ == "__main__":
    threads = [threading.Thread(target=work) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("ok")

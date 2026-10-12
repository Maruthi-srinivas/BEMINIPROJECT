import multiprocessing as mp
import threading

counter = {"n": 0}
lock = threading.Lock()


def bump_thread(times: int) -> None:
    for _ in range(times):
        with lock:
            counter["n"] += 1


def bump_process(times: int) -> None:
    local = {"n": 0}
    for _ in range(times):
        local["n"] += 1
    print("child total", local["n"])


if __name__ == "__main__":
    threads = [threading.Thread(target=bump_thread, args=(100_000,)) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert counter["n"] == 400_000

    p = mp.Process(target=bump_process, args=(100_000,))
    p.start()
    p.join()
    print("parent counter unchanged", counter["n"])

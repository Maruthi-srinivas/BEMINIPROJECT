import time
import concurrent.futures


def io_bound() -> None:
    time.sleep(0.05)


def cpu_bound(n: int) -> int:
    return sum(i * i for i in range(n))


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda _: io_bound(), range(16)))
    assert cpu_bound(10000) > 0
    print("ok")

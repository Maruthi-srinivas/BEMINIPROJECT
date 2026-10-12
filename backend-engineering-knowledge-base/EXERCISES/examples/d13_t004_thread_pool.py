import concurrent.futures


def work(n: int) -> int:
    return sum(range(n))


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        futs = [ex.submit(work, 1000) for _ in range(8)]
        total = sum(f.result() for f in futs)
    assert total == 8 * sum(range(1000))
    print("ok")

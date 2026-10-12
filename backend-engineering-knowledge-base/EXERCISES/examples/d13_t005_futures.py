import concurrent.futures


def square(x: int) -> int:
    return x * x


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        f1 = ex.submit(square, 6)
        f2 = ex.submit(square, 7)
        assert f1.result() == 36 and f2.result() == 49
    print("ok")

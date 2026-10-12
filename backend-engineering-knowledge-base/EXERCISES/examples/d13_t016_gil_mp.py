import multiprocessing as mp


def square(n: int) -> int:
    return n * n


if __name__ == "__main__":
    with mp.Pool(4) as pool:
        out = pool.map(square, range(10))
    assert out == [i * i for i in range(10)]
    print("ok")

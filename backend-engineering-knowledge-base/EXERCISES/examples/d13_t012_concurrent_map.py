from concurrent.futures import ThreadPoolExecutor


def main() -> None:
    # Java: ConcurrentHashMap; Python: use lock around dict or concurrent external store
    counts: dict[str, int] = {}
    lock = __import__("threading").Lock()

    def hit(key: str) -> None:
        with lock:
            counts[key] = counts.get(key, 0) + 1

    with ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda _: hit("api"), range(1000)))
    assert counts["api"] == 1000
    print("ok")


if __name__ == "__main__":
    main()

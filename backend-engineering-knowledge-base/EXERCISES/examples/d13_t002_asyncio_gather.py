import asyncio


async def fetch(n: int) -> int:
    await asyncio.sleep(0.01)
    return n * n


async def main() -> None:
    results = await asyncio.gather(*(fetch(i) for i in range(5)))
    print(sum(results))


asyncio.run(main())

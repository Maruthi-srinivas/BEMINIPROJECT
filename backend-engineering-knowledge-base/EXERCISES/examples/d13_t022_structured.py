import asyncio


async def child(x: int) -> int:
    return x * 2


async def main() -> None:
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(child(3))
        t2 = tg.create_task(child(4))
    assert t1.result() + t2.result() == 14
    print("ok")


if __name__ == "__main__":
    asyncio.run(main())

import asyncio


async def slow() -> None:
    await asyncio.sleep(10)


async def main() -> None:
    try:
        await asyncio.wait_for(slow(), timeout=0.1)
    except asyncio.TimeoutError:
        print("cancelled by timeout")


if __name__ == "__main__":
    asyncio.run(main())

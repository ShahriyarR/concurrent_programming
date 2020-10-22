import asyncio


async def async_generator():
    for i in range(1, 100000):
        yield i
        await asyncio.sleep(0.5)


async def process(item):
    async for i in async_generator():
        print("Processed", i, item)


async def main():
    task1 = asyncio.create_task(process("order"))
    task2 = asyncio.create_task(process("refund"))

    await task1
    await task2


if __name__ == "__main__":
    asyncio.run(main())

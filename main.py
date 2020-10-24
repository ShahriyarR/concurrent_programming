import asyncio


async def async_generator():
    for i in range(1, 6):
        yield i


async def process(item):
    async for i in async_generator():
        print("Processed", i, item)
        await asyncio.sleep(1)


async def main():
    task1 = asyncio.create_task(process("order"))
    task2 = asyncio.create_task(process("refund"))

    # One possible way
    # await task1
    # await task2
    # await process("cancel")

    # Second more understandable way
    tasks = [task1, task2]
    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    await process("cancel")


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from channels import Chan, Goroutine


async def async_generator():
    for i in range(1, 6):
        yield i


async def process(item, c, sleep_time=0.5):
    async for _ in async_generator():
        await c.put(item)
        await asyncio.sleep(sleep_time)


async def process_channel(c, sleep_time=0.5):
    async for item in c:
        await asyncio.sleep(sleep_time)
        print(item)


async def main():
    c1 = Chan()
    c2 = Chan()
    Goroutine.go(process("order", c1, sleep_time=0.5))
    Goroutine.go(process("refund", c2, sleep_time=1))

    task1 = asyncio.create_task(process_channel(c1, sleep_time=0.5))
    task2 = asyncio.create_task(process_channel(c2, sleep_time=1))
    await task2
    await task1


if __name__ == "__main__":
    asyncio.run(main())

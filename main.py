import asyncio
from channels import Chan, Goroutine


async def async_generator():
    for i in range(1, 6):
        yield i


async def process(item, c):
    async for _ in async_generator():
        await c.put(item)
        print(f"Put the {item}")
        await asyncio.sleep(0.5)


async def main():
    c = Chan()
    Goroutine.go(process("order", c))
    await asyncio.sleep(0.5)
    async for item in c:
        print("Processed", item)
        await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(main())

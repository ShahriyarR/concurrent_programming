import asyncio
from channels import Chan, Goroutine

item = [{'price': 8, 'category': 'shirt'},
         {'price': 20, 'category': 'shoe'},
         {'price': 24, 'category': 'shoe'},
         {'price': 4, 'category': 'drink'}]


async def gen(*items):
    out = Chan()
    for i in items:
        await out.put(i)
    return out


async def apply_discount(out_channel, items_channel):
    async for i in items_channel:
        if i['category'] == "shoe":
            i['price'] = i['price'] / 2
        await out_channel.put(i)
        await asyncio.sleep(1)


async def discount(out_channel, items_channel):
    Goroutine.go(apply_discount(out_channel, items_channel))


async def process_channel(out_channel, channel):
    async for i in channel:
        await out_channel.put(i)


async def fan_in(out_channel, *channels):
    for ch in channels:
        Goroutine.go(process_channel(out_channel, ch))


async def main():
    c = await gen({'price': 8, 'category': 'shirt'},
                  {'price': 20, 'category': 'shoe'},
                  {'price': 24, 'category': 'shoe'},
                  {'price': 4, 'category': 'drink'})

    out = Chan()
    out1 = Chan()
    out2 = Chan()
    task1 = asyncio.create_task(discount(out1, c))
    task2 = asyncio.create_task(discount(out2, c))
    task3 = asyncio.create_task(fan_in(out, out1, out2))
    await asyncio.gather(task1, task2)
    await task3

    print(len(out1))
    print(len(out2))
    print(len(out))
    await process_output(out)


async def process_output(channel):
    async for processed in channel:
        # print(f"Category: {processed['category']} Price: {processed['price']}")
        print("-", processed)

if __name__ == "__main__":
    asyncio.run(main())

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
        await asyncio.sleep(0.5)


async def discount(out_channel, items_channel):
    # Goroutine.go(apply_discount(out_channel, items_channel))
    # await asyncio.sleep(0.5)
    await apply_discount(out_channel, items_channel)


async def process_channel(out_channel, channel):
    async for i in channel:
        await out_channel.put(i)


async def fan_in(out_channel, *channels):
    for ch in channels:
        await process_channel(out_channel, ch)
        await process_output(out_channel)
        # TODO enable below to show the difference
        print(ch)
        await asyncio.sleep(0.5)


async def main():
    c = await gen({'price': 8, 'category': 'shirt'},
                  {'price': 20, 'category': 'shoe'},
                  {'price': 24, 'category': 'shoe'},
                  {'price': 4, 'category': 'drink'})

    out = Chan()
    out1 = Chan()
    out2 = Chan()
    await asyncio.gather(discount(out2, c), discount(out1, c))
    await asyncio.create_task(fan_in(out, out1, out2))


async def process_output(channel):
    async for processed in channel:
        print(f"Category: {processed['category']} Price: {processed['price']}")


if __name__ == "__main__":
    asyncio.run(main())

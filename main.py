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
        await asyncio.sleep(0.5)
        await out_channel.put(i)


async def discount(items_channel):
    out = Chan()
    Goroutine.go(apply_discount(out, items_channel))
    await asyncio.sleep(0.5)
    return out


async def process_channel(out_channel, channel):
    async for i in channel:
        await out_channel.put(i)
        await asyncio.sleep(0.5)


async def fan_in(*channels):
    out = Chan()
    for ch in channels:
        Goroutine.go(process_channel(out, ch))
        await asyncio.sleep(0.5)
    return out


async def main():
    c = await gen({'price': 8, 'category': 'shirt'},
                  {'price': 20, 'category': 'shoe'},
                  {'price': 24, 'category': 'shoe'},
                  {'price': 4, 'category': 'drink'})
    c1 = await discount(c)
    await asyncio.sleep(0.5)
    c2 = await discount(c)
    await asyncio.sleep(0.5)
    print(len(c1))
    print(len(c2))
    out = await fan_in(c1, c2)
    await asyncio.sleep(0.5)
    print(len(out))
    async for processed in out:
        print(f"Category: {processed['category']} Price: {processed['price']}")
    # await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(main())

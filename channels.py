import asyncio


class Chan:

    def __init__(self, buffer=0):
        self.channel = asyncio.Queue(maxsize=buffer)

    async def put(self, value):
        await self.channel.put(value)

    async def get(self):
        if self.channel.empty():
            return None
        return await self.channel.get()

    def __aiter__(self):
        return self

    async def __anext__(self):
        val = await self.get()
        if val is None:
            raise StopAsyncIteration
        return val


class Goroutine:

    @staticmethod
    def go(coroutine):
        asyncio.create_task(coroutine)

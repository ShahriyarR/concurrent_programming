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

    def __len__(self):
        return self.channel.qsize()

    def __aiter__(self):
        return self

    def __iter__(self):
        return self

    def __next__(self):
        try:
            val = self.channel.get_nowait()
        except asyncio.QueueEmpty:
            raise StopIteration
        return val

    async def __anext__(self):
        val = await self.get()
        if val is None:
            raise StopAsyncIteration
        return val


class Goroutine:

    @staticmethod
    def go(coroutine):
        asyncio.create_task(coroutine)

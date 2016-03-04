import asyncio
import websockets


async def client():
    async with websockets.connect("ws://localhost:8765") as webs:
        await webs.send('I am client')

asyncio.get_event_loop().run_until_complete(client())
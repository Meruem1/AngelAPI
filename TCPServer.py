import asyncio
import websockets

path = "ws://192.168.10.103:8000/ws/ticker"

# WS client example

async def hello():
    async with websockets.connect(path) as websocket:

        await websocket.send("Hello")
        print("Hello")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
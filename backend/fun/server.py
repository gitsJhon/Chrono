import asyncio
import json
import websockets
from apps import get_apps_with_time

async def apps_handler(websocket):
    while True:
        apps = get_apps_with_time()
        await websocket.send(json.dumps(apps))
        await asyncio.sleep(2)

async def main():
    async with websockets.serve(apps_handler, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

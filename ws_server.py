import websockets
import asyncio
import time
import json
from hk_usb_io import *


def xy(x, b):
    return json.dumps((x, round(b/310, 2)))


async def graph(websocket, path):
    usb = init()
    x = 0
    try:
        while True:
            b = adc_ra0(usb)
            await websocket.send(str(xy(x, b)))
            # time.sleep(0.1)
            x += 1
    except Exception as e:
        print(e)


start_server = websockets.serve(graph, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
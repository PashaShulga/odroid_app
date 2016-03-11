import websockets
import asyncio
import time
import json
from hk_usb_io import *


async def xy(x, b):
    return json.dumps((x, round(b/310, 2)))

async def consumer(websocket):
    message = ''
    # while True:
    message = await websocket.recv()
    if message is not '':
        return message
    return False


async def producer(websocket):
    usb = init()
    x = 0
    while True:
        b = adc_ra0(usb)
        await websocket.send(str(xy(x, b)))
        x += 1
        time.sleep(0.7)


async def handler(websocket, path):
    usb = init()
    x = 0
    while True:
        check_first_click = await websocket.recv()
        if check_first_click == "start":
            while True:
                b = adc_ra0(usb)
                tasks = [asyncio.ensure_future(websocket.recv()), asyncio.ensure_future(xy(x, b))]
                done, panding = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                if tasks[0] in done:
                    if tasks[0].result():
                        #TODO: read email and complit the task
                        break
                else:
                    tasks[0].cancel()

                if tasks[1] in done:
                    mess = tasks[1].result()
                    await websocket.send(str(mess))
                    await asyncio.sleep(0.1)
                else:
                    tasks[1].cancel()
                x += 1

            # if mess == 'start':
            #     producer(websocket)


start_server = websockets.serve(handler, 'localhost', 8765)

# if __name__ == '__main__':
loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()

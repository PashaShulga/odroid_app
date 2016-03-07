import websockets
import asyncio
import time
import json
val = json.dumps({"xy": [(1, -5.5),(1.2, -4.7),(2.1, 4.1),(3, 5.5),(3.2, 5.7),(4.1, 8.1),(4.5, 1.5),(4.7, 4.9),(4.8, 4.1),(4.9, 5.5),(5.1, 5.7),(5.4, 8.1)]
                  })
# with open('points') as file:
#     val = file.readline()


class ServerWS(object):
    def __init__(self, items=None):
        self.items = items

    @staticmethod
    async def graph(websocket, path):
        js = json.loads(val)
        try:
            for xy in js['xy']:
                await websocket.send(str(xy))
                time.sleep(0.1)
                # list_.append(item)
        except Exception as e:
            print(e)



start_server = websockets.serve(ServerWS.graph, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
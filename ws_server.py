import websockets
import asyncio
import time
import json
val = [-5.5,-4.7,-4.1,-3.5,-3.2,-2.4,-2.8,-1.7,-1.2,-0.9,-0.7,-0.4,-0.4,-0.3,0.2,0.2,0.3,0.3,-0.7,-0.9]


def points():
    list_ = []
    for item in val:
        list_.append(item)
        del val[0]
    data_list = json.dumps({"data": list_})
    print(data_list)
    return data_list


class ServerWS(object):
    def __init__(self, items=None):
        self.items = items

    @staticmethod
    async def graph(websocket, path):
        try:
            list_ = []
            await websocket.send(str(val))
            # time.sleep(0.4)
                # list_.append(item)
        except Exception as e:
            print(e)


start_server = websockets.serve(ServerWS.graph, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
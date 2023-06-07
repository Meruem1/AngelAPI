import asyncio
import websockets
# from Feed import *
import json
from random import randint

# feedObj = feed()

async def echo(websocket, path):
    try :
        while True:
            # data = feedObj.MarketFeeed
            # print(data)
            data = {'token':randint(100,103),'bid':randint(1,10),'ask':randint(1,10),'ltp':randint(1,10)}
            print(data)
            await websocket.send(str(json.dumps(data)))
            await asyncio.sleep(0.5)

            # gc.collect()
            # time.sleep(0.00000001)
    except Exception as e :
        print(str(e))
        # ErrorLog.writeErrorLog("webserver","echo",str(e))



try :
    asyncio.get_event_loop().run_until_complete(websockets.serve(echo, '192.168.1.6', 6111))
    asyncio.get_event_loop().run_forever()
except Exception as e :
    print(e)


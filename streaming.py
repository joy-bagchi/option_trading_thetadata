import asyncio
import websockets
from constants import THETADATA_TERMINAL_WEBSOCKETS as THETA_TERMINAL


# This only works on Python 3.11, not 3.12!
async def stream_trades():
    async with websockets.connect(THETA_TERMINAL) as websocket:
        req = {
            'msg_type': 'STREAM_BULK',
            'sec_type': 'OPTION',
            'req_type': 'TRADE',
            'add': True,
            'id': 0
        }
        await websocket.send(req.__str__())
        while True:
            response = await websocket.recv()
            print(response)


asyncio.get_event_loop().run_until_complete(stream_trades())

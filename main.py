import asyncio
import websockets
import json

from Utils.WSUtils.Parcel import handleParcel
from Utils.WSUtils.WSStateSingletone import WSStateSingletone
from Utils.SETTINGS.SETTINGS import DB_connection

WS_STATE = WSStateSingletone()
DB_connection()


def message_to_json(message) -> str:
    return json.dumps(message, ensure_ascii=False)


async def message_handler(websocket):
    async for parcel in websocket:
        print('[InParcel]: ', parcel)

        outParcel = handleParcel(parcel, sender=websocket)
        print(str(outParcel)[:100])

        websockets.broadcast(outParcel.destination, outParcel.to_json())


async def handler(websocket):
    print('[Info]: Client connected')
    try:
        await message_handler(websocket)
    except websockets.exceptions.ConnectionClosed:
        await websocket.close()
        WS_STATE.remove_recv(websocket)
        try:
            WS_STATE.remove_trans(websocket)
            print("[Info]: Transmitter disconnected")
        except KeyError:
            print("[Info]: Reciever disconnected")
        return


async def main():
    async with websockets.serve(handler, '192.168.1.100', 8765):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        DB_connection.close_connection()
        print('[Warning]: Exiting because of keyboard interrupt')

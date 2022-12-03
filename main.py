import asyncio
import websockets
import json
import logging
import sys

from Utils.WSUtils.Parcel import handleParcel
from Utils.WSUtils.WSStateSingletone import WSStateSingletone
from Utils.SETTINGS.SETTINGS import DB_connection

WS_STATE = WSStateSingletone()
DB_connection()


def message_to_json(message) -> str:
    return json.dumps(message, ensure_ascii=False)


async def message_handler(websocket):
    async for parcel in websocket:
        logging.info(f'[InParcel]: {parcel}')

        try:
            outParcel = handleParcel(parcel, sender=websocket)
        except Exception:
            logging.error("Exception occurred", exc_info=True)

        logging.info(f'{str(outParcel)[:100]}')

        websockets.broadcast(outParcel.destination, outParcel.to_json())


async def handler(websocket):
    logging.info('[Info]: Client connected')

    try:
        await message_handler(websocket)
    except websockets.exceptions.ConnectionClosed:
        await websocket.close()
        WS_STATE.remove_recv(websocket)
        try:
            WS_STATE.remove_trans(websocket)
            logging.info('[Info]: Transmitter disconnected')
        except KeyError:
            logging.info('[Info]: Reciever disconnected')
        return


async def main():
    async with websockets.serve(handler, '192.168.1.100', 8765):
        await asyncio.Future()

if __name__ == "__main__":
    logging.basicConfig(
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler(sys.stdout)
        ],
        format='%(asctime)s - %(message)s',
        level=logging.INFO,
    )
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        DB_connection.close_connection()
        print('[Warning]: Exiting because of keyboard interrupt')

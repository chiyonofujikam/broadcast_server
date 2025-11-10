import asyncio
import websockets
import logging
from config import config
import aioconsole

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(".logs/client.log", mode="a"),
        logging.StreamHandler()
    ]
)

async def receive_messages(websocket):
    """ Receive messages from server """
    try:
        async for message in websocket:
            # print log output without breaking the current input line
            print(f"\r📩 Received: {message}\nEnter message: ", end="", flush=True)
    except websockets.exceptions.ConnectionClosed:
        logging.info("⚠️ Server closed connection.")

async def send_messages(websocket):
    """ Send messages to server """
    while True:
        message = await aioconsole.ainput("Enter message: ")

        if message.lower() in {"quit", "exit"}:
            logging.info("👋 Disconnecting...")
            await websocket.close()
            break

        await websocket.send(message)
        logging.info(f"➡️ Sent: {message}")

async def chat():
    """ Main chat handler """
    async with websockets.connect(f"ws://{config.SERVER_HOST}:{config.SERVER_PORT}") as websocket:
        logging.info("✅ Connected to chat server!")
        await asyncio.gather(
            send_messages(websocket),
            receive_messages(websocket)
        )

if __name__ == "__main__":
    asyncio.run(chat())
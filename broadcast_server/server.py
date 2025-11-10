import asyncio
import websockets
import logging
from config import config

logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more detail
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        # logs to file
        logging.FileHandler(".logs/server.log", mode="a"),
        # also logs to console
        logging.StreamHandler()
    ]
)

# Set of connected clients
connected_clients = set()

async def broadcast(message: str, exclude=None):
    """Send message to all clients except `exclude`."""
    disconnected = []
    for client in connected_clients:
        if client == exclude:
            continue
        try:
            await client.send(message)
        except websockets.exceptions.ConnectionClosed:
            disconnected.append(client)
            logging.warning(f"Client {id(client)} disconnected during broadcast.")

    for client in disconnected:
        connected_clients.discard(client)
        logging.info(f"Removed disconnected client {id(client)}. Total: {len(connected_clients)}")

async def handle_client(websocket):
    """ Function to handle each client connection """
    connected_clients.add(websocket)
    client_id = id(websocket)
    logging.info(f"Client {client_id} connected. Total clients: {len(connected_clients)}")

    # Broadcast join notification
    await broadcast(f"🟢 Client {client_id} joined the chat!", exclude=websocket)

    try:
        async for message in websocket:
            message = message.strip()
            if not message:
                continue

            logging.info(f"Received from {client_id}: {message}")

            # broadcast the sended message
            await broadcast(f"Client {client_id}: {message}", exclude=websocket)

    except websockets.exceptions.ConnectionClosedError as e:
        logging.warning(f"Client {client_id} disconnected with error: {e}")

    except Exception as e:
        logging.error(f"Unexpected error from client {client_id}: {e}", exc_info=True)

    finally:
        connected_clients.discard(websocket)
        logging.info(f"Client {client_id} removed. Total clients: {len(connected_clients)}")

        # Broadcast leave notification
        await broadcast(f"🔴 Client {client_id} left the chat!")

async def main():
    """ Main function to start the WebSocket server """
    async with websockets.serve(handle_client, config.SERVER_HOST, config.SERVER_PORT):
        print(f"✅ Server started at ws://{config.SERVER_HOST}:{config.SERVER_PORT}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
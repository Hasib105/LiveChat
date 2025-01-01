from typing import List
from fastapi import WebSocket


async def broadcast(websockets: List[WebSocket], data: dict):
    """Broadcast data to all connected websockets."""
    for ws in websockets:
        try:
            await ws.send_json(data)
        except Exception as e:
            print(f"Failed to send message: {e}")

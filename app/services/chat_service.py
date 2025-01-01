from fastapi import WebSocket, WebSocketDisconnect
from uuid import uuid4
from app.services.broadcast_data import broadcast
from app.models.core import Message

class ChatService:
    def __init__(self):
        self.guest_requests = {}  # Active guest requests
        self.active_rooms = {}  # Active chat rooms

    async def handle_guest_connection(self, websocket: WebSocket):
        """Handle guest connection requests."""
        await websocket.accept()
        guest_id = str(uuid4())
        self.guest_requests[guest_id] = {"websocket": websocket}
        try:
            while True:
                data = await websocket.receive_json()
                self.guest_requests[guest_id].update(data)
                # Broadcast new guest request
                print(f"Guest {guest_id} connected.")
        except WebSocketDisconnect:
            del self.guest_requests[guest_id]
            print(f"Guest {guest_id} disconnected.")

    async def handle_user_connection(self, websocket: WebSocket):
        """Handle user (agent) connections."""
        await websocket.accept()
        try:
            while True:
                data = await websocket.receive_json()
                if data["type"] == "accept_request":
                    guest_id = data["guest_id"]
                    if guest_id in self.guest_requests:
                        room_id = str(uuid4())
                        guest_ws = self.guest_requests[guest_id]["websocket"]
                        del self.guest_requests[guest_id]
                        self.active_rooms[room_id] = [guest_ws, websocket]
                        await broadcast([guest_ws, websocket], {"room_id": room_id, "message": "Chat started"})
        except WebSocketDisconnect:
            print("User disconnected.")

    async def handle_chat_room(self, websocket: WebSocket, room_id: str):
        """Handle real-time messaging in a chat room."""
        if room_id not in self.active_rooms:
            self.active_rooms[room_id] = []
        self.active_rooms[room_id].append(websocket)
        try:
            while True:
                message = await websocket.receive_text()
                # Relay message to all participants
                for ws in self.active_rooms[room_id]:
                    if ws != websocket:
                        await ws.send_text(message)
        except WebSocketDisconnect:
            self.active_rooms[room_id].remove(websocket)
            if not self.active_rooms[room_id]:
                del self.active_rooms[room_id]
                print(f"Chat room {room_id} closed.")

from fastapi import WebSocket, WebSocketDisconnect
from uuid import uuid4
from app.services.broadcast_data import broadcast
from app.models.core import Message

from fastapi import WebSocket, WebSocketDisconnect

class ChatService:
    def __init__(self):
        self.guest_requests = {}  # Guest requests stored by guest_id
        self.user_connections = []  # List of user WebSocket connections
        self.active_rooms = {}  # Initialize active_rooms here

    async def handle_guest_connection(self, websocket: WebSocket):
        """Handle guest WebSocket connections."""
        await websocket.accept()
        guest_id = str(uuid4())
        self.guest_requests[guest_id] = {"websocket": websocket}
        try:
            while True:
                data = await websocket.receive_json()
                self.guest_requests[guest_id].update(data)

                # Broadcast new request to all users
                for user_ws in self.user_connections:
                    await user_ws.send_json({"guest_id": guest_id, **data})

        except WebSocketDisconnect:
            del self.guest_requests[guest_id]
            print(f"Guest {guest_id} disconnected.")

    async def handle_user_connection(self, websocket: WebSocket):
        """Handle user WebSocket connections."""
        await websocket.accept()
        self.user_connections.append(websocket)
        try:
            while True:
                data = await websocket.receive_json()
                if data["type"] == "accept_request":
                    guest_id = data["guest_id"]
                    if guest_id in self.guest_requests:
                        room_id = str(uuid4())
                        guest_ws = self.guest_requests[guest_id]["websocket"]
                        del self.guest_requests[guest_id]
                        await websocket.send_json({"room_id": room_id})
                        await guest_ws.send_json({"room_id": room_id})
        except WebSocketDisconnect:
            self.user_connections.remove(websocket)
            print("User disconnected.")


    async def handle_chat_room(self, websocket: WebSocket, room_id: str):
        """Handle real-time messaging in a chat room."""
        if room_id not in self.active_rooms:
            self.active_rooms[room_id] = []

        self.active_rooms[room_id].append(websocket)

        try:
            await websocket.accept()

            while True:
                try:
                    # Receive a message from the WebSocket
                    message = await websocket.receive_json()
                    # Relay the JSON message to all participants in the room
                    for ws in self.active_rooms[room_id]:
                        if ws != websocket:
                            try:
                                await ws.send_json(message)
                            except Exception as e:
                                print(f"Error sending message to participant: {e}")
                except Exception as e:
                    print(f"Error handling message: {e}")
        except WebSocketDisconnect:
            self.active_rooms[room_id].remove(websocket)
            if not self.active_rooms[room_id]:
                del self.active_rooms[room_id]
                print(f"Chat room {room_id} closed.")



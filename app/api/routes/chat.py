from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.services.chat_service import ChatService

app = FastAPI()

# Instantiate the chat service
chat_service = ChatService()

@app.websocket("/ws/guest")
async def guest_endpoint(websocket: WebSocket):
    """Endpoint for guest connections."""
    await chat_service.handle_guest_connection(websocket)

@app.websocket("/ws/user")
async def user_endpoint(websocket: WebSocket):
    """Endpoint for user (agent) connections."""
    await chat_service.handle_user_connection(websocket)

@app.websocket("/ws/room/{room_id}")
async def chat_room_endpoint(websocket: WebSocket, room_id: str):
    """Endpoint for chat room connections."""
    await chat_service.handle_chat_room(websocket, room_id)

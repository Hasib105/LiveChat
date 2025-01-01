import pytest
import websockets
import asyncio

BASE_URL = "ws://localhost:8000"

@pytest.mark.asyncio
async def test_guest_connection():
    async with websockets.connect(f"{BASE_URL}/ws/guest") as websocket:
        await websocket.send('{"message": "Hello from guest"}')
        response = await websocket.recv()
        assert "acknowledged" in response  # Adjust based on server logic

@pytest.mark.asyncio
async def test_chat_room():
    room_id = "test-room"
    async with websockets.connect(f"{BASE_URL}/ws/room/{room_id}") as client1:
        async with websockets.connect(f"{BASE_URL}/ws/room/{room_id}") as client2:
            await client1.send("Hello from client 1")
            message = await client2.recv()
            assert message == "Hello from client 1"

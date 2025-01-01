import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_swagger_redirect():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert "Swagger UI" in response.text

@pytest.mark.asyncio
async def test_user_routes():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        # Replace with your actual route and data
        response = await client.get("/api/users")
    assert response.status_code == 200

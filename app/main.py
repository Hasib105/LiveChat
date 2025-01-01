from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import user  # Ensure this path points to your actual user routes module
from app.services.chat_service import ChatService

# FastAPI app instance
app = FastAPI(
    title="User Management API",
    description=(
        "API for managing users with roles like Admin and Employee. "
        "Includes WebSocket for real-time chat functionality."
    ),
    version="1.0.0",
)

# Instantiate ChatService
chat_service = ChatService()

# OAuth2 for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# CORS Middleware (adjust allow_origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Swagger UI Redirect
@app.get("/", include_in_schema=False)
async def swagger_ui_redirect():
    """Redirect to Swagger UI."""
    return get_swagger_ui_html(openapi_url="/openapi.json", title=app.title)


# Include user routes
app.include_router(user.router, prefix="/api", tags=["Users"])


# WebSocket endpoints
@app.websocket("/ws/guest")
async def guest_websocket(websocket: WebSocket):
    """Handle guest WebSocket connections."""
    await chat_service.handle_guest_connection(websocket)


@app.websocket("/ws/user")
async def user_websocket(websocket: WebSocket):
    """Handle user (agent) WebSocket connections."""
    await chat_service.handle_user_connection(websocket)


@app.websocket("/ws/room/{room_id}")
async def chat_room_websocket(websocket: WebSocket, room_id: str):
    """Handle real-time messaging in a chat room."""
    await chat_service.handle_chat_room(websocket, room_id)


# WebSocket Lifecycle Events
@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    print("Server starting up... ChatService is ready.")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    print("Server shutting down... Cleaning up resources.")

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import OAuth2PasswordBearer
from app.api.routes import user  # Ensure this import is correct

app = FastAPI(
    title="User Management API",
    description="API for managing users with roles like Admin and Employee",
    version="1.0.0",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

@app.get("/", include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_html(openapi_url="/openapi.json", title=app.title)

@app.get("/test")
async def test_route():
    return {"message": "This is a test route"}

# Include user routes
app.include_router(user.router, prefix="/api", tags=["Users"])

from fastapi import FastAPI
from app.api.routes import user

app = FastAPI()

# Include routers
app.include_router(user.router, prefix="/api", tags=["Users"])

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI with MongoDB!"}

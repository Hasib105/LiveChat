from fastapi import APIRouter
from app.db.database import db

router = APIRouter()

@router.get("/users")
async def get_users():
    users = list(db["users"].find({}, {"_id": 0}))
    return {"users": users}

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class Role(str, Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"

class Status(str, Enum):
    OPEN = "open"
    CLOSED = "closed"

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, *args, **kwargs):
        return {
            "type": "string",
            "format": "objectid"
        }

class UserResponse(BaseModel):
    id: PyObjectId = Field(default=None, alias="_id")
    email: EmailStr
    full_name: str
    role: Role = Role.EMPLOYEE  # Default role is 'employee'

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: Role = Role.EMPLOYEE  # Default role is 'employee'

class UserCreate(UserBase):
    password: str  # Password for new users


class Guest(BaseModel):
    email: EmailStr
    full_name: str

class Message(BaseModel):
    id: PyObjectId = Field(default=None, alias="_id")
    sender_id: PyObjectId
    content: str = Field(..., min_length=1, max_length=500)  # Limit content length
    timestamp: datetime = Field(default_factory=datetime.utcnow)  # Default to now

class ChatRoom(BaseModel):
    id: PyObjectId = Field(default=None, alias="_id")
    title: str
    participants: List[PyObjectId]
    status: Status = Status.OPEN  # Default status is 'open'

class ChatRoomWithMessages(BaseModel):
    chat_room: ChatRoom
    messages: List[Message] = []
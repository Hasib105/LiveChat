from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"

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

# FastAPI setup remains unchanged...

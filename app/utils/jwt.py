import jwt
from datetime import datetime, timedelta
from app.core.config import settings
from app.models.core import UserResponse
from typing import Optional

# Secret key for encoding and decoding JWT
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"  # You can choose a different algorithm if needed
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiry time in minutes

# Function to create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify access token and decode it
def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.JWTError:
        raise Exception("Token is invalid")

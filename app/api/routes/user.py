from fastapi import APIRouter, HTTPException, Depends, status
from app.db.database import db
from app.models.user import UserCreate, UserResponse
from app.utils.security import hash_password
from app.utils.security import verify_password
from app.utils.jwt import create_access_token
from pydantic import EmailStr
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()

@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    # Check if email already exists
    existing_user = db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password before saving
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)

    # Insert user into the database
    result = db["users"].insert_one(user_dict)
    user_dict["_id"] = result.inserted_id

    return user_dict


@router.post("/login")
async def login(email: str, password: str):
    user = db["users"].find_one({"email": email})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify the password
    if not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    # Create JWT token
    access_token = create_access_token(data={"sub": str(user["_id"])})
    
    return {"access_token": access_token, "token_type": "bearer"}


# Dependency to get the current user from the token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db["users"].find_one({"_id": user_id})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/profile")
async def get_profile(current_user: UserResponse = Depends(get_current_user)):
    return {"email": current_user["email"], "role": current_user["role"]}
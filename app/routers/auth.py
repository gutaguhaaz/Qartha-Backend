
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta
import hashlib
import secrets
from bson import ObjectId
from ..db import get_db

router = APIRouter()
security = HTTPBearer()

class UserRegister(BaseModel):
    username: str
    password: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str

def hash_password(password: str) -> str:
    """Hash password with salt"""
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}:{hashed.hex()}"

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    try:
        salt, hash_hex = hashed.split(':', 1)  # Split only on first ':'
        expected_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return expected_hash.hex() == hash_hex
    except Exception as e:
        print(f"Password verification error: {e}")  # Debug
        return False

@router.post("/api/auth/register")
async def register_user(user: UserRegister, db = Depends(get_db)):
    """Register a new user"""
    # Check if user exists
    existing = await db.users.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Create user
    user_doc = {
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password),
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    
    result = await db.users.insert_one(user_doc)
    return {
        "id": str(result.inserted_id),
        "username": user.username,
        "email": user.email
    }

@router.post("/api/auth/login")
async def login_user(user: UserLogin, db = Depends(get_db)):
    """Authenticate user and return token"""
    print(f"Login attempt for username/email: {user.username}")  # Debug
    
    # Try to find user by username OR email
    user_doc = await db.users.find_one({
        "$or": [
            {"username": user.username},
            {"email": user.username}
        ]
    })
    
    if not user_doc:
        print(f"User not found with username/email: {user.username}")  # Debug
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    print(f"Found user: {user_doc['username']}, verifying password...")  # Debug
    password_valid = verify_password(user.password, user_doc["password"])
    print(f"Password verification result: {password_valid}")  # Debug
    
    if not password_valid:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate simple token (in production, use JWT)
    token = secrets.token_urlsafe(32)
    
    # Store token in database
    await db.tokens.insert_one({
        "token": token,
        "user_id": str(user_doc["_id"]),
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(days=7)
    })
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": str(user_doc["_id"]),
            "username": user_doc["username"],
            "email": user_doc["email"]
        }
    }

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    """Get current authenticated user"""
    token_doc = await db.tokens.find_one({
        "token": credentials.credentials,
        "expires_at": {"$gt": datetime.utcnow()}
    })
    
    if not token_doc:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_doc = await db.users.find_one({"_id": ObjectId(token_doc["user_id"])})
    if not user_doc:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user_doc

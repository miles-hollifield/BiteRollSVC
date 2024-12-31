from passlib.context import CryptContext
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
import bcrypt

# Load environment variables
load_dotenv()

# Secret key for JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str, salt: str) -> str:
    """Hash a password with the given salt."""
    salted_password = (password + salt).encode()  # Combine password with salt
    return bcrypt.hashpw(salted_password, bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str, salt: str) -> bool:
    """Verify a plain password against a hashed password using the same salt."""
    salted_password = (plain_password + salt).encode()  # Combine entered password with salt
    return bcrypt.checkpw(salted_password, hashed_password.encode())
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

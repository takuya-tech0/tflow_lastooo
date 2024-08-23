# /Users/takuya/Documents/talent-flow1.1/fastapi-backend/auth.py
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import Employee

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, username: str, password: str):
    print(f"Attempting to authenticate user: {username}")
    user = db.query(Employee).filter(Employee.name == username).first()
    print(f"User found: {user}")
    if not user:
        print("User not found")
        return False
    if user.password != password:  # 'hashed_password' ではなく 'password' を使用
        print("Password verification failed")
        return False
    print("Authentication successful")
    return user
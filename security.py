__import__("dotenv").load_dotenv() #Dotenv
import os
from schemas.users import User
from schemas import UserSchema
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from db import users
from typing import List, Union, Annotated, Optional
from datetime import datetime, timedelta, timezone


ph = PasswordHasher()

oauth2_scheme = OAuth2PasswordBearer("/auth/token")

def verifyPassword(password: str, hashedPassword: str) -> bool:
    try:
        ph.verify(hashedPassword, password)
        return True
    except VerifyMismatchError:
        return False

def getUser(username: str) -> User:
    user = users.find_one(
        {
            "username": username
        }
    )
    if user:
        return User(**user)

def authenticateUser(username: str, password: str) -> bool:
    user = getUser(username)
    if not user: return False
    return user if verifyPassword(password, user.password) else False

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update(
        {
            "exp": expire
        }
    )
    encoded_jwt = jwt.encode(
        to_encode,
        os.environ.get("SECRET_KEY"),
        algorithm="HS256"
    )
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(**{
        "status_code": 401,
        "detail": "Could not validate credentials",
        "headers": {
            "WWW-Authenticate": "Bearer"
        }
    })
    try:
        payload = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # token_data = TokenData(username=username)
    except jwt.JWTError:
        raise credentials_exception
    user = getUser(username)
    if user is None:
        raise credentials_exception
    del user.__dict__["password"]
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

# Note: To enable authentication on any route, import get_current_active_user from security.py and User model from schemas/users.py# Additionally, you will also need Annotated (import from typing), Depends (import from FastAPI)

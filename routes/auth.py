from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from security import *
from typing import Annotated
from schemas.users import User
from schemas import UserSchema
from db import users

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

"""Authentication routes of this API"""

@router.post('/register')
async def register_user(user: UserSchema):
    """User Registration"""
    user.password = ph.hash(user.password)
    user = User(**user.dict())
    if getUser(user.username, email=user.email):
        return {"message": "User Already Exists"}
    users.insert_one(user.dict())
    return {"message": "User Created"}

@router.post('/token')
async def login(
        form_data: Annotated[
            OAuth2PasswordRequestForm,
            Depends()
        ]
    ):
    """User Login"""
    user = authenticateUser(form_data.username, form_data.password)
    if not user:
        return {
            "message": "Invalid Credentials"
        }
    access_token = create_access_token(
        data={
            "sub": user.username
        }
    )
    print(access_token)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
 
@router.get('/profile')
async def test_token(
        current_user: Annotated[
            User,
            Depends(get_current_active_user)
        ]
    ):
    """Retrive Profile Information"""
    return current_user

@router.post('/profile')
async def update_profile(
        user_data: UserSchema,
        current_user: Annotated[
            User,
            Depends(get_current_active_user)
        ]
    ):
    user_data.password = ph.hash(user_data.password)
    users.update_one(
        {
            "username": current_user.username
        },
        {
            "$set": user_data.dict()
        }
    )
    del user_data.__dict__['password']
    return user_data

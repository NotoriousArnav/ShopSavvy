from pydantic import BaseModel, EmailStr
from typing import List, Literal

class Permissions(BaseModel):
    read: bool
    write: bool
    delete: bool
    scope: str

class User(BaseModel):
    username: str
    password: str
    email: EmailStr = None
    role: Literal["admin", "staff", "user"] = "user" # Can be either admin, staff ot user
    permissions: List[Permissions] = []

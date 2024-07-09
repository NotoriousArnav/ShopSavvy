from pydantic import BaseModel, EmailStr
from .product import Product

class ProductResponseModel(BaseModel):
    product_id: str

class Product_w_ID(Product):
    id: str

class UserSchema(BaseModel):
    username: str
    password: str
    email: EmailStr = None

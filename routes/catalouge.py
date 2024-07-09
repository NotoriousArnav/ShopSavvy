from fastapi import APIRouter, Depends
from schemas.product import Product
from typing import List, Annotated
from schemas import ProductResponseModel, Product_w_ID
from schemas.users import User
from uuid import uuid4
from db import products
from bson import ObjectId
import json
from security import get_current_user

router = APIRouter(
    prefix="/catalouge",
    tags=["Catalouge"],
)

@router.get('/product', response_model=List[Product_w_ID])
async def get_products():
    products_list = [Product_w_ID(id=str(x.get('_id')),**x) for x in products.find()]
    return products_list

@router.get('/product/{product_id}', response_model=Product)
async def get_product(product_id: str):
    product = products.find_one(
        {
            "_id": ObjectId(product_id)
        }
    )
    __import__('pprint').pprint(product)
    obj = Product(**product)
    return obj

@router.delete('/product/{product_id}', response_model=ProductResponseModel)
async def delete_product(product_id: str, current_user: Annotated[User, Depends(get_current_user)]):
    products.delete_one(
        {
            "_id": ObjectId(product_id)
        }
    )
    return ProductResponseModel(product_id = product_id)

@router.put('/product/{product_id}', response_model=Product)
async def update_product(product_id: str, product: Product, current_user: Annotated[User, Depends(get_current_user)]):
    products.update_one(
        {
            "_id": ObjectId(product_id)
        },
        {
            "$set": product.dict()
        }
    )
    return product

@router.post('/product/', response_model=ProductResponseModel)
async def add_product(product: Product, current_user: Annotated[User, Depends(get_current_user)]):
    pid = products.insert_one(product.dict())
    print(pid)
    return ProductResponseModel(product_id = str(pid.inserted_id))

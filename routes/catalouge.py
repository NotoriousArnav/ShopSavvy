from fastapi import APIRouter, Depends, Query
from schemas.product import Product
from typing import List, Annotated, Optional, Dict
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

"""Catalouge routes of this API"""

def filter_params(
    name: Optional[str] = Query(None),
    tags: Optional[List[str]] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
) -> Dict:
    query = {}
    
    if name:
        query['name'] = {'$regex': name, '$options': 'i'}
    if tags:
        query['tags'] = {'$all': tags.split(',')}
    if min_price is not None:
        query['price'] = {'$gte': min_price}
    if max_price is not None:
        if 'price' in query:
            query['price']['$lte'] = max_price
        else:
            query['price'] = {'$lte': max_price}
    
    return query

# Add filtering using URL Params
@router.get('/product', response_model=List[Product_w_ID])
async def get_products(query: Annotated[dict, Depends(filter_params)]):
    """Get All Products"""
    products_list = [
        Product_w_ID(
            id=str(x.get('_id')),
            **x
        ) for x in products.find(query)
    ]
    return products_list

@router.get('/product/{product_id}', response_model=Product)
async def get_product(product_id: str):
    """Get Product by ID"""
    product = products.find_one(
        {
            "_id": ObjectId(product_id)
        }
    )
    # __import__('pprint').pprint(product)
    obj = Product(**product)
    return obj

@router.delete('/product/{product_id}', response_model=ProductResponseModel)
async def delete_product(product_id: str, current_user: Annotated[User, Depends(get_current_user)]):
    """Delete Product by ID"""
    products.delete_one(
        {
            "_id": ObjectId(product_id)
        }
    )
    return ProductResponseModel(product_id = product_id)

@router.put('/product/{product_id}', response_model=Product)
async def update_product(product_id: str, product: Product, current_user: Annotated[User, Depends(get_current_user)]):
    """Update Product by ID"""
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
    """Add Product"""
    pid = products.insert_one(product.dict())
    print(pid)
    return ProductResponseModel(product_id = str(pid.inserted_id))

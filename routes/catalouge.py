from fastapi import APIRouter, Depends, Query, HTTPException
from schemas.product import Product
from typing import List, Annotated, Optional, Dict
from schemas import ProductResponseModel, Product_w_ID
from schemas.users import User
from uuid import uuid4
from db import products
from bson import ObjectId
import json
from security import get_current_user

async def admin_staff_check(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.role not in ['admin', 'staff']:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to perform this action"
        )
    return current_user

router = APIRouter(
    prefix="/catalouge",
    tags=["Catalouge"],
)

"""Catalouge routes of this API"""

def filter_params(
    name: Optional[str] = Query(None),
    tags: Optional[List[str]] = Query(None),
    in_desc: Optional[str] = Query(None),
    in_short_desc: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
) -> Dict:
    query = {}
    
    if name:
        query['name'] = {'$regex': name, '$options': 'i'}
    if in_desc:
        query['description.content'] = {'$regex': in_desc, '$options': 'i'}
    if in_short_desc:
        query['short_description'] = {'$regex': in_short_desc, '$options': 'i'}
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
    """Get All Products

    Parameters
    ----------
    - name: Optional[str] = Query(None)
    - tags: Optional[List[str]] = Query(None)
    - in_desc: Optional[str] = Query(None)
    - in_short_desc: Optional[str] = Query(None)
    - min_price: Optional[float] = Query(None)
    - max_price: Optional[float] = Query(None)

    """
    products_list = [
        Product_w_ID(
            id=str(x.get('_id')),
            **x
        ) for x in products.find(query)
    ]
    return products_list

@router.get('/product/{product_id}', response_model=Product)
async def get_product(product_id: str):
    """Get Product by ID

    Parameters
    ----------
    - product_id: str
    """
    product = products.find_one(
        {
            "_id": ObjectId(product_id)
        }
    )
    obj = Product(**product)
    return obj


# TODO:Check for the Permission and its scopes. HTTPException will be raised if permission is not granted.

@router.delete('/product/{product_id}', response_model=ProductResponseModel)
async def delete_product(product_id: str, current_user: Annotated[User, Depends(admin_staff_check)]):
    """Delete Product by ID

    Parameters
    ----------
    - product_id: str

    Token is Required to perform this action
    """
    products.delete_one(
        {
            "_id": ObjectId(product_id)
        }
    )
    return ProductResponseModel(product_id = product_id)

@router.put('/product/{product_id}', response_model=Product)
async def update_product(product_id: str, product: Product, current_user: Annotated[User, Depends(admin_staff_check)]):
    """Update Product by ID
    Parameters
    ----------
    - product_id: str

    Body
    ----
    - product: Product

    Token is Required to perform this action
    """
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
async def add_product(product: Product, current_user: Annotated[User, Depends(admin_staff_check)]):
    """Add Product
    
    Body
    ----
    - product: Product

    Token is Required to perform this action.
    """
    pid = products.insert_one(
        product.dict()
    )
    return ProductResponseModel(product_id = str(pid.inserted_id))

from fastapi import APIRouter, Depends, HTTPException
from security import get_current_user
from schemas.users import User
from schemas.inventory import Inventory
from schemas import CatalogueResponseModel
from typing import Annotated, List, Literal
from bson import ObjectId
from db import inventory

async def admin_staff_check(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.role not in ['admin', 'staff']:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to perform this action"
        )
    return current_user

async def inventory_scope_check(current_user: Annotated[User, Depends(admin_staff_check)]):
    user_permissions = current_user.permissions 
    flag = any(
        x.scope in (
            'inventory',
            '*'
        ) and x.read
        for x in user_permissions
    )
    if not flag:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to perform this action"
        )
    return current_user

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory Management"],
    dependencies=[
        Depends(inventory_scope_check)
    ]
)

"""Inventory routes of this API"""

@router.get('/item', response_model=List[Inventory])
async def get_inventory():
    """Get All Products"""
    inventory_list = [
        Inventory(**x) for x in inventory.find()
    ]
    return inventory_list

@router.get('/item/{catalogue_id}', response_model=Inventory)
async def get_inventory(catalogue_id: str):
    """Get Inventory by ID

    Parameters
    ----------
    - catalogue_id: str
    """
    inventory_obj = inventory.find_one(
        {
            "_id": ObjectId(
                catalogue_id
            )
        }
    )
    if not inventory_obj:
        raise HTTPException(
            404,
            "Inventory not found"
        )
    obj = Inventory(
        **inventory_obj
    )
    return obj

@router.put('/item/{catalogue_id}', response_model=CatalogueResponseModel)
async def update_inventory(
        catalogue_id: str,
        inventory: Inventory,
):
    """Update Inventory by ID
    Parameters
    ----------
    - catalogue_id: str

    Body
    ----
    - inventory: Inventory

    Token is Required to perform this action
    """
    inventory.update_one(
        {
            "catalogue_id": ObjectId(catalogue_id)
        },
        {
            "$set": inventory.dict()
        }
    )
    return CatalogueResponseModel(
        catalogue_id = catalogue_id
    )


@router.delete('/item/{catalogue_id}', response_model=CatalogueResponseModel)
async def delete_inventory(catalogue_id: str):
    """Delete Inventory by ID

    Parameters
    ----------
    - catalogue_id: str

    Token is Required to perform this action
    """
    inventory.delete_one(
        {
            "catalogue_id": ObjectId(catalogue_id)
        }
    )
    return CatalogueResponseModel(
        catalogue_id = catalogue_id
    )

@router.post('/item/', response_model=Inventory)
async def add_inventory(inventory: Inventory):
    """Add new Inventory item
    
    Body
    ----
    - inventory: Inventory

    Token is Required to perform this action.
    """
    inventory.insert_one(
        inventory.dict()
    )
    return inventory

from pydantic import BaseModel
from typing import List

class Inventory(BaseModel):
    name: str
    description: str
    quantity: int
    tags: List[str]
    catalogue_id: str

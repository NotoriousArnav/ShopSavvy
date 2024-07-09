from pydantic import BaseModel
from typing import List
from .images import Image, ImageCarousel
from .currency import Currency, default_currency
from .markdown import MarkdownModel
from bson import ObjectId

class ProductSpecs(BaseModel):
    specs: dict = {}

class Product(BaseModel):
    name: str
    description: MarkdownModel
    short_description: str
    specs: ProductSpecs = ProductSpecs()
    tags: List[str]
    price: float
    currency: Currency = default_currency
    images: ImageCarousel

    def inDescription(self, query):
        """Check if query is in product description"""
        return True if query.lower() in self.description.content.lower() else False

from pydantic import BaseModel
from typing import List

class Image(BaseModel):
        url: str
        alt_text: str
        caption: str

class ImageCarousel(BaseModel):
        images: List[Image]
        default_image: int = 0



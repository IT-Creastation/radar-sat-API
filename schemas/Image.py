from typing import Optional
from pydantic import BaseModel


class ImageBase(BaseModel):
    path: str
    name: str


class ImageCreate(ImageBase):
    product_id: str


class Image(ImageCreate):
    id: int
    user_id: int
    is_downloaded: bool
    class Config:
        orm_mode = True

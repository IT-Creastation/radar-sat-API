from pydantic import BaseModel
from typing import List


class ImageBase(BaseModel):
    path: str
    name: str


class ImageCreate(ImageBase):
    pass


class Image(ImageBase):
    id: int
    path:str
    user_id: int
    name:str
    class Config:
        orm_mode = True
class UserViewer(BaseModel):
    id: int
    email:str
    images: List[Image] = []
    class Config:
        orm_mode = True

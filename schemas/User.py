from typing import List
from pydantic import BaseModel

from Image import Image


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    images: List[Image] = []

    class Config:
        orm_mode = True

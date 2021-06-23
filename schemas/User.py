from typing import List
from pydantic import BaseModel



class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class ShowUser(UserBase):
    class Config:
        orm_mode = True



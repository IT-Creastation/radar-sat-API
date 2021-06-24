from typing import List,Optional
from pydantic import BaseModel
from sqlalchemy.sql.selectable import lateral



class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class patchUser(BaseModel):
    pass
class putUser(BaseModel):
   

    pass
class ShowUser(UserBase):
    class Config:
        orm_mode = True



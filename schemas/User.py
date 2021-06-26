from pydantic import BaseModel

from typing import Optional

class UserBase(BaseModel):
    email: Optional[str]
    satellite: str = None
    latitude: float = None
    longitude: float = None
    cloud_coverage: int = None
    download_image_from: str = None


class UserCreate(UserBase):
    password: str


class PatchUser(BaseModel):
    pass


class PutUser(UserBase):
    pass


class ShowUser(UserBase):
    id: int

    class Config:
        orm_mode = True

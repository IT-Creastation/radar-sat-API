from pydantic import BaseModel

from typing import Optional


class UserBase(BaseModel):
    email: Optional[str]


class UserCreate(UserBase):
    password: str


class PatchUser(BaseModel):
    satellite: str = None
    latitude: float = None
    longitude: float = None
    cloud_coverage: int = None
    download_image_from: str = None


class PutUser(PatchUser):
    pass


class ShowUser(PutUser):
    id: int

    class Config:
        orm_mode = True

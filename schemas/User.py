from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    satellite: str = None
    latitude: float = None
    longitude: float = None
    cloud_coverage: int = None


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

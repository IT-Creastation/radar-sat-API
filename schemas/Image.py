from pydantic import BaseModel

from User import User


class ImageBase(BaseModel):
    path: str
    name: str


class ImageCreate(ImageBase):
    pass


class Image(ImageBase):
    id: int

    user: User

    class Config:
        orm_mode = True

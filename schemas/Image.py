from pydantic import BaseModel


class ImageBase(BaseModel):
    path: str
    name: str


class ImageCreate(ImageBase):
    pass


class Image(ImageBase):
    id: int
    path: str
    user_id: int
    name: str
    is_downloaded: bool

    class Config:
        orm_mode = True

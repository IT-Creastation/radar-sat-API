from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status
from DB.database import get_db

from typing import List
from schemas.Image import Image, ImageCreate
from services.auth_services import get_current_user
from services import UserService


router = APIRouter(
    prefix="/users",
    dependencies=[Depends(get_current_user)],
    tags=["User images"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get(
            "/{id}/images",
            response_model=List[Image],
            status_code=status.HTTP_200_OK)
async def get_user_images(id: int, db: Session = Depends(get_db)):
    return UserService.get_user_images(db, id)


@router.put(
            "/{id}/images",
            response_model=Image,
            status_code=status.HTTP_201_CREATED)
async def create_user_image(id: int, request: ImageCreate, db: Session = Depends(get_db)):
    return UserService.store_user_image(db, request, id)

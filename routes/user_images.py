from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status
from DB.database import get_db

from typing import List
from schemas.Image import Image
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
    """
    <h5>Get all user images by providing the current user id as a prammetre</h5>
    <p style="margin-left:5%">It require one parametre {id} as string which represent the user id.</p>
    """
    return UserService.get_user_images(db, id)

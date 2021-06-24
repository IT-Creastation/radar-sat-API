from services.auth_services import get_current_user
from fastapi import HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from DB.database import get_db
from models.Image import Image
from models.User import User
router = APIRouter(
    tags=["images"],
    prefix="/images"
)


@router.get("/")
def get_images(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    images = db.query(Image).all()
    return images

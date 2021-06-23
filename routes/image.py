from fastapi import HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from DB.database import get_db
from models.Image import Image
router = APIRouter(
    tags=["images"]
)

@router.get("/images")
def get_images(db: Session = Depends(get_db)):
    images=db.query(Image).all()
    return images

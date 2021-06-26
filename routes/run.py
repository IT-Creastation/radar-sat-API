from services.UserService import index
from DB.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.ImageDownloader import handle_image_information
router = APIRouter(prefix="/run")


@router.post("/")
def handle_cron_request(db: Session = Depends(get_db)):
    """
    TODO:docs
    """
    try:
        users=index(db)
        print(users)
        return users
    except Exception as ex:
        print(ex)

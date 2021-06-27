import os
from pathlib import Path

from fastapi.responses import FileResponse
from services.UserService import update_image_status
from services.auth_services import get_current_user
from services.ImageDownloader import download_image as download
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from DB.database import get_db
from models.Image import Image
from models.User import User
from schemas.Image import Image as Im

router = APIRouter(
    tags=["images"],
    prefix="/images",
    # dependencies=[Depends(get_current_user)]
)


@router.get("/")
def get_images(db: Session = Depends(get_db)):
    images = db.query(Image).all()
    return images


@router.get("/{name}/download")
def dowload_image(name: str, db: Session = Depends(get_db)):
    try:
        image = db.query(Image).filter(Image.name == name).first()
        path = os.getcwd() + image.path.replace("./", "/")

        return FileResponse(path, filename=f"{image.name}.zip")

    except Exception as error:
        return error

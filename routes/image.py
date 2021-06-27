import os
from pathlib import Path

from starlette.responses import FileResponse
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


@router.get("/{name}/download", response_class=FileResponse)
def dowload_image(name: str, db: Session = Depends(get_db)):
    """
    <h5>Download one image by giving the API the name of the image which you would like download</h5>
    <p style="margin-left:5%">It require one parametre {name} as string which represent the image name that you want to download, <br/>
    the response is a file with extession {name}.zip</p>
    """
    try:
        image = db.query(Image).filter(Image.name == name).first()
        print(image)
        if image:
            # download(userId=image.user_id,imageId=image.product_id,imageTitle=image.name)
            image=update_image_status(db, image.id, True)
            # path=image.path.replace('./','')
            # path=os.path.join(os.getcwd(),path)
            return FileResponse('./auth.py')
    except Exception as error:
        return error

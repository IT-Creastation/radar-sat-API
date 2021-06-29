from schemas.Image import ImageCreate
from services.UserService import index, store_user_image
from DB.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.ImageDownloader import handle_image_information
router = APIRouter(prefix="/run")

import os
@router.post("/")
def handle_cron_request(db: Session = Depends(get_db)):
    """
    This endpoints triggers automatic download of users' images,
    shouldn't be used by clients.
    Left exposed for now for testing purposes
    """
    errors = []
    downloaded = []
    try:
        users = index(db)
        print(users)
        for user in users:
            print("Iterating over users, trying to download images infos")
            try:
                info = handle_image_information(
                    user.download_image_from,
                    {"lon": user.longitude, "lat": user.latitude},
                    user.cloud_coverage,
                    userId=user.id,
                    platformname=user.satellite)

                downloaded.append({user.id: info["title"]})

                try:
                    store_user_image(db, ImageCreate(
                        path=info["path"], name=info["title"], product_id=info["id"]), user_id=user.id)
                except Exception as e:
                    print("Couldn't save image to db")
                    print(e)
                    continue
            except Exception as ex:
                errors.append(ex)
                continue
        print(downloaded)
        return {
            "status": "batch operation successfully completed",
            "data": downloaded
        }
    except Exception as ex:
        errors.append(ex)
        return errors

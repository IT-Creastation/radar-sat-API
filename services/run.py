from schemas.Image import ImageCreate
from services.UserService import index, store_user_image
from sqlalchemy.orm import Session
from services.ImageDownloader import handle_image_information

def handle_cron_request(db: Session):
    """
    This endpoints triggers automatic download of users' images,
    shouldn't be used by clients.
    Left exposed for now for testing purposes

    NB: this function fetches all images from the given date till now 
    for every user. and returns names of all new images

    this doesn't download actual images, it saves only images metadata
    on the database, you can then download images later using the appropriate
    endpoint
    """
    errors = []
    response = []
    try:
        users = index(db)
        for user in users:
            print("Iterating over users, trying to download images infos")
            try:
                info = handle_image_information(
                    user.download_image_from,
                    {"lon": user.longitude, "lat": user.latitude},
                    user.cloud_coverage,
                    userId=user.id,
                    platformname=user.satellite)

                for id, image_data in info.items():
                    try:
                        store_user_image(
                            db,
                            ImageCreate(
                                path=image_data["path"],
                                name=image_data["title"],
                                product_id=id
                            ),
                            user_id=user.id
                        )

                        response.append({
                            "user_id": user.id,
                            "image_name": image_data["title"]
                        })
                        print(response)
                    except Exception as e:
                        db.rollback()
                        print(f"error saving image {image_data['title']} to Db")
                        print(e)
                        continue
            except Exception as ex:
                errors.append(ex)
                continue
        return {
            "status": "batch operation successfully completed",
            "data": response
        }
    except Exception as ex:
        errors.append(ex)
        return errors

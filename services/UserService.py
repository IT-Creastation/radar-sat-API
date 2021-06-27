from sqlalchemy.orm import Session

from models.User import User as UserModel
from models.Image import Image as ImageModel

from schemas import User as UserSchema
from schemas.Image import ImageCreate


def index(db: Session):
    return db.query(UserModel).all()


def view(db: Session, id: int):
    return db.query(UserModel).filter(UserModel.id == id).first()


def create(db: Session, user: UserSchema.UserCreate):
    # TODO: We should actually hash the password :p :p
    user.password = user.password + "qsfdkjn"

    user_model = UserModel(
        **UserSchema.dict()
    )

    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model


def update(db: Session, id: int, user: UserSchema.PutUser):
    db.query(UserModel).filter(UserModel.id == id).update(
                                        user.dict(exclude_unset=True))
    db.commit()
    return view(db, id)


def delete(db: Session, id: int):
    try:
        db.query(UserModel).filter(UserModel.id == id).delete()
        db.commit()
    except Exception as e:
        raise e


def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()


def get_user_images(db: Session, id: int):
    return db.query(ImageModel).filter(ImageModel.user_id == id).all()


def store_user_image(db: Session, request: ImageCreate, user_id):
    image = ImageModel(**request.dict(), user_id=user_id)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


def update_image_status(db: Session, id: int, status: bool):
    image = db.query(ImageModel).filter(ImageModel.id == id).first()
    image.is_downloaded = status
    db.commit()
    db.refresh(image)

    return image

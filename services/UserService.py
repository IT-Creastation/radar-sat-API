from sqlalchemy.orm import Session

from ..models.User import User as UserModel
from ..schemas.User import User as UserSchema


class UserService():

    def index(db: Session):
        return db.query(UserModel.User).all()

    def view(db: Session, id: int):
        return db.query(UserModel.User).filter(UserModel.id == id).first()

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

from fastapi import HTTPException
from DB.database import get_db
from sqlalchemy.orm.session import Session
from starlette import status
from schemas.User import ShowUser, PutUser
from fastapi import APIRouter, Depends
from models.User import User
from passlib.context import CryptContext
from services.auth_services import get_current_user
from typing import List
from services import UserService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(tags=["Users"],
                   prefix="/users",
                   dependencies=[Depends(get_current_user)])


@router.get("/", response_model=List[ShowUser])
def get_all_users(db: Session = Depends(get_db)):
    users = []

    try:
        users = UserService.index(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Error fetching all users {e}")
    else:
        return users


@router.get("/{id}", response_model=ShowUser)
def get_user_by_id(
                id: int,
                db: Session = Depends(get_db)
            ):
    try:
        user = db.query(User).filter(User.id == id).first()
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There's no user with the given {id}")
    else:
        return user


@router.patch("/{id}", response_model=ShowUser)
def update_user(
                        id: int,
                        request: PutUser,
                        db: Session = Depends(get_db),
                    ):

    user = UserService.update(db, id, request)

    if user:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"There's no user with the given {id}")


@router.delete("/{id}")
def delete_user(
                id: int,
                db: Session = Depends(get_db)
            ):
    try:
        UserService.delete(db, id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{e}")
    else:
        return True

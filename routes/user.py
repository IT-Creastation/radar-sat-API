from fastapi import HTTPException
from DB.database import get_db
from sqlalchemy.orm.session import Session
from schemas.User import UserCreate
from starlette import status
from schemas.Image import UserViewer
from fastapi import APIRouter, Depends, HTTPException
from models.User import User
from passlib.context import CryptContext
from services.auth_services import get_current_user
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(tags=["users"],
                   prefix="/user")


@router.get("/", response_model=UserViewer)
def get_current_user(current_user: User = Depends(get_current_user)):

    if current_user:
        return current_user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Oops somthing went wrong, try to loggin again! ")


@router.put("/", response_model=UserViewer)
def update_email_and_password(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == id).first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"There's no user with the given {id}")


@router.patch("/", response_model=UserViewer)
def update_email_or_password(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == id).first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"There's no user with the given {id}")


@router.delete("/", response_model=UserViewer)
def delete_account(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == id).first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"R=There's no user with the given {id}")
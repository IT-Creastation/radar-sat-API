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
    """
    Get all users, for admin managing purposes
    """
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
    """
    Get one user, for admin managing purposes
    """
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
    """
    Update user information, this endpoint is used for setting user config too.
    
    date: (type: string) date from which the search is done 
                        FORMAT: YYYYMMDD
                        EXAMPLE: 20150212

    location: (type: dictionary) containing two keys
                lon and lat of type float.
                EXAMPLE {lon: "-5", lat: "39.14"}

    cloudCoverage: (type: float) percentage of cloud
                      coverage of images.

    platformname: (type: string) choose the platform which
                    you want to downlow sat images from.</br>
                     for example:</br>
                         Sentinel-1</br>
                         Sentinel-2</br>
                         Sentinel-3</br>
                         Sentinel-4</br>

                    default Sentinel-1
    """
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
    """
    delete user account
    """
    try:
        UserService.delete(db, id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{e}")
    else:
        return True

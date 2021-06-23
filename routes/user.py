from fastapi import HTTPException
from DB.database import get_db
from sqlalchemy.orm.session import Session
from schemas.User import UserCreate
from starlette import status
from schemas.Image import UserViewer
from fastapi import APIRouter, Depends,HTTPException
from models.User import User
from passlib.context import CryptContext
from services.auth_services import get_current_user
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(tags=["users"])


@router.post("/user", response_model=UserViewer, status_code=status.HTTP_201_CREATED)
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    hashedPassword = pwd_context.hash(request.password)
    new_user = User(email=request.email, password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/user/{id}", response_model=UserViewer)
def get_current_user(id: int, db: Session = Depends(get_db),current_user:User=Depends(get_current_user)):
    user = db.query(User).filter(User.id == id).first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"R=There's no user with the given {id}")

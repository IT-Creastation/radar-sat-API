from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from services.auth_services import create_access_token
from starlette import status
from DB.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.auth import Login
from models.User import User
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(
    tags=["authentication"],
)


@router.post("/login")
def login(request: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username).first()
    print(user.password)
    print(request.password)
    if user:
        if pwd_context.verify(request.password,user.password):
            access_token = create_access_token(
                data={"sub": user.email})
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid email or password")

    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid credentials")

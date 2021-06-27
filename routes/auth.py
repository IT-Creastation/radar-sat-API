from schemas.User import UserCreate, ShowUser
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from services.auth_services import create_access_token
from starlette import status
from DB.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.User import User
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(
    tags=["authentication"],
)


@router.post("/login")
def login(
        request: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    """
    <h5>Authentication</h5>
    <p>The sat-image-api provide a high level authentication security based on Oauth2, first you must create a user account via this <a href="/docs#/authentication/create_user_user_post">endpoint</a> or read the doc how to <a href="/redoc#operation/create_user_user_post">create use</a> </p>
    <hr/>
    <h5>username :</h5>
    <p style="margin-left:5%">(String,Required):Your name provided when you have created a new account</p>
    <h5>password :</h5>
    <p style="margin-left:5%">(String,Required):Your account password </p>
    """    
    user = db.query(User).filter(User.email == request.username).first()
    if user:
        if pwd_context.verify(request.password, user.password):
            access_token = create_access_token(
                data={"sub": user.email})
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Invalid email or password"
            )

    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Invalid credentials"
    )


@router.post(
    "/user",
    response_model=ShowUser,
    status_code=status.HTTP_201_CREATED)
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    """
    <p>The RADAR_API provide a high level authentication security based on Oauth2, first you must create a user account via this <a href="/docs#/authentication/create_user_user_post">endpoint</a> or read the doc how to <a href="/redoc#operation/create_user_user_post">create use</a> </p>
    <hr/>
    <h5>username :</h5>
    <p style="margin-left:5%">(String,Required):Your account username, we reccomend you to use your real email</p>
    <h5>password :</h5>
    <p style="margin-left:5%">(String,Required):Your password, we recommend to use a strong password and at least 6 characters</p>
    """
    hashedPassword = pwd_context.hash(request.password)
    new_user = User(email=request.email, password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

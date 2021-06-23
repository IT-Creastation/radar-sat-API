from schemas.auth import TokenData
from fastapi import Depends, HTTPException, status
from typing import Optional
from datetime import timedelta, datetime
from jose import JWTError, jwt
import os
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=2880)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv(
        "SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt


def verifyToken(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"),
                             algorithms=[os.getenv("ALGORITHM")])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    return verifyToken(token, credentials_exception)

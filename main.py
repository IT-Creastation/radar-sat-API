from DB.database import Base, get_db, engine
from fastapi import FastAPI, Depends, status, HTTPException
# import uvicorn
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from schemas.User import UserCreate
from schemas.Image import UserViewer
from models.User import User
from models.Image import Image
from passlib.context import CryptContext
from routes import image, user,auth
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
load_dotenv()
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(auth.router)
app.include_router(image.router)
app.include_router(user.router)



# if __name__ == '__main__':
#     uvicorn.run('main:app', host='127.0.0.1', port=8000)

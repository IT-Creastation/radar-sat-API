from fastapi import FastAPI
# import uvicorn
from dotenv import load_dotenv
from passlib.context import CryptContext
from DB.database import Base, engine
from routes import image, user, auth
import uvicorn


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv()

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

# Registering routes
app.include_router(auth.router)
app.include_router(image.router)
app.include_router(user.router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000)

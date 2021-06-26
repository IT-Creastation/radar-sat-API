from fastapi import FastAPI
from dotenv import load_dotenv
from DB.database import Base, engine
import uvicorn
from routes import image, user, auth, user_images, user_config,run


load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Registering routes
app.include_router(auth.router)
app.include_router(image.router)
app.include_router(user.router)
app.include_router(user_images.router)
app.include_router(run.router)
app.include_router(user_config.router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000)

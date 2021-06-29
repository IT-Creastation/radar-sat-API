from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.responses import RedirectResponse
from DB.database import Base, engine
import uvicorn
from routes import image, user, auth, user_images, run
import os

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="sat-image-api",
                    description="This api provide a service of downloading free Sentinel satelite images for free, and support 4 first platform of sentinel",
                    version="1.0.0",)


@app.get("/")
def home_page():
    return RedirectResponse(url="/redoc")


# Registering routes
app.include_router(auth.router)
app.include_router(image.router)
app.include_router(user.router)
app.include_router(user_images.router)
app.include_router(run.router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=os.getenv("PORT"))

from services.run import handle_cron_request
from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.responses import RedirectResponse
from DB.database import Base, engine, get_db
import uvicorn
from routes import image, user, auth, user_images
import os
from fastapi_utils.tasks import repeat_every

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



@app.on_event("startup")
@repeat_every(seconds=60*60*24)
def remove_expired_tokens_task() -> None:
    try:
        handle_cron_request(db=get_db())
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=os.getenv("PORT"))

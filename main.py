from DB.database import Base, engine
from fastapi import FastAPI
# import uvicorn
from dotenv import load_dotenv

from routes import user

load_dotenv()
Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(user.router)

# if __name__ == '__main__':
#     uvicorn.run('main:app', host='127.0.0.1', port=8000)

from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv

load_dotenv() 
app = FastAPI()


@app.get("/")
def index():
    return {'message': 'hello world'}

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000)
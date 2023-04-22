import uvicorn
from fastapi import FastAPI

from app.router.auth import router as auth_router
from app.router.user import router as user_router
from app.router.hotel import router as hotel_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(hotel_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    # PYTHONPATH=$PWD python main.py
    # uvicorn main:app --reload

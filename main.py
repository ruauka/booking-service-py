import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.router.auth import router as auth_router
from app.router.user import router as user_router
from app.router.hotel import router as hotel_router
from app.router.room import router as room_router
from app.router.uploader import router as uploader_router
from app.router.booking import router as booking_router
from app.router.pages import router as pages_router

app = FastAPI()
# монтирование папки static
app.mount("/frontend/static", StaticFiles(directory="app/frontend/static"), "static")

# Подключение CORS, чтобы запросы к API могли приходить из браузера
origins = [
    # 3000 - порт, на котором работает фронтенд на React.js
    "http://localhost:3000",  # https://mysite.cpm
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)

app.include_router(auth_router)
app.include_router(uploader_router)
app.include_router(user_router)
app.include_router(hotel_router)
app.include_router(room_router)
app.include_router(booking_router)
app.include_router(pages_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    # PYTHONPATH=$PWD python main.py
    # uvicorn main:app --reload

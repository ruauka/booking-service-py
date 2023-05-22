import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin_panel.auth import authentication_backend
from app.admin_panel.views import UserAdmin, BookingAdmin, HotelAdmin, RoomAdmin
from app.storage.database import engine
from config import cfg
from app.router.auth import router as auth_router
from app.router.user import router as user_router
from app.router.hotel import router as hotel_router
from app.router.room import router as room_router
from app.router.uploader import router as uploader_router
from app.router.booking import router as booking_router
from app.router.pages import router as pages_router

app = FastAPI()

# регистрация хендлеров
app.include_router(auth_router)
app.include_router(uploader_router)
app.include_router(user_router)
app.include_router(hotel_router)
app.include_router(room_router)
app.include_router(booking_router)
app.include_router(pages_router)

# монтирование папки static
app.mount("/frontend/static", StaticFiles(directory="app/frontend/static"), "static")
# Подключение CORS, чтобы запросы к API могли приходить из браузера
origins = [
    # 3000 - порт, на котором работает фронтенд на React.js
    "http://localhost:3000",  # https://mysite.cpm
]
# параметры CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)


# startup, shutdown - события fastapi
@app.on_event("startup")
async def startup():
    """
    Коннект с redis.
    redis-cli
    keys *
    """
    redis = aioredis.from_url(cfg.redis_url, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="booking-cache")


# Подключение админки
admin = Admin(app, engine, authentication_backend=authentication_backend)

# регистрация вьюх админки
admin.add_view(UserAdmin)
admin.add_view(HotelAdmin)
admin.add_view(RoomAdmin)
admin.add_view(BookingAdmin)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    # PYTHONPATH=$PWD python main.py
    # uvicorn main:app --reload

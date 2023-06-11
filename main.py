import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin_panel.auth import authentication_backend
from app.admin_panel.views import BookingAdmin, HotelAdmin, RoomAdmin, UserAdmin
from app.logger import logger
from app.router.auth import router as auth_router
from app.router.booking import router as booking_router
from app.router.hotel import router as hotel_router
from app.router.pages import router as pages_router
from app.router.room import router as room_router
from app.router.uploader import router as uploader_router
from app.router.user import router as user_router
from app.storage.database import engine
from config import cfg
from prometheus_fastapi_instrumentator import Instrumentator

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


@app.middleware("http")
async def request_time_count(request: Request, next):
    """
    Middleware для запросов.
    :param request: тело запроса
    :param next: хендлер
    """
    start_time = time.time()
    response = await next(request)
    process_time = time.time() - start_time

    extra = {
        "status_code": response.status_code,
        "duration": round(process_time, 4),
    }
    if response.status_code == 422:
        logger.error(msg="failed validation", extra=extra)
        return response

    if response.status_code in [400, 401, 403, 500]:
        return response
    else:
        logger.info(msg="success", extra=extra)

    return response


# логгирование ошибок в SENTRY
# https://docs.sentry.io/platforms/python/guides/fastapi/
# if settings.MODE != "TEST":
#     sentry_sdk.init(
#         dsn=settings.SENTRY_DSN,
#         traces_sample_rate=1.0,
#     )


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


# Подключение Prometheus
instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)

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

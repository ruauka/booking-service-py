import shutil

import sqlparse
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import admin_check
from app.storage.database import get_session
from app.storage.uploader import upload_sql_queries
from app.tasks.tasks import picture_compression

# регистрация роута загрузчика
router = APIRouter(
    prefix="/upload",
    tags=["Uploader"],
)


@router.post("/sql", dependencies=[Depends(admin_check)])
async def upload_from_sql_file(
        file: UploadFile,
        session: AsyncSession = Depends(get_session)
):
    """
    Доступно под ролью - админ.
    Хендлер загрузки в БД sql-файла.
    :param file: файл с sql запросами
    :param session: async сессия БД
    :return: информационное сообщение
    """
    # сырой вектор
    byte_queries: bytes = await file.read()
    queries: list[str] = sqlparse.split(
        sqlparse.format(
            byte_queries.decode("utf-8"),
            strip_comments=True)
    )
    await upload_sql_queries(session, queries)
    return "sql scripts loaded successfully"


@router.post("/image/hotel", dependencies=[Depends(admin_check)])
async def add_hotel_image(
        name: int,
        file: UploadFile,
):
    """
    Доступно под ролью - админ.
    Хендлер загрузки в проект фото гостиниц, форматы: JPEG, PNG, WEBP.
    :param name: id фото
    :param file: файл
    :return: информационное сообщение
    """
    image_path = f"app/frontend/static/images/hotels/{name}.webp"
    with open(image_path, "wb+") as file_object:
        # Сохраняем файл в локальное хранилище
        shutil.copyfileobj(file.file, file_object)
    # фоновый вызов celery
    picture_compression.delay(image_path)
    return "file loaded successfully"

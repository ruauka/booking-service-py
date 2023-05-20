import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from config import cfg
from app.tasks.engine import celery


@celery.task
def picture_compression(path: str):
    """
    Фоновая задача сжатия картинок.
    :param path: путь к файлу
    """
    # конвертация строки в объект Path
    image_path = Path(path)
    image = Image.open(image_path)
    for width, height in [
        (1000, 500),
        (200, 100)
    ]:
        resized_img = image.resize(size=(width, height))
        resized_img.save(f"app/frontend/static/images/hotels/resized/{width}_{height}_{image_path.name}")

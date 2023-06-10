import smtplib
from pathlib import Path
from typing import List

from PIL import Image
from pydantic import EmailStr

from app.tasks.email_templates import create_booking_confirmation_template
from app.tasks.engine import celery
from config import cfg


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


@celery.task
def send_booking_confirmation_email(booking: dict, email_to: EmailStr, room_name, hotel_name):
    """
    Фоновая задача отправки подтверждения бронирования номера на почту пользователя.
    :param hotel_name: название гостиницы
    :param room_name: название номера
    :param booking: словарь из БД
    :param email_to: почта пользователя
    """
    msg_content = create_booking_confirmation_template(booking, email_to, room_name, hotel_name)

    with smtplib.SMTP_SSL(cfg.SMTP_HOST, cfg.SMTP_PORT) as server:
        server.login(cfg.SMTP_GMAIL, cfg.SMTP_PASSWORD)
        server.send_message(msg_content)

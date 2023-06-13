from email.message import EmailMessage

from pydantic import EmailStr

from config import cfg


def create_booking_confirmation_template(booking: dict, email_to: EmailStr, room_name, hotel_name) -> EmailMessage:
    """
    Шаблон подтверждения бронирования.
    :param hotel_name: название гостиницы
    :param room_name: название номера
    :param booking: словарь из БД
    :param email_to: почта пользователя
    :return: шаблон
    """
    email = EmailMessage()

    email["To"] = email_to
    email["From"] = cfg.SMTP_GMAIL
    email["Subject"] = "Подтверждение бронирования"

    email.set_content(
        f"""
            <h1>Подтвердите бронирование</h1>
            Номер: <b>{room_name}</b><br>
            Отель: <b>{hotel_name}</b><br>
            Даты: с <b>{booking["date_from"]}</b> по <b>{booking["date_to"]}</b> на <b>{booking["total_days"]}</b> дней.<br>
            Общая стоимость: <b>{booking["total_cost"]}</b> т.р.
        """,
        subtype="html"
    )

    return email

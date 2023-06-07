from email.message import EmailMessage

from pydantic import EmailStr

from config import cfg


def create_booking_confirmation_template(booking: dict, email_to: EmailStr) -> EmailMessage:
    """
    Шаблон подтверждения бронирования.
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
            Вы забронировали отель с {booking["date_from"]} по {booking["date_to"]} на {booking["total_days"]} дней.
            Общая стоимость - {booking["total_cost"]} т.р.
        """,
        subtype="html"
    )

    return email

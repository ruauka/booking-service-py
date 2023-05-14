from typing import Optional, Any, List
from pydantic import BaseModel, Json
from datetime import date


class BookingUpdateRequest(BaseModel):
    """
    Валидационная схема входящего запроса полей обновления бронирования.
    """
    room_id: Optional[int]
    date_from: Optional[date]
    date_to: Optional[date]

    def is_empty(self) -> bool:
        """
        Проверка на пустые поля.
        :return: bool
        """
        return not any(vars(self).values())


class BookingResponse(BaseModel):
    """
    Валидационная схема исходящего запроса полей бронирования.
    """
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    # парсинг ответа sqlalchemy в pydantic
    class Config:
        orm_mode = True

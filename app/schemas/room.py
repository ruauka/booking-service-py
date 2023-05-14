from typing import Optional, Any, List
from pydantic import BaseModel, Json


class RoomRequest(BaseModel):
    """
    Валидационная схема входящего запроса полей комнаты.
    """
    hotel_id: int
    name: str
    description: str
    price: int
    services: Optional[List[str]]
    quantity: int
    image_id: Optional[int]


class RoomUpdateRequest(BaseModel):
    """
    Валидационная схема входящего запроса полей обновления комнаты.
    """
    hotel_id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    price: Optional[int]
    services: Optional[List[str]]
    quantity: Optional[int]
    image_id: Optional[int]

    def is_empty(self) -> bool:
        """
        Проверка на пустые поля.
        :return: bool
        """
        return not any(vars(self).values())


class RoomResponse(BaseModel):
    """
    Валидационная схема исходящего запроса полей комнаты.
    """
    id: str
    name: str
    description: str

    # парсинг ответа sqlalchemy в pydantic
    class Config:
        orm_mode = True

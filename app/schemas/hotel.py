from typing import Optional, Any, List
from pydantic import BaseModel, Json


class HotelRequest(BaseModel):
    """
    Валидационная схема входящего запроса полей гостиницы.
    """
    name: str
    location: str
    services: Optional[List[str]]
    rooms_quantity: int
    image_id: Optional[int]


class HotelUpdateRequest(BaseModel):
    """
    Валидационная схема входящего запроса полей обновления гостиницы.
    """
    name: Optional[str]
    location: Optional[str]
    services: Optional[List[str]]
    rooms_quantity: Optional[int]
    image_id: Optional[int]

    def is_empty(self) -> bool:
        """
        Проверка на пустые поля.
        :return: bool
        """
        return not any(vars(self).values())


class HotelResponse(BaseModel):
    """
    Валидационная схема исходящего запроса полей гостиницы.
    """
    id: str
    name: str

    # парсинг ответа sqlalchemy в pydantic
    class Config:
        orm_mode = True

from app.models.hotel import Hotel
from app.storage.dao import BaseDAO


class HotelDAO(BaseDAO):
    """
    Класс для использования DAO методов.
    """
    model = Hotel

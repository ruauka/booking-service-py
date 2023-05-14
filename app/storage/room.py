from app.models.room import Room
from app.storage.dao import BaseDAO


class RoomDAO(BaseDAO):
    """
    Класс для использования DAO методов.
    """
    model = Room

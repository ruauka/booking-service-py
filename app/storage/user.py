from app.models.user import User
from app.storage.dao import BaseDAO


class UserDAO(BaseDAO):
    """
    Класс для использования DAO методов.
    """
    model = User

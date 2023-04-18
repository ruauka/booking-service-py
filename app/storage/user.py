from app.models import User
from app.storage.dao import BaseDAO


class UserDAO(BaseDAO):
    model = User

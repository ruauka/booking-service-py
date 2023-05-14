from typing import Optional
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBearer

from app.models.user import User
from app.storage.user import UserDAO
from config import cfg


security = HTTPBearer()

# хэш-движок
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Хэширование пароля.
    :param password: пароль пользователя
    :return: хешированный пароль
    """
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    """
    Проверка на идентичность хэшированного пароля из БД и пароля введенного пользователем.
    :param plain_password: пароль пользователя
    :param hashed_password: хэшированный пароль из БД
    :return: bool
    """
    return pwd_context.verify(plain_password, hashed_password)


async def verify_user(session: AsyncSession, email: EmailStr, password: str) -> Optional[User]:
    """
    Аутентификация пользователя.
    :param session: async сессия БД
    :param email: email пользователя
    :param password: пароль пользователя
    :return: объект пользователя
    """
    user = await UserDAO.get_one(session, email=email)
    if not (user and verify_password(password, user.hashed_password)):
        return None

    return user


def create_JWT_token(data: dict) -> str:
    """
    Создание JWT-токена.
    :param data: словарь с id пользователя - {"sub": str(user.id)}
    :return: JWT-токен
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, cfg.secret_key, cfg.sha_algorithm,
    )

    return encoded_jwt

# from secrets import token_bytes
# from base64 import b64encode
# salt = b64encode((token_bytes(32).decode()))

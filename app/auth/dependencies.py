from typing import Dict, Optional
from fastapi import Depends, Request
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import TokenAbsentErr, JWTExpiredErr, IncorrectJWTFormatErr, UnauthorizedUserErr, NoAdminErr, \
    UnknownJWTPareErr
from app.models.user import User
from app.storage.database import get_session
from app.storage.user import UserDAO
from config import cfg


def get_token(request: Request) -> Optional[str]:
    """
    Получение JWT-токена из куки.
    :param request: входящий запрос
    :return: JWT-токен
    """
    token = request.cookies.get("JWT")
    if not token:
        raise TokenAbsentErr

    return token


def check_token(token: str = Depends(get_token)) -> Optional[dict]:
    """
    Проверка на валидность JWT-токена.
    :param token: JWT-токен
    :return: словарь с id пользователя {"sub": user.id}
    """
    try:
        # expire проверяется jwt.decode
        payload = jwt.decode(
            token, cfg.secret_key, cfg.sha_algorithm,
        )
    except ExpiredSignatureError:
        raise JWTExpiredErr
    except JWTError:
        raise IncorrectJWTFormatErr
    except Exception:
        raise UnknownJWTPareErr

    return payload


async def auth_user(
        session: AsyncSession = Depends(get_session),
        payload: Dict = Depends(check_token),
) -> User:
    """
    Авторизация пользователя.
    :param session: async сессия БД
    :param payload: словарь с id пользователя {"sub": user.id}
    :return: пользователь из БД
    """
    user_id: str = payload.get("sub")
    if not user_id:
        raise UnauthorizedUserErr

    user = await UserDAO.get_one(session, id=int(user_id))
    if not user:
        raise UnauthorizedUserErr

    return user


async def admin_check(user: User = Depends(auth_user)):
    """
    Проверка роли 'админ'.
    :param user: Авторизованный пользователь.
    """
    if not user.admin:
        raise NoAdminErr

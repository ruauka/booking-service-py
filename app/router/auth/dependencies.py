from typing import Dict, Optional

from fastapi import Depends, Request
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import TokenAbsentErr, JWTExpiredErr, IncorrectJWTFormatErr, NoUserErr
from app.models.user import User
from app.storage.database import get_session
from app.storage.user import UserDAO
from config import cfg


def get_token(request: Request) -> Optional[str]:
    token = request.cookies.get("access_token")
    if not token:
        raise TokenAbsentErr

    return token


def check_token(token: str = Depends(get_token)) -> Optional[dict]:
    try:
        # expire проверяется jwt.decode
        payload = jwt.decode(
            token, cfg.secret_key, cfg.sha_algorithm,
        )
    except ExpiredSignatureError:
        raise JWTExpiredErr
    except JWTError:
        raise IncorrectJWTFormatErr

    return payload


async def auth_user(
        session: AsyncSession = Depends(get_session),
        payload: Dict = Depends(check_token),
) -> User:
    user_id: str = payload.get("sub")
    if not user_id:
        raise NoUserErr

    user = await UserDAO.get_one(session, id=int(user_id))
    if not user:
        raise NoUserErr

    return user

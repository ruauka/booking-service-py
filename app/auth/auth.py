from typing import Optional
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.storage.user import UserDAO
from config import cfg

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def verify_user(session: AsyncSession, email: EmailStr, password: str) -> Optional[User]:
    user = await UserDAO.get_one(session, email=email)
    if not (user and verify_password(password, user.hashed_password)):
        return None

    return user


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, cfg.secret_key, cfg.sha_algorithm,
    )

    return encoded_jwt

# from secrets import token_bytes
# from base64 import b64encode
# salt = b64encode((token_bytes(32).decode()))

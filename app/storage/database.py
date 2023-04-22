from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import Column, Integer

from config import cfg

# асинхронный движок алхимии
engine = create_async_engine(cfg.db_url)
# асинхронный генератор сессий для бд
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# асинсхронная сессия для бд
async def get_session() -> Generator:
    async with async_session_maker() as session:
        yield session


# аккумулирует в себе данные по моделям для миграций alembic
class Base(DeclarativeBase):

    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

    id = Column(Integer, primary_key=True)

from sqlalchemy import Column, Integer, NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr

from config import cfg

if cfg.MODE == "TEST":
    DATABASE_URL = cfg.db_url_test
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = cfg.db_url
    DATABASE_PARAMS = {}

# асинхронный движок алхимии
engine = create_async_engine(DATABASE_URL)  # **DATABASE_PARAMS
# асинхронный генератор сессий для бд
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    """
    Асинхронный генератор сессий соединений с БД.
    :return: асинхронная сессия
    """
    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    """
    Аккумулирует в себе данные по моделям для миграций alembic
    """

    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

    # одинаковые поля венесенные из всех моделей
    id = Column(Integer, primary_key=True)

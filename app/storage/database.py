from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import Column, Integer, NullPool

from config import cfg

# if cfg.MODE == "TEST":
#     DATABASE_URL = "sqlite+aiosqlite:///:memory:"
#     # DATABASE_PARAMS = {"poolclass": NullPool}
# else:
#     DATABASE_URL = cfg.db_url
#     # DATABASE_PARAMS = {}

# асинхронный движок алхимии
engine = create_async_engine(cfg.db_url)
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

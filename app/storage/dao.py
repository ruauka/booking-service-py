from typing import Any
import sqlalchemy.exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update

from app.errors import InstanceAlreadyExistsErr


class BaseDAO:
    model = None

    @classmethod
    async def add(cls, session: AsyncSession, data) -> Any:
        query = insert(cls.model).values(**data).returning(cls.model)
        result = await session.execute(query)
        await session.commit()
        return result.scalar_one_or_none()

    @classmethod
    async def get_one(cls, session: AsyncSession, **filters) -> Any:
        query = select(cls.model).filter_by(**filters)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls, session: AsyncSession, **filters) -> Any:
        query = select(cls.model).filter_by(**filters)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def update(cls, session: AsyncSession, data, **filters) -> Any:
        query = update(cls.model).filter_by(**filters).values(**data).returning(cls.model)
        try:
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()
        except sqlalchemy.exc.IntegrityError:
            raise InstanceAlreadyExistsErr

    @classmethod
    async def delete(cls, session: AsyncSession, **filters) -> Any:
        query = delete(cls.model).filter_by(**filters).returning(cls.model)
        result = await session.execute(query)
        await session.commit()
        return result.scalar_one_or_none()

# scalars() преобразует ответ алхимии к списку объектов модели
# (без scalars() вернется список из кортежей)
# return result.scalars().all() преобразует ответ клиенту в список из словарей
# словарь - объект модели, возвращенный из алхимии

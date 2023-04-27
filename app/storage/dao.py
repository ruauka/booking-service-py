from typing import Any
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update

from app.errors import InstanceAlreadyExistsErr


class BaseDAO:
    model = None

    @classmethod
    async def add(cls, session: AsyncSession, data: dict) -> Any:
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
    async def get_all(cls, session: AsyncSession) -> Any:
        query = select(cls.model)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def update(cls, session: AsyncSession, data, id) -> Any:
        query = update(cls.model).where(cls.model.id == id).values(**data).returning(cls.model)
        try:
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()
        except IntegrityError:
            raise InstanceAlreadyExistsErr

    @classmethod
    async def delete(cls, session: AsyncSession, id) -> Any:
        query = delete(cls.model).where(cls.model.id == id).returning(cls.model)
        result = await session.execute(query)
        await session.commit()
        return result.scalar_one_or_none()

# scalars() преобразует ответ алхимии к списку объектов модели
# (без scalars() вернется список из кортежей объектов алхимии)
# return result.scalars().all() преобразует ответ клиенту в список из словарей
# словарь - объект модели, возвращенный из алхимии

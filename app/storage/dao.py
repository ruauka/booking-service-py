from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert


class BaseDAO:
    model = None

    @classmethod
    async def add(cls, session: AsyncSession, data):
        query = insert(cls.model).values(**data)
        await session.execute(query)
        await session.commit()

    @classmethod
    async def get_one(cls, session: AsyncSession, **filters):
        query = select(cls.model).filter_by(**filters)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls, session: AsyncSession, **filters):
        query = select(cls.model).filter_by(**filters)
        result = await session.execute(query)
        return result.scalars().all()

# scalars() преобразует ответ алхимии к списку объектов модели
# (без scalars() вернется список из кортежей)
# return result.scalars().all() преобразует ответ клиенту в список из словарей
# словарь - объект модели, возвращенный из алхимии

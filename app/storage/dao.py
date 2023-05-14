from typing import Any
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update

from app.errors import InstanceAlreadyExistsErr, UnknownErr


class BaseDAO:
    """
    Data Access Object модель с универсальными CRUD методами.
    """
    model = None

    @classmethod
    async def add(cls, session: AsyncSession, data: dict) -> Any:
        """
        Добавление инстанса в БД.
        :param session: async сессия БД
        :param data: значение полей инстанса
        :return: объект добавленного в БД инстанса
        """
        query = insert(cls.model).values(**data).returning(cls.model)
        result = await session.execute(query)
        await session.commit()
        return result.scalar_one_or_none()

    @classmethod
    async def get_one(cls, session: AsyncSession, **filters) -> Any:
        """
        Получение инстанса из БД.
        :param session: async сессия БД
        :param filters: фильтры запроса
        :return: инстанс
        """
        query = select(cls.model).filter_by(**filters)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls, session: AsyncSession, **filters) -> Any:
        """
        Получение инстансов из БД.
        :param session: async сессия БД
        :param filters: фильтры запроса
        :return: инстансы
        """
        query = select(cls.model).filter_by(**filters)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def update(cls, session: AsyncSession, data, id) -> Any:
        """
        Обновление инстанса в БД.
        :param session: async сессия БД
        :param data: значение полей инстанса
        :param id: id инстанса
        :return: обновленный инстанс
        """
        query = update(cls.model).where(cls.model.id == id).values(**data).returning(cls.model)
        try:
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as err:
            if isinstance(err, SQLAlchemyError):
                raise InstanceAlreadyExistsErr
            elif isinstance(err, Exception):
                raise UnknownErr

    @classmethod
    async def delete(cls, session: AsyncSession, id) -> Any:
        """
        Обновление инстанса в БД.
        :param session: async сессия БД
        :param id: id инстанса
        :return: удаленный инстанс
        """
        query = delete(cls.model).where(cls.model.id == id).returning(cls.model)
        result = await session.execute(query)
        await session.commit()
        return result.scalar_one_or_none()

# scalars() преобразует ответ алхимии к списку объектов модели
# (без scalars() вернется список из кортежей объектов алхимии)
# return result.scalars().all() преобразует ответ клиенту в список из словарей
# словарь - объект модели, возвращенный из алхимии

# return result.mappings().one_or_none() - добавляет название таблицы в ответ

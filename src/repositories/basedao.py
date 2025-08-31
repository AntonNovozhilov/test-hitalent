from abc import ABC
from typing import Optional, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

T = TypeVar("T")


class BaseDAO(ABC):
    """Абстрактный базовый Data Access Object."""

    def __init__(self, model: Type[T]) -> None:
        """Инициализация объекта."""
        self.model = model

    async def create(self, data: Union[dict, BaseModel], session: AsyncSession) -> T:
        """Создать новый объект в базе данных."""
        if isinstance(data, BaseModel):
            data = data.model_dump()
        new_object = self.model(**data)
        session.add(new_object)
        await session.commit()
        await session.refresh(new_object)
        return new_object

    async def get_by_id(
        self,
        obj_id: UUID,
        session: AsyncSession,
    ) -> Optional[T]:
        """Получить объект по его ID."""
        data_object = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return data_object.scalar()

    async def get_all(self, session: AsyncSession) -> list[T]:
        """Получить список объектов с возможностью фильтрации."""
        data_objects = await session.execute(select(self.model))
        return data_objects.scalars().all()
    
    async def delete(
        self,
        obj,
        session: AsyncSession,
    ) -> None:
        """Удалить объект по его ID."""
        await session.delete(obj)
        await session.commit()

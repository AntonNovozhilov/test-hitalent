from typing import AsyncGenerator

from sqlalchemy import Column, UUID, DateTime, func
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import (
    declarative_base,
    declared_attr,
    sessionmaker,
)
from src.core.config import settings


class PreBase:
    """Базовый класс для всех моделей SQLAlchemy."""

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"

    id = Column(UUID, primary_key=True, default=uuid4)
    created_at = Column(DateTime, server_default=func.now())


Base = declarative_base(cls=PreBase)

engine = create_async_engine(url=settings.db_path)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_async_session() -> AsyncGenerator:
    """Асинхронный генератор для получения сессии БД."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

from sqlalchemy import select
from src.schemas.user import UserCreate
from src.core.user import get_password_hash
from src.repositories.basedao import BaseDAO
from src.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


class UserDAO(BaseDAO):
    """DAO для пользователей."""

    async def get_by_username(sekf, username: str, session: AsyncSession) -> User:
        """Проверка наличия пользователя по нику"""
        user = await session.execute(select(User).where(User.username == username))
        user = user.scalars().one_or_none()
        return user

    async def create(self, data: UserCreate, session: AsyncSession) -> User:
        """Создать нового пользователя в базе."""
        hash_pass = get_password_hash(data.password)
        new_user = User(
            username=data.username, hash_password=hash_pass
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user


user_dao = UserDAO(User)

from fastapi import HTTPException, status
from src.repositories.user import UserDAO
from src.schemas.user import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.user import user_dao



class UserService:
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    async def register_user(self, data: UserCreate, session: AsyncSession) -> UserCreate:
        user = await self.user_dao.get_by_username(data.username, session)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким username уже существует",
            )
        user = await user_dao.create(data, session)
        return user
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.servises.user import UserService
from src.core.db import get_async_session
from src.schemas.user import UserCreate, UserDB
from src.repositories.user import user_dao

router = APIRouter()


@router.get("/", response_model=list[UserDB])
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    """Получить список всех пользователей"""
    users = await user_dao.get_all(session)
    return users


@router.post("/register", response_model=UserDB)
async def register_user(
    data: UserCreate, session: AsyncSession = Depends(get_async_session)
):
    """Регистрация нового пользователя"""
    user = await user_dao.get_by_username(data.username, session)
    if not user:
        check_user = UserService(user_dao)
        new_user = await check_user.register_user(data, session)
    return new_user

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy import select
from src.models.user import User
from src.schemas.user import TokenData
from src.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db import get_async_session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_password(plain_password, hash_password):
    """Проверка пароля"""
    return pwd_context.verify(plain_password, hash_password)


def get_password_hash(password: str):
    """Хешируем пароль"""
    return pwd_context.hash(password)


async def get_user(username: str, session: AsyncSession) -> User:
    """Получить пользователя"""
    user = await session.execute(select(User).where(User.username == username))
    return user.scalar()


async def authenticate_user(username: str, password: str, session: AsyncSession):
    """Аутентификация пользователя"""
    user = await get_user(username, session=session)
    if not user:
        return False
    if not verify_password(password, user.hash_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Создать токен"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_JWT_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session=Depends(get_async_session)
):
    """Получить текущего пользователя"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_JWT_KEY, algorithms=[settings.ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(username=str(token_data.username), session=session)
    if user is None:
        raise credentials_exception
    return user

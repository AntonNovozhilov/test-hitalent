from pydantic import BaseModel, ConfigDict
from uuid import UUID


class Token(BaseModel):
    """Схема для токена"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Схема для получения токена"""

    username: str | None = None


class UserBase(BaseModel):
    """Схема для пользователя"""

    username: str


class UserCreate(BaseModel):
    """Схема для создания пользователя"""

    username: str
    password: str


class UserUpdate(UserCreate):
    """Схема для обновления пользователя"""


class UserDB(UserBase):
    """Схема для получения пользователя"""

    id: UUID

    model_config = ConfigDict(from_attributes=True)

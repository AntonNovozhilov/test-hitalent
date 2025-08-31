from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class AnswerBase(BaseModel):
    """Основная схема для ответа"""

    text: str

class AnswerCreate(AnswerBase):
    """Схема для создания ответа"""

    question_id: UUID
    user_id: UUID

    model_config = ConfigDict()


class AnswerDB(AnswerBase):
    """Схема для возврата ответа"""

    id: UUID
    question_id: UUID
    user_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

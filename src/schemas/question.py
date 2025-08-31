from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class QuestionBase(BaseModel):
    """Схема для вопроса"""

    text: str


class QuestionCreate(QuestionBase):
    """Схема для создания вопроса"""


class QuestionRead(QuestionBase):
    """Схема для создания вопроса"""

    answers: list[str]


class QuestionDB(QuestionBase):
    """Схема для возврата вопроса из БД"""

    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestionWithAnswers(QuestionDB):
    answers: list[QuestionDB] = []

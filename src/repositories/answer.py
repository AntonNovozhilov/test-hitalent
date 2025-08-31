from src.repositories.basedao import BaseDAO
from src.models.answer import Answer
from typing import TypeVar


T = TypeVar("T")


class AnswerDAO(BaseDAO):
    "DAO для вопросов."

answer_dao = AnswerDAO(Answer)

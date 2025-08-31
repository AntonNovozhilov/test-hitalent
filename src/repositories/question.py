from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.repositories.basedao import BaseDAO
from src.models.question import Question
from sqlalchemy.ext.asyncio import AsyncSession


class QuestionDAO(BaseDAO):
    "DAO для ответов."

    async def get_by_id(self, obj_id: UUID, session: AsyncSession) -> Question:
        """Получить объект по его ID с подгрузкой связей"""
        result = await session.execute(
            select(self.model)
            .options(selectinload(self.model.answers))
            .where(self.model.id == obj_id)
        )
        return result.scalar_one_or_none()

question_dao = QuestionDAO(Question)

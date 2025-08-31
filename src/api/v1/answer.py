from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.core.db import get_async_session
from src.schemas.answer import AnswerBase, AnswerDB
from src.schemas.user import UserDB
from src.repositories.answer import answer_dao
from src.core.user import get_current_user
from uuid import UUID

router = APIRouter()


@router.post(
    "/questions/{question_id}/answers/",
    response_model=AnswerDB,
    dependencies=[Depends(get_current_user)],
)
async def create_answer(
    question_id: UUID,
    data: AnswerBase,
    user: UserDB = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Добавить ответ к вопросу"""
    data_for_create = {
        "text": data.text,
        "question_id": question_id,
        "user_id": user.id,
    }
    answer = await answer_dao.create(data_for_create, session)
    return answer


@router.get("/{id}", response_model=AnswerDB)
async def get_answer(id: UUID, session: AsyncSession = Depends(get_async_session)):
    """Получить ответ"""
    answer = await answer_dao.get_by_id(id, session)
    if not answer:
        raise HTTPException(status_code=404, detail="Ответа нет")
    return answer


@router.delete(
    "/{id}",
    dependencies=[Depends(get_current_user)],
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_answer(
    id: UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить ответ"""
    answer = await answer_dao.get_by_id(id, session)
    if not answer:
        raise HTTPException(status_code=404, detail="Ответа нет")
    if answer.user_id != user.id:
        raise HTTPException(status_code=403, detail="Нет прав на удаление")
    if answer.user_id == user.id:
        await answer_dao.delete(answer, session)

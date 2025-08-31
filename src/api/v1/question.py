from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_async_session
from src.repositories.question import question_dao
from src.schemas.question import (
    QuestionCreate,
    QuestionDB,
    QuestionWithAnswers,
)

router = APIRouter()


@router.get("/", response_model=list[QuestionDB])
async def get_questions(session: AsyncSession = Depends(get_async_session)):
    """Получить список всех вопросов"""
    result = await question_dao.get_all(session)
    return result


@router.post("/", response_model=QuestionDB)
async def create_question(
    data: QuestionCreate, session: AsyncSession = Depends(get_async_session)
):
    """Создать новый вопрос"""
    new_question = await question_dao.create(data, session)
    return new_question


@router.get("/{id}", response_model=QuestionWithAnswers)
async def get_question(id: UUID, session: AsyncSession = Depends(get_async_session)):
    """Получить вопрос и все его ответы"""
    question = await question_dao.get_by_id(id, session)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Вопроса нет."
        )
    return question


@router.delete("/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(id: UUID, session: AsyncSession = Depends(get_async_session)):
    """Удалить вопрос"""
    question = await question_dao.get_by_id(id, session)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Вопроса нет."
        )
    await question_dao.delete(question, session)

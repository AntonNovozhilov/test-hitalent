from fastapi import APIRouter
from src.api.v1.answer import router as answer
from src.api.v1.auth import router as auth
from src.api.v1.question import router as question
from src.api.v1.user import router as user


main_router = APIRouter()
main_router.include_router(answer, prefix="/answer", tags=["Answer"])
main_router.include_router(auth, prefix="/auth", tags=["Auth"])
main_router.include_router(question, prefix="/question", tags=["Question"])
main_router.include_router(user, prefix="/user", tags=["User"])

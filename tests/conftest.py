import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.db import Base, get_async_session
from src.core.user import get_current_user, get_password_hash
from src.main import app
from src.models.user import User
from src.models.question import Question
from src.models.answer import Answer
from uuid import uuid4

TEST_DB = "test_test.db"
SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{TEST_DB}"
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    class_=AsyncSession, autocommit=False, autoflush=False, bind=engine
)


async def override_db():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def test_user():
    async with TestingSessionLocal() as session:
        user = User(
            id=uuid4(), username="user1", hash_password=get_password_hash("hashedpass")
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


@pytest_asyncio.fixture
async def test_question(test_user):
    async with TestingSessionLocal() as session:
        question = Question(id=uuid4(), text="Тестовый вопрос")
        session.add(question)
        await session.commit()
        await session.refresh(question)
        return question


@pytest_asyncio.fixture
async def test_answer(test_user, test_question):
    async with TestingSessionLocal() as session:
        answer = Answer(
            id=uuid4(),
            text="Тестовый ответ",
            question_id=test_question.id,
            user_id=test_user.id,
        )
        session.add(answer)
        await session.commit()
        await session.refresh(answer)
        return answer


@pytest.fixture
def not_auth_test_client():
    app.dependency_overrides[get_async_session] = override_db
    app.dependency_overrides[get_current_user] = lambda: None
    with TestClient(app) as client:
        yield client


@pytest.fixture
def test_client(test_user):
    app.dependency_overrides[get_async_session] = override_db
    app.dependency_overrides[get_current_user] = lambda: test_user
    with TestClient(app) as client:
        yield client

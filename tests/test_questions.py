import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_question(test_client, test_user):
    data = {"text": "Новый тестовый вопрос"}
    response = test_client.post("/question/", json=data)
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response["text"] == "Новый тестовый вопрос"


@pytest.mark.asyncio
async def test_get_questions(test_client, test_question):
    response = test_client.get("/question/")
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert len(response) == 1
    assert response[0]["text"] == "Тестовый вопрос"


@pytest.mark.asyncio
async def test_get_question_by_id(test_client, test_question):
    response = test_client.get(f"/question/{test_question.id}")
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert "answers" in response
    assert response["text"] == "Тестовый вопрос"


@pytest.mark.asyncio
async def test_delete_question(test_client, test_question):
    response = test_client.delete(f"/question/{test_question.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_answer(test_client, test_user, test_question):
    data = {
        "text": "Новый тестовый ответ",
        "question_id": str(test_question.id),
        "user_id": str(test_user.id),
    }
    response = test_client.post(
        f"/answer/questions/{test_question.id}/answers/", json=data
    )
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response["text"] == "Новый тестовый ответ"


@pytest.mark.asyncio
async def test_get_answer_by_id(test_client, test_answer):
    response = test_client.get(f"/answer/{test_answer.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(test_answer.id)
    assert data["text"] == test_answer.text
    assert data["question_id"] == str(test_answer.question_id)


@pytest.mark.asyncio
async def test_delete_answer(test_client, test_answer):
    response = test_client.delete(f"/answer/{test_answer.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

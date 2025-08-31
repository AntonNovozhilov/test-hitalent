import pytest
from fastapi import status
from src.core.user import get_password_hash


@pytest.mark.asyncio
async def test_register_user(test_client):
    data = {"username": "username", "password": get_password_hash("password")}
    response = test_client.post("/user/register", json=data)
    assert response.status_code == status.HTTP_200_OK
    json_data = response.json()
    assert json_data["username"] == "username"
    assert "id" in json_data

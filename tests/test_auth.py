import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_read_users_me(test_client, test_user):
    response = test_client.get("/auth/me")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == test_user.username

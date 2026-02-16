import pytest

@pytest.mark.asyncio
async def test_login_success(client, admin_user):
    #Arrange
    login_data = {
        "username": admin_user.email,
        "password": "admin123"
    }
    #Act
    response = await client.post("/api/v1/auth/login", data=login_data)
    #Assert
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_inactive_user(client, inactive_user):
    #Arrange
    login_data = {
        "username": "inactive@test.com",
        "password": "inactive123"
    }
    #Act
    response = await client.post("/api/v1/auth/login", data=login_data)
    #Assert
    assert response.status_code == 400
    assert "detail" in response.json()
    assert response.json()["detail"] == "usuario desactivado. Solicitar reactivación de perfil"

@pytest.mark.asyncio
async def test_login_invalid_credentials(client, admin_user):
    #Arrange
    login_data = {
        "username": admin_user.email,
        "password": "weron_password"
    }
    #Act
    response = await client.post("/api/v1/auth/login", data=login_data)
    #Assert
    assert response.status_code == 401
    assert "detail" in response.json()




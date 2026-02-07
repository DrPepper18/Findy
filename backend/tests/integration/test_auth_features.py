import pytest
from httpx import AsyncClient
from app.utils.date_functions import calculate_birthdate

users = [
    {
        "email": "",
        "password": "", 
        "name": "", 
        "birthdate": None
    },
    {
        "email": "Late bird", 
        "password": "ihavetime", 
        "name": "Late bird", 
        "birthdate": calculate_birthdate(20).isoformat()
    },
    {
        "email": "naughtykid@mail.ru", 
        "password": "im18iswear", 
        "name": "Kid", 
        "birthdate": calculate_birthdate(17).isoformat()
    },
    {
        "email": "owner@mail.ru", 
        "password": "iamnormal", 
        "name": "Owner", 
        "birthdate": calculate_birthdate(27).isoformat()
    },
]

@pytest.mark.parametrize("user, status_code", [
    (users[0], 422),    # Пустые поля == 422
    (users[1], 422),    # email не в формате почты == 422
    (users[2], 422),    # Несовершеннолетний == 422
    (users[3], 201)     # OK == 201
])
@pytest.mark.asyncio
async def test_auth_register(client: AsyncClient, user, status_code):
    response = await client.post('/api/v1/auth/register', json=user)
    assert response.status_code == status_code


@pytest.mark.asyncio
async def test_auth_register_duplicate(client: AsyncClient):
    user = users[3]
    await client.post('/api/v1/auth/register', json=user)
    response = await client.post('/api/v1/auth/register', json=user)
    assert response.status_code == 409


@pytest.mark.parametrize("user, status_code", [
    # Пустые поля
    ({"email": "", "password": ""}, 422),
    # Несуществующий
    ({"email": "ghost@exists.not", "password": "password123"}, 404),
    # Неверный пароль
    ({"email": "wrongpass@mail.ru", "password": "correct_pass", "attempt": "wrong_pass"}, 401),
    # Успех
    ({"email": "good@user.ru", "password": "password123", "attempt": "password123"}, 200)
])
@pytest.mark.asyncio
async def test_auth_login(client: AsyncClient, user, status_code):
    if status_code in [401, 200]:
        await client.post('/api/v1/auth/register', json={
            "email": user["email"], 
            "password": user["password"],
            "name": "TestUser", "birthdate": calculate_birthdate(20).isoformat()
        })

    login_password = user.get("attempt", user["password"])
    
    response = await client.post('/api/v1/auth/login', json={
        "email": user["email"],
        "password": login_password
    })
    
    assert response.status_code == status_code


@pytest.mark.asyncio
async def test_tokens_refresh(client: AsyncClient):
    user = {
        "email": "good@user.ru", 
        "password": "password123",
        "name": "TestUser", 
        "birthdate": calculate_birthdate(20).isoformat()
    }
    response = await client.post('/api/v1/auth/register', json=user)
    refresh_token = response.cookies.get("refresh")
    access_token = response.json()["token"]
    assert refresh_token
    assert access_token

    client.cookies.set("refresh", refresh_token)
    response = await client.get('/api/v1/auth/refresh')
    new_refresh_token = response.cookies.get("refresh")
    new_access_token = response.json()["token"]
    assert new_refresh_token
    assert new_access_token

    # I still didn't add refresh token rotation.
    # So theoretically every generated RT
    # that isn't out of date will be valid. 
    # But OK i think nevermind rn.

    client.cookies.set("refresh", new_refresh_token)
    response = await client.get('/api/v1/auth/', headers={'Authorization': f"Bearer {new_access_token}"})
    user_data = response.json()
    assert user_data["name"] == user["name"]
    
    client.cookies.clear()
    response = await client.get('/api/v1/auth/refresh')
    assert response.status_code == 401
import pytest

users = [
    {"email": "", "password": "", "name": "", "age": None},
    {"email": "Late bird", "password": "ihavetime", "name": "Late bird", "age": 20},
    {"email": "naughtykid@mail.ru", "password": "im18iswear", "name": "Kid", "age": 17},
]

@pytest.mark.parametrize("user, status_code", [
    (users[0], 422),    # Пустые поля == 422
    (users[1], 422),    # email не в формате почты == 422
    (users[2], 201),    # OK == 201
])
@pytest.mark.asyncio
async def test_auth_register(client, user, status_code):
    response = await client.post('/api/v1/auth/register', json=user)
    assert response.status_code == status_code


@pytest.mark.asyncio
async def test_auth_register_duplicate(client):
    user = users[2]
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
async def test_auth_login(client, user, status_code):
    if status_code in [401, 200]:
        await client.post('/api/v1/auth/register', json={
            "email": user["email"], 
            "password": user["password"],
            "name": "TestUser", "age": 20
        })

    login_password = user.get("attempt", user["password"])
    
    response = await client.post('/api/v1/auth/login', json={
        "email": user["email"],
        "password": login_password
    })
    
    assert response.status_code == status_code
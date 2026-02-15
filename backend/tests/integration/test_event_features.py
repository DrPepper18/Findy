import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta
from app.utils.date_functions import calculate_birthdate

@pytest.mark.parametrize("name, datetime, min_age, max_age, status_code", [
    ("", (datetime.now()+timedelta(days=1)).isoformat(), None, None, 422),
    ("Настолки в Парке Горького", (datetime.now()-timedelta(days=1)).isoformat(), None, None, 422),
    ("Настолки в Парке Горького", (datetime.now()+timedelta(days=1)).isoformat(), 50, 40, 422),
    ("Настолки в Парке Горького", (datetime.now()+timedelta(days=1)).isoformat(), 18, None, 201),
])
@pytest.mark.asyncio
async def test_event_create(client: AsyncClient, name: str, datetime: str, min_age: int, max_age: int, status_code: int):
    user = {
        "email": "owner@gmail.com", 
        "password": "imaboss", 
        "name": "Owner", 
        "birthdate": calculate_birthdate(30).isoformat()
    }
    response = await client.post('/api/auth/register', json=user)
    token = response.json()["token"]

    event = {
        "name": name,
        "latitude": 55.727050,
        "longitude": 37.600500,
        "datetime": datetime,
        "min_age": min_age,
        "max_age": max_age,
        "capacity": 1
    }
    response = await client.post('/api/event/',
                                    headers={"Authorization": f"Bearer {token}"}, 
                                    json=event
    )
    assert response.status_code == status_code


@pytest.mark.asyncio
async def test_event_join(client: AsyncClient):
    users = [
        {"email": "owner@gmail.com", "password": "imaboss", "name": "Owner", "birthdate": calculate_birthdate(30).isoformat()},
        {"email": "naughtykid@mail.ru", "password": "im18iswear", "name": "Kid", "birthdate": calculate_birthdate(18).isoformat()},
        {"email": "niceguy@ya.ru", "password": "absolutelynormal", "name": "Normis", "birthdate": calculate_birthdate(20).isoformat()},
        {"email": "latebird@yandex.ru", "password": "ihavetime", "name": "Late bird", "birthdate": calculate_birthdate(20).isoformat()},
    ]
    tokens = list()
    
    for user in users:
        response = await client.post('/api/auth/register', json=user)
        tokens.append(response.json()["token"])

    event = {
        "name": "Настолки в Парке Горького",
        "latitude": 55.727050,
        "longitude": 37.600500,
        "datetime": (datetime.now() + timedelta(days=1)).isoformat(),
        "min_age": 19,
        "max_age": None,
        "capacity": 1
    }
    response = await client.post('/api/event/',
                                    headers={"Authorization": f"Bearer {tokens[0]}"}, 
                                    json=event
    )
    event_id = response.json()["event_id"]

    parameters = [
        {"token": tokens[1], "status_code": 403},   # Возраст ниже положенного == 403
        {"token": tokens[2], "status_code": 200},   # OK == 200
        {"token": tokens[3], "status_code": 409}    # Мест нет == 409
    ]

    for param in parameters:  
        response = await client.post(f'/api/book/{event_id}', headers={"Authorization": f"Bearer {param["token"]}"})
        assert response.status_code == param["status_code"]
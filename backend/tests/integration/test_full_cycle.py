import pytest
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_full_cycle(client):
    users = [
        {"email": "owner@gmail.com", "password": "imaboss", "name": "Owner", "age": 30},
        {"email": "latebird@yandex.ru", "password": "ihavetime", "name": "Late bird", "age": 20},
        {"email": "naughtykid@mail.ru", "password": "im18iswear", "name": "Kid", "age": 17},
    ]

    # Registration
    response = await client.post('/api/v1/auth/register', json=users[0])
    assert response.status_code == 201
    response = await client.post('/api/v1/auth/register', json=users[1])
    assert response.status_code == 201
    response = await client.post('/api/v1/auth/register', json=users[2])
    assert response.status_code == 201

    # Authentication (Owner)
    response = await client.post('/api/v1/auth/login', json={
        "email": users[0]["email"],
        "password": users[0]["password"]
    })
    token = response.json()["token"]
    assert token
    

    # Create an event
    event = {
        "name": "Настолки в Парке Горького",
        "latitude": 55.727050,
        "longitude": 37.600500,
        "datetime": (datetime.now() + timedelta(days=1)).isoformat(),
        "min_age": 18,
        "max_age": None,
        "capacity": 1
    }
    response = await client.post('/api/v1/event/',
                                    headers={"Authorization": f"Bearer {token}"}, 
                                    json=event
    )
    assert response.status_code == 201
    event_id = response.json()["event_id"]
    assert event_id
    

    # Authentication (Kid)
    response = await client.post('/api/v1/auth/login', json={
        "email": users[2]["email"],
        "password": users[2]["password"]
    })
    token = response.json()["token"]
    assert token

    # Join the event (failed: too young)
    response = await client.post(f'/api/v1/event/{event_id}/join', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

    # Check participation (expect: false)
    response = await client.get(f'/api/v1/event/{event_id}/join', headers={"Authorization": f"Bearer {token}"})
    assert response.json()["joined"] == False

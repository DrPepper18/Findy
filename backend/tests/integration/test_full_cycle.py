import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta
from app.utils.date_functions import calculate_birthdate


@pytest.mark.asyncio
async def test_full_cycle(client: AsyncClient):
    users = [
        {"email": "owner@gmail.com", "password": "imaboss", "name": "Owner", "birthdate": calculate_birthdate(30).isoformat()},
        {"email": "latebird@yandex.ru", "password": "ihavetime", "name": "Late bird", "birthdate": calculate_birthdate(20).isoformat()},
        {"email": "naughtykid@mail.ru", "password": "im18iswear", "name": "Kid", "birthdate": calculate_birthdate(18).isoformat()},
    ]

    tokens = []
    
    for user in users:
        # Registration
        response = await client.post('/api/v1/auth/register', json=user)
        assert response.status_code == 201

        # Login
        response = await client.post('/api/v1/auth/login', json={
            "email": user["email"],
            "password": user["password"]
        })
        assert response.status_code == 200
        token = response.json()["token"]
        tokens.append(token)
    

    # Create an event
    event = {
        "name": "Настолки в Парке Горького",
        "latitude": 55.727050,
        "longitude": 37.600500,
        "datetime": (datetime.now() + timedelta(days=1)).isoformat(),
        "min_age": 19,
        "max_age": None,
        "capacity": 1
    }
    response = await client.post('/api/v1/event/',
                                    headers={"Authorization": f"Bearer {tokens[0]}"}, 
                                    json=event
    )
    assert response.status_code == 201
    event_id = response.json()["event_id"]
    assert event_id
    

    # Join the event (failed: too young)
    response = await client.post(f'/api/v1/book/{event_id}', headers={"Authorization": f"Bearer {tokens[2]}"})
    assert response.status_code == 403

    # Check participation (expect: false)
    response = await client.get(f'/api/v1/book/{event_id}', headers={"Authorization": f"Bearer {tokens[2]}"})
    assert not response.json()["joined"]

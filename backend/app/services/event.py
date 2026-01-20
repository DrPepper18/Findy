from app.models.models import User, Event, Records
from app.models.database import AsyncSession
from app.services.user import get_user_info
from app.schemas import EventPostRequest
from fastapi import HTTPException
import sqlalchemy as db
from sqlalchemy import or_, and_
from datetime import datetime


async def get_all_events(user_data: User, session: AsyncSession) -> list:
    """
    SELECT * FROM events
    WHERE datetime >= NOW()
    AND ($age >= events.min_age OR events.min_age IS NULL)
    AND ($age <= events.max_age OR events.max_age IS NULL)
    """
    query_select = db.select(Event).where(
        and_(
            Event.datetime >= datetime.now(),
            or_(user_data.age >= Event.min_age, Event.min_age.is_(None)),
            or_(user_data.age <= Event.max_age, Event.max_age.is_(None))
        )
    )
    result = await session.execute(query_select)
    return result.scalars().fetchall()


async def add_new_event(data: EventPostRequest, session: AsyncSession) -> int:
    """
    INSERT INTO events ($name, $latitude, $longitude, ...)
    """
    new_event = Event(
        name=data.name,
        latitude=data.latitude,
        longitude=data.longitude,
        capacity=data.capacity,
        datetime=data.datetime.astimezone().replace(tzinfo=None),
        min_age=data.min_age,
        max_age=data.max_age
    )
    session.add(new_event)
    await session.commit()
    await session.refresh(new_event)

    return new_event.id


async def delete_expired_events(session: AsyncSession) -> None:
    """
    DELETE FROM records
    INNER JOIN events ON records.event_id = events.id
    WHERE events.datetime < NOW()

    DELETE FROM events
    WHERE events.datetime < NOW()
    """
    delete_records_query = db.delete(Records).where(
        Records.Event.in_(db.select(Event.id).where(Event.datetime < datetime.now()))
    )
    delete_events_query = db.delete(Event).where(Event.datetime < datetime.now())
    await session.execute(delete_records_query)
    await session.execute(delete_events_query)
    await session.commit()


async def get_event_info(id: int, session: AsyncSession) -> Event:
    """
    SELECT * FROM events WHERE id = $id
    """
    query_select = db.select(Event).where(Event.id == id)
    result = await session.execute(query_select)
    event_data = result.scalars().first()
    return event_data

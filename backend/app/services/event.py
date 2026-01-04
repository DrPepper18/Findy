from app.models.models import User, Event, Records
from app.models.database import async_session_maker
from app.services.user import get_user_info
from app.schemas import EventPostRequest
from fastapi import HTTPException
import sqlalchemy as db
from sqlalchemy import or_, and_
from datetime import datetime


async def get_event_signups(id: int) -> int:
    """
    SELECT COUNT(*) FROM records
    WHERE event_id = $event_id
    """
    async with async_session_maker() as session:
        query_select = db.select(db.func.count(Records.id)).where(Records.event_id == id)
        result = await session.execute(query_select)
        event_signups_count = result.scalar()
        return event_signups_count


async def get_all_events(user_data: User) -> list:
    """
    SELECT * FROM events
    WHERE datetime >= NOW()
    AND ($age >= events.min_age OR events.min_age IS NULL)
    AND ($age <= events.max_age OR events.max_age IS NULL)
    """
    async with async_session_maker() as session:
        query_select = db.select(Event).where(
            and_(
                Event.datetime >= datetime.now(),
                or_(user_data.age >= Event.min_age, Event.min_age.is_(None)),
                or_(user_data.age <= Event.max_age, Event.max_age.is_(None))
            )
        )
        result = await session.execute(query_select)
        return result.scalars().fetchall()


async def add_new_event(data: EventPostRequest):
    """
    INSERT INTO events ($name, $latitude, $longitude, ...)
    """
    async with async_session_maker() as session:
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


async def register_join(event_id: str, user_email: str):
    """
    INSERT INTO records ($event_id, $user_email)
    """
    async with async_session_maker() as session:
        new_record = Records(
            event_id=event_id,
            user_email=user_email
        )
        session.add(new_record)
        await session.commit()


async def join_user_to_event(event_id: int, user_email: str):
    user = await get_user_info(user_email)
    event = await get_event_info(event_id)
    event_load = await get_event_signups(event_id)

    if not event:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    if not((not event.min_age or event.min_age <= user.age) and (not event.max_age or user.age <= event.max_age)):
        raise HTTPException(status_code=403, detail="Возраст не подходит")
    if not (event.capacity > event_load):
        raise HTTPException(status_code=403, detail="Мест нет")

    await register_join(event_id, user.email)        


async def delete_expired_events():
    """
    DELETE FROM records
    INNER JOIN events ON records.event_id = Event.id
    WHERE datetime < NOW()

    DELETE FROM events
    WHERE datetime < NOW()
    """
    async with async_session_maker() as session:
        delete_records_query = db.delete(Records).where(
            Records.Event.in_(db.select(Event.id).where(Event.datetime < datetime.now()))
        )
        delete_events_query = db.delete(Event).where(Event.datetime < datetime.now())
        await session.execute(delete_records_query)
        await session.execute(delete_events_query)
        await session.commit()


async def get_event_info(id: int) -> Event:
    """
    SELECT * FROM events WHERE ID = $id
    """
    async with async_session_maker() as session:
        query_select = db.select(Event).where(Event.id == id)
        result = await session.execute(query_select)
        event_data = result.scalars().first()
        return event_data

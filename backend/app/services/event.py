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
        query_select = db.select(db.func.count(Records.ID)).where(Records.Event == id)
        result = await session.execute(query_select)
        event_signups_count = result.scalar()
        return event_signups_count


async def get_all_events(user_data: User) -> list:
    """
    SELECT * FROM events
    WHERE DateTime >= NOW()
    AND ($Age >= events.MinAge OR events.MinAge IS NULL)
    AND ($Age <= events.MaxAge OR events.MaxAge IS NULL)
    """
    async with async_session_maker() as session:
        query_select = db.select(Event).where(
            and_(
                Event.DateTime >= datetime.now(),
                or_(user_data.Age >= Event.MinAge, Event.MinAge.is_(None)),
                or_(user_data.Age <= Event.MaxAge, Event.MaxAge.is_(None))
            )
        )
        result = await session.execute(query_select)
        return result.scalars().fetchall()


async def add_new_event(data: EventPostRequest):
    """
    INSERT INTO events ($Name, $Longitude, $Latitude, ...)
    """
    async with async_session_maker() as session:
        new_event = Event(
            Name=data.Name,
            Longitude=data.Longitude,
            Latitude=data.Latitude,
            Capacity=data.Capacity,
            DateTime=data.DateTime.astimezone().replace(tzinfo=None),
            MinAge=data.MinAge,
            MaxAge=data.MaxAge
        )
        session.add(new_event)
        await session.commit()


async def register_join(event_id: str, user_email: str):
    """
    INSERT INTO records ($EventID, $UserEmail)
    """
    async with async_session_maker() as session:
        new_record = Records(
            Event=event_id,
            User=user_email
        )
        session.add(new_record)
        await session.commit()


async def join_user_to_event(event_id: int, user_email: str):
    user = await get_user_info(user_email)
    event = await get_event_info(event_id)
    event_load = await get_event_signups(event_id)

    if not event:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    if not((not event.MinAge or event.MinAge <= user.Age) and (not event.MaxAge or user.Age <= event.MaxAge)):
        raise HTTPException(status_code=403, detail="Возраст не подходит")
    if not (event.Capacity > event_load):
        raise HTTPException(status_code=403, detail="Мест нет")

    await register_join(event_id, user.Email)        


async def delete_expired_events():
    """
    DELETE FROM records
    INNER JOIN events ON records.Event = Event.ID
    WHERE DateTime < $datetime.now()

    DELETE FROM events
    WHERE DateTime < $datetime.now()
    """
    async with async_session_maker() as session:
        delete_records_query = db.delete(Records).where(
            Records.Event.in_(db.select(Event.ID).where(Event.DateTime < datetime.now()))
        )
        delete_events_query = db.delete(Event).where(Event.DateTime < datetime.now())
        await session.execute(delete_records_query)
        await session.execute(delete_events_query)
        await session.commit()


async def get_event_info(id: int) -> Event:
    """
    SELECT * FROM events WHERE ID = $id
    """
    async with async_session_maker() as session:
        query_select = db.select(Event).where(Event.ID == id)
        result = await session.execute(query_select)
        event_data = result.scalars().first()
        return event_data

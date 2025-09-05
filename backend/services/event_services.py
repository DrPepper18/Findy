from models.models import *
from models.database import *
from crypt_module import *
from datetime import datetime
from pydantic import BaseModel


class EventPostRequest(BaseModel):
    Name: str
    DateTime: datetime
    Longitude: float
    Latitude: float
    Capacity: int
    MinAge: int
    MaxAge: int

class EventJoinRequest(BaseModel):
    EventID: int


async def get_all_events() -> list:
    """
    SELECT * FROM events WHERE DateTime >= $current_date
    """
    async with async_session_maker() as session:
        query_select = db.select(Event).where(Event.DateTime >= datetime.now())
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
            DateTime=data.DateTime,
            MinAge=data.MinAge,
            MaxAge=data.MaxAge
        )
        session.add(new_event)
        await session.commit()


async def register_join(data: EventJoinRequest, userEmail: str):
    """
    INSERT INTO records ($EventID, $UserEmail)
    """
    async with async_session_maker() as session:
        new_record = Records(
            Event=data.EventID,
            User=userEmail
        )
        session.add(new_record)
        await session.commit()


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
            Records.Event.in_(
                db.select(Event.ID).where(Event.DateTime < datetime.now())
            )
        )
        delete_events_query = db.delete(Event).where(Event.DateTime < datetime.now())
        await session.execute(delete_records_query)
        await session.execute(delete_events_query)
        await session.commit()

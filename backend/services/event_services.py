from models.models import *
from models.database import *
from crypt_module import *
from datetime import datetime
from pydantic import BaseModel


class EventPostRequest(BaseModel):
    name: str
    date: datetime
    lon: float
    lat: float
    capacity: int
    minage: int
    maxage: int


async def get_all_events() -> list:
    """
    SELECT * FROM events
    """
    async with async_session_maker() as session:
        query_select = db.select(Event)
        result = await session.execute(query_select)
        return result.scalars().fetchall()

async def add_new_event(data: EventPostRequest):
    """
    INSERT INTO events (Name, Longitude, Latitude, ...)
    """
    async with async_session_maker() as session:
        new_event = Event(
            Name=data.name,
            Longitude=data.lon,
            Latitude=data.lat,
            MaxMembers=data.capacity,
            DateTime=data.date,
            MinAge=data.minage,
            MaxAge=data.maxage
        )
        session.add(new_event)
        await session.commit()
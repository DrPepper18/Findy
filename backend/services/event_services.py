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
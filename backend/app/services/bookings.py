from app.models.models import User, Event, Records
from app.models.database import AsyncSession
from app.services.user import get_user_info
from app.services.event import get_event_info
from app.schemas import EventPostRequest
from fastapi import HTTPException
import sqlalchemy as db
from sqlalchemy import or_, and_
from datetime import datetime


async def get_event_signups(id: int, session: AsyncSession) -> int:
    """
    SELECT COUNT(*) FROM records
    WHERE event_id = $event_id
    """
    query_select = db.select(db.func.count(Records.id)).where(Records.event_id == id)
    result = await session.execute(query_select)
    event_signups_count = result.scalar()
    return event_signups_count


async def get_join_status(event_id: int, user_email: str, session: AsyncSession) -> bool:
    """
    SELECT * FROM records
    WHERE event_id = $event_id AND user_email = $user_email
    """
    query_select = db.select(Records).where(
        (Records.event_id == event_id) & 
        (Records.user_email == user_email)
    )
    result = await session.execute(query_select)
    joined_data = result.scalars().first()
    return joined_data is not None


async def register_join(event_id: str, user_email: str, session: AsyncSession) -> None:
    """
    INSERT INTO records ($event_id, $user_email)
    """
    new_record = Records(
        event_id=event_id,
        user_email=user_email
    )
    session.add(new_record)
    await session.commit()


async def join_user_to_event(event_id: int, user_email: str, session: AsyncSession) -> None:
    user = await get_user_info(user_email, session=session)
    event = await get_event_info(event_id, session=session)
    event_load = await get_event_signups(event_id, session=session)

    if not event:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    if not((not event.min_age or event.min_age <= user.age) and (not event.max_age or user.age <= event.max_age)):
        raise HTTPException(status_code=403, detail="Возраст не подходит")
    if not (event.capacity > event_load):
        raise HTTPException(status_code=409, detail="Мест нет")

    await register_join(event_id=event_id, user_email=user_email, session=session)


async def cancel_join_to_event(event_id: int, user_email: str, session: AsyncSession) -> None:
    """
    DELETE FROM records WHERE event_id = $event_id AND user_email = $user_email
    """
    delete_record_query = db.delete(Records).where(
        (Records.user_email == user_email) & 
        (Records.event_id == event_id)
    )
    await session.execute(delete_record_query)
    await session.commit()
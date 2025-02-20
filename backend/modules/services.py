from .models import *
from .database import *
from .crypt import *
from datetime import datetime

async def register_user(email: str, passwordhash: str, name: str) -> str:
    async with async_session_maker() as session:
        new_user = User(
            Email=email,
            PasswordHash=passwordhash,
            Name=name,
        )
        session.add(new_user)
        await session.commit()
    jwttoken = await create_jwt_token(email=email)
    return jwttoken


async def get_password_hash(email: str) -> bytes:
    async with async_session_maker() as session:
        query_select = db.select(User).where(User.Email == email)
        result = await session.execute(query_select)
        user_data = result.scalars().first()
        return user_data.PasswordHash


async def login_check(email: str, password: str) -> str:
    passwordhash = await get_password_hash(email=email)
    if not passwordhash:
        return False
    success = await is_password_correct(password, passwordhash)
    if success:
        jwttoken = await create_jwt_token(email=email)
        return jwttoken
    else:
        return False


async def get_all_events() -> list:
    async with async_session_maker() as session:
        query_select = db.select(Event)
        result = await session.execute(query_select)
        return result.scalars().fetchall()

async def add_new_event(name: str, date: datetime, lon: float, lat: float, capacity: int, minage: int, maxage: int):
    async with async_session_maker() as session:
        new_event = Event(
            Name=name,
            Longitude=lon,
            Latitude=lat,
            MaxMembers=capacity,
            DateTime=date,
            MinAge=minage,
            MaxAge=maxage
        )
        session.add(new_event)
        await session.commit()
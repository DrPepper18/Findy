from fastapi import HTTPException
import sqlalchemy as db
from sqlalchemy.exc import IntegrityError
from app.models.models import User
from app.models.database import AsyncSession
from app.utils.security import create_jwt_token, create_password_hash, is_password_correct
from app.schemas import RegisterRequest, LoginRequest, EditUserInfoRequest


async def register_user(data: RegisterRequest, session: AsyncSession) -> str:
    query = db.select(User).where(User.email == data.email)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=409, 
            detail="Пользователь с таким email уже зарегистрирован"
        )

    password_hash = create_password_hash(password=data.password)
    new_user = User(
        email=data.email,
        password_hash=password_hash,
        name=data.name,
        birthdate=data.birthdate
    )
    session.add(new_user)

    try:
        await session.commit()
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при сохранении в базу")
    
    return data.email


async def get_password_hash(email: str, session: AsyncSession) -> bytes:
    query_select = db.select(User).where(User.email == email)
    result = await session.execute(query_select)
    user_data = result.scalars().first()

    if not user_data:
        raise HTTPException(status_code=404, detail="Not found")

    return user_data.password_hash


async def authenticate_user(data: LoginRequest, session: AsyncSession) -> str:
    password_hash = await get_password_hash(email=data.email, session=session)
    success = is_password_correct(data.password, password_hash)

    if not success:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return data.email
    

async def get_user_info(email: str, session: AsyncSession) -> User:
    query_select = db.select(User).where(User.email == email)
    result = await session.execute(query_select)
    user_data = result.scalars().first()
    return user_data


async def update_user_info(data: EditUserInfoRequest, email: str, session: AsyncSession) -> User:
    query_select = (
        db.update(User)
        .where(User.email == email)
        .values(
            name=data.name,
            birthdate=data.birthdate
        )
    )
    await session.execute(query_select)
    await session.commit()
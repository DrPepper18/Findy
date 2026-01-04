from app.models.models import User, Records
from app.models.database import async_session_maker
from app.crypt_module import create_jwt_token, create_password_hash, is_password_correct
from app.schemas import RegisterRequest, LoginRequest
import sqlalchemy as db


async def register_user(data: RegisterRequest) -> str:
    """
    INSERT INTO users ($email, $passwordhash, $name)
    """
    passwordhash = create_password_hash(password=data.password)
    async with async_session_maker() as session:
        new_user = User(
            email=data.email,
            password_hash=passwordhash,
            name=data.name,
            age=18
        )
        session.add(new_user)
        await session.commit()
    jwttoken = create_jwt_token(email=data.email)
    return jwttoken


async def get_password_hash(email: str) -> bytes:
    """
    SELECT passwordhash FROM users WHERE Email == $email
    """
    async with async_session_maker() as session:
        query_select = db.select(User).where(User.email == email)
        result = await session.execute(query_select)
        user_data = result.scalars().first()
        return user_data.password_hash


async def authenticate_user(data: LoginRequest) -> str:
    passwordhash = await get_password_hash(email=data.email)
    if not passwordhash:
        return False
    success = is_password_correct(data.password, passwordhash)
    if success:
        jwttoken = create_jwt_token(email=data.email)
        return jwttoken
    else:
        return False

    
async def get_join_status(event_id: int, user_email: str) -> bool:
    async with async_session_maker() as session:
        query_select = db.select(Records).where(
            (Records.event_id == event_id) & 
            (Records.user_email == user_email)
        )
        result = await session.execute(query_select)
        joined_data = result.scalars().first()
        return joined_data is not None
    

async def get_user_info(email: str) -> User:
    """
    SELECT * FROM users WHERE Email = $email
    """
    async with async_session_maker() as session:
        query_select = db.select(User).where(User.email == email)
        result = await session.execute(query_select)
        user_data = result.scalars().first()
        return user_data


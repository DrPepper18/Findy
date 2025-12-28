from app.models.models import User, Records
from app.models.database import async_session_maker
from app.crypt_module import create_jwt_token, create_password_hash, is_password_correct
from app.schemas import RegisterRequest, LoginRequest, CheckJoinRequest
import sqlalchemy as db


async def register_user(data: RegisterRequest) -> str:
    """
    INSERT INTO users ($email, $passwordhash, $name)
    """
    passwordhash = create_password_hash(password=data.password)
    async with async_session_maker() as session:
        new_user = User(
            Email=data.email,
            PasswordHash=passwordhash,
            Name=data.name,
            Age=18
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
        query_select = db.select(User).where(User.Email == email)
        result = await session.execute(query_select)
        user_data = result.scalars().first()
        return user_data.PasswordHash


async def login_check(data: LoginRequest) -> str:
    passwordhash = await get_password_hash(email=data.email)
    if not passwordhash:
        return False
    success = is_password_correct(data.password, passwordhash)
    if success:
        jwttoken = create_jwt_token(email=data.email)
        return jwttoken
    else:
        return False
    
async def join_check(data: CheckJoinRequest, userEmail: str) -> bool:
    async with async_session_maker() as session:
        query_select = db.select(Records).where(
            (Records.Event == data.EventID) & 
            (Records.User == userEmail)
        )
        result = await session.execute(query_select)
        joined_data = result.scalars().first()
        return joined_data is not None
    
async def get_user_info(email: str) -> User:
    """
    SELECT * FROM users WHERE Email = $email
    """
    async with async_session_maker() as session:
        query_select = db.select(User).where(User.Email == email)
        result = await session.execute(query_select)
        user_data = result.scalars().first()
        return user_data


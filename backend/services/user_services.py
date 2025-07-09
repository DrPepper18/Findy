from models.models import *
from models.database import *
from crypt_module import *
from datetime import datetime
from pydantic import BaseModel

# Схема запроса для регистрации
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class CheckJoinRequest(BaseModel):
    EventID: int


async def register_user(data: RegisterRequest) -> str:
    """
    INSERT INTO users ($email, $passwordhash, $name)
    """
    passwordhash = await create_password_hash(password=data.password)
    async with async_session_maker() as session:
        new_user = User(
            Email=data.email,
            PasswordHash=passwordhash,
            Name=data.name,
        )
        session.add(new_user)
        await session.commit()
    jwttoken = await create_jwt_token(email=data.email)
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
    success = await is_password_correct(data.password, passwordhash)
    if success:
        jwttoken = await create_jwt_token(email=data.email)
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

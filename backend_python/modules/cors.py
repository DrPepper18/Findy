from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .models import *
from .database import *
from .crypt import *


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


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Схема запроса для регистрации
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    interests: list

class LoginRequest(BaseModel):
    email: str
    password: str


@app.post("/api/v1/auth/register")
async def register(data: RegisterRequest):
    passwordhash = await create_password_hash(password=data.password)
    jwt_token = await register_user(
        email=data.email, 
        passwordhash=passwordhash,
        name=data.name
    )
    return {"message": "Registration successful", "token": jwt_token}


@app.post("/api/v1/auth/login")
async def login(data: LoginRequest):
    jwt_token = await login_check(email=data.email, password=data.password)
    if jwt_token:
        return {"message": "Registration successful", "token": jwt_token}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    

@app.get("/api/v1/events")
async def get_events():
    eventlist = await get_all_events()
    print('ALL EVENTS:', eventlist)
    return {"message": "Here will be your events", "events": eventlist}
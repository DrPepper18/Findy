from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.services import *
from config import YANDEX_API
from crypt_module import *

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

class EventPostRequest(BaseModel):
    name: str
    date: datetime
    lon: float
    lat: float
    capacity: int
    minage: int
    maxage: int


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
    return {"message": "Here will be your events", "events": eventlist}

@app.post("/api/v1/events")
async def new_event(data: EventPostRequest):
    await add_new_event(
        name=data.name, 
        date=data.date, 
        lon=data.lon, 
        lat=data.lat, 
        capacity=data.capacity, 
        minage=data.minage, 
        maxage=data.maxage
    )
    return {"message": "POST request is completed"}

@app.get("/api/v1/yandexmap")
async def get_api_key():
    return {"api_key": YANDEX_API}
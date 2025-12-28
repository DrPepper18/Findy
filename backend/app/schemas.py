from datetime import datetime
from pydantic import BaseModel


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class CheckJoinRequest(BaseModel):
    EventID: int


class EventPostRequest(BaseModel):
    Name: str
    DateTime: datetime
    Longitude: float
    Latitude: float
    Capacity: int
    MinAge: int | None = None
    MaxAge: int | None = None

class EventJoinRequest(BaseModel):
    EventID: int
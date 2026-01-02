from datetime import datetime
from pydantic import BaseModel, EmailStr, model_validator


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
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

    @model_validator(mode='after')
    def validate_ages(self):
        if self.MinAge > self.MaxAge:
            raise ValueError('Минимальный возраст не может быть больше максимального')
        return self
    
    @model_validator(mode='after')
    def validate_future_date(self):
        if self.DateTime.replace(tzinfo=None) < datetime.now():
            raise ValueError('Нельзя создать событие в прошлом')
        return self

class EventJoinRequest(BaseModel):
    EventID: int
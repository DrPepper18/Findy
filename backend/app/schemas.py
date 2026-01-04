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
    event_id: int


class EventPostRequest(BaseModel):
    name: str
    datetime: datetime
    longitude: float
    latitude: float
    capacity: int
    min_age: int | None = None
    max_age: int | None = None

    @model_validator(mode='after')
    def validate_ages(self):
        if self.min_age and self.max_age and self.min_age > self.max_age:
            raise ValueError('Минимальный возраст не может быть больше максимального')
        return self
    
    @model_validator(mode='after')
    def validate_future_date(self):
        if self.datetime.replace(tzinfo=None) < datetime.now():
            raise ValueError('Нельзя создать событие в прошлом')
        return self

class EventJoinRequest(BaseModel):
    event_id: int
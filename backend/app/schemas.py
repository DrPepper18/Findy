from datetime import date, datetime
from pydantic import BaseModel, EmailStr, model_validator


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    birthdate: date


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class EditUserInfoRequest(BaseModel):
    name: str
    birthdate: date


class EventPostRequest(BaseModel):
    name: str
    datetime: datetime
    longitude: float
    latitude: float
    capacity: int
    min_age: int | None = None
    max_age: int | None = None

    @model_validator(mode='after')
    def validate_name(self):
        if not(self.name and self.latitude and self.longitude and self.capacity):
            raise ValueError('Не все поля заполнены')
        return self
    
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

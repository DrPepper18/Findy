from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, AfterValidator, EmailStr, Field, model_validator
from app.utils.date_functions import calculate_age


CURFEW_BEGIN = 23
CURFEW_END = 5
AGE_LIMIT = 18
CAPACITY_LIMIT = 16


def validate_age(birthdate):
    if calculate_age(birthdate) < AGE_LIMIT:
        raise ValueError("Сервис предназначен для лиц старше 18 лет")
    return birthdate


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    birthdate: Annotated[datetime, AfterValidator(validate_age)]


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class EditUserInfoRequest(BaseModel):
    name: str
    birthdate: Annotated[datetime, AfterValidator(validate_age)]


class EventPostRequest(BaseModel):
    name: Annotated[str, Field(min_length=1)]
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
    def validate_datetime(self):
        if self.datetime.replace(tzinfo=None) < datetime.now():
            raise ValueError('Нельзя создать событие в прошлом')
        if self.datetime.hour >= CURFEW_BEGIN or self.datetime.hour < CURFEW_END:
            raise ValueError('Нельзя создавать события в период 23:00-05:00')
        return self
    
    @model_validator(mode="after")
    def validate_capacity(self):
        if self.capacity < 1 or self.capacity > CAPACITY_LIMIT:
            raise ValueError('Некорректное количество человек')
        return self

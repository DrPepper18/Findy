from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    BigInteger,
    ForeignKey,
    LargeBinary,
    Float,
    UniqueConstraint
)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    Email = Column(String(), primary_key=True)
    PasswordHash = Column(LargeBinary())
    Name = Column(String())

class Event(Base):
    __tablename__ = "events"
    ID = Column(BigInteger(), primary_key=True, autoincrement=True)
    Name = Column(String())
    Latitude = Column(Float())
    Longitude = Column(Float())
    DateTime = Column(DateTime())
    MinAge = Column(Integer())
    MaxAge = Column(Integer())
    Capacity = Column(Integer())

class Records(Base):
    __tablename__ = "records"
    Event = Column(ForeignKey(Event.ID), primary_key=True)
    User = Column(ForeignKey(User.Email))
    __table_args__ = (
        UniqueConstraint(Event, User, name='unique_record'),
    )
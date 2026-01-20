from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    BigInteger,
    ForeignKey,
    LargeBinary,
    Float,
    UniqueConstraint
)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    email = Column(String(), primary_key=True)
    password_hash = Column(LargeBinary())
    name = Column(String())
    age = Column(Integer())


class Event(Base):
    __tablename__ = "events"
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    name = Column(String())
    latitude = Column(Float())
    longitude = Column(Float())
    datetime = Column(DateTime())
    min_age = Column(Integer(), nullable=True)
    max_age = Column(Integer(), nullable=True)
    capacity = Column(Integer())


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    event_id = Column(ForeignKey(Event.id))
    user_email = Column(ForeignKey(User.email))
    __table_args__ = (
        UniqueConstraint(event_id, user_email, name='unique_record'),
    )

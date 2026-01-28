from sqlalchemy.orm import declarative_base
import sqlalchemy as sa


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.BigInteger(), primary_key=True, autoincrement=True)
    email = sa.Column(sa.String(), unique=True)
    password_hash = sa.Column(sa.LargeBinary())
    name = sa.Column(sa.String())
    birthdate = sa.Column(sa.Date())


class Event(Base):
    __tablename__ = "events"
    id = sa.Column(sa.BigInteger(), primary_key=True, autoincrement=True)
    name = sa.Column(sa.String())
    latitude = sa.Column(sa.Float())
    longitude = sa.Column(sa.Float())
    datetime = sa.Column(sa.DateTime())
    min_age = sa.Column(sa.Integer(), nullable=True)
    max_age = sa.Column(sa.Integer(), nullable=True)
    capacity = sa.Column(sa.Integer())


class Booking(Base):
    __tablename__ = "bookings"
    id = sa.Column(sa.BigInteger(), primary_key=True, autoincrement=True)
    event_id = sa.Column(sa.ForeignKey(Event.id))
    user_email = sa.Column(sa.ForeignKey(User.email))
    __table_args__ = (
        sa.UniqueConstraint(event_id, user_email, name='unique_record'),
    )

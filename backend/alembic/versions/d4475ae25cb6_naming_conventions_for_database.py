"""Naming conventions for database

Revision ID: d4475ae25cb6
Revises: 1531b9fcc2a0
Create Date: 2026-01-03 13:34:49.034307

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4475ae25cb6'
down_revision: Union[str, Sequence[str], None] = '1531b9fcc2a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('users', 'Name', new_column_name='name')
    op.alter_column('users', 'Email', new_column_name='email')
    op.alter_column('users', 'PasswordHash', new_column_name='password_hash')
    op.alter_column('users', 'Age', new_column_name='age')

    op.alter_column('events', 'ID', new_column_name='id')
    op.alter_column('events', 'Name', new_column_name='name')
    op.alter_column('events', 'Latitude', new_column_name='latitude')
    op.alter_column('events', 'Longitude', new_column_name='longitude')
    op.alter_column('events', 'DateTime', new_column_name='datetime')
    op.alter_column('events', 'MinAge', new_column_name='min_age')
    op.alter_column('events', 'MaxAge', new_column_name='max_age')
    op.alter_column('events', 'Capacity', new_column_name='capacity')

    op.alter_column('records', 'ID', new_column_name='id')
    op.alter_column('records', 'Event', new_column_name='event_id')
    op.alter_column('records', 'User', new_column_name='user_email')


def downgrade() -> None:
    op.alter_column('records', 'user_email', new_column_name='User')
    op.alter_column('records', 'event_id', new_column_name='Event')
    op.alter_column('records', 'id', new_column_name='ID')

    op.alter_column('events', 'capacity', new_column_name='Capacity')
    op.alter_column('events', 'max_age', new_column_name='MaxAge')
    op.alter_column('events', 'min_age', new_column_name='MinAge')
    op.alter_column('events', 'datetime', new_column_name='DateTime')
    op.alter_column('events', 'longitude', new_column_name='Longitude')
    op.alter_column('events', 'latitude', new_column_name='Latitude')
    op.alter_column('events', 'name', new_column_name='Name')
    op.alter_column('events', 'id', new_column_name='ID')

    op.alter_column('users', 'age', new_column_name='Age')
    op.alter_column('users', 'password_hash', new_column_name='PasswordHash')
    op.alter_column('users', 'email', new_column_name='Email')
    op.alter_column('users', 'name', new_column_name='Name')

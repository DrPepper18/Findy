"""Migrate age to birthdate

Revision ID: b4c9b485e65e
Revises: f9ff619414b7
Create Date: 2026-01-24 13:40:45.031327

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4c9b485e65e'
down_revision: Union[str, Sequence[str], None] = 'f9ff619414b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users", sa.Column("birthdate", sa.Date())
    )
    op.execute("UPDATE users SET birthdate = (CURRENT_DATE - (age * interval '1 year'))::date")
    op.drop_column("users", "age")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column("users", sa.Column("age", sa.Integer(), nullable=True))
    op.execute(
        "UPDATE users SET age = EXTRACT(YEAR FROM AGE(birthdate))"
    )
    op.drop_column("users", "birthdate")

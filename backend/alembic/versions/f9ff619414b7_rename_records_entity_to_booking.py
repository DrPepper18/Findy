"""Rename records entity to booking

Revision ID: f9ff619414b7
Revises: d4475ae25cb6
Create Date: 2026-01-20 18:20:12.432549

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9ff619414b7'
down_revision: Union[str, Sequence[str], None] = 'd4475ae25cb6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table('records', 'bookings')


def downgrade() -> None:
    """Downgrade schema."""
    op.rename_table('bookings', 'records')

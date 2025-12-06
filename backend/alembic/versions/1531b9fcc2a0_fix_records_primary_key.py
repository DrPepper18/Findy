"""Fix records primary key

Revision ID: 1531b9fcc2a0
Revises: 
Create Date: 2025-12-06 14:52:02.973194

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1531b9fcc2a0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'records_new',
        sa.Column('ID', sa.BigInteger(), 
                 sa.Identity(start=1, increment=1),
                 primary_key=True),
        sa.Column('Event', sa.BigInteger(), 
                 sa.ForeignKey('events.ID'), 
                 nullable=False),
        sa.Column('User', sa.String(), 
                 sa.ForeignKey('users.Email'), 
                 nullable=False),
        sa.UniqueConstraint('Event', 'User', name='unique_record')
    )
    
    op.execute("""
        INSERT INTO records_new ("Event", "User")
        SELECT DISTINCT ON ("Event", "User") 
               "Event", 
               COALESCE("User", 'unknown@example.com') as "User"
        FROM records
        WHERE "User" IS NOT NULL  -- если есть записи без пользователя
        ORDER BY "Event", "User"
    """)
    
    op.drop_table('records')
    
    op.rename_table('records_new', 'records')


def downgrade():
    op.create_table(
        'records_old',
        sa.Column('Event', sa.BigInteger(), 
                 sa.ForeignKey('events.ID'), 
                 primary_key=True),
        sa.Column('User', sa.String(), 
                 sa.ForeignKey('users.Email'), 
                 nullable=True),
        sa.UniqueConstraint('Event', 'User', name='unique_record')
    )
    
    op.execute("""
        INSERT INTO records_old ("Event", "User")
        SELECT DISTINCT ON ("Event") "Event", "User"
        FROM records
        ORDER BY "Event", "ID"  -- Берем запись с наименьшим ID для каждого Event
    """)
    
    op.drop_table('records')
    
    op.rename_table('records_old', 'records')
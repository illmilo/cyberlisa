"""add work hours to employee

Revision ID: 909bc4a4286d
Revises: 71c4d0336add
Create Date: 2025-06-24 16:09:34.839586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '909bc4a4286d'
down_revision: Union[str, Sequence[str], None] = '71c4d0336add'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employees', sa.Column('work_start_time', sa.Time(), nullable=True))
    op.add_column('employees', sa.Column('work_end_time', sa.Time(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('employees', 'work_end_time')
    op.drop_column('employees', 'work_start_time')
    # ### end Alembic commands ###

"""add last_heartbeat to employee

Revision ID: 2ade52a4267a
Revises: 932c757fbfbc
Create Date: 2025-07-15 20:05:46.680775

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ade52a4267a'
down_revision: Union[str, Sequence[str], None] = '932c757fbfbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employees', sa.Column('last_heartbeat', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('employees', 'last_heartbeat')
    # ### end Alembic commands ###

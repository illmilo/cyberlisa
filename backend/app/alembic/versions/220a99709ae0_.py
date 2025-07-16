"""empty message

Revision ID: 220a99709ae0
Revises: 653de2de3c13, cf44f6faa8b1
Create Date: 2025-07-16 12:18:22.157648

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '220a99709ae0'
down_revision: Union[str, Sequence[str], None] = ('653de2de3c13', 'cf44f6faa8b1')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

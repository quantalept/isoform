"""Modified ENUMS

Revision ID: d153fe3d5ae7
Revises: 2dbb5b7ad175
Create Date: 2025-05-16 10:18:26.666239
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd153fe3d5ae7'
down_revision: Union[str, None] = '2dbb5b7ad175'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('options', sa.Column(
        'option_type',
        sa.Enum('RADIO', 'MULTIPLE_GRID', 'SCALE', 'CHECKBOX', 'DROPDOWN', name='optiontype'),
        nullable=False
    ))
    op.add_column('options', sa.Column('order', sa.Integer(), nullable=False))


def downgrade() -> None:
    # Downgrade: Drop new columns
    op.drop_column('options', 'order')
    op.drop_column('options', 'option_type')

    # Drop enum type if it's no longer used anywhere
    op.execute("DROP TYPE optiontype")



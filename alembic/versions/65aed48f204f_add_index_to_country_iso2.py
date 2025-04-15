"""Add index to country_iso2

Revision ID: 65aed48f204f
Revises: bef8e9a4593e
Create Date: 2025-04-15 16:33:24.608525

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65aed48f204f'
down_revision: Union[str, None] = 'bef8e9a4593e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_swift_codes_country_iso2'), 'swift_codes', ['country_iso2'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_swift_codes_country_iso2'), table_name='swift_codes')
    # ### end Alembic commands ###

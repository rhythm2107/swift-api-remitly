"""create swift_codes table

Revision ID: bef8e9a4593e
Revises: 
Create Date: 2025-04-12 23:50:21.355255

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bef8e9a4593e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('swift_codes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('swift_code', sa.String(length=11), nullable=False),
    sa.Column('bank_name', sa.String(length=255), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('country_iso2', sa.String(length=2), nullable=False),
    sa.Column('country_name', sa.String(length=100), nullable=False),
    sa.Column('is_headquarter', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.CheckConstraint('char_length(country_iso2) = 2', name='check_country_iso2_len'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('swift_code')
    )
    op.create_index(op.f('ix_swift_codes_id'), 'swift_codes', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_swift_codes_id'), table_name='swift_codes')
    op.drop_table('swift_codes')
    # ### end Alembic commands ###

"""add apt num column

Revision ID: d85ffe05c489
Revises: 023eba21dfc9
Create Date: 2023-04-27 19:59:26.150214

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd85ffe05c489'
down_revision = '023eba21dfc9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('address', sa.Column('apt_num', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('address', 'apt_num')

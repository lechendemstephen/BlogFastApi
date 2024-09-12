"""add password field in the users table

Revision ID: a9e2d7079673
Revises: b6ac16fd6e7b
Create Date: 2024-09-12 00:36:52.148185

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9e2d7079673'
down_revision: Union[str, None] = 'b6ac16fd6e7b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('password', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('users', 'password')
    pass

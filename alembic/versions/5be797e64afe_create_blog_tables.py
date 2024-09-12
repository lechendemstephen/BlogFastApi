"""create blog tables

Revision ID: 5be797e64afe
Revises: 
Create Date: 2024-09-06 02:06:30.854664

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5be797e64afe'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('title', sa.String, nullable=False), sa.Column('description', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')

    pass
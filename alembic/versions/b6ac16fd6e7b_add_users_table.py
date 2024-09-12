"""add users table

Revision ID: b6ac16fd6e7b
Revises: 5be797e64afe
Create Date: 2024-09-12 00:26:05.564950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6ac16fd6e7b'
down_revision: Union[str, None] = '5be797e64afe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer, primary_key=True, nullable=False), 
                    sa.Column('email', sa.String, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))


def downgrade() -> None:
    op.drop_table('users')
    pass

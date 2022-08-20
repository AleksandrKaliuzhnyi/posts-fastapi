"""add last few columns to posts table

Revision ID: 49884e2ec0f9
Revises: 2d6d61d78cd5
Create Date: 2022-08-20 12:47:42.370107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49884e2ec0f9'
down_revision = '2d6d61d78cd5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                                   nullable=False, server_default=sa.text('now()')))


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')

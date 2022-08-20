"""add content column

Revision ID: 6069a24b1a64
Revises: aebec2f9dc59
Create Date: 2022-08-20 12:23:14.571933

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6069a24b1a64'
down_revision = 'aebec2f9dc59'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")

"""add foreign-key to posts table

Revision ID: 2d6d61d78cd5
Revises: 8dda81b57f5a
Create Date: 2022-08-20 12:39:21.049756

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d6d61d78cd5'
down_revision = '8dda81b57f5a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts',
                          referent_table='users', local_cols=['owner_id'],
                          remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_column('posts', 'owner_id')
    op.drop_constraint('posts_users_fk', table_name='posts')

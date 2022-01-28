"""add content column to posts table

Revision ID: 2ecb9ecaec9c
Revises: 4dd11c200573
Create Date: 2022-01-28 09:32:08.243546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ecb9ecaec9c'
down_revision = '4dd11c200573'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass

"""add content column to posts table

Revision ID: 2115392bbdce
Revises: 1f93ee0bd329
Create Date: 2021-12-02 22:17:25.667803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2115392bbdce'
down_revision = '1f93ee0bd329'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass

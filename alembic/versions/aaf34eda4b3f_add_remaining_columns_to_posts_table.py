"""add remaining columns to posts table

Revision ID: aaf34eda4b3f
Revises: 41ad0ba669ef
Create Date: 2021-12-02 22:35:44.221089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aaf34eda4b3f'
down_revision = '41ad0ba669ef'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created')
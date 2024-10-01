"""initial migration

Revision ID: 87970689bdb1
Revises:
Create Date: 2024-10-01 12:35:20.362182

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '87970689bdb1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create the users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, default=0),
        sa.Column('username', sa.String()),
        sa.Column('firstname', sa.String()),
        sa.Column('lastname', sa.String()),
        sa.Column('age', sa.Integer()),
        sa.Column('slug', sa.String(), nullable=True, unique=True, index=True),
    )

    # Create the tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True, default=0),
        sa.Column('title', sa.String()),
        sa.Column('content', sa.String()),
        sa.Column('priority', sa.Integer(), default=0),
        sa.Column('completed', sa.Boolean(), default=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('slug', sa.String(), nullable=True, unique=True, index=True),
    )


def downgrade():
    op.drop_table('tasks')
    op.drop_table('users')
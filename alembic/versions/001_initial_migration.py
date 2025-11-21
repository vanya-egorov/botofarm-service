"""Initial migration

Revision ID: 001_initial
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('login', sa.String(length=255), nullable=False),
        sa.Column('password', sa.String(length=500), nullable=False),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('env', sa.String(length=50), nullable=False),
        sa.Column('domain', sa.String(length=50), nullable=False),
        sa.Column('locktime', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_login'), 'users', ['login'], unique=True)
    op.create_index(op.f('ix_users_project_id'), 'users', ['project_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_users_project_id'), table_name='users')
    op.drop_index(op.f('ix_users_login'), table_name='users')
    op.drop_table('users')


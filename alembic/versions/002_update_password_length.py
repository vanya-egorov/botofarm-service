"""Update password length

Revision ID: 002_update_password
Revises: 001_initial
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '002_update_password'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('users', 'password',
                    existing_type=sa.String(length=255),
                    type_=sa.String(length=500),
                    existing_nullable=False)


def downgrade() -> None:
    op.alter_column('users', 'password',
                    existing_type=sa.String(length=500),
                    type_=sa.String(length=255),
                    existing_nullable=False)


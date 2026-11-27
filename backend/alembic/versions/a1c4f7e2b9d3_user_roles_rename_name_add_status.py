"""user_roles: rename name -> role_name, add status, unique role_name

Revision ID: a1c4f7e2b9d3
Revises: 6d54c616a4fd
Create Date: 2026-11-28 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1c4f7e2b9d3'
down_revision: Union[str, Sequence[str], None] = '6d54c616a4fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Rename name -> role_name, add status column, make role_name unique."""
    # Rename (not drop + add), taaki existing roles ka data safe rahe
    op.alter_column('user_roles', 'name', new_column_name='role_name')

    # Existing rows ko status = true mil jayega server_default se
    op.add_column(
        'user_roles',
        sa.Column('status', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    )

    op.create_unique_constraint('uq_user_roles_role_name', 'user_roles', ['role_name'])


def downgrade() -> None:
    """Undo the changes above."""
    op.drop_constraint('uq_user_roles_role_name', 'user_roles', type_='unique')
    op.drop_column('user_roles', 'status')
    op.alter_column('user_roles', 'role_name', new_column_name='name')

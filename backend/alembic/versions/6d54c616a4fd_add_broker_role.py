"""add broker role

Revision ID: 6d54c616a4fd
Revises: 67bf45e132dc
Create Date: 2026-11-27 18:49:15.631830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d54c616a4fd'
down_revision: Union[str, Sequence[str], None] = '67bf45e132dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add the Broker role."""
    # Fixed id 3, taaki har database (local, production) mein Broker ki id same rahe
    op.execute(
        "INSERT INTO user_roles (id, name) VALUES (3, 'Broker') "
        "ON CONFLICT (id) DO NOTHING"
    )
    # auto-increment counter aage badhao, taaki agla naya role id 4 se shuru ho
    op.execute(
        "SELECT setval(pg_get_serial_sequence('user_roles', 'id'), "
        "(SELECT MAX(id) FROM user_roles))"
    )


def downgrade() -> None:
    """Remove the Broker role."""
    op.execute("DELETE FROM user_roles WHERE id = 3")

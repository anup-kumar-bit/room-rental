"""seed user roles

Revision ID: 67bf45e132dc
Revises: e3e7c9b9e29a
Create Date: 2026-11-27 18:47:21.607643

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67bf45e132dc'
down_revision: Union[str, Sequence[str], None] = 'e3e7c9b9e29a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add the default user roles."""
    # ON CONFLICT DO NOTHING: agar role pehle se hai (jaise Admin), toh skip kar do
    op.execute(
        """
        INSERT INTO user_roles (id, name) VALUES
            (0, 'Admin'),
            (1, 'Owner'),
            (2, 'Tenant')
        ON CONFLICT (id) DO NOTHING
        """
    )
    # IDs khud di hain, toh auto-increment counter ko aage badhao,
    # taaki agla naya role id 3 se shuru ho (warna 1 par duplicate error aayega)
    op.execute(
        "SELECT setval(pg_get_serial_sequence('user_roles', 'id'), "
        "(SELECT MAX(id) FROM user_roles))"
    )


def downgrade() -> None:
    """Remove the roles added above (Admin is kept)."""
    op.execute("DELETE FROM user_roles WHERE id IN (1, 2)")

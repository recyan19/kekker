"""add FK to posts table

Revision ID: 822be1afba81
Revises: 7f2a07516766
Create Date: 2025-08-13 18:55:15.665889

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '822be1afba81'
down_revision: Union[str, Sequence[str], None] = '7f2a07516766'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column("owner_id", sa.Integer(), nullable=False, index=True)
    )
    op.create_foreign_key(
        "fk_posts_owner_id_users_id",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE"
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_posts_owner_id_users_id",
        table_name="posts",
        type_="foreignkey"
    )
    op.drop_column("posts", "owner_id")

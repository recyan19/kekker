"""create posts table

Revision ID: 524f3c877455
Revises: 
Create Date: 2025-08-13 18:33:19.245235

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '524f3c877455'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False, index=True),
        sa.Column("title", sa.String(length=80), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts")

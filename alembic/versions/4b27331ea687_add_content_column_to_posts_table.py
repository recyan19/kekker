"""add content column to posts table

Revision ID: 4b27331ea687
Revises: 524f3c877455
Create Date: 2025-08-13 18:42:30.706262

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b27331ea687'
down_revision: Union[str, Sequence[str], None] = '524f3c877455'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column("content", sa.String(length=800), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")

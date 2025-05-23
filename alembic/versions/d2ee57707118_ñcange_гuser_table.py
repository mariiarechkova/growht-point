"""Ñcange гuser table

Revision ID: d2ee57707118
Revises: 67e30f32ea98
Create Date: 2025-04-30 13:26:41.077570

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "d2ee57707118"
down_revision: Union[str, None] = "67e30f32ea98"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("roles", schema=None) as batch_op:
        batch_op.alter_column(
            "created_at", existing_type=postgresql.TIMESTAMP(), type_=sa.DateTime(timezone=True), existing_nullable=True
        )

    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.alter_column(
            "created_at", existing_type=postgresql.TIMESTAMP(), type_=sa.DateTime(timezone=True), existing_nullable=True
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.alter_column(
            "created_at", existing_type=sa.DateTime(timezone=True), type_=postgresql.TIMESTAMP(), existing_nullable=True
        )

    with op.batch_alter_table("roles", schema=None) as batch_op:
        batch_op.alter_column(
            "created_at", existing_type=sa.DateTime(timezone=True), type_=postgresql.TIMESTAMP(), existing_nullable=True
        )

    # ### end Alembic commands ###

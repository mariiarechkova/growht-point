"""make department_id and organisation_id nullable

Revision ID: effef729f609
Revises: 99ebd3aad91d
Create Date: 2025-04-16 16:14:55.912849

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "effef729f609"
down_revision: Union[str, None] = "99ebd3aad91d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.alter_column("department_id", existing_type=sa.INTEGER(), nullable=True)
        batch_op.alter_column("organisation_id", existing_type=sa.INTEGER(), nullable=True)

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.alter_column("organisation_id", existing_type=sa.INTEGER(), nullable=False)
        batch_op.alter_column("department_id", existing_type=sa.INTEGER(), nullable=False)

    # ### end Alembic commands ###

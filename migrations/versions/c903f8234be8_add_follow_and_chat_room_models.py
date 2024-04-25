"""add follow and chat room models

Revision ID: c903f8234be8
Revises: 6f4eabbe0ee3
Create Date: 2024-04-20 20:13:39.788645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c903f8234be8'
down_revision: Union[str, None] = '6f4eabbe0ee3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('followers', sa.Column('is_following', sa.Boolean(), nullable=True))
    op.alter_column('followers', 'followers_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('followers', 'followers_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('followers', 'is_following')
    # ### end Alembic commands ###

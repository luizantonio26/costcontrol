"""Add foreign key of user to recipe

Revision ID: 29344bf7ee17
Revises: de5a9d2953f0
Create Date: 2024-06-19 16:03:56.782817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29344bf7ee17'
down_revision: Union[str, None] = 'de5a9d2953f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'recipe', 'user_account', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'recipe', type_='foreignkey')
    op.drop_column('recipe', 'user_id')
    # ### end Alembic commands ###

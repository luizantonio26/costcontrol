"""add recipe_sales and recipe_sales_items

Revision ID: 27cabd228caf
Revises: fedee66e9977
Create Date: 2024-06-27 18:45:31.091950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27cabd228caf'
down_revision: Union[str, None] = 'fedee66e9977'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

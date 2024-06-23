"""Fixing models

Revision ID: 464be6d3276d
Revises: 29344bf7ee17
Create Date: 2024-06-20 11:50:31.417827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '464be6d3276d'
down_revision: Union[str, None] = '29344bf7ee17'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('ingredient', 'name',
               existing_type=sa.VARCHAR(length=150),
               nullable=True)
    op.alter_column('ingredient', 'quantity',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('ingredient', 'unit',
               existing_type=sa.VARCHAR(length=15),
               nullable=True)
    op.alter_column('ingredient', 'value',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('ingredient', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('ingredient', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('recipe', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('recipe', 'name',
               existing_type=sa.VARCHAR(length=150),
               nullable=True)
    op.alter_column('recipe', 'prep_time',
               existing_type=sa.VARCHAR(length=10),
               nullable=True)
    op.alter_column('recipe', 'servings',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('recipe', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('recipe', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('recipe_ingredient', 'quantity',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('recipe_ingredient', 'quantity',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('recipe', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('recipe', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('recipe', 'servings',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('recipe', 'prep_time',
               existing_type=sa.VARCHAR(length=10),
               nullable=False)
    op.alter_column('recipe', 'name',
               existing_type=sa.VARCHAR(length=150),
               nullable=False)
    op.alter_column('recipe', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('ingredient', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('ingredient', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('ingredient', 'value',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('ingredient', 'unit',
               existing_type=sa.VARCHAR(length=15),
               nullable=False)
    op.alter_column('ingredient', 'quantity',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('ingredient', 'name',
               existing_type=sa.VARCHAR(length=150),
               nullable=False)
    # ### end Alembic commands ###

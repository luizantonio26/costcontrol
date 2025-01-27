"""fix secret size

Revision ID: 1a0e11fa4012
Revises: 86bffceee834
Create Date: 2024-06-24 09:56:08.988429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a0e11fa4012'
down_revision: Union[str, None] = '86bffceee834'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('security_settings', 'secret',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=100),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('security_settings', 'secret',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=20),
               existing_nullable=True)
    # ### end Alembic commands ###

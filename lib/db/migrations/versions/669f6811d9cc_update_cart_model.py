"""Update Cart model

Revision ID: 669f6811d9cc
Revises: cc51495802b6
Create Date: 2024-12-18 20:00:01.014259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '669f6811d9cc'
down_revision: Union[str, None] = 'cc51495802b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        UPDATE cart
        SET user_name = 'default_user',
            supplement_name = 'default_supplement',
            quantity = 1,
            supplement_price = 10.0
        WHERE user_name IS NULL OR supplement_name IS NULL OR quantity IS NULL OR supplement_price IS NULL
    """)


def downgrade():
    op.drop_column('cart', 'user_name')
    op.drop_column('cart', 'supplement_name')
    op.drop_column('cart', 'quantity')
    op.drop_column('cart', 'supplement_price')
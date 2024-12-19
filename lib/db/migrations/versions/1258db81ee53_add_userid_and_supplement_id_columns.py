"""add userid and supplement id columns

Revision ID: 1258db81ee53
Revises: 669f6811d9cc
Create Date: 2024-12-19 01:19:07.217635

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1258db81ee53'
down_revision: Union[str, None] = '669f6811d9cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the cart table without foreign keys initially
    op.create_table(
        'cart',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('quantity', sa.Integer),
        sa.Column('user_name', sa.String),
        sa.Column('supplement_name', sa.String),
        sa.Column('supplement_price', sa.Float),
        sa.Column('user_id', sa.Integer),
        sa.Column('supplement_id', sa.Integer)
    )
    
    # First add the user_id foreign key constraint
    op.create_foreign_key(
        "fk_cart_user", "cart", "users", ["user_id"], ["id"]
    )

    # Then add the supplement_id foreign key constraint
    op.create_foreign_key(
        "fk_cart_supplement", "cart", "supplements", ["supplement_id"], ["id"]
    )




def downgrade():
    with op.batch_alter_table('cart', schema=None) as batch_op:
        # Drop the foreign key constraints in reverse order
        batch_op.drop_constraint('fk_cart_supplement', type_='foreignkey')
        batch_op.drop_constraint('fk_cart_user', type_='foreignkey')
        
        # Drop the columns
        batch_op.drop_column('supplement_id')
        batch_op.drop_column('user_id')

"""Create tables

Revision ID: 7fc4e51049f5
Revises: 
Create Date: 2024-12-17 16:33:06.281768

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7fc4e51049f5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    pass
        

def downgrade():
    pass

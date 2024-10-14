"""empty message

Revision ID: 71d49d9939b0
Revises: 6f724b65cd09
Create Date: 2024-09-26 21:01:33.435282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71d49d9939b0'
down_revision: Union[str, None] = '6f724b65cd09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

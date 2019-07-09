"""Migration token model

Revision ID: 53ac80e44a59
Revises: fde99be08182
Create Date: 2019-07-01 22:59:28.592490

"""

import uuid
import sys

import sqlalchemy as sa
from alembic import op
from sqlalchemy import orm
from sqlalchemy.dialects import postgresql

from wolf.models import Token


# revision identifiers, used by Alembic.
revision = '53ac80e44a59'
down_revision = 'fde99be08182'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    op.add_column('token', sa.Column('uuid', postgresql.UUID, nullable=True))
    tokens = session.query(Token).all()
    for token in tokens:
        op.execute(
            f"UPDATE token SET uuid = '{uuid.uuid1()}' where id = {token.id};"
        )


def downgrade():
    pass


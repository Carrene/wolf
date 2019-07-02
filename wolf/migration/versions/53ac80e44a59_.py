"""Migration token model

Revision ID: 53ac80e44a59
Revises: fde99be08182
Create Date: 2019-07-01 22:59:28.592490

"""

import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import orm

from wolf.models import Token


# revision identifiers, used by Alembic.
revision = '53ac80e44a59'
down_revision = 'fde99be08182'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    op.drop_index('ix_member_password', table_name='member')
    op.drop_index('ix_member_username', table_name='member')
    op.drop_table('member')

    op.add_column('token', sa.Column('uuid', postgresql.UUID, nullable=True))
    tokens = session.query(Token).all()
    with open('tosee-uuid.csv','w') as f:
        for token in tokens:
            new_uuid = uuid.uuid1()
            f.write(f'{token.id},{new_uuid}\n')
            op.execute(
                f"UPDATE token SET uuid = '{new_uuid}' where id = {token.id};"
            )

        f.close()

    op.drop_column('token', 'id')
    op.execute('ALTER TABLE token RENAME uuid TO id')
    op.execute('ALTER TABLE token ALTER COLUMN id SET NOT NULL')
    op.create_unique_constraint('token_id_key', 'token', ['id'])
    op.create_primary_key('token_pkey', 'token', ['id'])


def downgrade():
    op.create_table(
        'member',
        sa.Column(
            'created_at',
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False
        ),
        sa.Column(
            'modified_at',
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True
        ),
        sa.Column(
            'id',
            sa.INTEGER(),
            autoincrement=True,
            nullable=False
        ),
        sa.Column(
            'username',
            sa.VARCHAR(length=64),
            autoincrement=False,
            nullable=False
        ),
        sa.Column(
            'password',
            sa.VARCHAR(length=128),
            autoincrement=False,
            nullable=False
        ),
        sa.Column(
            'bank_id',
            sa.INTEGER(),
            autoincrement=False,
            nullable=True
        ),
        sa.Column(
            'type',
            sa.VARCHAR(length=50),
            autoincrement=False,
            nullable=False
        ),
        sa.PrimaryKeyConstraint('id', name='member_pkey')
    )
    op.create_index('ix_member_username', 'member', ['username'], unique=True)
    op.create_index('ix_member_password', 'member', ['password'], unique=False)


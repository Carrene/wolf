"""Create member table

Revision ID: b356f6ae9969
Revises: ef9f84d306d3
Create Date: 2019-05-16 11:51:32.184191

"""

# revision identifiers, used by Alembic.
revision = 'b356f6ae9969'
down_revision = 'cc2f884779bb'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'member',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('modified_at', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.Unicode(length=64), nullable=False),
        sa.Column('password', sa.Unicode(length=128), nullable=False),
        sa.Column('bank_id', sa.Integer(), nullable=True),
        sa.Column('type', sa.Unicode(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        'ix_member_password',
        'member',
        ['password']
    )
    op.create_index(
        'ix_member_username',
        'member',
        ['username'],
        unique=True
    )

def downgrade():
    op.drop_index(
        'ix_member_username',
        table_name='member'
    )
    op.drop_index(
        'ix_member_password',
        table_name='member'
    )
    op.drop_table('member')

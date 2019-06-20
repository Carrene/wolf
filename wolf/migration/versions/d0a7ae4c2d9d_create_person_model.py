"""Create person model

Revision ID: d0a7ae4c2d9d
Revises: b356f6ae9969
Create Date: 2019-06-20 13:24:27.042628

"""

# revision identifiers, used by Alembic.
revision = 'd0a7ae4c2d9d'
down_revision = 'b356f6ae9969'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('person',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_code', sa.String(length=15), nullable=False),
    sa.Column('national_id', sa.String(length=12), nullable=False),
    sa.Column('name', sa.Unicode(length=40), nullable=False),
    sa.Column('family', sa.Unicode(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('person')
    # ### end Alembic commands ###

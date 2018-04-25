"""empty message

Revision ID: 34eeeb3054e2
Revises:
Create Date: 2018-04-24 04:06:53.246590

"""

# revision identifiers, used by Alembic.
revision = '34eeeb3054e2'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cryptomodule', 'challenge_response_length')
    op.drop_column('token', 'consecutive_tries')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('token', sa.Column('consecutive_tries', sa.INTEGER(), autoincrement=False, nullable=False, default=0))
    op.add_column('cryptomodule', sa.Column('challenge_response_length', sa.INTEGER(), autoincrement=False, nullable=False, default=7))
    # ### end Alembic commands ###
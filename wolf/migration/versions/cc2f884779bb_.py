"""empty message

Revision ID: cc2f884779bb
Revises: 15f9ed9a9d13
Create Date: 2019-01-15 15:12:38.778370

"""

# revision identifiers, used by Alembic.
revision = 'cc2f884779bb'
down_revision = '15f9ed9a9d13'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('token', sa.Column('bank_id', sa.Integer(), nullable=False, server_default='1'))
    op.create_unique_constraint('uix_name_phone_cryptomodule_id_bank_id', 'token', ['name', 'phone', 'cryptomodule_id', 'bank_id'])
    op.drop_constraint('uix_name_phone_cryptomodule_id', 'token', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('uix_name_phone_cryptomodule_id', 'token', ['name', 'phone', 'cryptomodule_id'])
    op.drop_constraint('uix_name_phone_cryptomodule_id_bank_id', 'token', type_='unique')
    op.drop_column('token', 'bank_id')
    # ### end Alembic commands ###

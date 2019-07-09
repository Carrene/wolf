"""empty message

Revision ID: e6513c79ae02
Revises: 53ac80e44a59
Create Date: 2019-07-03 17:36:22.888156

"""

# revision identifiers, used by Alembic.
revision = 'e6513c79ae02'
down_revision = '53ac80e44a59'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('token', 'id')
    op.execute('ALTER TABLE token RENAME uuid TO id')
    op.execute('ALTER TABLE token ALTER COLUMN id SET NOT NULL')
    op.create_unique_constraint('token_id_key', 'token', ['id'])
    op.create_primary_key('token_pkey', 'token', ['id'])


def downgrade():
    pass


"""empty message

Revision ID: ef9f84d306d3
Revises: cc2f884779bb
Create Date: 2019-04-14 16:31:19.539227

"""

# revision identifiers, used by Alembic.
revision = 'ef9f84d306d3'
down_revision = 'cc2f884779bb'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_table('device')

def downgrade():
    raise Exception('Invalid operation, cannot downgrade this revision.')

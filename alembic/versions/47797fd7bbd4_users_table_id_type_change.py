"""users table id type change

Revision ID: 47797fd7bbd4
Revises: 4a7155a13610
Create Date: 2016-08-22 23:34:58.295611

"""

# revision identifiers, used by Alembic.
revision = '47797fd7bbd4'
down_revision = '4a7155a13610'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('users', 'id', sa.Sequence, primary_key=True)


def downgrade():
    op.alter_column('users', 'id', sa.Integer, primary_key=True)

"""add users table

Revision ID: 4a7155a13610
Revises: 
Create Date: 2016-08-22 23:30:51.395501

"""

# revision identifiers, used by Alembic.
revision = '4a7155a13610'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # op.create_table(
    #     'users',
    #     sa.Column('id', sa.Integer, primary_key=True),
    #     sa.Column('username', sa.String(32)),
    #     sa.Column('password_hash', sa.String(250))
    # )
    pass


def downgrade():
    # op.drop_table('users')
    pass

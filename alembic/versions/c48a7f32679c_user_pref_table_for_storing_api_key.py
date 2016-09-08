"""user_pref table for storing api key

Revision ID: c48a7f32679c
Revises: d4138b397482
Create Date: 2016-09-07 14:50:05.000307

"""

# revision identifiers, used by Alembic.
revision = 'c48a7f32679c'
down_revision = 'd4138b397482'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'user_pref',
        sa.Column('id', sa.Integer, sa.ForeignKey("users.id"), primary_key=True, nullable=False),
        sa.Column('api_key', sa.String())
    )


def downgrade():
    op.drop_table('user_pref')

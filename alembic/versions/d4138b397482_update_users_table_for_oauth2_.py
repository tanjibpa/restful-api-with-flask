"""update users table for oauth2 credentials

Revision ID: d4138b397482
Revises: 9bb1bad79bcc
Create Date: 2016-08-24 12:53:39.155421

"""

# revision identifiers, used by Alembic.
revision = 'd4138b397482'
down_revision = '9bb1bad79bcc'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'users',
        sa.Column('picture', sa.String),
        sa.Column('email', sa.String, index=True)
    )


def downgrade():
    op.drop_column('users', 'picture', 'email')

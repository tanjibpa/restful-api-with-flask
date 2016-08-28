"""update users table for oauth2 credentials

Revision ID: 9bb1bad79bcc
Revises: 1702027f79ec
Create Date: 2016-08-24 12:36:17.668976

"""

# revision identifiers, used by Alembic.
revision = '9bb1bad79bcc'
down_revision = '1702027f79ec'
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

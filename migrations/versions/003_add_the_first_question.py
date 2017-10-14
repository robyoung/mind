"""Add the first question

Revision ID: 003
Revises: 002
Create Date: 2017-10-14 11:31:17.226050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        INSERT INTO question (title, slug, created_at)
        VALUES ('How are you today?', 'how-are-you-today', now());
    """)


def downgrade():
    op.execute("""
        DELETE FROM question WHERE slug='how-are-you-today';
    """)

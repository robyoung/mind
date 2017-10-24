"""Add email field to Answer

Revision ID: 004
Revises: 003
Create Date: 2017-10-23 09:41:08.972164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answer', sa.Column('email', sa.String(), nullable=True))
    op.alter_column('question', 'slug',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('question', 'slug',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('answer', 'email')
    # ### end Alembic commands ###
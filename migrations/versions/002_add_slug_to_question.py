"""Add slug to Question

Revision ID: 002
Revises: 001
Create Date: 2017-10-12 07:33:37.320206

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question', sa.Column('slug', sa.String(), nullable=True))
    op.execute("UPDATE question SET slug=trim(both '-' from lower(regexp_replace(title, '[^a-zA-Z0-9_]', '-', 'g')))")
    op.alter_column('question', 'slug', nullable=True)
    op.create_index(op.f('ix_question_slug'), 'question', ['slug'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_question_slug'), table_name='question')
    op.drop_column('question', 'slug')
    # ### end Alembic commands ###
"""right answer add

Revision ID: 7871eb5d92fd
Revises: 8eb366119220
Create Date: 2021-02-05 20:37:33.227905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7871eb5d92fd'
down_revision = '8eb366119220'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answers', sa.Column('right_answer', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('answers', 'right_answer')
    # ### end Alembic commands ###

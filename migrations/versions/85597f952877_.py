"""empty message

Revision ID: 85597f952877
Revises: ad46e64edd0d
Create Date: 2022-08-14 11:12:05.571674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85597f952877'
down_revision = 'ad46e64edd0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'category')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('category', sa.INTEGER(), nullable=True))
    # ### end Alembic commands ###

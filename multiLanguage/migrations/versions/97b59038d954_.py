"""empty message

Revision ID: 97b59038d954
Revises: 5bcac56f22cc
Create Date: 2019-03-28 10:36:16.592613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97b59038d954'
down_revision = '5bcac56f22cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('m_permission', sa.Column('endpoint', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('m_permission', 'endpoint')
    # ### end Alembic commands ###

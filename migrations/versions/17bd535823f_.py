"""empty message

Revision ID: 17bd535823f
Revises: 4d3a316335b
Create Date: 2015-11-17 17:23:09.867681

"""

# revision identifiers, used by Alembic.
revision = '17bd535823f'
down_revision = '4d3a316335b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'email')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sa.VARCHAR(), nullable=True))
    ### end Alembic commands ###

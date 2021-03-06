"""004_delete_last_message

Revision ID: 9292b5e389c4
Revises: bf3396f3e8e2
Create Date: 2019-05-09 19:15:02.350635

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '9292b5e389c4'
down_revision = 'bf3396f3e8e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('chats_last_message_id_fkey', 'chats', type_='foreignkey')
    op.drop_column('chats', 'last_message_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chats', sa.Column('last_message_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('chats_last_message_id_fkey', 'chats', 'messages', ['last_message_id'], ['message_id'])
    # ### end Alembic commands ###

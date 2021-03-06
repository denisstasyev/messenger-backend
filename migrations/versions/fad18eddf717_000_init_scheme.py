"""000_init_scheme

Revision ID: fad18eddf717
Revises: 
Create Date: 2019-03-29 19:52:30.145336

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'fad18eddf717'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attachments',
    sa.Column('attachment_id', sa.Integer(), nullable=False),
    sa.Column('attachment_type', sa.String(length=80), nullable=False),
    sa.Column('attachment_url', sa.String(length=500), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('attachment_id')
    )
    op.create_table('chats',
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('chatname', sa.String(length=80), nullable=False),
    sa.Column('chat_title', sa.String(length=120), nullable=True),
    sa.Column('is_public', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('chat_id')
    )
    op.create_index(op.f('ix_chats_chat_title'), 'chats', ['chat_title'], unique=False)
    op.create_index(op.f('ix_chats_chatname'), 'chats', ['chatname'], unique=True)
    op.create_table('members',
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('new_messages', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('member_id')
    )
    op.create_table('messages',
    sa.Column('message_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('message_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('first_name', sa.String(length=80), nullable=False),
    sa.Column('last_name', sa.String(length=80), nullable=False),
    sa.Column('birth_date', sa.Date(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('email', sqlalchemy_utils.types.email.EmailType(length=255), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
    op.drop_table('messages')
    op.drop_table('members')
    op.drop_index(op.f('ix_chats_chatname'), table_name='chats')
    op.drop_index(op.f('ix_chats_chat_title'), table_name='chats')
    op.drop_table('chats')
    op.drop_table('attachments')
    # ### end Alembic commands ###

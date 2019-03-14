from sqlalchemy.sql import func
from app import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column("user_id", db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=func.utcnow())
    updated_at = db.Column(db.DateTime(), onupdate=func.utcnow())
    email = db.Column(db.String(120), unique=True)

    messages = db.relationship("Message", backref="user_owner", lazy="dynamic")
    attachments = db.relationship("Attachment", backref="user_owner", lazy="dynamic")
    memberships = db.relationship("Member", backref="user_owner", lazy="dynamic")

    def __init__(self, username, first_name, last_name, email=None):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):
        return "<{}: id={}, username={}, first_name={}, last_name={}, created_at={}, updated_at={}>".format(
            self.__class__.__name__,
            self.id,
            self.username,
            self.first_name,
            self.last_name,
            self.created_at,
            self.updated_at,
        )


class Member(db.Model):
    __tablename__ = "members"
    id = db.Column("member_id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey("chats.chat_id"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.utcnow())
    updated_at = db.Column(db.DateTime(), onupdate=func.utcnow())
    new_messages = db.Column(db.Integer, default=0)
    last_read_message_id = db.Column(db.Integer, db.ForeignKey("messages.message_id"))

    def __init__(self, user_id, chat_id, new_messages=None, last_read_message_id=None):
        self.user_id = user_id
        self.chat_id = chat_id
        self.new_messages = new_messages
        self.last_read_message_id = last_read_message_id

    def __repr__(self):
        return "<{}: id={}, user_id={}, chat_id={}, created_at={}, updated_at={}>".format(
            self.__class__.__name__,
            self.id,
            self.user_id,
            self.chat_id,
            self.created_at,
            self.updated_at,
        )


class Chat(db.Model):
    __tablename__ = "chats"
    id = db.Column("chat_id", db.Integer, primary_key=True)
    chatname = db.Column(db.String(120), index=True, nullable=False)
    is_public = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.utcnow())
    updated_at = db.Column(db.DateTime(), onupdate=func.utcnow())
    last_message_id = db.Column(db.Integer, db.ForeignKey("messages.message_id"))

    messages = db.relationship("Message", backref="chat_owner", lazy="dynamic")
    members = db.relationship("Member", backref="chat_owner", lazy="dynamic")
    attachments = db.relationship("Attachment", backref="chat_owner", lazy="dynamic")

    def __init__(self, chatname, is_public, last_message=None):
        self.chatname = chatname
        self.is_public = is_public
        self.last_message = last_message

    def __repr__(self):
        return "<{}: id={}, chatname={}, is_public={}, created_at={}, updated_at={}>".format(
            self.__class__.__name__,
            self.id,
            self.chatname,
            self.is_public,
            self.created_at,
            self.updated_at,
        )


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column("message_id", db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey("chats.chat_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.utcnow())
    updated_at = db.Column(db.DateTime(), onupdate=func.utcnow())
    text = db.Column(db.Text)

    attachments = db.relationship("Attachment", backref="message_owner", lazy="dynamic")

    def __init__(self, chat_id, user_id, text=None):
        self.chat_id = chat_id
        self.user_id = user_id
        self.text = text

    def __repr__(self):
        return "<{}: id={}, chat_id={}, user_id={}, created_at={}, updated_at={}>".format(
            self.__class__.__name__,
            self.id,
            self.chat_id,
            self.user_id,
            self.created_at,
            self.updated_at,
        )


class Attachment(db.Model):
    __tablename__ = "attachments"
    id = db.Column("attachment_id", db.Integer, primary_key=True)
    attachment_type = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.utcnow())
    updated_at = db.Column(db.DateTime(), onupdate=func.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    chat_id = db.Column(db.Integer, db.ForeignKey("chats.chat_id"))
    message_id = db.Column(db.Integer, db.ForeignKey("messages.message_id"))

    def __init__(
        self, attachment_type, url, user_id=None, chat_id=None, message_id=None
    ):
        self.attachment_type = attachment_type
        self.url = url
        self.user_id = user_id
        self.chat_id = chat_id
        self.message_id = message_id

    def __repr__(self):
        return "<{}: id={}, attachment_type={}, url={}, created_at={}, updated_at={}>".format(
            self.__class__.__name__,
            self.id,
            self.attachment_type,
            self.url,
            self.created_at,
            self.updated_at,
        )

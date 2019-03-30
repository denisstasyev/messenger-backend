# pylint: disable=bad-continuation

from datetime import datetime
from sqlalchemy_utils import PasswordType, EmailType
from flask_login import UserMixin

from app import db, lm


def model_as_dict(model):
    dict_result = {}
    for key in model.__mapper__.c.keys():
        dict_result[key] = getattr(model, key)
    return dict_result


class User(UserMixin, db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True, unique=True, nullable=False)
    password = db.Column(PasswordType(schemes=["pbkdf2_sha256"]))  # password hash
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    birth_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=None, onupdate=datetime.utcnow)
    email = db.Column(EmailType, unique=True)

    messages = db.relationship(
        "Message", backref="user_owner", lazy="dynamic", foreign_keys="Message.user_id"
    )
    attachments = db.relationship(
        "Attachment",
        backref="user_owner",
        lazy="dynamic",
        foreign_keys="Attachment.user_id",
    )
    memberships = db.relationship(
        "Member", backref="user_owner", lazy="dynamic", foreign_keys="Member.user_id"
    )

    def __init__(self, username=None, first_name=None, last_name=None, email=None):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):
        # pylint: disable=line-too-long
        return "<{}: user_id={}, username={}, first_name={}, last_name={}, created_at={}, updated_at={}>".format(
            self.__class__.__name__,
            self.user_id,
            self.username,
            self.first_name,
            self.last_name,
            self.created_at,
            self.updated_at,
        )

    def get_id(self):
        return self.user_id


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Member(db.Model):
    __tablename__ = "members"
    member_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey("chats.chat_id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=None, onupdate=datetime.utcnow)
    new_messages = db.Column(db.Integer, default=0)
    last_read_message_id = db.Column(db.Integer, db.ForeignKey("messages.message_id"))

    def __init__(
        self, user_id=None, chat_id=None, new_messages=None, last_read_message_id=None
    ):
        self.user_id = user_id
        self.chat_id = chat_id
        self.new_messages = new_messages
        self.last_read_message_id = last_read_message_id

    def __repr__(self):
        return "<{}: member_id={}, user_id={}, chat_id={}, created_at={}, updated_at={}>".format(
            self.__class__.__name__,
            self.member_id,
            self.user_id,
            self.chat_id,
            self.created_at,
            self.updated_at,
        )


class Chat(db.Model):
    __tablename__ = "chats"
    chat_id = db.Column(db.Integer, primary_key=True)
    chatname = db.Column(
        db.String(80), index=True, unique=True, default="chat" + chat_id
    )
    chat_title = db.Column(db.String(120), index=True)
    is_public = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=None, onupdate=datetime.utcnow)
    last_message_id = db.Column(db.Integer, db.ForeignKey("messages.message_id"))

    messages = db.relationship(
        "Message", backref="chat_owner", lazy="dynamic", foreign_keys="Message.chat_id"
    )
    members = db.relationship(
        "Member", backref="chat_owner", lazy="dynamic", foreign_keys="Member.chat_id"
    )
    attachments = db.relationship(
        "Attachment",
        backref="chat_owner",
        lazy="dynamic",
        foreign_keys="Attachment.chat_id",
    )

    def __init__(self, chatname=None, is_public=None, last_message=None):
        self.chatname = chatname
        self.is_public = is_public
        self.last_message = last_message

    def __repr__(self):
        return "<{}: chat_id={}, chatname={}, is_public={}, created_at={}, updated_at={}>".format(
            self.__class__.__name__,
            self.chat_id,
            self.chatname,
            self.is_public,
            self.created_at,
            self.updated_at,
        )


class Message(db.Model):
    __tablename__ = "messages"
    message_id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey("chats.chat_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=None, onupdate=datetime.utcnow)
    text = db.Column(db.Text)

    attachments = db.relationship(
        "Attachment",
        backref="message_owner",
        lazy="dynamic",
        foreign_keys="Attachment.message_id",
    )

    def __init__(self, chat_id=None, user_id=None, text=None):
        self.chat_id = chat_id
        self.user_id = user_id
        self.text = text

    def __repr__(self):
        return "<{}: message_id={}, chat_id={}, user_id={}, created_at={}, updated_at={}>".format(
            self.__class__.__name__,
            self.message_id,
            self.chat_id,
            self.user_id,
            self.created_at,
            self.updated_at,
        )


class Attachment(db.Model):
    __tablename__ = "attachments"
    attachment_id = db.Column(db.Integer, primary_key=True)
    attachment_type = db.Column(db.String(80), nullable=False)
    attachment_url = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=None, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    chat_id = db.Column(db.Integer, db.ForeignKey("chats.chat_id"))
    message_id = db.Column(db.Integer, db.ForeignKey("messages.message_id"))

    def __init__(
        self,
        attachment_type=None,
        url=None,
        user_id=None,
        chat_id=None,
        message_id=None,
    ):
        self.attachment_type = attachment_type
        self.url = url
        self.user_id = user_id
        self.chat_id = chat_id
        self.message_id = message_id

    def __repr__(self):
        # pylint: disable=line-too-long
        return "<{}: attachment_id={}, attachment_type={}, url={}, created_at={}, updated_at={}>".format(
            self.__class__.__name__,
            self.attachment_id,
            self.attachment_type,
            self.url,
            self.created_at,
            self.updated_at,
        )

from app import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column("user_id", db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    registered_at = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, first_name, last_name, registered_at, email=None):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.registered_at = registered_at
        self.email = email

    def __repr__(self):
        return "<User('%s','%s', '%s', '%s')>" % (
            self.username,
            self.first_name,
            self.last_name,
            self.registered_at,
        )


class Member(db.Model):
    __tablename__ = "members"
    id = db.Column("member_id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    chat_id = db.Column(db.Integer, nullable=False)
    new_messages = db.Column(db.Integer)
    last_read_message_id = db.Column(db.Integer)

    def __init__(self, user_id, chat_id, new_messages=None, last_read_message_id=None):
        self.user_id = user_id
        self.chat_id = chat_id
        self.new_messages = new_messages
        self.last_read_message_id = last_read_message_id

    def __repr__(self):
        return "<Member('%s','%s')>" % (self.user_id, self.chat_id)


class Chat(db.Model):
    __tablename__ = "chats"
    id = db.Column("chat_id", db.Integer, primary_key=True)
    chatname = db.Column(db.String(120), nullable=False)
    is_public = db.Column(db.Boolean, nullable=False)
    last_message = db.Column(db.Integer)

    def __init__(self, chatname, is_public, last_message=None):
        self.chatname = chatname
        self.is_public = is_public
        self.last_message = last_message

    def __repr__(self):
        return "<Chat('%s','%s')>" % (self.chatname, self.is_public)


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column("message_id", db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    added_at = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text)

    def __init__(self, chat_id, user_id, added_at, text=None):
        self.chat_id = chat_id
        self.user_id = user_id
        self.added_at = added_at
        self.text = text

    def __repr__(self):
        return "<Message('%s','%s', '%s')>" % (
            self.chat_id,
            self.user_id,
            self.added_at,
        )


class Attachment(db.Model):
    __tablename__ = "attachments"
    id = db.Column("attachment_id", db.Integer, primary_key=True)
    type = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer)
    chat_id = db.Column(db.Integer)
    message_id = db.Column(db.Integer)

    def __init__(self, type, url, user_id=None, chat_id=None, message_id=None):
        self.type = type
        self.url = url
        self.user_id = user_id
        self.chat_id = chat_id
        self.message_id = message_id

    def __repr__(self):
        return "<Message('%s','%s')>" % (self.type, self.url)

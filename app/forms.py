from wtforms_alchemy import ModelForm, Form
from wtforms_alchemy.validators import Unique
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Length, DataRequired, EqualTo

from .models import User, Chat, Message, Attachment


# API general forms


class UserForm(ModelForm):
    class Meta:
        model = User
        only = ["birth_date", "email"]

    username = TextField("username", validators=[Length(max=80), Unique(User.username)])
    password = PasswordField("password")
    first_name = TextField("first_name", validators=[Length(max=80)])
    last_name = TextField("last_name", validators=[Length(max=80)])


class MemberForm(Form):
    username = TextField("username", validators=[DataRequired(), Length(max=80)])
    chatname = TextField("chatname", validators=[DataRequired(), Length(max=80)])


class ChatForm(ModelForm):
    class Meta:
        model = Chat


class MessageForm(ModelForm):
    class Meta:
        model = Message


class AttachmentForm(ModelForm):
    class Meta:
        model = Attachment
        include = ["user_id", "chat_id", "message_id"]


class FileForm(Form):
    filename = TextField("filename", validators=[DataRequired()])
    base64content = TextField("base64content", validators=[DataRequired()])


# Authorization forms


class LoginForm(ModelForm):
    class Meta:
        model = User
        only = ["password"]

    username = TextField("username", validators=[DataRequired(), Length(max=80)])
    remember_me = BooleanField("remember me", default=False)


class RegistrationForm(ModelForm):
    class Meta:
        model = User

    password2 = PasswordField(
        "repeat password", validators=[DataRequired(), EqualTo("password")]
    )

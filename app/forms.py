from wtforms_alchemy import ModelForm, Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo

from .models import User, Chat, Message, Attachment


# API general forms


class UserForm(ModelForm):
    class Meta:
        model = User


class MemberForm(Form):
    username = StringField("username", validators=[DataRequired()])
    chatname = StringField("chatname", validators=[DataRequired()])


class ChatForm(ModelForm):
    class Meta:
        model = Chat


class MessageForm(ModelForm):
    class Meta:
        model = Message
        include = ["chat_id", "user_id"]


class AttachmentForm(ModelForm):
    class Meta:
        model = Attachment
        include = ["user_id", "chat_id", "message_id"]


# Authorization forms


class LoginForm(ModelForm):
    class Meta:
        model = User
        only = ["password"]

    username = StringField("username", validators=[DataRequired()])
    remember_me = BooleanField("remember me", default=False)


class RegistrationForm(ModelForm):
    class Meta:
        model = User

    password2 = PasswordField(
        "repeat password", validators=[DataRequired(), EqualTo("password")]
    )

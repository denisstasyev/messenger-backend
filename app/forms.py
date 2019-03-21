from wtforms_alchemy import ModelForm
from .models import User, Member, Chat, Message


class UserForm(ModelForm):
    class Meta:
        model = User


class MemberForm(ModelForm):
    class Meta:
        model = Member
        include = ["user_id", "chat_id", "last_read_message_id"]


class ChatForm(ModelForm):
    class Meta:
        model = Chat
        include = ["last_message_id"]


class MessageForm(ModelForm):
    class Meta:
        model = Message
        include = ["chat_id", "user_id"]


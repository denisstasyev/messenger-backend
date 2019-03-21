from wtforms_alchemy import ModelForm
from .models import User, Member, Chat


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

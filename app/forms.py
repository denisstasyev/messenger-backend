from wtforms_alchemy import ModelForm
from .models import User, Member


class UserForm(ModelForm):
    class Meta:
        model = User


class MemberForm(ModelForm):
    class Meta:
        model = Member
        include = ["user_id", "chat_id", "last_read_message_id"]


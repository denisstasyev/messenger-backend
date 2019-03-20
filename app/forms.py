from wtforms_alchemy import ModelForm
from .models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        # include manually added Foreign Keys values!!!!!!!!!!

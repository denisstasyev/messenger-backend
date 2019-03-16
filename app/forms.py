from wtforms_alchemy import ModelForm
from .models import User


# class UserForm(Form):
#     name = TextField(validators=[DataRequired(), Length(max=100)])
#     email = TextField(validators=[DataRequired(), Length(max=255)])


class UserForm(ModelForm):
    class Meta:
        model = User
        # exclude = ["user_id", "created_at", "updated_at"]

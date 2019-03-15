from wtforms_alchemy import Form
from models import User


class UserForm(Form):
    name = TextField(validators=[DataRequired(), Length(max=100)])
    email = TextField(validators=[DataRequired(), Length(max=255)])

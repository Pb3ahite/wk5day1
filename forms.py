from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class SignUP(FlaskForm):
        username = StringField(label = 'Username', validators=[DataRequired()])
        email = StringField()
        password = PasswordField()
        confirm_password = PasswordField()
        submit = SubmitField()


#class LoginForm(FlaskForm):
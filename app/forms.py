from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class SignUpForm(FlaskForm):
    username = StringField(label = 'Username', validators=[DataRequired()])
    email = StringField("Email", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    confirm_password = PasswordField("Confirm your password", [DataRequired(), EqualTo('password')])
    submit = SubmitField()

class SearchForm(FlaskForm):
    search_term = StringField('Search Term', validators=[DataRequired()])
    submit = SubmitField('Search')


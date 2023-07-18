from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class SignUpForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    first_name = StringField(label='First Name', validators=[DataRequired()])
    last_name = StringField(label='Last Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired()])
    date_created = StringField('Date Created', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Sign Up')


class SearchForm(FlaskForm):
    search_term = StringField('Search Term', validators=[DataRequired()])
    submit = SubmitField('Search')

class LoginForm(FlaskForm):
    username = StringField(label = 'Username', validators=[DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField()

class PostForm(FlaskForm):
    title = StringField(label = 'Title', validators=[DataRequired()])
    img_url = StringField(label = 'Image URL', validators=[DataRequired()])
    caption = StringField(label = 'Caption')    
    submit = SubmitField()
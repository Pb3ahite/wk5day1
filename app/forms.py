from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length

class SignUpForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    first_name = StringField(label='First Name', validators=[DataRequired()])
    last_name = StringField(label='Last Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired()])
    
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
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    caption = TextAreaField('Caption', validators=[DataRequired(), Length(max=500)])
    img_url = StringField('Image URL', validators=[DataRequired()])
    submit = SubmitField('Create Post')
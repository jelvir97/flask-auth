from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField
from wtforms.validators import InputRequired, Email, Length
from wtforms_validators import AlphaNumeric
class LoginForm(FlaskForm):
    """Form for logging in users"""
    username = StringField("Username",validators=[InputRequired(),Length(max=20),AlphaNumeric(message="Usernames may only use letters and numbers.")])
    password = PasswordField("Password", validators=[InputRequired(),Length(min=8)])

class RegisterForm(FlaskForm):
    """Form for adding new user"""
    username = StringField("Username",validators=[InputRequired(),Length(max=20),AlphaNumeric(message="Usernames may only use letters and numbers.")])
    password = PasswordField("Password", validators=[InputRequired(),Length(min=8)])
    email = StringField('Email Address', validators=[InputRequired(),Email(),Length(max=30)])
    first_name = StringField('First Name',validators=[InputRequired(),Length(max=30)])
    last_name = StringField('Last Name',validators=[InputRequired(),Length(max=30)])
    

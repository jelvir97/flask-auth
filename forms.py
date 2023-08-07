from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import InputRequired, Email, Length
from wtforms_validators import AlphaNumeric
class AddSnackForm(FlaskForm):
    """Form for adding snacks."""
    name = StringField("Snack Name")
    price = FloatField("Price in USD")

class RegisterForm(FlaskForm):
    """Form for adding new user"""
    username = StringField("Username",validators=[InputRequired(),Length(max=20),AlphaNumeric(message="Usernames may only use letters and numbers.")])
    password = StringField("Password", validators=[InputRequired(),Length(min=8)])
    email = StringField('Email Address', validators=[InputRequired(),Email(),Length(max=30)])
    first_name = StringField('First Name',validators=[InputRequired(),Length(max=30)])
    last_name = StringField('Last Name',validators=[InputRequired(),Length(max=30)])
    

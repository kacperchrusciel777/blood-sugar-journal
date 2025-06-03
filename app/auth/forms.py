from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, Regexp
from ..models import User

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='This field is required.'),
        Email(message='Invalid email address.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='This field is required.'),
        Length(min=6, message='Password must be at least 6 characters long.'),
        Regexp(r'.*\d', message='Password must contain at least one digit.')
    ])
    password2 = PasswordField('Repeat Password', validators=[
        DataRequired(message='This field is required.'),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already taken.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='This field is required.'),
        Email(message='Invalid email address.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='This field is required.')
    ])
    submit = SubmitField('Log In')

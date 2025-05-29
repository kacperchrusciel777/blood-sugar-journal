from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, Regexp
from ..models import User

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='To pole jest wymagane.'),
        Email(message='Nieprawidłowy adres email.')
    ])
    password = PasswordField('Hasło', validators=[
        DataRequired(message='To pole jest wymagane.'),
        Length(min=6, message='Hasło musi mieć co najmniej 6 znaków.'),
        Regexp(r'.*\d', message='Hasło musi zawierać przynajmniej jedną cyfrę.')
    ])
    password2 = PasswordField('Powtórz hasło', validators=[
        DataRequired(message='To pole jest wymagane.'),
        EqualTo('password', message='Pola hasła muszą być takie same.')
    ])
    submit = SubmitField('Zarejestruj się')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email jest już zajęty.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='To pole jest wymagane.'),
        Email(message='Nieprawidłowy adres email.')
    ])
    password = PasswordField('Hasło', validators=[
        DataRequired(message='To pole jest wymagane.')
    ])
    submit = SubmitField('Zaloguj się')

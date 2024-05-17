from app.models.usermodel import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_wtf.file import FileAllowed
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    fname = StringField('First Name', validators=[DataRequired(), Length(min=1, max=100)])
    lname = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    # profile_image = FileField('Profile Image', validators=[FileAllowed(['jpg', 'jpeg','png'], 'Images only!')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Please choose a different one.')

class UserUpdateForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    fname = StringField('First Name', validators=[DataRequired(), Length(min=1, max=100)])
    lname = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=100)])
    profile_image = FileField('Profile Image', validators=[FileAllowed(['jpg', 'jpeg','png'], 'Images only!')])
    submit = SubmitField('Update')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Please choose a different one.')




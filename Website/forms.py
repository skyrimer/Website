from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from flask_babel import gettext
from wtforms import (StringField, PasswordField, SubmitField,
                     BooleanField, TextAreaField)
from wtforms.validators import (DataRequired, Length, Email,
                                EqualTo, ValidationError)
from Website.models import User


class RegistrationForm(FlaskForm):
    username = StringField(gettext('Username'),
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(gettext('Email'),
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(gettext('Confirm Password'),
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField(gettext('Sign Up'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(gettext('That email is taken. Please choose a different one.'))


class LoginForm(FlaskForm):
    email = StringField(gettext('Email'),
                        validators=[DataRequired(), Email()])
    password = PasswordField(gettext('Password'), validators=[DataRequired()])
    remember = BooleanField(gettext('Remember Me'))
    submit = SubmitField(gettext('Login'))


class UpdateAccountForm(FlaskForm):
    username = StringField(gettext('Username'),
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(gettext('Email'),
                        validators=[DataRequired(), Email()])
    picture = FileField(gettext('Update Profile Picture'),
                        validators=[FileAllowed(['jpg', 'png', 'ico'])])
    submit = SubmitField(gettext('Update'))

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(gettext('That username is taken. Please choose a different one.'))

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(gettext('That email is taken. Please choose a different one.'))


class PostForm(FlaskForm):
    title = StringField(gettext('Title'), validators=[DataRequired()])
    content = TextAreaField(gettext('Content'), validators=[DataRequired()])
    submit = SubmitField(gettext('Post'))


class RequestResetForm(FlaskForm):
    email = StringField(gettext('Email'),
                        validators=[DataRequired(), Email()])
    submit = SubmitField(gettext('Request Password Reset'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(gettext('There is no account with that email. You must register first.'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(gettext('Password'), validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo(gettext('password'))])
    submit = SubmitField(gettext('Reset Password'))

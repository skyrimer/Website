from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, PasswordField, SubmitField,
                     BooleanField, TextAreaField)
from wtforms.validators import (DataRequired, Length, Email,
                                EqualTo, ValidationError)
from flask_login import current_user
from Website.models import User
from Website import bcrypt
from flask_babel import gettext


class UpdateAccountForm(FlaskForm):
    username = StringField(gettext('Username'),
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(gettext('Email'),
                        validators=[DataRequired(), Email()])
    bio = TextAreaField(gettext('Bio (optional)'))
    picture = FileField(gettext('Update Profile Picture'),
                        validators=[FileAllowed(['jpg', 'png'])])
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


class RegistrationForm(UpdateAccountForm):
    password = PasswordField(gettext('Password'), validators=[DataRequired()])
    confirm_password = PasswordField(gettext('Confirm Password'),
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField(gettext('Sign Up'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(gettext('That username is taken. Please choose a different one.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(gettext('That email is taken. Please choose a different one.'))




class LoginForm(FlaskForm):
    email_or_username = StringField(gettext('Email or Username'),
                                 validators=[DataRequired()])
    password = PasswordField(gettext('Password'), validators=[DataRequired()])
    remember = BooleanField(gettext('Remember Me'), default=True)
    submit = SubmitField(gettext('Login'))


class RequestResetForm(FlaskForm):
    email = StringField(gettext('Email'),
                        validators=[DataRequired(), Email()])
    submit = SubmitField(gettext('Request Password Reset'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(gettext('Password'), validators=[DataRequired()])
    confirm_password = PasswordField(gettext('Confirm Password'),
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Reset Password')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(gettext('Old Password'), validators=[DataRequired()])
    new_password = PasswordField(gettext('New Password'), validators=[DataRequired()])
    confirm_password = PasswordField(gettext('Confirm Password'),
                                      validators=[DataRequired(),
                                      EqualTo('new_password')])
    submit = SubmitField(gettext('Reset Password'))

    def validate_old_password(self, old_password):
        if not bcrypt.check_password_hash(current_user.password, self.old_password.data):
                raise ValidationError(gettext('Wrong password!'))
from flask_wtf import FlaskForm
from flask_babel import gettext
from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired


class CheckPasswordForm(FlaskForm):
    check_field = PasswordField(gettext('Check the password here'),
                                validators=[DataRequired()])
    submit = SubmitField(gettext('Check'))

class WeatherForm(FlaskForm):
    city = StringField(gettext('City'),
                                validators=[DataRequired()])
    submit = SubmitField(gettext('Get weather'))
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired


class CheckPasswordForm(FlaskForm):
    check_field = PasswordField('Check the password here',
                                validators=[DataRequired()])
    submit = SubmitField('Check')

class WeatherForm(FlaskForm):
    city = StringField('City', validators=[DataRequired()])
    submit = SubmitField('Get weather')

class ImageCompareForm(FlaskForm):
    image_1 = FileField('Image №1',
                        validators=[DataRequired(), FileAllowed(['jpg', 'png'])])

    image_2 = FileField('Image №2',
                        validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Compare Images')
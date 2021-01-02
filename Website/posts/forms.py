from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length
from flask_babel import gettext

class PostForm(FlaskForm):
    title = StringField(gettext('Title'), validators=[DataRequired(),
                                             Length(min=2, max=50)])
    content = TextAreaField(gettext('Content'), validators=[DataRequired(),
                                                   Length(min=2)])
    submit = SubmitField(gettext('Post'))

    valid_word = gettext('Unreal word')

    def validate_title(self, title):
        content = title.data.split(' ')
        for word in content:
            if len(word) > 30:
                raise ValidationError(valid_word)

    def validate_content(self, content):
        content = content.data.split(' ')
        for word in content:
            if len(word) > 30:
                raise ValidationError(valid_word)

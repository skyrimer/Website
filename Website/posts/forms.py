from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length


class PostForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired(), Length(min=2, max=50)])
    content = TextAreaField('Content',
                            validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Post')

    def validate_title(self, title):
        content = title.data.split(' ')
        for word in content:
            if len(word) > 30:
                raise ValidationError(f'Unreal word - {word}')

    def validate_content(self, content):
        self.validate_title(content)

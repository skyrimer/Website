from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length

class FeedbackForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired(), Length(min=2, max=50)])
    feedback_text = TextAreaField('Opinion',
                                  validators=[DataRequired(), Length(min=2)])
    submit = SubmitField('Send Feedback')

    valid_word = 'Unreal word'

    def validate_title(self, title):
        content = title.data.split(' ')
        for word in content:
            if len(word) > 30:
                raise ValidationError(f"Unreal word - {word}")

    def validate_content(self, content):
        self.validate_title(content)
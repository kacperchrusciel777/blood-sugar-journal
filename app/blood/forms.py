from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class BloodForm(FlaskForm):
    blood = IntegerField('Blood level (1-10)', validators=[DataRequired(), NumberRange(min=1, max=10)])
    note = TextAreaField('Note')
    submit = SubmitField('Save')


class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')

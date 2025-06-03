from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class GlucoseForm(FlaskForm):
    glucose = IntegerField('Glucose Level (mg/dL)', validators=[DataRequired(), NumberRange(min=40, max=400)])
    note = TextAreaField('Note')
    submit = SubmitField('Save')


class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')

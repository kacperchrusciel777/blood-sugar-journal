from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, NumberRange, Optional, ValidationError

class GlucoseForm(FlaskForm):
    glucose = IntegerField(
        'Glucose Level (mg/dL)',
        validators=[
            DataRequired(message="Please enter a glucose level."),
            NumberRange(min=40, max=400, message="Value must be between 40 and 400.")
        ]
    )
    tag = SelectField(
        'Measurement Type',
        choices=[
            ('', 'Select...'),
            ('fasting', 'Fasting'),
            ('post-meal', 'Post-meal'),
            ('before sleep', 'Before sleep')
        ],
        validators=[DataRequired(message="Please select a measurement type.")]
    )
    note = TextAreaField('Note', validators=[Optional()])
    submit = SubmitField('Save')

class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')

class FilterDateForm(FlaskForm):
    start_date = DateField('Start Date', validators=[Optional()])
    end_date = DateField('End Date', validators=[Optional()])
    tag = SelectField(
        'Filter by Tag',
        choices=[
            ('', 'All'),
            ('fasting', 'Fasting'),
            ('post-meal', 'Post-meal'),
            ('before sleep', 'Before sleep')
        ],
        validators=[Optional()]
    )
    submit = SubmitField('Filter')

    def validate_end_date(self, field):
        if self.start_date.data and field.data and field.data < self.start_date.data:
            raise ValidationError('End Date cannot be earlier than Start Date.')

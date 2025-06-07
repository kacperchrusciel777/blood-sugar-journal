from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, NumberRange, Optional, ValidationError
from datetime import date


class GlucoseForm(FlaskForm):
    glucose = IntegerField('Glucose level (mg/dL)', validators=[
        DataRequired(message="Please enter glucose level."),
        NumberRange(min=30, max=600, message="Glucose level must be between 30 and 600 mg/dL.")
    ])
    note = StringField('Note', validators=[Optional()])
    tag = SelectField(
        'Measurement Type',
        choices=[
            ('', 'Select measurement type'),
            ('Before meal', 'Before meal'),
            ('After meal', 'After meal'),
            ('Random', 'Random'),
            ('Fasting', 'Fasting')
        ],
        validators=[DataRequired(message="Please select a measurement type.")]
    )
    submit = SubmitField('Save')


class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')


class FilterDateForm(FlaskForm):
    start_date = DateField('Start Date', validators=[Optional()])
    end_date = DateField('End Date', validators=[Optional()])
    tag = SelectField(
        'Measurement Type',
        choices=[
            ('', 'All'),
            ('Before meal', 'Before meal'),
            ('After meal', 'After meal'),
            ('Random', 'Random'),
            ('Fasting', 'Fasting')
        ],
        validators=[Optional()]
    )
    submit = SubmitField('Filter')

    def validate_end_date(self, field):
        if self.start_date.data and field.data:
            if field.data < self.start_date.data:
                raise ValidationError('End date cannot be earlier than start date.')

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField


class AddForm(FlaskForm):
    name = StringField('Name of Owner')
    puppy_id = IntegerField('Id of Puppy: ')
    submit = SubmitField('Add Owner')


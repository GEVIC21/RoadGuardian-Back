from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField

class AddForm(FlaskForm):
    name = StringField('Name of Puppy')
    submit = SubmitField('Add Puppy')

class DelForm(FlaskForm):
    id = IntegerField('Id of Puppy to Delete')
    submit = SubmitField('Delete Puppy')
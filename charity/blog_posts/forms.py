from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired

class BlogPostForm(FlaskForm):
    # no empty titles or text possible
    # we'll grab the date automatically from the Model later
    libelle = StringField('Libelle', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    categorie = StringField('Categorie')
    image = FileField('Image')
    submit = SubmitField('Créer')

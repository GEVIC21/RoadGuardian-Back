import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.secret_key = "mysecretkey"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:vealeto@localhost/flask_test1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from myproject.owners.views import owners_blueprints
from myproject.puppies.views import puppies_blueprints

app.register_blueprint(owners_blueprints, url_prefix='/owners')
app.register_blueprint(puppies_blueprints, url_prefix='/puppies')
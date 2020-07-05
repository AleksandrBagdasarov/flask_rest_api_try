from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from flask_migrate import Migrate
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'top secret'
# Init db
db = SQLAlchemy(app)
# Init Bcrypt
bcrypt = Bcrypt(app)
# Init ma
ma = Marshmallow(app)
# Init migrate
migrate = Migrate(app, db)
# Except Circular Import
from myapi import models, routes


from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager
from flaskext.bcrypt import Bcrypt
#from flask.ext.sendmail import Mail
from flask.ext.mail import Mail
from flask_debugtoolbar import DebugToolbarExtension
import stripe
from config import *
import os


app = Flask(__name__)
app.config.from_object('config')
app.config["MONGODB_SETTINGS"] = {'DB': "my_tumble_log"}

bcrypt = Bcrypt(app)
lm = LoginManager()
lm.init_app(app)
mail = Mail(app)
toolbar = DebugToolbarExtension(app)
# the toolbar is only enabled in debug mode:
app.debug = True

if DB is 'MongoDB':
	db = MongoEngine(app)
	from app import routes, models2
else:
	db = SQLAlchemy(app)
	from app import routes, models



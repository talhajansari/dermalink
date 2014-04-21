from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flaskext.bcrypt import Bcrypt
#from flask.ext.sendmail import Mail
from flask.ext.mail import Mail

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

lm = LoginManager()
lm.init_app(app)

mail = Mail(app)

from app import routes, models

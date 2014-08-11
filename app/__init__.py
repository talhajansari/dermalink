from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager
from flaskext.bcrypt import Bcrypt
from flask.ext.mail import Mail
from flask_debugtoolbar import DebugToolbarExtension
import stripe
from flask.ext.admin import Admin
from werkzeug.contrib.fixers import ProxyFix

# Initiaize the App
app = Flask(__name__)
app.config.from_object('config')
app.wsgi_app = ProxyFix(app.wsgi_app)

# Initialize the extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
lm = LoginManager(app)
mail = Mail(app)
toolbar = DebugToolbarExtension(app) # not working properly # the toolbar is only enabled in debug mode:
#app.debug = True


from app import routes, models


# Admin Dashboard Configuration #
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from models import User, Patient, Doctor, Issue
admin = Admin(app, 'Dermify')

class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

# Add administrative views here
#admin.add_view(MyView(name="Index"))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Patient, db.session))
admin.add_view(ModelView(Doctor, db.session))
admin.add_view(ModelView(Issue, db.session))
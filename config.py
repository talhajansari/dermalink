import os
import stripe

## Configuration file for the SkinCheck App

# Other Settings
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOADED_IMAGES_DEST = os.path.join(basedir, 'uploads')
CSRF_ENABLED = True
SECRET_KEY = 'vkjrkvwjwhrbv49cn8hx239r8h'
DB = 'SQL'
if os.getenv('SERVER_ENV')=='PROD':
	SHOW_LOGIN = False
else:
 	SHOW_LOGIN = True
APP_NAME = 'Dermify'
LOGO_TYPE = 'dplus' #'dplus' or 'splus'
LOGO_URL_ICON = '/static/img/dplus_blueonwhite_icon.png'
LOGO_URL_LARGE = '/static/img/dplus_blueonwhite_large.png'



# SQLAlchemy Configuration
if os.environ.get('DATABASE_URL') is None:
	#SQLALCHEMY_DATABASE_URI = "postgresql://talhajansari:@localhost/testpsqldb"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True

# MongoDb Configuration
# MONGODB_SETTINGS = {'DB': "skincheck_db"}
# ,
# 	'USERNAME': 'tansari',
# 	'password': 'dermalink2014',
# 	'HOST': '127.0.0.1',
# 	'PORT': 27017}

## TWILIO ACCOUNT CONFIG
MY_ACCOUNT_SID = 'AC6056ccab9b128c038c932d4bbf81b662'
MY_ACCOUNT_TOKEN = 'd6a72dff4e0f118e2e52d15ef51f4548'
MY_TWILIO_NUMBER = '+14408478798'

## EMAIL SERVER CONFIG
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'dermaplus.skincheck@gmail.com'
MAIL_PASSWORD = 'skin-check'
# MAIL_USERNAME = 'dermangoplus@gmail.com'
# MAIL_PASSWORD = 'derMango-Plus'



## STRIPE Payments System Config
# Test
PUBLISHABLE_KEY_TEST = 'pk_test_JSOR9hzJNMDkITuRoZ1PWuP7' 
SECRET_KEY_TEST = 'sk_test_4OvoBnWfcP6941Qgj1gDKQZf'
# Live
PUBLISHABLE_KEY= 'sk_live_oZX4c8pFwZSWPMVqVwp5NdGb'
SECRET_KEY= 'pk_live_bXRCAUqhEIVn4qdtAA0rAvN4'
stripe_keys = {
    'secret_key': SECRET_KEY_TEST,
    'publishable_key': PUBLISHABLE_KEY_TEST
}
stripe.api_key = stripe_keys['secret_key']




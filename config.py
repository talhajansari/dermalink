import os
import stripe

## Configuration file for the SkinCheck App

basedir = os.path.abspath(os.path.dirname(__file__))
UPLOADED_IMAGES_DEST = os.path.join(basedir, 'uploads')
CSRF_ENABLED = True
SECRET_KEY = 'vkjrkvwjwhrbv49cn8hx239r8h'
APP_NAME = 'Dermifi'
LOGO_TYPE = 'dplus' #'dplus' or 'splus'
LOGO_URL_ICON = '/static/img/dplus_blueonwhite_icon.png'
LOGO_URL_LARGE = '/static/img/dplus_blueonwhite_large.png'
CASE_COST = '19.99'
CASE_COST_CENTS = '1999'

ALLOW_LOGIN = None
SERV_ENV = None
if os.getenv('SERVER_ENV')=='PROD':
	SERV_ENV = 'PROD'
	ALLOW_LOGIN = False
elif os.getenv('SERVER_ENV')=='STG':
 	SERV_ENV = 'STG'
 	ALLOW_LOGIN = False
elif os.getenv('SERVER_ENV')=='DEV':
	SERV_ENV = 'DEV'
 	ALLOW_LOGIN = True
else:
	SERV_ENV = 'NULL'
	ALLOW_LOGIN = True

# DATABASE
# SQLAlchemy Configuration
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True
# MongoDb Configuration
# MONGODB_SETTINGS = {'DB': "skincheck_db"}
# 	'USERNAME': 'tansari',
# 	'password': 'dermalink2014',
# 	'HOST': '127.0.0.1',
# 	'PORT': 27017}

## TWILIO ACCOUNT CONFIG
if SERV_ENV=="PROD":
	MY_ACCOUNT_SID = 'AC886935f9224fbf42128e6b030a90b84e'
	MY_ACCOUNT_TOKEN = '901db1d61d5420502c3675bad2ed8d9f'
	MY_TWILIO_NUMBER = '+14402206886'
elif SERV_ENV=="DEV" or SERV_ENV=="STG" or SERV_ENV=="NULL": #Test
	MY_ACCOUNT_SID = 'AC3f50636962a8d1fd0baea6bd747c7d52'
	MY_ACCOUNT_TOKEN = '75ac60db60fa0873c8662354ae15333e'
	MY_TWILIO_NUMBER = '+14402206886'

## STRIPE CONFIG
if SERV_ENV=="PROD":
	STRIPE_SECRET_KEY = 'sk_live_4VRBEOm9BLUfguuftEa3fMc2' 
	STRIPE_PUBLISHABLE_KEY = 'pk_live_4VRBUsNkaGdenlyMJkaUrPJ5'
elif SERV_ENV=="DEV" or SERV_ENV=="STG" or SERV_ENV=="NULL":
	STRIPE_SECRET_KEY= 'sk_test_4VRBWW3kjwaIVQjbYieSd6Qe'
	STRIPE_PUBLISHABLE_KEY= 'pk_test_4VRBgD7HHY4mL5W9dfl6cWuB'
stripe_keys = {
    'secret_key': STRIPE_SECRET_KEY,
    'publishable_key': STRIPE_PUBLISHABLE_KEY
}
stripe.api_key = stripe_keys['secret_key']

## EMAIL SERVER CONFIG
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'dermifi.App@gmail.com'
MAIL_PASSWORD = 'dermifi2014'


import os
basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
	#SQLALCHEMY_DATABASE_URI = "postgresql://talhajansari:@localhost/testpsqldb"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True

UPLOADED_IMAGES_DEST = os.path.join(basedir, 'uploads')

CSRF_ENABLED = True
SECRET_KEY = 'vkjrkvwjwhrbv49cn8hx239r8h'

MY_ACCOUNT_SID = 'AC6056ccab9b128c038c932d4bbf81b662'
MY_ACCOUNT_TOKEN = 'd6a72dff4e0f118e2e52d15ef51f4548'
MY_TWILIO_NUMBER = '+14408478798'

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'dermaplus.skincheck@gmail.com'
MAIL_PASSWORD = 'skin-check'
# MAIL_USERNAME = 'dermangoplus@gmail.com'
# MAIL_PASSWORD = 'derMango-Plus'

SPLASH_PAGE = True
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

UPLOADED_IMAGES_DEST = os.path.join(basedir, 'uploads')

CSRF_ENABLED = True
SECRET_KEY = 'vkjrkvwjwhrbv49cn8hx239r8h'


#!flask/bin/python
import os
os.environ['SERVER_ENV'] = 'DEV'

from app import app
app.run (debug=True)
#app.run(host='0.0.0.0')

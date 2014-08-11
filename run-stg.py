#!flask/bin/python
import os
os.environ('SERVER_ENV') = 'STG'
from app import app
app.run(host='0.0.0.0')
